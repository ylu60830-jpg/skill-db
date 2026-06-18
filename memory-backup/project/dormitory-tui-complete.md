---
name: dormitory-tui-complete
description: 宿舍管理系统 TUI 前端已实现，终端交互式 CRUD 完成
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b25c8b5-19b9-457b-b0e8-4c7e2d4dfa5d
---

## 宿舍管理系统 - TUI 前端已完成

**时间:** 2026-06-17

**数据库:** MySQL 8.4.9, `dormitory_system`, 4 表 + 4 视图 + 触发器 + 测试数据

**TUI 前端:** `宿舍管理系统/dormitory_tui.py`
- Python + mysql-connector-python
- 菜单导航式，覆盖学生/宿舍/班级/辅导员 4 模块 + 数据概览
- 中文等宽表格对齐（CJK 显示宽度修正函数 `dwidth` / `dpad`）
- 添加记录时展示可选列表，选班级自动填辅导员，选宿舍展示空位
- 所有列表视图带 ID，直接用于修改/删除
- `run-tui.bat` 一键启动（chcp 65001）

**MySQL 已知问题:**
- 系统服务 MySQL80 指向不存在的 8.0 路径，实际安装是 8.4.9
- 需手动启动：`"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld" --defaults-file="C:\ProgramData\MySQL\MySQL Server 8.4\my.ini" --console`
- 或修复服务：`sc delete MySQL80` 然后重新创建指向 8.4 路径

**Why:** 学校作业——数据库设计阶段已完成，先做终端交互前端，后升级为 Web 前端

**Web 前端 (2026-06-17):** `宿舍管理系统/web/`
- Flask + Jinja2 + MySQL，纯文字严谨风格，无 emoji
- 仪表盘 + 4 模块 CRUD（学生/宿舍/班级/辅导员）
- 18 条路由，班级-辅导员联动，搜索过滤，触发器自动同步
- `run.bat` 一键启动 + 自动打开浏览器 http://127.0.0.1:5000
- Dreamweaver CS6 可直接打开模板编辑，VS Code 可调试
- Git 已保存（commit: 宿舍管理系统 Web 前端）

**How to apply:** 先启动 MySQL，双击 `web/run.bat` 自动打开浏览器
