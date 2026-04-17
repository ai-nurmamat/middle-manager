"""
Chronos-MCP Server.

This module sets up the official Model Context Protocol (MCP) server,
allowing seamless integration with any MCP-compatible AI Assistant (e.g., Claude Desktop, Trae).
"""

import os
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from chronos.mcp import MCPGateway
from chronos.llm import UniversalExtractor


def create_server() -> Server:
    """
    Create and configure the MCP Server instance.

    Returns:
        Server: The configured MCP Server.
    """
    app = Server("chronos-mcp")
    gateway = MCPGateway()

    # Initialize the LLM extractor if an API key is provided
    api_key = os.environ.get("MINIMAX_API_KEY")
    if api_key:
        base_url = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
        model = os.environ.get("MINIMAX_MODEL", "abab6.5-chat")
        gateway.extractor = UniversalExtractor(
            api_key=api_key, base_url=base_url, model=model
        )

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="inject_knowledge",
                description="Extract S-P-O-T tuples from unstructured text into the temporal graph.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Unstructured text (e.g. news, reports)",
                        },
                        "source_id": {
                            "type": "string",
                            "description": "Unique identifier for the source",
                        },
                        "publish_date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format",
                        },
                    },
                    "required": ["text", "source_id", "publish_date"],
                },
            ),
            Tool(
                name="query_graph",
                description="Query the Universal 4D Hypergraph memory.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "Filter by Subject (Entity)",
                        },
                        "predicate": {
                            "type": "string",
                            "description": "Filter by Predicate (Relation/Property)",
                        },
                        "object": {
                            "type": "string",
                            "description": "Filter by Object (Value/Target Entity)",
                        },
                    },
                },
            ),
            Tool(
                name="trigger_sleep",
                description="Trigger cognitive consolidation to self-evolve the graph ontology.",
                inputSchema={"type": "object", "properties": {}},
            ),
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == "inject_knowledge":
            # Real-world scenarios should use run_in_executor for synchronous extraction calls
            if (
                not isinstance(gateway.extractor, UniversalExtractor)
                and "MINIMAX_API_KEY" not in os.environ
            ):
                # It's okay to run MockExtractor for demo, but warn the user
                pass

            res = gateway.inject_knowledge(
                text=arguments["text"],
                source_id=arguments["source_id"],
                publish_date_str=arguments["publish_date"],
            )
            return [TextContent(type="text", text=json.dumps(res))]

        elif name == "query_graph":
            res_query = gateway.query_graph(
                subject=arguments.get("subject"),
                predicate=arguments.get("predicate"),
                object=arguments.get("object"),
            )
            return [
                TextContent(
                    type="text",
                    text=json.dumps(res_query, ensure_ascii=False, indent=2),
                )
            ]

        elif name == "trigger_sleep":
            res_sleep = gateway.trigger_sleep()
            return [TextContent(type="text", text=json.dumps(res_sleep))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    return app


async def main_async() -> None:
    """Run the MCP server asynchronously over stdio."""
    app = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main() -> None:
    """Entry point for the chronos-mcp executable."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
