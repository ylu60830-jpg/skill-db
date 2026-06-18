---
name: ai-painter-skill-development
description: ai-painter 像素绘画 skill 完整开发历程——从 CSS 像素画到 GitHub 开源技能
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b5df916-6661-4484-aa29-c9ba37ce3a18
---

## 2026-06-06：一天内从零到 GitHub 开源技能

### 时间线

| 顺序 | 产出 | 说明 |
|------|------|------|
| 1 | 📇 像素名片 | pixel-card/index.html — 打字机效果 + Pastel Pixel 风格 + hover 动画 |
| 2 | 🎨 6 角色像素画 | CSS box-shadow 技法：小鸡、猫、蚊子、苍蝇拍、炸弹、手柄 |
| 3 | 🏃 角色动画 | steps() 顿挫、缓动函数、多层叠加 |
| 4 | 🪰 苍蝇拍精修 | 三次迭代——造型方向、旋转轴心（容器包裹法）、挥拍节奏 |
| 5 | 🦀 Clawd 技能 | 发现 mmguo.dev/clawd → 安装 + 精读三份参考（引擎/叙事/情绪） |
| 6 | 🎨 ai-painter v1-v3 | 自建像素绘画技能：画板→双路检索→36色调色板→尺寸自选 |
| 7 | 📸 photo2pixel.py | 照片→像素转换脚本（NEAREST缩放+颜色量化+调色板映射） |
| 8 | 🔬 LLM 视觉认知局限 | 三次猫迭代证明：AI 没见过实物，凭空设计必然比例诡异 |
| 9 | 📚 百科全书策略 | references/encyclopedia-search.md —— 先读百科获取量化比例数据 |
| 10 | 🌐 GitHub 发布 | https://github.com/ylu60830-jpg/ai-painter — SSH+gh CLI 推送 |
| 11 | 🦟 蚊子飞行动画 | Canvas requestAnimationFrame：翅膀扇动+身体起伏+8字飞行 |
| 12 | 💕 Clawd 安慰动画 | clawd-animation-lite 生成：四阶段叙事 + 爱心粒子 + 俏皮台词 |

### GitHub 仓库

- 地址: https://github.com/ylu60830-jpg/ai-painter
- SSH Key: ~/.ssh/id_ed25519 (yifeng-github)
- gh CLI: /c/Program Files/GitHub CLI/gh.exe

### 核心技术发现

1. **CSS box-shadow 动画**: 4×4 基元素太小，transform-origin 百分比定位不准。必须用等比例容器包裹。
2. **照片→像素转换**: 不能替代 AI 设计，但提供真实比例约束——比例有照片兜底就不会画歪。
3. **LLM 没有视觉皮层**: AI 从没见过猫，文字描述"尖耳圆脸"无法转化为正确像素坐标。百科策略是当前最优解。
4. **小画布避正面**: 32×32 及以下避免正面面部——蜷缩/背影/侧面几何形状成功率远高于肖像。

### 相关记忆

- [[aemeath-pet-setup]] — 桌宠同一天升级
- [[skills-recommendations-for-next-session]] — 技能安装同一天完成
- 游戏大厅设计文档: docs/superpowers/specs/2026-06-06-game-hub-design.md

**Why:** 记录完整开发历程，下次继续时了解上下文和已知问题
**How to apply:** 读这个文件即可恢复上下文；ai-painter 继续迭代时从 v5 开始
