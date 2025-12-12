"""
FastMCP quickstart example.

"""

from mcp.server.fastmcp import FastMCP
from prompt_writing_assistant.file_manager import ContentManager, TextType

# uv run mcp dev src/obsidian_sdk/mcp.py
# Create an MCP server
mcp = FastMCP("Demo")
content_manager = ContentManager()

@mcp.tool()
def save_content(text:str)->str:
    """
    text : 需要存储的内容

    return : 返回是否存储成功的信息
    """
    result =content_manager.save_content_auto(
                text = text)
    return result


@mcp.tool()
def similarit_content(text: str,limit: int):
    """
    text : 待查询的文字, 进行匹配
    limit : 查询的数量
    """
    
    result = content_manager.similarity(
        content = text,
        limit = limit
    )
    return result



@mcp.resource("file://notes/{name}")
def read_notes(name:str)-> str:
    """ 阅读备忘录"""

    return "你要做王子"


if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    mcp.run(transport="sse")
    # search_mcp.run(transport="sse", mount_path="/search")