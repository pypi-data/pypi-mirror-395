import asyncio
from .common import mcp

async def main():
    # Import tools and resources
    from . import tools
    
    # Run the mcp server
    await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
