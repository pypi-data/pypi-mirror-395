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
                        description="""
                        扫描指定本地目录（递归）以发现可读的 DICOM 文件（后缀通常为 .dcm）。

                        功能与输出：
                        - 遍历目录并统计：患者数（unique PatientID）、序列数（unique SeriesInstanceUID）、文件总数和总字节数。
                        - 返回内容为结构化 JSON（文本形式），包含每个患者/序列的基本统计信息和遇到的不可读文件列表或解析错误。

                        输入要求：
                        - `directory_path` 必须是可访问的本地绝对或相对路径，并且程序有权限读取该目录及其子目录。

                        注意事项和推荐流程：
                        - 如果扫描结果指示某个目录包含多于 1 个序列（series_count > 1），在使用 `Analysis_dicom_directory` 上传分析前，建议先使用 `fileforsep` 工具将文件按患者/序列拆分为独立子目录。
                        - 成功返回示例（简化）:
                            {
                                "patients": 2,
                                "series": 3,
                                "files": 120,
                                "bytes": 12345678,
                                "details": [{"patient_id":"P1","series_count":2,...}]
                            }

                        错误处理：若目录不存在或不可读，返回包含 `error` 字段的说明。""",
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
            description="""
            解析单个本地 DICOM 文件并提取常用元数据字段。

            功能与输出：
            - 读取目标文件并提取常见标签（例如：PatientID、PatientName、StudyInstanceUID、SeriesInstanceUID、SeriesDescription、StudyDate、Modality 等）。
            - 返回结构化 JSON（文本形式），包括解析到的字段、每个字段的原始值以及简短的校验信息（例如 UID 格式是否正常）。

            输入要求：
            - `file_path` 必须指向存在的 DICOM 文件（本地路径）。

            错误处理：
            - 对于非 DICOM 或损坏文件，返回包含 `error`、`message` 字段的说明，便于上层逻辑决定是否跳过或重试。""",
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
                        对单个 DICOM 序列目录执行分析上传流程，并返回上传与处理的结果信息。

                        适用场景与前提：
                        - 该工具期望 `directory_path` 指向一个只包含单个 DICOM 序列（即同一 SeriesInstanceUID）或一个已拆分好的序列目录。
                        - 若目录中包含多个序列，请先使用 `fileforsep` 对顶层目录进行拆分，然后对每个子序列目录单独调用本工具。

                        主要步骤：
                        1. 标准化并校验目录路径与文件权限。
                        2. 按 `series_type`（例如："1" 表示主动脉，"9" 表示二尖瓣）选择远端分析服务或参数集；不在允许列表中的 `series_type` 会被拒绝并返回错误。
                        3. 运行上传前检查（例如：文件完整性、必须的 DICOM 标签存在性、最大/最小切片数等），不满足要求的序列会返回明确原因并跳过上传。
                        4. 执行分步上传：上传序列元数据 -> 逐文件上传 DICOM 内容 -> 最终提交并确认。每一步都会记录进度与错误，以便恢复或重试。

                        返回值（结构化 JSON 示例）:
                        返回值的studyid对应上传时的StudyInstanceUID，可以用于'get_result_tool',查询分析结果。
                        错误与重试：如果单个序列上传失败，返回详细错误并允许用户对该目录跳过。""",
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
            将一个顶层 DICOM 目录按患者（PatientID）和序列（SeriesInstanceUID）拆分为一组有序的子目录，便于逐序列上传与后续分析。

            主要功能：
            - 扫描顶层目录并根据 DICOM 标签将文件分组到 `output_root/<PatientID>/<SeriesInstanceUID>/` 的结构中。
            - 生成并保存统计文件 `文件拆分信息.csv` 于与 `fileforsep` 输入目录同级位置，记录每个子序列的文件数、路径、患者信息等，作为幂等检查标志。
            - 若发现已存在 `文件拆分信息.csv`，默认直接返回该 CSV 的解析结果（避免重复工作），除非强制重新拆分（当前工具不包含强制标志）。

            输出（结构化 JSON 示例）:
            {
              "root_output": "...",
              "patient_count": 5,
              "series_count": 12,
              "copied_files": 480,
              "csv_path": "...\\文件拆分信息.csv",
              "folders": [ ...]
            }

           对每个返回的子目录使用 `Analysis_dicom_directory` 逐一上传分析。""",
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
            description="""
            根据远端分析的 `study_uid` 查询测量/分析结果的可用性和访问 URL。

            使用说明与前提：
            - 本工具仅用于查询已提交并被远端处理的任务；若尚未调用 `Analysis_dicom_directory` 完成上传并触发分析，查询会提示 `not_found` 或 `pending` 并说明需要先上传。
            - 对于一个 study 包含多个序列的情况，必须先使用 `fileforsep` 拆分并对每个序列分别调用 `Analysis_dicom_directory` 上传分析，然后再使用本工具查询合并或单个序列的结果（视远端实现）。

            返回示例：
            - 成功：{"study_uid":"...","status":"completed","result_url":"https://..."}
            - 处理中：{"study_uid":"...","status":"pending","estimated_time":"..."}
            - 未找到或需上传：{"study_uid":"...","status":"not_found","message":"请先使用 Analysis_dicom_directory 上传该 study 的 DICOM 文件"}

            错误处理：若提供的 `study_uid` 格式不正确或远端服务不可达，将返回包含 `error` 与 `message` 的说明，便于自动化系统决定重试或提醒人工干预。""",
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