---
name: 74ls181-experiment-report
description: 计算机组成原理运算器实验报告——74LS181功能表、实验数据计算、docx填充经验
metadata: 
  node_type: memory
  type: project
  originSessionId: a9485d05-5d25-4f6e-ae21-6ea6ee359561
---

本项目曾完成一份《计算机组成原理》运算器实验报告的自动填充（学生张三，西安财经学院信息学院）。

**实验仪器:** 计算机组成原理与系统结构试验箱

**74LS181关键知识点:**
- 正逻辑功能表：M=0算术运算16种（Cn=1无进位/Cn=0有进位），M=1逻辑运算16种
- 级联方式：低位Cn+4接高位Cn，用短路套实现进位链
- 减法：S=0110，Cn=0时F=A-B（内部做A+~B+1）。CY=1表示无借位，CY=0表示有借位

**docx填表经验:**
- LibreOffice转换的docx表格使用合并单元格，每个数据列一个cell含16个段落
- lxml解析OOXML比FODT替换更可靠，标签必须严格平衡
- 叙事内容插入用 `xml.sax.saxutils.escape()` 转义XML特殊字符
- `xml.find()` 只找第一个匹配，重复标题需特殊处理

**学号数据:** 05H和11H（本组成员学号后两位）
