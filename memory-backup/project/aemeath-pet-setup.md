---
name: aemeath-pet-setup
description: 爱弥斯桌宠已卸载（2026-06-07），此文件保留重建参考
metadata: 
  node_type: memory
  type: project
  status: uninstalled
  uninstalledDate: 2026-06-07
  originSessionId: 1d1121de-9266-4d21-9f19-80f4b5a47b27
---

爱弥斯桌宠已于 2026-06-07 卸载。

**已清理:**
- 进程: aemeath-claude.exe 已终止
- 程序目录: D:/aemeath_withclaude/ 已删除
- 全局 hooks: ~/.claude/settings.json 中所有 aemeath hooks 已移除
- 全局 MCP: ~/.claude/.mcp.json 中 aemeath 条目已移除
- 项目 hooks: .claude/settings.local.json 中 SessionStart 已移除

**重建参考（如需重新安装）:**
- 源码仓库: aemeath_withclaude
- 构建: cargo build --release (需 MinGW GCC 工具链)
- 端口: HTTP 9527, MCP 9528
