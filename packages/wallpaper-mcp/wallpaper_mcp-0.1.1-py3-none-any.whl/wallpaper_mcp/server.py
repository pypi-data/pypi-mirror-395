#!/usr/bin/env python3
"""
Wallpaper MCP Server - 桌面壁纸替换服务

提供通过 MCP 协议设置桌面壁纸的功能
"""

import asyncio
import logging
from typing import Any, Dict, Optional
from pathlib import Path

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from .wallpaper import WallpaperManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建服务器实例
server = Server("wallpaper-mcp")
wallpaper_manager = WallpaperManager()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用的工具"""
    return [
        types.Tool(
            name="set_wallpaper_from_url",
            description="从指定URL下载图片并设置为桌面壁纸",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "图片的URL地址"
                    },
                    "resolution": {
                        "type": "object",
                        "description": "目标分辨率（可选）",
                        "properties": {
                            "width": {
                                "type": "integer",
                                "description": "宽度（像素）"
                            },
                            "height": {
                                "type": "integer",
                                "description": "高度（像素）"
                            }
                        }
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="set_wallpaper_from_file",
            description="将本地图片文件设置为桌面壁纸",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "本地图片文件路径"
                    },
                    "resolution": {
                        "type": "object",
                        "description": "目标分辨率（可选）",
                        "properties": {
                            "width": {
                                "type": "integer",
                                "description": "宽度（像素）"
                            },
                            "height": {
                                "type": "integer",
                                "description": "高度（像素）"
                            }
                        }
                    }
                },
                "required": ["file_path"]
            }
        ),
        types.Tool(
            name="get_current_resolution",
            description="获取当前屏幕分辨率",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: Dict[str, Any]
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用"""

    try:
        if name == "set_wallpaper_from_url":
            url = arguments.get("url")
            resolution = arguments.get("resolution")

            if not url:
                return [types.TextContent(
                    type="text",
                    text="Error: image URL is required"
                )]

            # 处理分辨率参数
            res_tuple = None
            if resolution and isinstance(resolution, dict):
                width = resolution.get("width")
                height = resolution.get("height")
                if width and height:
                    res_tuple = (width, height)

            # 设置壁纸
            success = await asyncio.to_thread(
                wallpaper_manager.set_wallpaper_from_url,
                url,
                res_tuple
            )

            if success:
                return [types.TextContent(
                    type="text",
                    text=f"✅ Wallpaper set successfully\nImage URL: {url}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text="❌ Failed to set wallpaper; check logs for details"
                )]

        elif name == "set_wallpaper_from_file":
            file_path = arguments.get("file_path")
            resolution = arguments.get("resolution")

            if not file_path:
                return [types.TextContent(
                    type="text",
                    text="Error: file path is required"
                )]

            # 处理分辨率参数
            res_tuple = None
            if resolution and isinstance(resolution, dict):
                width = resolution.get("width")
                height = resolution.get("height")
                if width and height:
                    res_tuple = (width, height)

            # 设置壁纸
            success = await asyncio.to_thread(
                wallpaper_manager.set_wallpaper_from_file,
                file_path,
                res_tuple
            )

            if success:
                return [types.TextContent(
                    type="text",
                    text=f"✅ Wallpaper set successfully\nFile path: {file_path}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text="❌ Failed to set wallpaper; check logs for details"
                )]

        elif name == "get_current_resolution":
            resolution = await asyncio.to_thread(
                wallpaper_manager.get_screen_resolution
            )

            return [types.TextContent(
                type="text",
                text=f"📱 Current screen resolution: {resolution[0]} x {resolution[1]} px"
            )]

        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    except Exception as e:
        logger.error(f"工具执行错误: {e}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """主函数"""
    logger.info("启动 Wallpaper MCP 服务器...")

    # 使用stdio传输运行服务器
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="wallpaper-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
