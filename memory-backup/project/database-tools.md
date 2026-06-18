---
name: database-tools
description: PowerDesigner + DTASHELL + Dreamweaver——数据库相关工具的位置和用途
metadata: 
  node_type: memory
  type: reference
  originSessionId: 24b490bf-adca-48b5-b64d-b71a4c834b35
---

三个已安装的数据库相关工具（2026-06-08 确认）：

| 快捷方式名 | 应用名 | 路径 | 用途 |
|-----------|--------|------|------|
| pdlegacyshell16 | PowerDesigner 16.5 | `D:\powerdesigner\pdlegacyshell16.exe` | 数据库建模、ER图、反向工程 |
| DTASHELL | 数据库引擎优化顾问 19 | `D:\SQL\Common7\DTASHELL.EXE` | SQL Server 查询性能优化 |
| Dreamweaver | Adobe Dreamweaver CS6 | `D:\Dreamweaver_CS6\Adobe Dreamweaver CS6\Dreamweaver.exe` | 网页编辑器（老旧） |

**PowerDesigner 最实用**：可以反向工程 dormitory_system → 自动生成 ER 图。
- DBMS 选 MySQL 5.0（兼容 8.4）
- 菜单 File → Reverse Engineer → Database
- ⚠️ 许可证过期修复（2026-06-15）：替换 `D:\PowerDesigner\pdflm16.dll`，原版备份为 `pdflm16.dll.bak`。破解 dll 来源：百度网盘 https://pan.baidu.com/s/1jIIgeZO 密码 24xv。安装时需选 Trial + Hong Kong 地区。

**DTASHELL** 是 SQL Server 自带的数据库引擎优化顾问，对 MySQL 无用（只支持 SQL Server）。

## 关联
[[mysql-env]]
[[dormitory-db-design]]
