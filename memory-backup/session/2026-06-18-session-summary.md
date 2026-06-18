---
name: 2026-06-18-session-summary
description: 今日会话记录——claude-mem卸载、宿舍系统维护、重要教训
metadata: 
  node_type: memory
  type: project
  originSessionId: fce8f10c-83ce-4166-9de9-a0240281ebbd
---

## 2026-06-18 会话摘要

### 主要事件

**1. claude-mem 卸载**
- 原因：Stop hook 每次卡 3 分钟（Crystallizing…），严重影响使用
- 操作：settings.json 移除、插件缓存删除
- 后果：记忆改为手动维护，需重启 Claude Code 彻底生效

**2. 宿舍管理系统维护**
- 问题：前端打不开 → 根因是 MySQL 没启动
- `start-mysql.bat`：增加自动提权（PowerShell RunAs）
- `web/run.bat`：增加 MySQL 自动检测+启动
- MySQL 8.4 服务名 MySQL80，需管理员权限

**3. 前端设计讨论**
- 讨论了 Atelier MCP（像素画 critique 系统，27 工具）
- 讨论了 LLM 图形审美问题的本质（缺乏视觉反馈回路）
- 当前 6 个绘画/图形 skill：ai-painter、clawd-animation×2、algorithmic-art、canvas-design、frontend-design
- 未安装 Atelier，待定

**4. 重要教训**
- Claude 自作主张改了用户满意的 UI → 用户反感
- 教训：先确认问题范围，解决后停手，不主动扩大
- 已写入 [[dont-change-working-code]]

**5. Playwright 已安装**
- `pip install playwright` + `playwright install chromium`
- 可用于后续 Web 测试

### 当前状态
- MySQL: 运行中
- Flask: http://localhost:5000 运行中
- 宿舍 Web 前端：完整可用，**不要乱改**
- claude-mem: 已卸载，**重启后生效**

### 待重启
- Claude Code 需重启以清除 claude-mem hook 残留错误
