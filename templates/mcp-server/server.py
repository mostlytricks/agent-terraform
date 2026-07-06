"""Template MCP server for generated services.

Shows the three tool shapes generate-mcp emits: a readonly endpoint tool,
a destructive endpoint tool with confirm gating, and a workflow tool that
chains calls server-side. Generated servers replace the example tools with
ones derived from spec.yaml but keep this structure.
"""

from fastmcp import FastMCP
from fastmcp.tools.tool import ToolAnnotations

from client import call, make_client

mcp = FastMCP("SERVICE_NAME")
http = make_client()


# --- readonly endpoint tool -------------------------------------------------
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_example(example_id: str) -> str:
    """<when_to_use text from spec, including negative guidance>

    Args:
        example_id: <param description from spec, with format/example>
    """
    return await call(
        http,
        "GET",
        f"/api/v1/examples/{example_id}",
        error_map={
            404: "No example with that id. Report it was not found; suggest search_examples.",
        },
        retry_readonly=True,
    )


# --- destructive endpoint tool: confirm-gated -------------------------------
@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def delete_example(example_id: str, confirm: bool = False) -> str:
    """<when_to_use from spec> Destructive: requires user confirmation.

    Args:
        example_id: <param description>
        confirm: Must be true. Set only after the user has explicitly
            confirmed this specific deletion.
    """
    if not confirm:
        return (
            "Not executed. This permanently deletes the example. Confirm with "
            "the user (show them the id and what will be lost), then retry "
            "with confirm=true."
        )
    return await call(
        http,
        "DELETE",
        f"/api/v1/examples/{example_id}",
        error_map={409: "Example is referenced elsewhere. Surface the conflict to the user."},
    )


# --- workflow tool: chains endpoints server-side -----------------------------
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def check_example_health(example_id: str) -> str:
    """<workflow when_to_use from spec — one tool instead of N agent-side calls>

    Args:
        example_id: <param description>
    """
    detail = await call(http, "GET", f"/api/v1/examples/{example_id}", retry_readonly=True)
    status = await call(http, "GET", f"/api/v1/examples/{example_id}/status", retry_readonly=True)
    return f"Detail:\n{detail}\n\nStatus:\n{status}"


if __name__ == "__main__":
    mcp.run()
