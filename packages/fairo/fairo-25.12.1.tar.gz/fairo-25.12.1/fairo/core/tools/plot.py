import os
from pathlib import Path
import uuid
from langchain_core.messages import ToolMessage
from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from langchain_core.tools import tool
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import io
import base64

class ChartTypeEnum(str, Enum):
    line = "line"
    bar = "bar"
    scatter = "scatter"
    hist = "hist"
    area = "area"

EXAMPLES = [
    {
        "chart_type": "line",
        "data": {"month": ["Jan","Feb","Mar"], "revenue": [10, 12, 15]},
        "x": "month",
        "y": "revenue",
        "title": "Revenue by Month"
    },
    {
        "chart_type": "bar",
        "data": {"cat": ["A","B"], "m1": [1,2], "m2":[2,1]},
        "x": "cat",
        "y": ["m1","m2"],
        "title": "Grouped Bars"
    }
]

class PlotSpec(BaseModel):
    """
    Either provide a 'spec' for a chart OR provide 'python_code' to execute.

    If you provide 'spec', set:
      - chart_type: one of line|bar|scatter|hist|area
      - data: list of dicts (table rows) OR {"x":[...], "y":[...]} arrays
      - x: x key (for list-of-dicts) or leave None if arrays
      - y: y key or list of keys for multi-series
      - title, xlabel, ylabel: optional labels
      - width, height in inches (optional)
    If you provide 'python_code', it must create a 'fig' and 'ax' variable.
    """
    model_config = ConfigDict(extra="allow", json_schema_extra={"examples": EXAMPLES})

    # Option A: high-level specification
    chart_type: Optional[ChartTypeEnum] = Field(None, description="Chart type.")
    data: Optional[Union[List[Dict], Dict[str, List]]] = Field(
        None, description="Either list of dict rows OR dict of arrays."
    )
    x: Optional[Union[str, List[str]]] = Field(None, description="X column or key(s).")
    y: Optional[Union[str, List[str]]] = Field(None, description="Y column or key(s).")
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    width: Optional[float] = Field(6.0, description="Figure width in inches.")
    height: Optional[float] = Field(4.0, description="Figure height in inches.")
    legend: Optional[bool] = True
    grid: Optional[bool] = True
    alpha: Optional[float] = 1.0

    # Option B: low-level custom code (SAFE-ish)
    python_code: Optional[str] = Field(
        None,
        description=(
            "Matplotlib code that defines 'fig, ax'. Avoid imports; "
            "numpy is available as 'np' and matplotlib.pyplot as 'plt'."
        ),
    )


def _png_base64_from_fig(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return b64


def _plot_from_spec(spec: PlotSpec) -> str:
    # Build figure
    fig, ax = plt.subplots(figsize=(spec.width or 6.0, spec.height or 4.0))

    # Normalize data
    data = spec.data or {}
    is_rows = isinstance(data, list)
    is_arrays = isinstance(data, dict) and all(isinstance(v, list) for v in data.values())

    def extract_series(xkey, ykey):
        if is_rows:
            xs = [row.get(xkey) for row in data]
            ys = [row.get(ykey) for row in data]
        elif is_arrays:
            xs = data.get(xkey) if xkey else range(len(data.get(ykey, [])))
            ys = data.get(ykey, [])
        else:
            raise ValueError("Unsupported data format. Provide list[dict] or dict of arrays.")
        return xs, ys

    # Handle y being single or multiple
    y_keys = [spec.y] if isinstance(spec.y, (str, type(None))) else list(spec.y or [])
    if not y_keys:  # auto-choose 'y' if present
        y_keys = ["y"] if (is_arrays and "y" in data) else []
        if not y_keys:
            raise ValueError("Could not infer 'y' series; please set y.")

    # Plot by chart_type
    if spec.chart_type == "line":
        for ykey in y_keys:
            xs, ys = extract_series(spec.x, ykey)
            ax.plot(xs, ys, alpha=spec.alpha, label=ykey if len(y_keys) > 1 else None)
    elif spec.chart_type == "bar":
        # Simple grouped bar if multiple y
        import numpy as np
        xs, _ = extract_series(spec.x, y_keys[0])
        x_index = np.arange(len(xs))
        n = len(y_keys)
        width = 0.8 / n
        for i, ykey in enumerate(y_keys):
            _, ys = extract_series(spec.x, ykey)
            ax.bar(x_index + i * width, ys, width=width, alpha=spec.alpha, label=ykey)
        ax.set_xticks(x_index + width * (n - 1) / 2)
        ax.set_xticklabels(xs, rotation=0)
    elif spec.chart_type == "scatter":
        for ykey in y_keys:
            xs, ys = extract_series(spec.x, ykey)
            ax.scatter(xs, ys, alpha=spec.alpha, label=ykey if len(y_keys) > 1 else None)
    elif spec.chart_type == "hist":
        # Expect a single series in y
        xs, ys = extract_series(spec.x, y_keys[0])
        values = ys if ys else xs
        ax.hist(values, alpha=spec.alpha)
    elif spec.chart_type == "area":
        for ykey in y_keys:
            xs, ys = extract_series(spec.x, ykey)
            ax.fill_between(xs, ys, alpha=spec.alpha, label=ykey if len(y_keys) > 1 else None)
    else:
        raise ValueError("Unsupported chart_type. Use line|bar|scatter|hist|area.")

    # Labels & cosmetics
    if spec.title:
        ax.set_title(spec.title)
    if spec.xlabel:
        ax.set_xlabel(spec.xlabel)
    if spec.ylabel:
        ax.set_ylabel(spec.ylabel)
    if spec.grid:
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    if spec.legend and len(y_keys) > 1:
        ax.legend()

    # Return base64
    b64 = _png_base64_from_fig(fig)
    plt.close(fig)
    return b64


def _plot_from_code(code: str) -> str:
    """
    Execute minimal matplotlib code that must define 'fig' and 'ax'.
    VERY LIMITED namespace to reduce risk.
    """
    import numpy as np

    allowed_globals = {
        "__builtins__": {
            "len": len, "range": range, "min": min, "max": max, "sum": sum, "abs": abs
        },
        "np": np,
        "plt": plt,
    }
    local_vars = {}

    # Simple guardrails
    forbidden = ["import os", "import sys", "open(", "subprocess", "socket", "eval(", "exec("]
    if any(tok in code for tok in forbidden):
        raise ValueError("Disallowed token in python_code.")

    exec(code, allowed_globals, local_vars)  # noqa: S102 (intentional, guarded)
    fig = local_vars.get("fig")
    ax = local_vars.get("ax")
    if fig is None or ax is None:
        raise ValueError("Your python_code must create variables 'fig' and 'ax'.")
    b64 = _png_base64_from_fig(fig)
    plt.close(fig)
    return b64


class PlotReturn(BaseModel):
    mime_type: Literal["image/png"] = "image/png"
    data_base64: str
    alt_text: Optional[str] = None
    debug: Optional[str] = None

def save_to_png_file(base64_data: str):
    artifact_id = uuid.uuid4()
    base_dir = Path("/tmp") if Path("/tmp").exists() else Path.cwd()
    file_path = base_dir / f"{artifact_id}.png"

    if not os.path.exists(file_path):
        # Decode base64 data and write as binary PNG file
        png_data = base64.b64decode(base64_data)
        with open(file_path, "wb") as f:
            f.write(png_data)

    return artifact_id

@tool(args_schema=PlotSpec)
def generate_plot(**kwargs) -> str:
    """
    Generate a plot image (PNG base64). Returns a JSON string with keys:
      - mime_type: 'image/png'
      - data_base64: <base64 string>
      - alt_text: optional
    """
    spec = PlotSpec(**kwargs)
    try:
        if spec.python_code:
            b64 = _plot_from_code(spec.python_code)
            alt = spec.title or "Custom matplotlib figure"
        else:
            b64 = _plot_from_spec(spec)
            alt = spec.title or (
                f"{spec.chart_type} plot" if spec.chart_type else "Plot"
            )
        result = PlotReturn(data_base64=b64, alt_text=alt)
        # Save the base64 data as a PNG file
        artifact_id = save_to_png_file(result.data_base64)
        return ToolMessage(
            content=f"Plot successfully generated",
            artifact={"artifact_id": artifact_id, "artifact_type": "png"},
            tool_call_id=uuid.uuid4()
        )
    except Exception as e:
        # Return an error payload the orchestrator can handle
        err = PlotReturn(
            data_base64="",
            alt_text="Plot generation failed.",
            debug=str(e),
        )
        return err.model_dump_json()
