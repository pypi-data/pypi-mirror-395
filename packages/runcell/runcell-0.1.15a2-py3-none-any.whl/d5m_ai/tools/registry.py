"""
Simple registry for ask-mode proxy tools.

Provides a single place to execute local tools (read_file, list_dir, grep)
and normalize outputs for both LLM messages and SSE updates.
"""

from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

from .read_file import execute_read_file_tool
from .list_dir import execute_list_dir_tool
from .grep import execute_grep_tool
from .edit import execute_edit_tool
from .apply_patch import execute_apply_patch_tool
from .glob_search import execute_glob_tool


ToolExecutor = Callable[[Dict[str, Any]], Awaitable[Any]]
PostProcessor = Callable[[Any], Tuple[str, Any]]


def _default_postprocess(result: Any) -> Tuple[str, Any]:
    return str(result), result


def _list_dir_postprocess(result: Any) -> Tuple[str, Any]:
    """Return JSON string for LLM, structured list for SSE."""
    try:
        return json.dumps(result), result
    except Exception:
        return str(result), result


def _grep_postprocess(result: Any) -> Tuple[str, Any]:
    """
    Grep already returns JSON string; keep it for LLM, try to parse for SSE.
    """
    llm_output = result if isinstance(result, str) else str(result)
    try:
        sse_output = json.loads(llm_output)
    except Exception:
        sse_output = llm_output
    return llm_output, sse_output


def _glob_postprocess(result: Any) -> Tuple[str, Any]:
    """
    Return JSON string for LLM and structured list for SSE.
    """
    if isinstance(result, list):
        try:
            return json.dumps(result), result
        except Exception:
            pass
    return str(result), result


ASK_TOOL_REGISTRY: Dict[str, Tuple[ToolExecutor, PostProcessor]] = {
    "read_file": (execute_read_file_tool, _default_postprocess),
    "list_dir": (execute_list_dir_tool, _list_dir_postprocess),
    "grep": (execute_grep_tool, _grep_postprocess),
    "edit": (execute_edit_tool, _default_postprocess),
    "apply_patch": (execute_apply_patch_tool, _default_postprocess),
    "glob": (execute_glob_tool, _glob_postprocess),
}


async def run_ask_tool(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Execute a registered ask-mode tool.

    Returns:
        dict with llm_output (str) and sse_output (Any) or None if unsupported.
    """
    entry = ASK_TOOL_REGISTRY.get(tool_name)
    if not entry:
        return None

    executor, postprocess = entry
    raw_result = await executor(args)
    llm_output, sse_output = postprocess(raw_result)

    return {
        "llm_output": llm_output,
        "sse_output": sse_output,
    }
