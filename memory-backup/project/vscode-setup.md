---
name: vscode-setup
description: VS Code 已安装配置——D盘便携版，含 Python 扩展和中文界面
metadata: 
  node_type: memory
  type: reference
  originSessionId: fe3e6e46-47b4-4384-9c75-09250bca29d1
---

## VS Code 安装配置

**安装日期:** 2026-06-17
**位置:** `D:\VSCode\`（便携版，不在 C 盘）
**版本:** 1.125.0（最新稳定版）

## 已安装扩展
- **ms-python.python** — Python 支持 + Pylance + Debugpy
- **MS-CEINTL.vscode-language-pack-zh-hans** — 中文界面

## 配置
- 中文界面已启用（locale: zh-cn）
- 用户数据目录: `D:\VSCode\data\`（扩展 + 设置，重装系统不丢失）
- PATH: `/d/VSCode/bin` 已加入 bashrc，终端输 `code` 即可启动
- 快捷批处理: `D:\VSCode\vscode.bat`

## 宿舍管理系统项目配置
- `.vscode/settings.json` — Python 解释器路径、UTF-8 编码、文件排除
- `.vscode/launch.json` — Flask 调试启动 + TUI 调试启动

## 启动方式
```bash
code "D:/新建1 CLAUDE/宿舍管理系统"   # 打开项目
code .                                 # 当前目录
```

**Why:** Claude 可通过命令行操作 VS Code（与操作文件/终端相同），免费且是当前行业标准编辑器
**How to apply:** 终端输 `code` 或双击 `D:\VSCode\vscode.bat`

## 关联
[[dormitory-tui-complete]]
