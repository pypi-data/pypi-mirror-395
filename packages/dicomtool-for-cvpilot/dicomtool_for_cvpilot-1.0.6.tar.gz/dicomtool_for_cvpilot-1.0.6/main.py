#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DICOM 工具 MCP 服务器主文件

基于 MCP (Model Context Protocol) 的 DICOM 医学影像文件分析工具的Python实现。
"""

import os
import asyncio
import json
import logging
import sys
from typing import Any, Dict

# 设置标准输出编码为 UTF-8 (Windows 兼容性)
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 配置MCP服务器所需的导入
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
    from pydantic import BaseModel
except ImportError as e:
    print(f"错误: 缺少必要的MCP依赖库: {e}", file=sys.stderr)
    print("请运行: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# 导入DICOM工具
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dicom_tools.scanner import scan_dicom_directory_tool
from dicom_tools.parser import parse_dicom_file_tool
from setup import Analysis_dicom_directory_tool, separate_series_by_patient_tool, get_result_tool

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# 创建MCP服务器实例
server = Server("dicom-tools-python")


# 工具参数模型
class DirectoryPathArgs(BaseModel):
    directory_path: str


class DirectoryPathWithSeriesArgs(BaseModel):
    directory_path: str
    series_type: str


class FilePathArgs(BaseModel):
    file_path: str

class fileforsep(BaseModel):
    fileforsep: str

class study_id(BaseModel):
    study_uid: str

@server.list_tools()
async def list_tools() -> list[Tool]:
    """注册所有可用的DICOM工具"""
    return [
        Tool(
            name="scan-dicom-directory",
            description="扫描指定目录下所有可读的 .dcm 文件，汇总患者数、序列数、文件数和总字节数，返回 JSON 文本；目录需存在并可访问。",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "待扫描的本地目录路径，绝对路径，必须存在且可读"
                    }
                },
                "required": ["directory_path"]
            }
        ),
        Tool(
            name="parse-dicom-file",
            description="解析单个 DICOM 文件，提取 PatientID、PatientName、SeriesInstanceUID、SeriesDescription 等元数据，返回结构化 JSON；无效文件会返回错误说明。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "待解析的本地 DICOM 文件路径，需指向实际存在的 .dcm 文件"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="Analysis_dicom_directory",
            description="""
                        扫描目录中的 DICOM 序列，按 series_type 选择分析流程并上传到预配置的远端分析服务，返回上传结果及序列信息，只能对一个包含dicom的文件夹进行分析。
                        它具备以下功能：
                        1. 目录路径标准化，支持多种输入格式。
                        2. 按指定的 series_type 选择分析流程，支持主动脉和二尖瓣等多种分析类型。
                        3. 上传前检查序列是否符合上传标准，避免无效上传。
                        4. 分步上传流程，包含初始元数据上传、DICOM 文件上传和最终元数据确认。
                        他每调用一次只能对单个序列进行拆分，如果拆分的序列超过一个请调用{fileforsep}工具进行拆分。""",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "包含待分析 DICOM 序列的本地目录路径，必须存在且具备读取权限"
                    },
                    "series_type": {
                        "type": "string",
                        "description": "分析流程类型：`1`=主动脉分析，`9`=二尖瓣分析，其他值将被拒绝"
                    }
                },
                "required": ["directory_path", "series_type"]
            }
        ),
        Tool(
            name="fileforsep",
            description="""
                按患者和序列拆分目录下的 DICOM 文件，生成新的子目录结构，并以 JSON 返回整理后的统计结果,统计结果的 CSV 文件保存在同级目录下的 '文件拆分信息.csv' 文件中。
                它具备一下功能：
                1. 检测到已存在的 '文件拆分信息.csv' 文件时，直接返回已拆分的信息，避免重复拆分。
                2. 按患者 ID 创建子目录，并在每个患者目录下按序列 UID 创建子目录，确保文件有序存放。
                3. 记录每个序列的元数据信息，包括患者 ID、患者姓名、序列 UID 等，并将新文件位置添加到记录中。
                4. 返回拆分后的患者数量、序列数量和成功复制的文件数量，方便用户了解拆分结果。
                他的返回信息包括：创建的文件夹路径可以调用{Analysis_dicom_directory}工具进行上传分析。""",
            inputSchema={
                "type": "object",
                "properties": {
                    "fileforsep": {
                        "type": "string",
                        "description": "待整理的顶层目录路径，执行过程中会在同级创建输出目录"
                    }
                }, 
                "required": ["fileforsep"]
            }
        ),
        Tool(
            name="get_result_tool",
            description="根据文件夹的study_uid，如果没有分析结果，需要进行{Analysis_dicom_directory}工具上传分析，返回测量结果的url,",
            inputSchema={
                "type": "object",
                "properties": {
                    "study_uid": {
                        "type": "string",
                        "description": "DICOM序列的 study_uid，用于查询分析结果"
                    }
                },
                "required": ["study_uid"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """处理工具调用请求"""
    try:
        logger.info(f"调用工具: {name}, 参数: {arguments}")

        if name == "scan-dicom-directory":
            args = DirectoryPathArgs(**arguments)
            result = await scan_dicom_directory_tool(args.directory_path)
        elif name == "parse-dicom-file":
            args = FilePathArgs(**arguments)
            result = await parse_dicom_file_tool(args.file_path)
        elif name == "Analysis_dicom_directory":
            args = DirectoryPathWithSeriesArgs(**arguments)
            result = await Analysis_dicom_directory_tool(args.directory_path, args.series_type)
        elif name == "fileforsep":
            args = fileforsep(**arguments)
            result = await separate_series_by_patient_tool(args.fileforsep)
        elif name == "get_result_tool":
            args = study_id(**arguments)
            result = await get_result_tool(args.study_uid)
        else:
            raise ValueError(f"未知工具: {name}")

        # 转换结果格式为MCP标准格式
        return [
            TextContent(
                type="text",
                text=content["text"]
            )
            for content in result["content"]
            if content["type"] == "text"
        ]

    except Exception as e:
        logger.error(f"工具调用失败: {name}, 错误: {e}", exc_info=True)

        error_response = {
            "error": True,
            "message": f"工具 {name} 执行失败: {str(e)}"
        }

        return [
            TextContent(
                type="text",
                text=json.dumps(error_response, ensure_ascii=False)
            )
        ]


async def main():
    """启动MCP服务器"""
    try:
        logger.info("启动 DICOM 工具 MCP 服务器 ...")

        # 使用stdio传输启动服务器
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
    except Exception as e:
        logger.error(f"服务器运行失败: {e}", exc_info=True)
        sys.exit(1)


def run():
    """同步入口函数，用于 uvx 调用"""
    # 设置事件循环策略（Windows兼容性）
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # 运行服务器
    asyncio.run(main())


if __name__ == "__main__":
    run()