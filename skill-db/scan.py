#!/usr/bin/env python3
"""扫描 ~/.claude/skills/ 目录，生成 skill-index.json

用法: python scan.py [--watch]
  --watch  每30秒自动重新扫描（开发调试用）
"""

import os
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

SKILLS_DIR = Path.home() / ".claude" / "skills"
OUTPUT_FILE = Path(__file__).parent / "skill-index.json"

# ============================================================
# 分类映射表 —— 手工维护，scan 时自动合并
# skill_name → category / subcategory / type / function_zh / tags
# ============================================================

CLASSIFICATION = {
    # ── 文档处理 ──
    "pdf": {
        "category": "文档处理", "subcategory": "PDF",
        "type": "domain", "function_zh": "PDF读取/合并/拆分/旋转/水印/OCR/表单",
        "tags": ["pdf", "阅读", "合并", "拆分", "旋转", "水印", "表单", "OCR"]
    },
    "docx": {
        "category": "文档处理", "subcategory": "Word文档",
        "type": "domain", "function_zh": "Word文档创建/编辑/读取/格式转换/批注",
        "tags": ["word", "docx", "报告", "信函", "备忘录", "模板"]
    },
    "pptx": {
        "category": "文档处理", "subcategory": "PPT演示",
        "type": "domain", "function_zh": "PPT创建/编辑/读取/模板/演讲者备注",
        "tags": ["ppt", "pptx", "演示", "幻灯片", "deck", "presentation"]
    },
    "xlsx": {
        "category": "文档处理", "subcategory": "Excel表格",
        "type": "domain", "function_zh": "Excel创建/编辑/公式/图表/数据清洗",
        "tags": ["excel", "xlsx", "表格", "公式", "图表", "csv", "tsv"]
    },

    # ── 前端与设计 ──
    "frontend-design": {
        "category": "前端与设计", "subcategory": "界面设计",
        "type": "domain", "function_zh": "生产级前端界面，大胆美学风格",
        "tags": ["前端", "界面", "UI", "HTML", "CSS", "React", "landing", "dashboard"]
    },
    "web-artifacts-builder": {
        "category": "前端与设计", "subcategory": "界面设计",
        "type": "domain", "function_zh": "复杂多组件HTML工件(React/Tailwind/shadcn)",
        "tags": ["前端", "工件", "React", "Tailwind", "shadcn", "HTML"]
    },
    "impeccable": {
        "category": "前端与设计", "subcategory": "界面设计",
        "type": "domain", "function_zh": "前端界面全方位优化/UX审查/视觉层次/动效",
        "tags": ["UI", "UX", "审查", "优化", "无障碍", "动效", "设计系统"]
    },
    "canvas-design": {
        "category": "前端与设计", "subcategory": "视觉设计",
        "type": "domain", "function_zh": "静态视觉设计(.png/.pdf海报/艺术)",
        "tags": ["海报", "设计", "视觉", "png", "pdf", "艺术"]
    },
    "brand-guidelines": {
        "category": "前端与设计", "subcategory": "视觉设计",
        "type": "domain", "function_zh": "Anthropic品牌颜色/字体应用到任意产出物",
        "tags": ["品牌", "颜色", "字体", "Anthropic", "视觉规范"]
    },
    "theme-factory": {
        "category": "前端与设计", "subcategory": "视觉设计",
        "type": "domain", "function_zh": "10套预设主题+自定义主题，应用到产出物",
        "tags": ["主题", "配色", "字体", "风格", "幻灯片", "文档"]
    },
    "design-an-interface": {
        "category": "前端与设计", "subcategory": "接口设计",
        "type": "domain", "function_zh": "并行生成多个截然不同的接口设计方案对比",
        "tags": ["API", "接口", "方案对比", "模块设计"]
    },
    "design-is": {
        "category": "前端与设计", "subcategory": "设计审查",
        "type": "domain", "function_zh": "Dieter Rams十条设计原则审查+改进方案",
        "tags": ["设计审查", "Rams", "UI审查", "设计原则"]
    },

    # ── 创意与视觉 ──
    "ai-painter": {
        "category": "创意与视觉", "subcategory": "像素画",
        "type": "domain", "function_zh": "像素画逐格绘制，支持参考图搜索+画布绘制",
        "tags": ["像素画", "画", "draw", "pixel", "sprite", "像素"]
    },
    "algorithmic-art": {
        "category": "创意与视觉", "subcategory": "算法艺术",
        "type": "domain", "function_zh": "p5.js算法生成艺术(流场/粒子系统/种子随机)",
        "tags": ["生成艺术", "p5.js", "算法", "粒子", "流场", "creative coding"]
    },
    "clawd-animation": {
        "category": "创意与视觉", "subcategory": "Clawd动画",
        "type": "domain", "function_zh": "Clawd像素动画生成器(完整版)，复杂多场景",
        "tags": ["clawd", "动画", "像素", "螃蟹", "HTML动画"]
    },
    "clawd-animation-lite": {
        "category": "创意与视觉", "subcategory": "Clawd动画",
        "type": "domain", "function_zh": "Clawd像素动画生成器(轻量版)，1-3秒简短",
        "tags": ["clawd", "动画", "像素", "螃蟹", "简短"]
    },
    "slack-gif-creator": {
        "category": "创意与视觉", "subcategory": "GIF制作",
        "type": "domain", "function_zh": "Slack优化动画GIF制作(约束+验证)",
        "tags": ["gif", "slack", "动画", "动图"]
    },

    # ── 角色与写作 ──
    "light-novel-writing": {
        "category": "角色与写作", "subcategory": "轻小说创作",
        "type": "domain", "function_zh": "日系轻小说创作：角色设定/世界观/剧情/对话/互动",
        "tags": ["轻小说", "小说", "角色扮演", "异世界", "校园", "奇幻", "对话"]
    },
    "csp": {
        "category": "角色与写作", "subcategory": "角色蒸馏",
        "type": "domain", "function_zh": "二次元角色技能蒸馏器：资料检索→行为蒸馏→生成Skill",
        "tags": ["角色", "skill生成", "蒸馏", "二次元", "动漫", "人格"]
    },
    "edit-article": {
        "category": "角色与写作", "subcategory": "文章写作",
        "type": "domain", "function_zh": "文章编辑/结构重组/文笔改进",
        "tags": ["编辑", "文章", "改进", "结构", "文笔"]
    },
    "writing-beats": {
        "category": "角色与写作", "subcategory": "文章写作",
        "type": "domain", "function_zh": "选择你自己的冒险式文章节拍写作",
        "tags": ["写作", "节拍", "叙事", "选择", "文章"]
    },
    "writing-fragments": {
        "category": "角色与写作", "subcategory": "文章写作",
        "type": "domain", "function_zh": "碎片化写作素材挖掘+收集",
        "tags": ["写作", "素材", "碎片", "想法", "挖掘"]
    },
    "writing-shape": {
        "category": "角色与写作", "subcategory": "文章写作",
        "type": "domain", "function_zh": "原始材料→出版物级文章的对话式塑造",
        "tags": ["写作", "塑造", "编辑", "材料", "文章"]
    },

    # ── 代码开发 ──
    "tdd": {
        "category": "代码开发", "subcategory": "测试",
        "type": "process", "function_zh": "测试驱动开发：红-绿-重构循环",
        "tags": ["tdd", "测试", "红绿重构", "单元测试", "集成测试"]
    },
    "diagnose": {
        "category": "代码开发", "subcategory": "调试",
        "type": "process", "function_zh": "系统化调试：复现→最小化→假设→插桩→修复",
        "tags": ["调试", "debug", "bug", "性能", "回归"]
    },
    "review": {
        "category": "代码开发", "subcategory": "代码审查",
        "type": "process", "function_zh": "双轴代码审查：规范符合度+需求匹配度",
        "tags": ["审查", "review", "代码", "规范", "PR"]
    },
    "improve-codebase-architecture": {
        "category": "代码开发", "subcategory": "架构",
        "type": "domain", "function_zh": "代码库架构深化改进：耦合/可测试性/AI导航性",
        "tags": ["架构", "重构", "耦合", "可测试性", "设计"]
    },
    "smart-explore": {
        "category": "代码开发", "subcategory": "代码搜索",
        "type": "domain", "function_zh": "基于tree-sitter AST的结构化代码搜索",
        "tags": ["搜索", "AST", "tree-sitter", "代码结构", "函数"]
    },
    "learn-codebase": {
        "category": "代码开发", "subcategory": "代码库学习",
        "type": "process", "function_zh": "通读所有源文件为代码库建立全局认知",
        "tags": ["学习", "代码库", "通读", "入门", "熟悉"]
    },
    "pathfinder": {
        "category": "代码开发", "subcategory": "架构",
        "type": "domain", "function_zh": "代码库功能映射→流程图→重复关注点→统一架构",
        "tags": ["架构", "映射", "流程图", "重构", "统一"]
    },
    "prototype": {
        "category": "代码开发", "subcategory": "原型",
        "type": "domain", "function_zh": "快速构建抛弃式原型(终端应用/UI多方案切换)",
        "tags": ["原型", "mockup", "UI", "终端", "快速"]
    },

    # ── 工作流(流程型Skill) ──
    "brainstorming": {
        "category": "工作流", "subcategory": "启动前",
        "type": "process", "function_zh": "创意/功能前必用：理清用户意图+需求+设计",
        "tags": ["头脑风暴", "创意", "需求", "设计", "规划"]
    },
    "make-plan": {
        "category": "工作流", "subcategory": "规划",
        "type": "process", "function_zh": "创建详细分阶段实施计划+文档发现",
        "tags": ["计划", "规划", "实施", "阶段", "文档"]
    },
    "do": {
        "category": "工作流", "subcategory": "执行",
        "type": "process", "function_zh": "使用子代理执行分阶段实施计划",
        "tags": ["执行", "实施", "子代理", "计划"]
    },
    "writing-plans": {
        "category": "工作流", "subcategory": "规划",
        "type": "process", "function_zh": "多步骤任务的文件规划（含review检查点）",
        "tags": ["计划", "文件", "规划", "检查点", "review"]
    },
    "planning-with-files": {
        "category": "工作流", "subcategory": "规划",
        "type": "process", "function_zh": "Manus风格文件规划：task_plan/findings/progress.md",
        "tags": ["计划", "Manus", "文件", "规划", "进度"]
    },
    "executing-plans": {
        "category": "工作流", "subcategory": "执行",
        "type": "process", "function_zh": "在独立session中执行实施计划+review检查点",
        "tags": ["执行", "计划", "session", "分离", "检查点"]
    },
    "finishing-a-development-branch": {
        "category": "工作流", "subcategory": "收尾",
        "type": "process", "function_zh": "开发完成后的合并/PR/清理结构化决策",
        "tags": ["收尾", "合并", "PR", "分支", "清理"]
    },
    "verification-before-completion": {
        "category": "工作流", "subcategory": "收尾",
        "type": "process", "function_zh": "声称完成前强制运行验证命令+确认输出",
        "tags": ["验证", "完成", "确认", "证据", "测试"]
    },
    "requesting-code-review": {
        "category": "工作流", "subcategory": "审查",
        "type": "process", "function_zh": "任务完成/大功能/合并前请求代码审查",
        "tags": ["审查", "review", "代码", "合并", "验证"]
    },
    "receiving-code-review": {
        "category": "工作流", "subcategory": "审查",
        "type": "process", "function_zh": "接收审查反馈后：技术严谨性验证+不盲从",
        "tags": ["审查", "反馈", "验证", "严谨"]
    },
    "subagent-driven-development": {
        "category": "工作流", "subcategory": "执行",
        "type": "process", "function_zh": "当前session内用独立任务执行实施计划",
        "tags": ["子代理", "执行", "计划", "并行"]
    },
    "using-git-worktrees": {
        "category": "工作流", "subcategory": "Git",
        "type": "process", "function_zh": "创建隔离git worktree开始功能开发",
        "tags": ["git", "worktree", "隔离", "分支"]
    },
    "using-superpowers": {
        "category": "工作流", "subcategory": "启动前",
        "type": "process", "function_zh": "会话启动：建立skill查找和使用规则",
        "tags": ["启动", "skill", "规则", "会话"]
    },
    "caveman": {
        "category": "工作流", "subcategory": "通信",
        "type": "process", "function_zh": "超压缩通信模式，token减少~75%",
        "tags": ["压缩", "token", "简洁", "caveman"]
    },
    "handoff": {
        "category": "工作流", "subcategory": "通信",
        "type": "process", "function_zh": "当前对话压缩成交接文档给另一个代理",
        "tags": ["交接", "handoff", "压缩", "代理"]
    },
    "zoom-out": {
        "category": "工作流", "subcategory": "通信",
        "type": "process", "function_zh": "获取更广上下文视角/高层次概览",
        "tags": ["概览", "上下文", "视角", "高层次"]
    },
    "version-bump": {
        "category": "工作流", "subcategory": "发布",
        "type": "domain", "function_zh": "语义化版本发布：package.json/npm/git tag/GitHub Release",
        "tags": ["版本", "发布", "npm", "git tag", "changelog"]
    },
    "setup-pre-commit": {
        "category": "工作流", "subcategory": "Git",
        "type": "domain", "function_zh": "Husky pre-commit hooks配置(lint-staged+类型检查+测试)",
        "tags": ["git", "hooks", "pre-commit", "husky", "lint"]
    },
    "setup-matt-pocock-skills": {
        "category": "工作流", "subcategory": "配置",
        "type": "domain", "function_zh": "Matt Pocock工程skills配置(AGENTS.md+triage标签)",
        "tags": ["配置", "TypeScript", "工程", "skills", "triage"]
    },
    "template": {
        "category": "工作流", "subcategory": "配置",
        "type": "domain", "function_zh": "空模板skill（未配置，可替换）",
        "tags": ["模板", "空", "替换", "示例"]
    },

    # ── Git与项目管理 ──
    "git-guardrails-claude-code": {
        "category": "Git与项目管理", "subcategory": "Git安全",
        "type": "domain", "function_zh": "阻止危险git命令(push/reset --hard/clean/branch -D)",
        "tags": ["git", "安全", "防护", "hooks", "push", "reset"]
    },
    "git-workflow": {
        "category": "Git与项目管理", "subcategory": "Git工作流",
        "type": "process", "function_zh": "Git工作流编排：代码审查→PR创建+质量门",
        "tags": ["git", "PR", "审查", "工作流", "质量"]
    },
    "babysit": {
        "category": "Git与项目管理", "subcategory": "PR管理",
        "type": "process", "function_zh": "监控PR/审查周期直到可合并",
        "tags": ["PR", "审查", "监控", "合并", "CI"]
    },
    "oh-my-issues": {
        "category": "Git与项目管理", "subcategory": "Issue管理",
        "type": "domain", "function_zh": "GitHub Issue聚类/去重/根因分析→plan-master",
        "tags": ["issue", "聚类", "去重", "根因", "GitHub"]
    },
    "to-issues": {
        "category": "Git与项目管理", "subcategory": "Issue管理",
        "type": "domain", "function_zh": "计划/规格→独立可抓取Issue(追踪子弹垂直切片)",
        "tags": ["issue", "拆分", "计划", "ticket", "实现"]
    },
    "to-prd": {
        "category": "Git与项目管理", "subcategory": "文档",
        "type": "domain", "function_zh": "当前上下文→PRD并发布到Issue Tracker",
        "tags": ["PRD", "需求", "文档", "issue"]
    },
    "triage": {
        "category": "Git与项目管理", "subcategory": "Issue管理",
        "type": "process", "function_zh": "Issue分类状态机：按角色路由+优先级",
        "tags": ["issue", "分类", "路由", "优先级", "状态机"]
    },
    "request-refactor-plan": {
        "category": "Git与项目管理", "subcategory": "重构",
        "type": "domain", "function_zh": "通过用户访谈创建详细重构计划→GitHub Issue",
        "tags": ["重构", "计划", "issue", "访谈", "增量"]
    },
    "review": {
        "category": "Git与项目管理", "subcategory": "代码审查",
        "type": "process", "function_zh": "双轴审查：规范符合度+需求匹配度",
        "tags": ["审查", "review", "规范", "需求", "PR"]
    },

    # ── 文档与内部沟通 ──
    "doc-coauthoring": {
        "category": "文档与沟通", "subcategory": "技术文档",
        "type": "process", "function_zh": "结构化文档协作工作流：上下文传递+迭代+验证",
        "tags": ["文档", "协作", "技术文档", "提案", "规范"]
    },
    "internal-comms": {
        "category": "文档与沟通", "subcategory": "内部沟通",
        "type": "domain", "function_zh": "内部沟通文档：状态报告/领导更新/3P/FAQ/事件报告",
        "tags": ["沟通", "内部", "报告", "状态", "更新", "事件"]
    },
    "timeline-report": {
        "category": "文档与沟通", "subcategory": "项目报告",
        "type": "domain", "function_zh": "从claude-mem时间线生成项目开发历程叙事报告",
        "tags": ["时间线", "报告", "项目", "历史", "叙事"]
    },
    "weekly-digests": {
        "category": "文档与沟通", "subcategory": "项目报告",
        "type": "domain", "function_zh": "按ISO周生成项目每周叙事摘要章节",
        "tags": ["周报", "摘要", "叙事", "章节", "时间线"]
    },
    "wowerpoint": {
        "category": "文档与沟通", "subcategory": "演示",
        "type": "domain", "function_zh": "文档→kawaii NotebookLM风格幻灯片PDF",
        "tags": ["幻灯片", "pdf", "notebooklm", "kawaii", "演示"]
    },

    # ── AI与知识管理 ──
    "skill-creator": {
        "category": "AI与知识管理", "subcategory": "Skill管理",
        "type": "domain", "function_zh": "创建/修改/评估Skill，含性能基准测试",
        "tags": ["skill", "创建", "修改", "评估", "性能"]
    },
    "write-a-skill": {
        "category": "AI与知识管理", "subcategory": "Skill管理",
        "type": "domain", "function_zh": "创建新Agent Skill：结构/渐进披露/资源打包",
        "tags": ["skill", "创建", "结构", "资源", "打包"]
    },
    "writing-skills": {
        "category": "AI与知识管理", "subcategory": "Skill管理",
        "type": "process", "function_zh": "创建/编辑/验证/部署Skill",
        "tags": ["skill", "创建", "编辑", "验证", "部署"]
    },
    "knowledge-agent": {
        "category": "AI与知识管理", "subcategory": "知识库",
        "type": "domain", "function_zh": "从claude-mem观察构建/查询AI知识库",
        "tags": ["知识库", "claude-mem", "查询", "观察"]
    },
    "mem-search": {
        "category": "AI与知识管理", "subcategory": "知识库",
        "type": "domain", "function_zh": "搜索claude-mem跨会话持久记忆数据库",
        "tags": ["记忆", "搜索", "claude-mem", "跨会话"]
    },
    "how-it-works": {
        "category": "AI与知识管理", "subcategory": "工具原理",
        "type": "domain", "function_zh": "解释claude-mem工作原理(捕获/注入/数据位置)",
        "tags": ["claude-mem", "原理", "文档", "解释"]
    },
    "obsidian-vault": {
        "category": "AI与知识管理", "subcategory": "知识库",
        "type": "domain", "function_zh": "Obsidian笔记库搜索/创建/管理(wikilinks+索引)",
        "tags": ["obsidian", "笔记", "wikilinks", "索引"]
    },
    "ubiquitous-language": {
        "category": "AI与知识管理", "subcategory": "知识库",
        "type": "domain", "function_zh": "DDD通用语言术语表提取+歧义标记+建议",
        "tags": ["DDD", "术语", "语言", "词汇表", "歧义"]
    },

    # ── 后端与API ──
    "mcp-builder": {
        "category": "后端与API", "subcategory": "MCP",
        "type": "domain", "function_zh": "MCP服务器构建(Python FastMCP / Node MCP SDK)",
        "tags": ["MCP", "服务器", "API", "工具", "集成"]
    },
    "claude-api": {
        "category": "后端与API", "subcategory": "Claude API",
        "type": "domain", "function_zh": "Claude API/SDK应用：缓存/thinking/tool use/迁移",
        "tags": ["claude", "API", "SDK", "缓存", "anthropic"]
    },
    "openclaw": {
        "category": "后端与API", "subcategory": "插件",
        "type": "domain", "function_zh": "Claude-Mem OpenClaw插件安装配置",
        "tags": ["openclaw", "claude-mem", "插件", "网关"]
    },

    # ── 测试与质量 ──
    "webapp-testing": {
        "category": "测试与质量", "subcategory": "Web测试",
        "type": "domain", "function_zh": "Playwright本地Web应用测试/截图/浏览器日志",
        "tags": ["测试", "playwright", "浏览器", "截图", "E2E"]
    },
    "qa": {
        "category": "测试与质量", "subcategory": "QA",
        "type": "process", "function_zh": "交互式QA会话：对话式报Bug→自动提交Issue",
        "tags": ["QA", "bug", "issue", "对话", "测试"]
    },
    "scaffold-exercises": {
        "category": "测试与质量", "subcategory": "练习",
        "type": "domain", "function_zh": "创建练习目录结构(章节/问题/解答/说明)+lint通过",
        "tags": ["练习", "习题", "教学", "目录", "结构"]
    },

    # ── 网络与访问 ──
    "web-access-main": {
        "category": "网络与访问", "subcategory": "联网",
        "type": "domain", "function_zh": "所有联网操作总入口：搜索/抓取/登录/浏览器",
        "tags": ["联网", "搜索", "网页", "抓取", "浏览器", "登录"]
    },

    # ── 特殊/教学 ──
    "teach": {
        "category": "其他", "subcategory": "教学",
        "type": "domain", "function_zh": "在此工作区内教授新技能或概念",
        "tags": ["教学", "学习", "技能", "概念"]
    },
    "migrate-to-shoehorn": {
        "category": "其他", "subcategory": "迁移",
        "type": "domain", "function_zh": "测试文件as断言→@total-typescript/shoehorn迁移",
        "tags": ["typescript", "测试", "断言", "迁移", "shoehorn"]
    },
    "grill-me": {
        "category": "其他", "subcategory": "评审",
        "type": "process", "function_zh": "对计划/设计进行无休止的追问直到达成共识",
        "tags": ["追问", "评审", "计划", "设计", "压力测试"]
    },
    "grill-with-docs": {
        "category": "其他", "subcategory": "评审",
        "type": "process", "function_zh": "用领域模型追问计划+更新CONTEXT.md/ADR",
        "tags": ["追问", "文档", "领域模型", "ADR", "术语"]
    },
}

# ============================================================
# 预定义协同组（多skill协同推荐）
# ============================================================
SYNERGY_GROUPS = {
    "全栈Web应用": {
        "skills": ["frontend-design", "web-artifacts-builder", "mcp-builder", "tdd", "webapp-testing"],
        "description": "前端界面 + 后端API + 测试全覆盖"
    },
    "技术文档产出": {
        "skills": ["doc-coauthoring", "docx", "pdf", "pptx"],
        "description": "文档协作 → 多种格式输出"
    },
    "设计到交付": {
        "skills": ["frontend-design", "impeccable", "design-is", "canvas-design"],
        "description": "设计 → 审查 → 优化 → 静态产出"
    },
    "代码审查完整流程": {
        "skills": ["review", "requesting-code-review", "receiving-code-review"],
        "description": "审查 → 请求审查 → 接收反馈处理"
    },
    "规划到执行": {
        "skills": ["brainstorming", "make-plan", "do", "verification-before-completion"],
        "description": "创意 → 计划 → 执行 → 验证"
    },
    "角色创作完整流": {
        "skills": ["csp", "light-novel-writing"],
        "description": "角色蒸馏 → 轻小说创作/对话"
    },
    "项目管理全流程": {
        "skills": ["to-prd", "to-issues", "triage", "oh-my-issues", "babysit"],
        "description": "PRD → Issue拆分 → 分类 → 聚类 → 监控"
    },
    "Skill开发发布": {
        "skills": ["skill-creator", "write-a-skill", "writing-skills", "version-bump"],
        "description": "创建 → 验证 → 评估 → 发布"
    },
    "知识管理": {
        "skills": ["obsidian-vault", "mem-search", "knowledge-agent", "ubiquitous-language"],
        "description": "笔记 + 记忆搜索 + 知识库 + 术语表"
    },
}

# ============================================================
# 特殊的嵌套skill目录（父目录无SKILL.md，子目录各自有）
# ============================================================
NESTED_SKILL_DIRS = {
    "cybersecurity": {
        "category": "网络安全", "type": "domain",
        "function_prefix": "网络安全 - ",
        "tags_prefix": ["安全", "网络安全"]
    },
    "data-engineering": {
        "category": "数据工程", "type": "domain",
        "function_prefix": "数据工程 - ",
        "tags_prefix": ["数据工程", "大数据"]
    },
    "domain-expert": {
        "category": "领域专家", "type": "domain",
        "function_prefix": "领域专家 - ",
        "tags_prefix": ["领域专家", "技术栈"]
    },
}


def parse_frontmatter(filepath: Path) -> dict | None:
    """解析 SKILL.md 的 YAML frontmatter，返回 {name, description, ...}"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    # 检查是否以 --- 开头
    if not text.startswith("---"):
        return None

    # 找到第二个 ---
    end_idx = text.find("---", 3)
    if end_idx == -1:
        return None

    yaml_str = text[3:end_idx].strip()
    if not yaml_str:
        return None

    try:
        import yaml
        meta = yaml.safe_load(yaml_str)
        if isinstance(meta, dict):
            return meta
    except Exception:
        pass

    return None


def scan_skills() -> list[dict]:
    """扫描所有 skill，返回原始 skill 列表"""
    skills = []
    seen_names = set()

    # 第一轮：扫描顶层 SKILL.md
    for item in sorted(SKILLS_DIR.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if item.name in NESTED_SKILL_DIRS:
            continue  # 交给第二轮处理

        skill_md = item / "SKILL.md"
        if skill_md.exists():
            meta = parse_frontmatter(skill_md)
            if meta:
                name = meta.get("name", item.name)
                if name not in seen_names:
                    seen_names.add(name)
                    skills.append({
                        "name": name,
                        "path": str(skill_md),
                        "dir_name": item.name,
                        "description": meta.get("description", ""),
                        "file_count": count_files(item),
                        "has_references": has_subdirs(item),
                    })
        elif item.name == "subagents":
            # subagents 特殊处理：列出所有 .md 文件
            for agent_file in sorted(item.glob("*.md")):
                agent_name = agent_file.stem.replace("-expert", "")
                skills.append({
                    "name": f"agent:{agent_name}",
                    "path": str(agent_file),
                    "dir_name": f"subagents/{agent_file.name}",
                    "description": f"技术子代理：{agent_name}",
                    "file_count": 1,
                    "has_references": False,
                })

    # 第二轮：扫描嵌套 skill 目录
    for parent_dir, config in NESTED_SKILL_DIRS.items():
        parent_path = SKILLS_DIR / parent_dir
        if not parent_path.exists():
            continue
        for item in sorted(parent_path.iterdir()):
            if not item.is_dir():
                continue
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                meta = parse_frontmatter(skill_md)
                if meta:
                    name = meta.get("name", item.name)
                    if name not in seen_names:
                        seen_names.add(name)
                        skills.append({
                            "name": name,
                            "path": str(skill_md),
                            "dir_name": f"{parent_dir}/{item.name}",
                            "description": meta.get("description", ""),
                            "file_count": count_files(item),
                            "has_references": has_subdirs(item),
                        })

    return skills


def count_files(dirpath: Path) -> int:
    """统计目录下所有文件数"""
    count = 0
    for f in dirpath.rglob("*"):
        if f.is_file():
            count += 1
    return count


def has_subdirs(dirpath: Path) -> bool:
    """是否有子目录（references/examples等）"""
    for item in dirpath.iterdir():
        if item.is_dir():
            return True
    return False


def clean_description(desc) -> str:
    """清理 description 字符串"""
    if isinstance(desc, str):
        # 移除换行和多余空格
        desc = " ".join(desc.split())
        # 截断过长的描述（保留前200字符作为摘要）
        if len(desc) > 200:
            desc = desc[:197] + "..."
    return desc or ""


def classify_skill(skill: dict) -> dict:
    """为 skill 匹配分类信息"""
    name = skill["name"]
    dir_name = skill.get("dir_name", name)

    # 子代理分类
    if name.startswith("agent:"):
        return {
            "category": "技术子代理",
            "subcategory": "Agent定义",
            "type": "domain",
            "function_zh": f"技术专家子代理：{name.replace('agent:', '')}",
            "tags": ["子代理", "agent", "专家"],
        }

    # 嵌套 skill 自动分类（根据父目录）
    for parent, config in NESTED_SKILL_DIRS.items():
        if dir_name.startswith(parent + "/"):
            sub_name = dir_name.split("/", 1)[1]
            prefix = config.get("function_prefix", "")
            return {
                "category": config["category"],
                "subcategory": sub_name,
                "type": config.get("type", "domain"),
                "function_zh": f"{prefix}{name}",
                "tags": list(config.get("tags_prefix", [])),
            }

    # 查分类表：先按 dir_name，再按 name
    for key in (dir_name, name):
        if key in CLASSIFICATION:
            c = CLASSIFICATION[key]
            return {
                "category": c["category"],
                "subcategory": c["subcategory"],
                "type": c.get("type", "domain"),
                "function_zh": c.get("function_zh", ""),
                "tags": c.get("tags", []),
            }

    # 未分类
    return {
        "category": "未分类",
        "subcategory": "待整理",
        "type": "domain",
        "function_zh": "",
        "tags": [],
    }


def build_index(skills: list[dict]) -> dict:
    """按三层树结构构建完整索引"""
    # 先给每个 skill 补上分类
    classified = []
    for s in skills:
        c = classify_skill(s)
        desc = clean_description(s.get("description", ""))
        classified.append({
            "name": s["name"],
            "path": s["path"],
            "dir_name": s.get("dir_name", s["name"]),
            "type": c["type"],
            "category": c["category"],
            "subcategory": c["subcategory"],
            "function_zh": c["function_zh"],
            "function_en": desc[:120] if desc else "",
            "tags": c["tags"],
            "file_count": s.get("file_count", 0),
            "has_references": s.get("has_references", False),
            "description_short": desc[:100] if desc else "",
        })

    # 构建分类树
    cat_map: dict[str, dict] = {}  # category → {subcategory → [skills]}
    for s in classified:
        cat = s["category"]
        sub = s["subcategory"]
        if cat not in cat_map:
            cat_map[cat] = {}
        if sub not in cat_map[cat]:
            cat_map[cat][sub] = []
        cat_map[cat][sub].append(s)

    # 构建关键词索引
    keyword_index: dict[str, list[str]] = {}
    for s in classified:
        for tag in s["tags"]:
            tag_lower = tag.lower()
            if tag_lower not in keyword_index:
                keyword_index[tag_lower] = []
            if s["name"] not in keyword_index[tag_lower]:
                keyword_index[tag_lower].append(s["name"])
        # 也索引中文功能描述中的关键词
        func = s.get("function_zh", "")
        for word in extract_keywords(func):
            if word not in keyword_index:
                keyword_index[word] = []
            if s["name"] not in keyword_index[word]:
                keyword_index[word].append(s["name"])

    # 构建分类树输出格式
    categories = []
    for cat_name in sorted(cat_map.keys()):
        subcats = []
        for sub_name in sorted(cat_map[cat_name].keys()):
            skills_in_sub = sorted(cat_map[cat_name][sub_name], key=lambda x: x["name"])
            subcats.append({
                "name": sub_name,
                "skills": skills_in_sub,
            })
        categories.append({
            "name": cat_name,
            "subcategories": subcats,
        })

    # 统计
    total = len(classified)
    domain_count = sum(1 for s in classified if s["type"] == "domain")
    process_count = sum(1 for s in classified if s["type"] == "process")
    unclassified_count = sum(1 for s in classified if s["category"] == "未分类")

    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "skills_dir": str(SKILLS_DIR),
            "total_skills": total,
            "domain_skills": domain_count,
            "process_skills": process_count,
            "unclassified": unclassified_count,
            "categories_count": len(categories),
        },
        "categories": categories,
        "keyword_index": keyword_index,
        "synergy_groups": SYNERGY_GROUPS,
        # 扁平列表（方便搜索）
        "flat_list": sorted(classified, key=lambda x: (x["category"], x["subcategory"], x["name"])),
    }


def extract_keywords(text: str) -> list[str]:
    """从中文文本提取关键词（简单分词）"""
    # 按常见分隔符切分
    import re
    words = re.split(r'[/、，,.\s]+', text)
    return [w.strip() for w in words if len(w.strip()) >= 2 and w.strip()]


def main():
    print("[1/3] Scanning skills directory...")
    skills = scan_skills()
    print(f"      Found {len(skills)} skills")

    print("[2/3] Building index...")
    index = build_index(skills)

    print(f"[3/3] Writing {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    m = index["meta"]
    print(f"""
Done!
   Total: {m['total_skills']} (domain: {m['domain_skills']}, process: {m['process_skills']})
   Unclassified: {m['unclassified']}
   Categories: {m['categories_count']}
""")


if __name__ == "__main__":
    if "--watch" in sys.argv:
        print("🔄 Watch 模式，每30秒自动刷新...")
        while True:
            main()
            time.sleep(30)
    else:
        main()
