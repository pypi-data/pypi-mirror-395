# DicomToolsForMCP

`DicomToolsForMCP` 是一个基于 MCP (Model Context Protocol) 的 DICOM 医学影像文件分析与上传工具。它提供了一整套命令行工具，用于处理、分析 DICOM 文件，并将其安全地上传到兼容 MCP 的服务器。

## 功能特性

- **DICOM 文件扫描与解析**: 递归扫描指定目录，解析 DICOM 文件，并提取元数据。
- **数据映射与预处理**: 根据预定义的规则，将 DICOM 标签映射为 MCP 模型所需的数据结构。
- **安全上传**: 通过 Cookie 认证，将处理后的序列安全上传到服务器。
- **状态查询**: 实时查询已上传序列的处理状态。
- **日志记录**: 自动记录每次上传的详细信息（如 `study_uid` 和目录路径），方便后续追踪。

## 安装

您可以通过 pip 从 PyPI 安装此工具：

```bash
pip install DicomToolsForMCP
```

## 使用方法

该工具提供了一个名为 `DicomToolsForMCP` 的命令行入口。

### 1. 配置文件

在运行前，请确保您的项目根目录中包含一个 `config.json` 文件，用于配置服务器地址和认证信息。

**`config.json` 示例:**

```json
{
  "base_url": "https://your-mcp-server.com",
  "cookie": "ls=your_session_cookie_here"
}
```

### 2. 运行主程序

通过以下命令启动主程序：

```bash
DicomToolsForMCP
```

程序将引导您完成以下操作：
1.  选择要处理的 DICOM 文件目录。
2.  自动扫描、解析并上传文件。
3.  查询并显示上传结果。

## 依赖项

本项目依赖于以下 Python 包：

- `mcp>=0.9.0`
- `pydicom>=2.4.0`
- `requests>=2.31.0`
- `pydantic>=2.0.0`
- `tqdm>=4.66.0`
- `pandas`
- `pyorthanc`

所有依赖项将在安装 `DicomToolsForMCP` 时自动安装。

## 许可证

本项目采用 MIT 许可证。详情请参阅 `LICENSE` 文件。

