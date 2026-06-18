---
name: pptx-editing-experience
description: PPTX修改工作流与踩坑经验——解包、编辑、案例加强、打包全流程
metadata: 
  node_type: memory
  type: project
  originSessionId: 6b41ae4b-b6a7-483b-b9b7-ab314e60f0fb
---

# PPTX 修改实战经验

**日期**：2026-06-07
**项目**：马克思PPT——垄断资本主义的形成与发展

## 工作流

```
解包 → 提取原文 → 对照教材 → 加案例加内容 → 批量编辑XML → 清理 → 打包 → QA
```

### 工具链
- **解包**：`python scripts/office/unpack.py input.pptx unpacked/`
- **提取文本**：`python -m markitdown input.pptx` 或 python-pptx 库
- **修改**：直接编辑 `ppt/slides/slideN.xml` 中的 `<a:t>` 标签
- **打包**：`python scripts/office/pack.py unpacked/ output.pptx --original input.pptx`

## 设计规范（本项目的PPT风格）

| 元素 | 颜色 | 用途 |
|------|------|------|
| `#FDF6F0` | 暖奶油色 | 内容页背景 |
| `#8B1A2B` | 深褐红 | 左侧装饰条、卡片色条 |
| `#C8963E` | 金色 | 顶部装饰线、分隔页大号字、分节标题 |
| `#5C0E1A` | 暗红 | 分隔页/总结页整体背景、深色卡片 |
| `#FFFFFF` | 白色 | 深色背景上的文字 |
| `#1A1A1A` | 近黑色 | 浅色卡片上的正文（对比度关键！） |

字体：标题 Arial Black，正文 Calibri，中文沿用系统映射。

## 内容方法论：概念+实例结合

纯概念枯燥，有实例才有记忆点。每个知识点配一个真实历史案例：

- 垄断形成 → 标准石油（洛克菲勒，1880年控制90%炼油）
- 金融寡头 → 摩根财团（多人出任财长/防长）
- 国家干预 → 罗斯福新政（TVA、社会保障法）
- 金融危机 → 2008雷曼兄弟破产
- 国际扩展 → 苹果供应链、沃尔玛全球采购

来源用教材原话 + 公开历史事实，不编造。

## 踩过的坑

### 1. 白字白底
小结页背景是暗红色 `#5C0E1A`，但卡片是半透明白色（alpha=90%），卡片内文字也是 `#FFFFFF`——结果白字在浅白卡片上完全不可读。修复：内容文字改 `#1A1A1A`，标题保持白色。

### 2. 跨行文本替换导致XML标签破损
有些文本在XML里被拆成多行 `<a:t>` 标签：
```xml
<a:t>垄断资本凭</a:t>
<a:t>借垄断地位</a:t>
```
用整句替换时容易破坏 `<` 或 `>`。必须用精准的 `<a:t>原文</a:t>` 匹配，不能用模糊替换。

### 3. pack.py 验证可能报错
内置验证脚本遇到某些XML会报 `argument is not iterable`，不是真的错误。可以跳过，手动用 zipfile 打包：
```python
# 以原始PPTX为基础，用修改过的文件覆盖
with zipfile.ZipFile(orig, 'r') as zin:
    with zipfile.ZipFile(output, 'w') as zout:
        for item in zin.infolist():
            data = unpacked_files.get(item.filename, zin.read(item.filename))
            zout.writestr(item, data)
```

### 4. 新增幻灯片时要配套更新
新增幻灯片不仅要加 `slideN.xml`，还要：
- `ppt/_rels/presentation.xml.rels` 加关系
- `[Content_Types].xml` 加条目
- `ppt/presentation.xml` 的 `<p:sldIdLst>` 加ID

用 `add_slide.py` 可自动处理这些。

### 5. 文本太长会撑破文本框
PPT模板的文本框有固定大小，追加案例时要控制字数。如果溢出，宁可缩案例不要删概念。

## 对后续的建议

- 改PPT前先解包看原始XML结构，搞清楚每个 `<p:sp>` 的名字和位置
- 用 `python-pptx` 做内容提取比 markitdown 更可控
- 批量修改用 Python 脚本 + 精准 `<a:t>` 替换，不要用正则全局搜
- 改完后用 `lxml.etree.fromstring` 逐文件验证XML合法性
- 视觉QA用 `soffice` 转PDF再转图片

[[skills-inventory]] [[generated-files-location]]
