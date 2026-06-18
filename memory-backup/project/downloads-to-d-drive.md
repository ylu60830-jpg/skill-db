---
name: downloads-to-d-drive
description: 熠枫要求所有下载默认存D盘，C盘空间宝贵
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f7fec7fb-ef70-4847-a90c-2c5b0d552f79
---

熠枫明确要求：所有下载、包管理器缓存、全局安装默认使用 D 盘，避免占用 C 盘空间。

**已配置（2026-06-06）：**
- `npm config set prefix "D:/npm-global"` — 全局包装到 D 盘
- `npm config set cache "D:/npm-cache"` — npm 缓存到 D 盘
- `pip config set global.cache-dir "D:/pip-cache"` — pip 缓存到 D 盘
- PATH 已添加 `D:/npm-global`（2026-06-08 修正：原 `.bashrc` 错写为 `/bin` 子目录，已修复）

**Why:** 用户明确要求，C 盘空间重要
**How to apply:** 以后装任何包/工具默认往 D 盘放；下载临时文件优先放 `D:/temp/` 或项目目录
