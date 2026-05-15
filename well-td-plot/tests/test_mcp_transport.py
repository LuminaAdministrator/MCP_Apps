"""Real subprocess stdio transport test — exercises the MCP boundary directly."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MCP_MODULE = "well_td_plot.mcp_server"


def _make_rpc(method: str, params: dict | None = None, *, id: int = 1) -> str:
    return json.dumps({"jsonrpc": "2.0", "id": id, "method": method, "params": params or {}}) + "\n"


def _make_notification(method: str, params: dict | None = None) -> str:
    return json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}}) + "\n"


def _read_response(proc: subprocess.Popen, timeout: float = 5.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if line:
            return json.loads(line)
    raise TimeoutError("No response from MCP server within timeout")


@pytest.fixture()
def mcp_proc():
    env = {**os.environ, "TD_PLOT_DATA_SOURCE_MODE": "fixture"}
    proc = subprocess.Popen(
        [sys.executable, "-m", MCP_MODULE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        cwd=str(PROJECT_ROOT),
    )
    yield proc
    proc.stdin.close()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def _do_initialize(proc: subprocess.Popen) -> dict:
    proc.stdin.write(
        _make_rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "0.0.1"},
        }).encode()
    )
    proc.stdin.flush()
    response = _read_response(proc)
    proc.stdin.write(_make_notification("notifications/initialized").encode())
    proc.stdin.flush()
    return response


def test_mcp_server_starts_and_initializes(mcp_proc):
    response = _do_initialize(mcp_proc)
    assert "result" in response
    assert "error" not in response


def test_mcp_tool_list_includes_render_td_plot(mcp_proc):
    _do_initialize(mcp_proc)
    mcp_proc.stdin.write(_make_rpc("tools/list", {}, id=2).encode())
    mcp_proc.stdin.flush()
    response = _read_response(mcp_proc)
    names = [t["name"] for t in response["result"].get("tools", [])]
    assert "render_td_plot" in names


def test_mcp_tool_call_returns_valid_envelope(mcp_proc, envelope_schema, schema_registry):
    import jsonschema

    _do_initialize(mcp_proc)
    mcp_proc.stdin.write(_make_rpc("tools/list", {}, id=2).encode())
    mcp_proc.stdin.flush()
    _read_response(mcp_proc)

    mcp_proc.stdin.write(
        _make_rpc(
            "tools/call",
            {"name": "render_td_plot", "arguments": {"uniquedataid": "example-well-001"}},
            id=3,
        ).encode()
    )
    mcp_proc.stdin.flush()

    response = _read_response(mcp_proc, timeout=10.0)
    assert "result" in response

    result = response["result"]
    envelope = result.get("structuredContent")
    if envelope is None:
        for item in result.get("content", []):
            if isinstance(item, dict) and item.get("type") == "text":
                try:
                    parsed = json.loads(item["text"])
                    if parsed.get("result_kind") == "app_instance":
                        envelope = parsed
                        break
                except (json.JSONDecodeError, KeyError):
                    pass

    assert envelope is not None, "No JIO envelope found in tool response"
    assert envelope["result_kind"] == "app_instance"
    assert envelope["app_id"] == "well.TD.plot"
    assert envelope["state"]["time_ref"] == "TWT"

    validator = jsonschema.Draft202012Validator(envelope_schema, registry=schema_registry)
    errors = list(validator.iter_errors(envelope))
    assert not errors, "MCP tool envelope errors:\n" + "\n".join(str(e) for e in errors)


def test_mcp_stdout_has_no_banner(mcp_proc):
    response = _do_initialize(mcp_proc)
    assert json.dumps(response).startswith("{")
