import os
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from chronos.mcp import MCPGateway
from chronos.llm import UniversalExtractor

def create_server() -> Server:
    app = Server("chronos-mcp")
    gateway = MCPGateway()
    
    # 初始化提取器（如果在环境中配置了API KEY）
    api_key = os.environ.get("MINIMAX_API_KEY")
    if api_key:
        base_url = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
        model = os.environ.get("MINIMAX_MODEL", "abab6.5-chat")
        gateway.extractor = UniversalExtractor(api_key=api_key, base_url=base_url, model=model)
    
    @app.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="inject_knowledge",
                description="Extract S-P-O-T tuples from unstructured text into the temporal graph.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Unstructured text (e.g. news, reports)"},
                        "source_id": {"type": "string", "description": "Unique identifier for the source"},
                        "publish_date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["text", "source_id", "publish_date"]
                }
            ),
            Tool(
                name="query_graph",
                description="Query the Universal 4D Hypergraph memory.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string", "description": "Filter by Subject (Entity)"},
                        "predicate": {"type": "string", "description": "Filter by Predicate (Relation/Property)"},
                        "object": {"type": "string", "description": "Filter by Object (Value/Target Entity)"}
                    }
                }
            ),
            Tool(
                name="trigger_sleep",
                description="Trigger cognitive consolidation to self-evolve the graph ontology.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        import json
        if name == "inject_knowledge":
            if not gateway.extractor:
                return [TextContent(type="text", text=json.dumps({"error": "Extractor not configured. Set MINIMAX_API_KEY."}))]
            
            # 由于底层 extractor.extract_to_graph 目前是同步方法，如果是真正的异步环境，应该用 run_in_executor
            res = gateway.inject_knowledge(
                text=arguments["text"],
                source_id=arguments["source_id"],
                publish_date_str=arguments["publish_date"]
            )
            return [TextContent(type="text", text=json.dumps(res))]
            
        elif name == "query_graph":
            res = gateway.query_graph(
                subject=arguments.get("subject"),
                predicate=arguments.get("predicate"),
                object=arguments.get("object")
            )
            return [TextContent(type="text", text=json.dumps(res, ensure_ascii=False, indent=2))]
            
        elif name == "trigger_sleep":
            res = gateway.trigger_sleep()
            return [TextContent(type="text", text=json.dumps(res))]
            
        else:
            raise ValueError(f"Unknown tool: {name}")

    return app

async def main_async():
    app = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
