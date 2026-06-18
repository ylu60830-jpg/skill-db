---
name: skills-inventory
description: Claude Code 已安装的全部 skills 清单，按类别整理
metadata: 
  node_type: memory
  type: reference
  originSessionId: 053caba2-aa47-4475-bca2-9e4a6db41433
---

熠枫的技能库，截至 2026-06-07 安装完毕。

## 基础框架（06-06）
- **superpowers** v5.1.0 — 官方市场，开发流程骨架
- **planning-with-files** v2.43.0 — 文件式任务规划
- **playwright-skill** v4.1.0 — 浏览器自动化测试
- **ui-ux-pro-max** v2.5.0 — 设计智能体
- **git-pr-workflows** v1.0.0 — Git/PR 自动化

## 06-07 新增

### Anthropic 官方创作套件
- **canvas-design** — 静态视觉设计（海报、PNG/PDF）
- **frontend-design** — 生产级前端界面
- **pdf** — PDF 读写合并拆分 OCR
- **pptx** — 幻灯片创建编辑
- **xlsx** — 电子表格处理
- **docx** — Word 文档（已有 LibreOffice 工具链）
- **web-artifacts-builder** — 复杂 HTML artifact（React/Tailwind/shadcn）
- **webapp-testing** — Playwright 本地 Web 应用测试
- **slack-gif-creator** — Slack 动图
- **theme-factory** — 10 套预设主题配色
- **brand-guidelines** — Anthropic 品牌色/字体
- **web-access-main** — 所有联网操作统一入口

### 开发流程
- **tdd** — 测试驱动开发（红-绿-重构）
- **diagnose** — 系统化调试循环
- **make-plan** — 分阶段实施计划
- **do** — 执行计划
- **review** — 双维度审查（规范+需求）
- **code-review** — diff 审查（bug + 简化）
- **simplify** — 代码简化重构
- **verify** — 手动验证改动
- **prototype** — 快速原型（CLI 或 UI 分支）
- **learn-codebase** — 通读整个代码库
- **smart-explore** — tree-sitter AST 结构化搜索
- **pathfinder** — 功能分组流程图 + 架构提案
- **improve-codebase-architecture** — 架构深度优化

### 写作与文档
- **doc-coauthoring** — 结构化协作文档
- **edit-article** — 文章编辑润色
- **writing-beats** — 节拍式叙事写作
- **writing-fragments** — 碎片挖掘收集
- **writing-shape** — 原始材料→成文塑造
- **internal-comms** — 内部沟通模板

### Claude Code 工具
- **skill-creator** — 创建/优化/测评 skill
- **mcp-builder** — 构建 MCP 服务器
- **claude-api** — Anthropic SDK 开发调试
- **init** — 初始化 CLAUDE.md
- **loop** — 定时循环任务
- **caveman** — 超压缩通信模式
- **keybindings-help** — 自定义快捷键
- **update-config** — 配置 settings.json
- **fewer-permission-prompts** — 减少权限弹窗

### Git 与协作
- **git-guardrails-claude-code** — Git 危险命令拦截钩子
- **setup-pre-commit** — Husky + lint-staged 预提交
- **version-bump** — 语义化版本发布
- **oh-my-issues** — Issue 聚类去重
- **triage** — Issue 状态机分流
- **request-refactor-plan** — 重构计划 + Issue
- **babysit** — 监控 PR 审查周期

### 二次元与创意
- **csp** — 二次元角色技能蒸馏器
- **clawd-animation** — Clawd 像素动画（完整版）
- **clawd-animation-lite** — Clawd 像素动画（轻量版）
- **ai-painter** — CSS 像素画绘制
- **algorithmic-art** — p5.js 算法艺术

### 知识管理
- **obsidian-vault** — Obsidian 笔记管理
- **mem-search** — 跨会话记忆搜索
- **knowledge-agent** — AI 知识库构建查询
- **timeline-report** — 项目开发历程叙事报告
- **weekly-digests** — 按周拆分叙事摘要
- **handoff** — 会话压缩交接文档
- **how-it-works** — claude-mem 工作原理

### 语言与数据库专项
- **Python:** async-python-patterns, python-anti-patterns, python-background-jobs, python-code-style, python-configuration, python-design-patterns, python-error-handling, python-observability, python-packaging, python-performance-optimization, python-project-structure, python-resilience, python-resource-management, python-testing-patterns, python-type-safety, uv-package-manager
- **JavaScript/TypeScript:** javascript-testing-patterns, modern-javascript-patterns, nodejs-backend-patterns, typescript-advanced-types
- **数据库:** postgresql
- **AI 哲学:** karpathy-guidelines

### 其他
- **design-an-interface** — 多方案 API 设计
- **design-is** — Dieter Rams 十原则设计审计
- **grill-me** — 计划/设计深度拷问
- **grill-with-docs** — 对照文档拷问
- **migrate-to-shoehorn** — 测试 as 断言迁移
- **openclaw** — OpenClaw 插件指南
- **qa** — 交互式 QA → GitHub Issue
- **scaffold-exercises** — 练习题目录结构生成
- **template** — 待定
- **to-issues** — 计划→Issue 拆分
- **to-prd** — 会话→PRD
- **deep-research** — 深度研究报告
- **wowerpoint** — kawaii NotebookLM 风格幻灯片
- **security-review** — 安全审查

**Why:** 用户今天（06-07）新装了大量 skills，覆盖面从开发流程到创意设计到语言专项
**How to apply:** 根据任务类型自动匹配对应 skill；优先使用专项 skill（如 pdf/pptx/xlsx/docx 处理对应文件）
