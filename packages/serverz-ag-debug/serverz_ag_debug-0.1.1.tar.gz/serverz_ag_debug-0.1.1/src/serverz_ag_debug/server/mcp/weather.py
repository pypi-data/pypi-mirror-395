from datetime import datetime
from mcp.server.fastmcp import FastMCP


def create_mcp():
    # region MCP Weather
    mcp = FastMCP("Weather")

    @mcp.tool()
    def get_weather(location: str) -> str:
        return "Cloudy"

    @mcp.tool()
    def get_time() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # endregion
    return mcp



if __name__ == "__main__":
    mcp = create_mcp()
    mcp.run(transport="streamable-http")


