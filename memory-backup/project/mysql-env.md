---
name: mysql-env
description: MySQL 8.4.9 环境——服务自启、连接方式、编码、查询要点
metadata: 
  node_type: memory
  type: reference
  originSessionId: 24b490bf-adca-48b5-b64d-b71a4c834b35
---

## MySQL 8.4.9

- 路径：`C:\Program Files\MySQL\MySQL Server 8.4\bin\`
- 数据目录：`C:/ProgramData/MySQL/MySQL Server 8.4/Data/`
- 配置文件：`C:/ProgramData/MySQL/MySQL Server 8.4/my.ini`
- root 无密码

## 启动方式

**服务启动（推荐）**：
```bash
net start MySQL80   # 需管理员，已设为 AUTO_START 开机自启
```
服务名：`MySQL80`，START_TYPE: AUTO_START（2026-06-08 配置）。

**手动后台进程**（备选，无需管理员）：
```bash
"C:/Program Files/MySQL/MySQL Server 8.4/bin/mysqld" --defaults-file="C:/ProgramData/MySQL/MySQL Server 8.4/my.ini" &
```

## 连接（关键：中文必须加 utf8mb4）
```bash
"C:/Program Files/MySQL/MySQL Server 8.4/bin/mysql" -u root --default-character-set=utf8mb4
```

不加 `--default-character-set=utf8mb4` 中文会乱码。

## 工具
- **MySQL Workbench 8.0 CE** 已安装，左边 Schemas 标签看数据库
- Workbench 版本显示的客户端是 8.0.46，服务器是 8.4.9，不影响使用
- `dormitory_system` 数据库已建好并验证

## 关联
[[dormitory-db-design]]
[[database-tools]]
