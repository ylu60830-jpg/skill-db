---
name: dormitory-db-design
description: 宿舍信息管理系统——基于CDM改造为4表方案，全部验证通过
metadata:
  node_type: memory
  type: project
  originSessionId: 54afefe7-7696-416b-b8dd-65abff1bdcb2
---

## 完成状态

✅ 第一版 8 表方案完成（2026-06-07）
✅ 基于 CDM 改造为 4 表方案，全部验证通过（2026-06-08）
✅ MySQL ↔ DDL ↔ CDM 三方比对一致，含测试数据（2026-06-15）
✅ 目录已清理，移除旧 doc 生成脚本残留

## 当前状态（2026-06-15）

数据库部署完整，无需修改：
- 4 表：counselor(3条) / class(5条) / dormitory(8条) / student(9条)
- 4 视图：v_student_full / v_dorm_occupancy / v_class_stats / v_counselor_workload
- 4 触发器：3个宿舍入住自动更新 + 1个班级辅导员同步
- Word 文档和查询速查表仍为旧版 8 表方案，待更新

## CDM 改造版（当前版本，2026-06-08）

用户使用 PowerDesigner 16.5 绘制了新的概念数据模型 `dormitory management.cdm`，包含 5 个实体 + 5 个关系：

| 实体 | 物理表 | 说明 |
|------|--------|------|
| 学号 | → student.PK | 1:1 合并入学生表 |
| 学生 | student | 含 3 个 FK |
| 宿舍号 | dormitory | 床位号内置为 bed_count |
| 班级 | class | FK→counselor |
| 辅导员 | counselor | 独立表 |

| CDM关系 | 基数 | 物理实现 |
|----------|------|----------|
| R5 学号→学生 | 1:1 | student_id PK |
| R4 班级→学生 | 1:N | student.class_id NOT NULL |
| R2 辅导员→学生 | 1:N | student.counselor_id NOT NULL |
| R3 辅导员→班级 | 1:N | class.counselor_id NOT NULL |
| R1 宿舍→学生 | 1:N (学生0,1) | student.dorm_id NULL |

4 视图: v_student_full, v_dorm_occupancy, v_class_stats, v_counselor_workload
4 触发器: trg_student_dorm_insert/update/delete, trg_class_counselor_sync

传递依赖处理: student.counselor_id 与 class.counselor_id 冗余，通过 trg_class_counselor_sync 自动同步。

## 产出文件

> 2026-06-09 整理：所有数据库相关文件已归入 `宿舍管理系统/` 子目录

| 产出 | 路径 |
|------|------|
| CDM 概念模型 | `D:\新建1 CLAUDE\宿舍管理系统\dormitory management.cdm` |
| CDB 物理模型 | `D:\新建1 CLAUDE\宿舍管理系统\dormitory management.cdb` |
| DDL 脚本（最新） | `D:\新建1 CLAUDE\宿舍管理系统\dormitory_ddl.sql` |
| Word 文档（旧版8表） | `D:\新建1 CLAUDE\宿舍管理系统\宿舍信息管理系统_数据库设计.docx` |
| 查询速查表（旧版） | `D:\新建1 CLAUDE\宿舍管理系统\查询速查表.md` |
| MySQL 启动 | `D:\新建1 CLAUDE\宿舍管理系统\start-mysql.bat` |
| 开机自启 | `D:\新建1 CLAUDE\宿舍管理系统\mysql-auto.bat` |
| 文档生成脚本 | `D:\新建1 CLAUDE\宿舍管理系统\generate-doc.js` |
| PowerDesigner 工作区 | `D:\新建1 CLAUDE\宿舍管理系统\Workspace.sws` |

> 注意：Word 文档和查询速查表仍是旧版 8 表方案，未更新到 CDM 4 表版。

## MySQL 连接

```bash
"C:/Program Files/MySQL/MySQL Server 8.4/bin/mysql" -u root --default-character-set=utf8mb4
```

数据库: `dormitory_system`

## 关联
[[mysql-env]]
[[database-tools]]
