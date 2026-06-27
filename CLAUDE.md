# 新建1 CLAUDE

## 项目简介
TODO: 一句话说明这个项目是干什么的

## 技术栈
TODO: 例如 Node.js / Python / Java / React 等

## 目录结构
```
/
├── skill-db/        # Skill 索引数据库（浏览器 + 扫描器）
│   ├── scan.py      #   扫描 ~/.claude/skills → 生成 skill-index.json
│   ├── skill-index.json  #  自动生成的结构化索引（人机共读）
│   ├── index.html   #   Skill 浏览器前端
│   └── run.bat      #   一键启动浏览器
├── src/            # 源代码
├── tests/          # 测试
├── docs/           # 文档
└── scripts/        # 脚本
```

## 常用命令
<!-- 按需填写 -->
```bash
# 启动开发服务器
# npm run dev

# 运行测试
# npm test

# 构建
# npm run build
```

## 注意事项
<!-- 项目特定的约定、禁忌、注意事项 -->
- TODO

## 编码规范
<!-- 如果有特定规范，在此说明 -->
- TODO

---

## 🧠 工作模式（系统规则）

### 场景判断

| 场景 | 行为 |
|------|------|
| 🗣️ 闲聊 / 讨论 / 情感交流 | 自然回应，不启动流程 |
| 📋 多步骤任务（写代码、做作业、安装配置、生成文档等） | **先规划再动手** |

### 任务执行流程

```
收到任务
  ↓
① brainstorming    → 理清目标，确认优先级
  ↓
② 🔍 Skill 自动匹配 → 查 skill-db/skill-index.json（见下方协议）
  ↓
③ planning-with-files → 建 task_plan.md，拆分步骤
  ↓
④ 逐项执行         → 每步加载对应 skill，完成打勾
```

### 第②步：Skill 自动匹配协议

**不靠记忆，靠索引。** 75+ skill 太多，每次任务前走以下流程：

#### 1. 加载索引

读 `skill-db/skill-index.json`。若 `meta.generated_at` 距今超过 **24 小时**，先跑 `python skill-db/scan.py` 刷新。

#### 2. 提取意图 → 匹配

从任务描述提取关键词（中英文）→ 查 `keyword_index`：
- **直接命中** → 拿到候选 skill 列表
- **无命中** → 按大类匹配（文档处理？前端？代码？）

#### 3. 结果处理

| 匹配数 | 行为 |
|--------|------|
| **0** | 无专精 skill，直接手干 |
| **1** | 自动 `Skill("xxx")` 调用，不询问 |
| **多个** | 列出对比表 + 推荐，等用户确认 |

#### 4. 多 Skill 对比格式

```
🔍 「任务描述」匹配到 N 个相关技能：

skill-a          ★★★★★  擅长什么，为什么匹配
skill-b          ★★★☆   擅长什么，差在哪
skill-c          ★☆☆☆   擅长什么，方向不同

推荐：skill-a — 原因。
```

#### 5. 多 Skill 协同

任务需要多个 skill 配合时 → 列出清单 + 建议执行顺序：

```
🔍 「从零设计用户系统」建议协同：

  📦 database-architect   数据库设计
  📄 docx                 输出文档
  🧪 tdd                  验证接口

  顺序：database-architect → docx，tdd 可并行
```

#### 6. 流程型 Skill 自动套用

`type: "process"` 的 skill 是方法论，不询问直接套用：
- 创造性任务 → `brainstorming`
- 调试 → `diagnose` 或 `systematic-debugging`
- 写代码 → `tdd`
- 声称完成前 → `verification-before-completion`

#### 7. 必须避开的陷阱

- ❌ 任务描述匹配了某个 skill 名称但实际不相关（如「画流程图」不应匹配 `ai-painter`）
- ❌ 因为「记得有某个 skill」就跳过索引直接调用——索引是唯一权威
- ✅ 索引无匹配 ≠ 不能做。直接用通用能力手干

### Skill 索引维护

- 手动刷新：说「更新 skill 索引」我跑 `python skill-db/scan.py`
- 前端浏览：`skill-db/run.bat` 双击启动，访问 http://localhost:8765
- 分类修正：编辑 `skill-db/scan.py` 中的 `CLASSIFICATION` 字典后重跑

### 关键规则

- **第②步不能跳过**：规划前强制查 skill-index.json，避免徒手硬干
- **闲聊不启动流程**：日常对话保持轻量，以上流程仅在需要产出交付物时触发
- **用工具而非被工具用**：skill 是参考书，按需查阅，不被流程绑架
