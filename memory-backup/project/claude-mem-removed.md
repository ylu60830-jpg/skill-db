---
name: claude-mem-removed
description: claude-mem 已卸载——原因、时间、后果
metadata: 
  node_type: memory
  type: project
  originSessionId: fce8f10c-83ce-4166-9de9-a0240281ebbd
---

## claude-mem 已卸载

**时间:** 2026-06-18

**原因:** Stop hook 每次回复后卡顿 3 分钟（Crystallizing… running stop hook），严重影响使用体验。

**操作:**
- `claude-mem@thedotmack` 从 `C:\Users\ASUS\.claude\settings.json` 的 enabledPlugins 中移除
- 缓存目录已删除：`plugins/cache/thedotmack/claude-mem/`
- 市场文件已删除：`plugins/marketplaces/thedotmack/`

**后果:**
- 不再有跨会话自动记忆注入
- 不再有自动 observation 记录
- 所有记忆改为手动维护，通过 MEMORY.md + memory/*.md 文件管理
- 每次会话开始时，MEMORY.md 会被加载到上下文

**Why:** 用户原话——「这个Claude-mem一点用都没有干脆删除了」

**How to apply:** 重要信息必须手动写入 memory/ 目录下的 .md 文件，并在 MEMORY.md 中添加索引。每次会话结束时检查是否有需要记录的新信息。
