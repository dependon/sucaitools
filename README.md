# SucaiTools 素材处理工具集

[English](#english) | [中文](#chinese)

## bilibili 
[使用方法地址](https://www.bilibili.com/video/BV1ojJGzZEve)

<a name="english"></a>
## English

### Introduction
SucaiTools is a comprehensive suite of tools designed to streamline various media processing tasks. It includes functionalities for video processing, image resizing, and image renaming, all within a user-friendly interface.

### Features

#### Video to PNG Conversion
- **Batch Conversion**: Convert multiple video files to PNG image sequences simultaneously.
- **Customizable Frame Rate**: Specify the desired frame rate for the extracted images.
- **Output Directory Selection**: Choose the directory where the extracted images will be saved.

#### Image Resizing
- **Scale Mode**: Resize images proportionally by specifying a scaling factor.
- **Fixed Resolution Mode**: Resize images to a specific width and height.
- **Batch Processing**: Apply resizing operations to multiple images within a directory.
- **Preview**: See the result before processing.

#### Image Renaming
- **Recursive Renaming**: Rename images within a directory and its subdirectories.
- **Customizable Naming Scheme**: Rename images based on the folder name and a sequential counter.
- **Batch Processing**: Apply renaming operations to multiple images within a directory.

#### General Features
- **Drag and Drop Support**: Easily add files and folders by dragging and dropping them into the application.
- **Multilingual Support**: Supports multiple languages, including English and Chinese.
- **User-Friendly Interface**: Intuitive and easy-to-use interface for all tasks.

### Installation

#### Method 1: Download Executable Files
Download the latest version of the executable file from the [GitHub Releases](https://github.com/dependon/sucaitools/releases) page:

- Windows: `sucaitools_windows_x64.exe`
- Linux: `sucaitools_linux_x64`
- macOS: `sucaitools_macos_x64`

#### Method 2: Install from Source
1. Ensure you have Python 3.6+ installed
2. Clone this repository or download the source code
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
1. Run the application:
   ```
   python main_app.py
   ```
2. Use the interface to:
   - Select the desired tool from the tab view.
   - Load files or folders using the drag and drop functionality or the browse button.
   - Configure the processing options for the selected tool.
   - Start the processing task.

### Dependencies
- customtkinter: For the GUI interface
- tkinterdnd2: For drag and drop functionality
- Pillow: For image processing
- opencv-python: For video processing
- 其他依赖项请参考 `requirements.txt` 文件

<a name="chinese"></a>
## 中文

### 简介
SucaiTools 是一套全面的工具，旨在简化各种媒体处理任务。它包括视频处理、图像大小调整和图像重命名等功能，所有这些都在一个用户友好的界面中。

### 功能特点

#### 视频转 PNG
- **批量转换**: 同时将多个视频文件转换为 PNG 图像序列。
- **可自定义的帧率**: 指定提取图像所需的帧率。
- **输出目录选择**: 选择保存提取图像的目录。

#### 图像大小调整
- **缩放模式**: 通过指定缩放因子按比例调整图像大小。
- **固定分辨率模式**: 将图像大小调整为特定的宽度和高度。
- **批量处理**: 将大小调整操作应用于目录中的多个图像。
- **预览**: 在处理之前查看结果。

#### 图像重命名
- **递归重命名**: 重命名目录及其子目录中的图像。
- **可自定义的命名方案**: 根据文件夹名称和顺序计数器重命名图像。
- **批量处理**: 将重命名操作应用于目录中的多个图像。

#### 通用功能
- **拖放支持**: 通过将文件和文件夹拖放到应用程序中来轻松添加它们。
- **多语言支持**: 支持多种语言，包括英语和中文。
- **用户友好的界面**: 适用于所有任务的直观且易于使用的界面。

### 安装方法

#### 方法1：直接下载可执行文件
从 [GitHub Releases](https://github.com/dependon/sucaitools/releases) 页面下载最新版本的可执行文件：

- Windows: `sucaitools_windows_x64.exe`
- Linux: `sucaitools_linux_x64`
- macOS: `sucaitools_macos_x64`

#### 方法2：从源码安装
1. 确保已安装 Python 3.6 或更高版本
2. 克隆此仓库或下载源代码
3. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

### 使用方法
1. 运行应用程序：
   ```
   python main_app.py
   ```
2. 使用界面来：
   - 从选项卡视图中选择所需的工具。
   - 使用拖放功能或浏览按钮加载文件或文件夹。
   - 配置所选工具的处理选项。
   - 启动处理任务。

### 依赖项
- customtkinter：用于图形用户界面
- tkinterdnd2：用于拖放功能
- Pillow：用于图像处理
- opencv-python：用于视频处理
- 其他依赖项请参考 `requirements.txt` 文件

## License
MIT License - See [LICENSE](LICENSE) file for details.

## Links
[GitHub Repository](https://github.com/dependon/sucaitools)

## 开发者信息

### 自动构建与发布

本项目使用GitHub Actions自动构建和发布可执行文件。每当推送到主分支或创建新的Release时，GitHub Actions会自动执行以下操作：

1. 在多个平台（Windows、Linux、macOS）上构建应用程序
2. 运行测试确保代码质量
3. 使用PyInstaller打包成独立的可执行文件
4. 将构建好的可执行文件上传到GitHub Releases

### 手动触发构建

开发者可以通过GitHub Actions界面手动触发构建流程：

1. 进入项目的GitHub页面
2. 点击"Actions"选项卡
3. 选择"Build and Release SucaiTools"工作流
4. 点击"Run workflow"按钮
