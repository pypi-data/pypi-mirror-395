
from typing import List
import inspect
import re
from fairo.core.agent.base_agent import SimpleAgent


def extract_vector_stores_from_tool(tool):
    vector_stores = []
    seen_collections = set()

    fn = getattr(tool, "func", None)
    if not fn:
        return vector_stores

    if fn.__closure__:
        for cell in fn.__closure__:
            try:
                val = cell.cell_contents
                if type(val).__name__ in ("FairoVectorStore", "PostgresVectorStore"):
                    if val.collection_name not in seen_collections:
                        store_info = {"collection_name": val.collection_name}
                        if hasattr(val, 'collection_uuid'):
                            store_info['collection_uuid'] = val.collection_uuid
                        vector_stores.append(store_info)
                        seen_collections.add(val.collection_name)
            except Exception:
                continue

    try:
        source = inspect.getsource(fn)
        store_patterns = [
            r'FairoVectorStore\s*\([^)]+\)',
            r'PostgresVectorStore\s*\([^)]+\)',
        ]

        for pattern in store_patterns:
            matches = list(re.finditer(pattern, source))
            for match in matches:
                instantiation = match.group(0)

                name_match = re.search(r'collection_name\s*=\s*["\']([^"\']+)["\']', instantiation)
                if not name_match:
                    continue

                collection_name = name_match.group(1)
                if collection_name in seen_collections:
                    continue

                store_info = {"collection_name": collection_name}

                uuid_match = re.search(r'collection_uuid\s*=\s*["\']([^"\']+)["\']', instantiation)
                if uuid_match:
                    store_info['collection_uuid'] = uuid_match.group(1)
                else:
                    try:
                        if 'FairoVectorStore' in instantiation:
                            from fairo.core.workflow.dependency import FairoVectorStore
                            temp_store = FairoVectorStore(collection_name=collection_name, create_if_not_exists=True)
                            if hasattr(temp_store, 'collection_uuid') and temp_store.collection_uuid:
                                store_info['collection_uuid'] = temp_store.collection_uuid
                    except Exception:
                        pass

                vector_stores.append(store_info)
                seen_collections.add(collection_name)
    except Exception:
        pass

    return vector_stores

def output_workflow_tools(agents):
        tools = []
        seen_names = set()
        tool_num = 1

        for agent in agents:
            for tool in agent.tool_instances:
                if tool.name in seen_names:
                    continue

                seen_names.add(tool.name)
                tools.append({
                    "name": tool.name,
                    "schema": tool.args_schema.args_schema.model_json_schema() if tool.args_schema else None,
                    "returns": tool.returns,
                    "tool_num": tool_num,
                    "description": tool.description
                })
                tool_num += 1

        return tools

def output_workflow_dependencies(agents: List[SimpleAgent]):
    dependencies = []
    seen_dependencies = set()
    dependency_num = 1
    for agent in agents:
        for store in agent.knowledge_stores:
            if store.collection_name in seen_dependencies:
                continue
            seen_dependencies.add(store.collection_name)
            store_info = {
                "dependency_num": dependency_num,
                "name": store.collection_name
            }
            if hasattr(store, 'collection_uuid'):
                store_info['id'] = store.collection_uuid
            dependencies.append(store_info)
            dependency_num += 1
    return dependencies

def output_workflow_agent_nodes(tools, dependencies, agents: List[SimpleAgent]):
    tool_map = {t['name']: t['tool_num'] for t in tools}
    dependency_map = {t['name']: t['dependency_num'] for t in dependencies}
    _agents = []
    outputs = []
    agent_num = 1
    output_num = 1
    for agent in agents:
        agent_outputs = []
        agent_tools = [
            tool_map[tool.name]
            for tool in agent.tool_instances
            if tool.name in tool_map
        ]
        agent_dependencies = [
            dependency_map[store.collection_name]
            for store in agent.knowledge_stores
            if store.collection_name in dependency_map
        ]
        if agent.output and len(agent.output) > 0:
            for output in agent.output:
                outputs.append({
                    "name": output.name,
                    "source": f"Node-{agent_num}",
                    "description": output.description,
                    "destination": output.destination,
                    "num": output_num
                })
                agent_outputs.append(output_num)
                output_num += 1
        _agents.append({
            "goal": agent.goal,
            "name": agent.agent_name,
            "role": agent.role,
            "tool": agent_tools,
            "knowledge_store": agent_dependencies,
            "output": agent_outputs,
            "tigger": {},
            "backstory": agent.backstory,
        })
        agent_num += 1
    nodes = {
                "1": {
                    "id": "1",
                    "slug": "",
                    "stage": "middle",
                    "title": "Agent Executor",
                    "params": {
                        "agents": _agents
                    },
                    "handler": [{
                        "step": "2",
                        "type": "go_to",
                        "condition": {
                            "value": "is_success",
                            "test_value": True,
                            "condition_test": "=="
                        },
                        "edge_description": ""
                    }],
                    "node_type": "KNOWLEDGE_STORE_AGENT_EXECUTOR",
                    "position_x": 490.24,
                    "position_y": 66.4,
                    "description": ""
                },
            }
    if len(outputs) > 0:
        nodes["2"] = {
                        "id": "2",
                        "slug": "",
                        "stage": "end",
                        "title": "Outputs",
                        "params": {
                            "outputs": outputs
                        },
                        "handler": [
                            {
                                "step": None,
                                "type": "finish",
                                "condition": {
                                    "value": "output",
                                    "test_value": True,
                                    "condition_test": "=="
                                },
                                "edge_description": "=="
                            }
                        ],
                        "node_type": "KNOWLEDGE_STORE_OUTPUT",
                        "position_x": 1031.65,
                        "position_y": 66.4,
                        "description": ""
                    }
    return nodes

def output_workflow_process_graph(agents):
    tools = output_workflow_tools(agents)
    dependencies = output_workflow_dependencies(agents)
    tools_json = {"tool": {
            "id": "tool",
            "slug": "",
            "type": "KNOWLEDGE_STORE_TOOLS",
            "stage": "start",
            "title": "Tools",
            "params": {
                "tools": tools
            },
            "handler": [
                {
                    "step": "1",
                    "type": "go_to",
                    "condition": None,
                    "edge_description": ""
                }
            ],
            "position_x": -152.7,
            "position_y": 353,
            "description": ""
        }} if len(tools) > 0 else {}
    dependency_json = {"dependency": {
            "id": "dependency",
            "slug": "",
            "type": "KNOWLEDGE_STORE_DEPENDENCIES",
            "stage": "start",
            "title": "Dependencies",
            "params": {
                "dependencies": dependencies
            },
            "handler": [
                {
                    "step": "1",
                    "type": "go_to",
                    "condition": None,
                    "edge_description": ""
                }
            ],
            "position_x": -152.7,
            "position_y": 121.61,
            "description": ""
        }} if len(dependencies) > 0 else {}
    return {
        "nodes": output_workflow_agent_nodes(tools, dependencies, agents),
        **dependency_json,
        **tools_json,
    }        
            

def output_langchain_process_graph(agents):
    if not isinstance(agents, list):
        agents = [agents]

    def _agent_display_name(a):
        return (
            getattr(a, "name", None)
            or getattr(getattr(a, "agent", None), "name", None)
            or "LangChain Agent"
        )

    parent_name_of = {}
    agent_id_map = {}

    def iter_agent_tools(a):
        """Yield tools from various agent shapes safely."""
        for t in getattr(a, "tools", []) or []:
            yield t
        inner = getattr(a, "agent", None)
        if inner is not None and inner is not a:
            for t in getattr(inner, "tools", []) or []:
                yield t

    def closure_cells(fn):
        try:
            return list(getattr(fn, "__closure__", []) or [])
        except Exception:
            return []

    def is_vector_store(val):
        return type(val).__name__ in ("FairoVectorStore", "PostgresVectorStore")

    def is_agent_like(val):
        if type(val).__name__ in ("AgentExecutor"):
            return True
        return hasattr(val, "invoke") and (hasattr(val, "agent") or hasattr(val, "tools"))

    tools = []
    tool_map = {}
    seen_tool_names = set()

    vector_stores = []
    seen_collections = set()

    all_agents = []
    seen_agents = set()

    tools_to_remove = set()

    queue = list(agents)
    while queue:
        agent = queue.pop(0)
        if id(agent) in seen_agents:
            continue
        seen_agents.add(id(agent))
        all_agents.append(agent)
        if id(agent) not in agent_id_map:
            agent_id_map[id(agent)] = str(len(agent_id_map) + 1)

        for tool in iter_agent_tools(agent):
            if getattr(tool, "name", None) and tool.name not in seen_tool_names:
                seen_tool_names.add(tool.name)

                schema = None
                schema_obj = getattr(tool, "args_schema", None)
                if schema_obj is not None and hasattr(schema_obj, "model_json_schema"):
                    schema = schema_obj.model_json_schema()

                tools.append({
                    "name": tool.name,
                    "schema": schema,
                    "returns": None,
                    "tool_num": len(tools) + 1,
                    "description": getattr(tool, "description", "")
                })
                tool_map[tool.name] = len(tools)

            tool_vector_stores = extract_vector_stores_from_tool(tool)
            for store_info in tool_vector_stores:
                collection_name = store_info['collection_name']
                if collection_name not in seen_collections:
                    class VectorStoreInfo:
                        def __init__(self, name, uuid=None):
                            self.collection_name = name
                            if uuid:
                                self.collection_uuid = uuid

                    store_obj = VectorStoreInfo(
                        collection_name,
                        store_info.get('collection_uuid')
                    )
                    vector_stores.append(store_obj)
                    seen_collections.add(collection_name)

                if tool.name:
                    tools_to_remove.add(tool.name)

            fn = getattr(tool, "func", None)
            for cell in closure_cells(fn):
                val = getattr(cell, "cell_contents", None)
                if val is not None and is_agent_like(val):
                    if id(val) not in seen_agents:
                        parent_name_of[id(val)] = agent_id_map.get(id(agent))
                        queue.append(val)
                    if tool.name:
                        tools_to_remove.add(tool.name)

    filtered_tools = [t for t in tools if t["name"] not in tools_to_remove]

    tool_map = {}
    for idx, tool in enumerate(filtered_tools, start=1):
        tool["tool_num"] = idx
        tool_map[tool["name"]] = idx

    dependencies = []
    dependency_map = {}
    for idx, store in enumerate(vector_stores, start=1):
        dep = {
            "dependency_num": idx,
            "name": store.collection_name,
        }
        if hasattr(store, "collection_uuid") and store.collection_uuid:
            dep["id"] = store.collection_uuid
        dependencies.append(dep)
        dependency_map[store.collection_name] = idx

    _agents = []
    for agent in all_agents:
        agent_tools = [
            tool_map[t.name]
            for t in iter_agent_tools(agent)
            if getattr(t, "name", None) in tool_map
        ]

        agent_deps = []
        for t in iter_agent_tools(agent):
            tool_vector_stores = extract_vector_stores_from_tool(t)
            for store_info in tool_vector_stores:
                collection_name = store_info['collection_name']
                num = dependency_map.get(collection_name)
                if num and num not in agent_deps:
                    agent_deps.append(num)

        agent_kwargs = getattr(agent, "agent_kwargs", {}) or {}
        name = _agent_display_name(agent)

        _agents.append({
            "name": name,
            "idx": agent_id_map.get(id(agent)),
            "parent_agent_idx": parent_name_of.get(id(agent), ""),
            "tool": agent_tools,
            "output": [],
            "trigger": {},
            "agent_goal": agent_kwargs.get("goal", ""),
            "agent_role": agent_kwargs.get("role", ""),
            "agent_backstory": agent_kwargs.get("backstory", ""),
            "knowledge_stores": agent_deps,
            "prompt": get_agent_prompt(agent),
            "prefix": agent_kwargs.get("prefix", ""),
            "suffix": agent_kwargs.get("suffix", ""),
            "schema": get_agent_schema(agent),
        })

    nodes = {
        "1": {
            "id": "1",
            "slug": "",
            "stage": "middle",
            "title": "Agent Executor",
            "params": {"agents": _agents},
            "handler": [
                {
                    "step": None,
                    "type": "finish",
                    "condition": {"value": "output", "test_value": True, "condition_test": "=="},
                    "edge_description": "",
                }
            ],
            "node_type": "KNOWLEDGE_STORE_AGENT_EXECUTOR",
            "position_x": 490.24,
            "position_y": 66.4,
            "description": "",
        }
    }

    tools_json = {
        "tool": {
            "id": "tool",
            "slug": "",
            "type": "KNOWLEDGE_STORE_TOOLS",
            "stage": "start",
            "title": "Tools",
            "params": {"tools": filtered_tools},
            "handler": [
                {
                    "step": "1",
                    "type": "go_to",
                    "condition": None,
                    "edge_description": "",
                }
            ],
            "position_x": -152.7,
            "position_y": 353,
            "description": "",
        }
    } if filtered_tools else {}

    dependency_json = {
        "dependency": {
            "id": "dependency",
            "slug": "",
            "type": "KNOWLEDGE_STORE_DEPENDENCIES",
            "stage": "start",
            "title": "Dependencies",
            "params": {"dependencies": dependencies},
            "handler": [
                {
                    "step": "1",
                    "type": "go_to",
                    "condition": None,
                    "edge_description": "",
                }
            ],
            "position_x": -152.7,
            "position_y": 121.61,
            "description": "",
        }
    } if dependencies else {}

    return {
        "nodes": nodes,
        **dependency_json,
        **tools_json,
    }

def get_agent_prompt(agent) -> str:
    import inspect
    from collections import deque

    # Safe import of prompt classes – works even when LangChain is absent
    try:
        from langchain_core.prompts import PromptTemplate
        from langchain_core.prompts.chat import (
            ChatPromptTemplate,
            SystemMessagePromptTemplate,
        )
        prompt_classes = (PromptTemplate, ChatPromptTemplate)
    except Exception:  # pragma: no cover
        PromptTemplate = ChatPromptTemplate = SystemMessagePromptTemplate = None
        prompt_classes = tuple()

    def _extract_prompt(val):
        """Return the underlying template string if *val* looks like a prompt."""
        # PromptTemplate
        if PromptTemplate and isinstance(val, PromptTemplate):
            return val.template

        # ChatPromptTemplate – look for a system‑message prompt first
        if ChatPromptTemplate and isinstance(val, ChatPromptTemplate):
            for msg in getattr(val, "messages", []):
                if (
                    SystemMessagePromptTemplate
                    and isinstance(msg, SystemMessagePromptTemplate)
                ):
                    tpl = getattr(msg, "prompt", None)
                    if PromptTemplate and isinstance(tpl, PromptTemplate):
                        return tpl.template
            # Fallback – some ChatPromptTemplates expose `.template`
            if hasattr(val, "template"):
                return getattr(val, "template")

        # Raw string prompt
        if isinstance(val, str):
            return val

        return None

    # 0. Unwrap AgentExecutor‑like containers
    runnable_agent = getattr(agent, "agent", None) or agent

    # 1. Quick path via agent_kwargs
    agent_kwargs = getattr(runnable_agent, "agent_kwargs", {}) or {}
    for key in ("system_message", "prefix", "prompt"):
        if agent_kwargs.get(key):
            return agent_kwargs[key]

    # 2. Breadth‑first search through common nesting patterns
    search_queue = deque([runnable_agent])
    visited_ids = set()

    candidate_attrs = (
        "prompt",
        "llm_chain",
        "chain",
        "default_chain",
        "router_chain",
        "destination_chains",
        "executor_chain",
        "retriever_chain",
        "runnable",
        "middle",
    )

    while search_queue:
        current = search_queue.popleft()
        if id(current) in visited_ids:
            continue
        visited_ids.add(id(current))

        # The object itself might be a prompt
        extracted = _extract_prompt(current)
        if extracted:
            return extracted

        # Explore child attributes
        for attr in candidate_attrs:
            if not hasattr(current, attr):
                continue
            child = getattr(current, attr)

            # Direct extraction
            extracted = _extract_prompt(child)
            if extracted:
                return extracted

            # Queue nested structures for further exploration
            if isinstance(child, (list, tuple, set)):
                search_queue.extend(child)
            elif isinstance(child, dict):
                search_queue.extend(child.values())
            else:
                # Ignore primitives, strings, callables, prompt classes themselves
                if (
                    not isinstance(child, (*prompt_classes, str))
                    and not inspect.isroutine(child)
                ):
                    search_queue.append(child)

    # Nothing found – return empty string
    return ""


def get_agent_schema(agent):
    """
    Returns a JSON schema dict when available, otherwise None.
    Checks common attributes across SimpleAgent and LangChain agents.
    """
    candidate_attrs = ("args_schema", "input_schema", "agent_schema", "schema")
    for attr in candidate_attrs:
        obj = getattr(agent, attr, None)
        if obj is None:
            continue
        try:
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "model_json_schema") and callable(getattr(obj, "model_json_schema")):
                return obj.model_json_schema()
            if hasattr(obj, "schema") and callable(getattr(obj, "schema")):
                return obj.schema()
        except Exception as e:
            pass

    inner = getattr(agent, "agent", None)
    if inner is not None and inner is not agent:
        return get_agent_schema(inner)

    return None