from typing import Any, Dict, Optional
import mlflow
import json
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks import CallbackManagerForChainRun
from pathlib import Path
from langchain_core.runnables import RunnableLambda, Runnable
from langchain.chains import SimpleSequentialChain
import logging
import types
import threading
import inspect
import pandas as pd
logger = logging.getLogger(__name__)

# Thread-local context for S3 client and bucket path to prevent cross-execution contamination
import threading
_agent_context = threading.local()

def set_agent_context(s3_client, bucket_path, execution_id=None):
    """Set thread-local context for agent execution"""
    _agent_context.s3_client = s3_client
    _agent_context.bucket_path = bucket_path
    _agent_context.execution_id = execution_id

def get_agent_context():
    """Get thread-local context for agent execution"""
    return {
        's3_client': getattr(_agent_context, 's3_client', None),
        'bucket_path': getattr(_agent_context, 'bucket_path', None),
        'execution_id': getattr(_agent_context, 'execution_id', None)
    }

def clear_agent_context():
    """Clear thread-local context to prevent memory leaks"""
    for attr in ['s3_client', 'bucket_path', 'execution_id']:
        if hasattr(_agent_context, attr):
            delattr(_agent_context, attr)

class CustomPythonModel(mlflow.pyfunc.PythonModel):
    def __init__(self):
        self.agent = None
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("lock", None)
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()
    
    def load_context(self, context):
        import sys
        import os
        import shutil
        
        agent_code_path = context.model_config["agent_code"]
        agent_code_dir = os.path.dirname(agent_code_path)
        
        if agent_code_dir not in sys.path:
            sys.path.insert(0, agent_code_dir)
        
        for artifact_name, artifact_path in context.model_config.items():
            if artifact_name.startswith("local_module_"):
                module_name = artifact_name.replace("local_module_", "")
                module_filename = f"{module_name}.py"
                dest_path = os.path.join(agent_code_dir, module_filename)
                
                if not os.path.exists(dest_path):
                    shutil.copy2(artifact_path, dest_path)
                    print(f"Restored local module: {module_name}")
        
        try:
            import agent_code
            from agent_code import create_simple_agent
            self.agent_func = create_simple_agent
            self.agent = self.agent_func()
        except ImportError as e:
            raise ImportError(f"Failed to import agent_code: {e}")
    
    def predict(self, context, model_input: list[str]):
        if isinstance(model_input, list):
            parsed_data = json.loads(model_input[0])
            return self.run(parsed_data, callback_enabled=True)
        else:
            return self.run(model_input)
class AgentChainWrapper:
    def __init__(self, chain_class = SimpleSequentialChain, agent_functions_list = [], callback_enabled = False):
        self.chain_class = chain_class
        self.agents = [func() for func in agent_functions_list]
        self.agent_functions = agent_functions_list
        self.callback_enabled = callback_enabled
    
    def _wrap_agent_runnable(self, agent) -> RunnableLambda:
        """
        Wraps the agent's .run() method into a RunnableLambda with a custom function name.
        Properly propagates errors instead of continuing to the next agent.
        """
        def base_fn(
            x: Dict[str, Any],
            *,
            run_manager: CallbackManagerForChainRun = None,
        ):
            # Run the agent, but don't catch exceptions - let them propagate
            # This will stop the entire pipeline on agent failure
            if run_manager:
                run_manager.on_text(f"[{agent.__class__.__name__}] starting…")

            # If your agent supports .invoke, prefer it; otherwise fall back to .run
            try:
                # Propagate callbacks to the inner agent call too (if it’s a Runnable)
                if hasattr(agent, "invoke"):
                    sig = inspect.signature(agent.invoke)
                    if "config" in sig.parameters  and self.callback_enabled:
                        out = agent.invoke(
                            x,
                            config={"callbacks": [OutputAgentStatus()]}
                        )
                    else:
                        out = agent.invoke(x)
                else:
                    out = agent.run(x)  # legacy agents
            finally:
                if run_manager:
                    run_manager.on_text(f"[{agent.__class__.__name__}] finished.")

            return out
            
            # Check if result starts with "An error occurred" which indicates agent failure
            # if isinstance(result, str) and result.startswith("An error occurred during execution:"):
            #     # Propagate the error by raising an exception to stop the execution
            #     raise RuntimeError(f"Agent {agent.__class__.__name__} failed: {result}")
                
            # return result

        # Clone function and set custom name
        fn_name = f"runnable_{agent.__class__.__name__.lower().replace(' ', '_')}"
        runnable_fn = types.FunctionType(
            base_fn.__code__,
            base_fn.__globals__,
            name=fn_name,
            argdefs=base_fn.__defaults__,
            closure=base_fn.__closure__,
        )

        return RunnableLambda(runnable_fn)
    
    def run(self, query, callback_enabled: Optional[bool] = False):
        if callback_enabled:
            self.callback_enabled = callback_enabled
        result = query
        def is_dataframe(obj) -> bool:
            try:
                return isinstance(obj, pd.DataFrame)
            except Exception as e:
                return False
        if is_dataframe(result):
            result = result.to_dict(orient='records')[0]
        runnables = []
        for agent in self.agents:
            if isinstance(agent, Runnable):
                # Check if agent supports with_config (Runnable style)
                if hasattr(agent, "with_config") and self.callback_enabled:
                    # Inject default callbacks on the agent itself
                    enhanced = agent.with_config({"callbacks": [OutputAgentStatus()]})
                    runnables.append(enhanced)
                else:
                    # Not a Runnable — wrap with your fallback wrapper
                    runnables.append(agent)
            else:
                runnables.append(
                    self._wrap_agent_runnable(agent)
                )
        if self.chain_class is SimpleSequentialChain:
            pipeline = runnables[0]
            for r in runnables[1:]:
                pipeline = pipeline | r
            if is_dataframe(query):
                query = query.to_dict(orient='records')[0]
            return pipeline.invoke(query)
        chain = self.chain_class(
            chains=runnables,
        )
        return chain.run(result)
    
    def predict(self, context = "", model_input: list[str] = [""]):
        if isinstance(model_input, list):
            parsed_data = json.loads(model_input[0])
            return self.run(parsed_data, callback_enabled=True)
        else:
            return self.run(model_input)

class CustomChainModel(mlflow.pyfunc.PythonModel):
    def __init__(self):
        self.agent_chain = None
        self.agents = []
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("lock", None)
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()
    
    def load_context(self, context):
        import sys
        import os
        import shutil
        import importlib.util
        
        # Get the directory where artifacts are stored
        base_dir = os.path.dirname(list(context.artifacts.values())[0])
        
        if base_dir not in sys.path:
            sys.path.insert(0, base_dir)
        
        # Restore local modules
        for artifact_name, artifact_path in context.artifacts.items():
            if artifact_name.startswith("local_module_"):
                module_name = artifact_name.replace("local_module_", "")
                module_filename = f"{module_name}.py"
                dest_path = os.path.join(base_dir, module_filename)
                
                if not os.path.exists(dest_path):
                    shutil.copy2(artifact_path, dest_path)
                    print(f"Restored local module: {module_name}")
        
        # Load chain configuration
        chain_config_path = context.artifacts["chain_config"]
        spec = importlib.util.spec_from_file_location("chain_config", chain_config_path)
        chain_config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(chain_config_module)
        
        chain_config = chain_config_module.CHAIN_CONFIG
        
        # Load each agent
        agent_functions = []
        for agent_info in chain_config["agents"]:
            agent_code_file = agent_info["agent_code_file"]
            function_name = agent_info["function_name"]
            
            # Load the agent module - handle the artifact key mapping
            artifact_key = agent_code_file.replace(".py", "")
            if artifact_key not in context.artifacts:
                # Try with agent_code_ prefix for consistency
                artifact_key = f"agent_code_{agent_info['name'].split('_')[-1]}"
            agent_code_path = context.artifacts[artifact_key]
            spec = importlib.util.spec_from_file_location("agent_module", agent_code_path)
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)
            
            # Get the agent function
            agent_function = getattr(agent_module, function_name)
            agent_functions.append(agent_function)
        
        # Create the agent chain
        self.agent_chain = AgentChainWrapper(agent_functions_list=agent_functions, callback_enabled=True)
    
    def predict(self, context, model_input: list[str]):
        if isinstance(model_input, list):
            parsed_data = json.loads(model_input[0])
            return self.agent_chain.run(parsed_data)
        else:
            return self.agent_chain.run(model_input)

class CrewAgentWrapper:
    def __init__(self, agent_func=None):
        if agent_func is not None:
            # During logging phase
            try:
                from crew_agent import create_crew_agent
                self.base_agent = create_crew_agent()
            except ImportError:
                raise ImportError("Could not import CrewAI agent functions")
        else:
            # During model loading phase
            try:
                from agent_code import create_crew_agent
                self.base_agent = create_crew_agent()
            except ImportError:
                try:
                    from crew_agent import create_crew_agent
                    self.base_agent = create_crew_agent()
                except ImportError:
                    raise ImportError("Could not import CrewAI agent")
    
    def run(self, query):
        try:
            if hasattr(self, 'base_agent'):
                # Import create_crew_with_task function
                try:
                    from agent_code import create_crew_with_task
                except ImportError:
                    from crew_agent import create_crew_with_task
                
                crew = create_crew_with_task(query)
                result = crew.kickoff()
                return str(result)
            else:
                return "Error: Agent not properly initialized"
        except Exception as e:
            print(f"Error running CrewAI crew: {e}")
            return f"Error executing query '{query}': {str(e)}"
    
    def predict(self, context, model_input: list[str]):
        return self.run(model_input)

class CustomCrewModel(mlflow.pyfunc.PythonModel):
    def __init__(self):
        self.agent = None
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("lock", None)
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()
    
    def load_context(self, context):
        import sys
        import os
        import shutil
        
        agent_code_path = context.model_config["agent_code"]
        agent_code_dir = os.path.dirname(agent_code_path)
        
        if agent_code_dir not in sys.path:
            sys.path.insert(0, agent_code_dir)
        
        for artifact_name, artifact_path in context.model_config.items():
            if artifact_name.startswith("local_module_"):
                module_name = artifact_name.replace("local_module_", "")
                module_filename = f"{module_name}.py"
                dest_path = os.path.join(agent_code_dir, module_filename)
                
                if not os.path.exists(dest_path):
                    shutil.copy2(artifact_path, dest_path)
                    print(f"Restored local module: {module_name}")
        
        try:
            import agent_code
            from agent_code import CrewAgentWrapper
            self.agent = CrewAgentWrapper()
        except ImportError as e:
            raise ImportError(f"Failed to import CrewAI agent_code: {e}")
    
    def predict(self, context, model_input: list[str]):
        if isinstance(model_input, list):
            return [self.agent.run(query) for query in model_input]
        else:
            return self.agent.run(model_input)


class OutputAgentStatus(BaseCallbackHandler):
    def __init__(self, s3_client=None, bucket_path=None):
        super().__init__()
        self.s3_client = s3_client
        self.bucket_path = bucket_path

        # If not provided, try to get from global context
        if not self.s3_client or not self.bucket_path:
            context = get_agent_context()
            self.s3_client = self.s3_client or context.get('s3_client')
            self.bucket_path = self.bucket_path or context.get('bucket_path')

    def save_to_s3(self, status, message):
        if not self.s3_client or not self.bucket_path:
            return

        # Validate execution_id is in bucket_path to prevent cross-execution contamination
        import os
        execution_id = os.environ.get('EXECUTION_ID')
        if execution_id and execution_id not in self.bucket_path:
            print(f"Warning: Execution ID {execution_id} not found in bucket path {self.bucket_path}. Skipping S3 write.")
            return

        try:
            import os
            import json
            from datetime import datetime

            bucket_name = os.environ.get('DEPLOYMENTS_BUCKET_NAME', 'local-development-deployments')
            status_key = f"{self.bucket_path}/last_output.json"

            # Try to read existing last_output.json
            existing_data = {}
            try:
                response = self.s3_client.get_object(Bucket=bucket_name, Key=status_key)
                existing_data = json.loads(response['Body'].read().decode('utf-8'))
            except self.s3_client.exceptions.NoSuchKey:
                # File doesn't exist yet, start with empty data
                pass
            except Exception as e:
                print(f"Warning: Could not read existing last_output.json: {e}")

            # Update the status and output fields
            existing_data.update({
                "status": status,
                "output": message
            })

            # Save updated last_output.json
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=status_key,
                Body=json.dumps(existing_data),
                ContentType='application/json'
            )
        except Exception as e:
            print(f"Error saving status to S3: {e}")

    def on_text(self, text: str, **kwargs):
        self.save_to_s3("text_output", f"Agent generated text: {text}")

    def on_llm_start(self, serialized, prompts, **kwargs):
        model_name = serialized.get('name', 'Unknown')
        self.save_to_s3("llm_start", f"Thinking")

    def on_llm_new_token(self, token: str, **kwargs):
        self.save_to_s3("llm_streaming", f"LLM generating response token: {token}")

    def on_llm_end(self, response, **kwargs):
        token_count = getattr(response, 'llm_output', {}).get('token_usage', {}).get('total_tokens', 'unknown')
        self.save_to_s3("llm_complete", f"LLM completed response generation (tokens: {token_count})")

    def on_tool_start(self, serialized, input_str: str, **kwargs):
        tool_name = serialized.get('name', 'Unknown Tool')
        self.save_to_s3("tool_start", f"Executing tool: {tool_name} with input: {input_str[:100]}")

    def on_tool_end(self, output: str, **kwargs):
        output_preview = str(output)[:100] if len(str(output)) > 100 else str(output)
        self.save_to_s3("tool_complete", f"Tool execution completed with output: {output_preview}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        chain_id = serialized.get('id', 'Unknown Chain')
        self.save_to_s3("chain_start", f"Starting chain execution: {chain_id}")

    def on_chain_end(self, outputs, **kwargs):
        output_preview = str(outputs)[:100] if len(str(outputs)) > 100 else str(outputs)
        self.save_to_s3("chain_complete", f"Chain execution completed with outputs: {output_preview}")

    def on_agent_action(self, action, **kwargs):
        action_tool = getattr(action, 'tool', 'Unknown')
        action_input = getattr(action, 'tool_input', '')
        self.save_to_s3("agent_action", f"Agent taking action with tool: {action_tool}, input: {str(action_input)[:100]}")

    def on_agent_finish(self, finish, **kwargs):
        return_values = getattr(finish, 'return_values', {})
        output_preview = str(return_values)[:100] if len(str(return_values)) > 100 else str(return_values)
        self.save_to_s3("agent_complete", f"Agent execution finished with result: {output_preview}")