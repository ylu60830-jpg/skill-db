# SkillDB

> Claude Code 的 Skill 索引中枢——扫描、分类、搜索、自动匹配，一站式管理你的 AI 技能库。

## 一句话

让 Claude 在每次任务前**自动检索**你有没有可用的专精 Skill，省去记忆 70+ 个触发词的负担。

## 核心组成

```
skill-db/
├── scan.py        # 扫描本地 ~/.claude/skills/ → 生成结构化索引
├── index.html     # 前端浏览器（分类树 + 实时搜索 + 卡片/列表视图）
└── run.bat        # 一键启动
```

## 快速开始

```bash
# 1. 生成索引（扫描你本机的 Claude Skills）
python skill-db/scan.py

# 2. 启动浏览器
# Windows: 双击 skill-db/run.bat
# 手动:   python -m http.server 8765 -d skill-db
#         浏览器访问 http://localhost:8765
```

## 工作流程

```
你发出任务
    ↓
Claude 提取意图 → 查询 skill-index.json
    ↓
┌─ 0 个匹配 → 直接手干
├─ 1 个匹配 → 自动调用对应 Skill
└─ 多个匹配 → 列出对比 + 推荐最佳
```

## 索引结构

三层分类树——大类 → 子类 → Skill，附带中英文关键词索引，人机共读。

首次运行 `scan.py` 自动分类，后续可在 `CLASSIFICATION` 字典中自定义。

## 许可

MIT
