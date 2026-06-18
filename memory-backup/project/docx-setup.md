---
name: docx-doc-editing-setup
description: LibreOffice已安装，.doc和.docx均可读写。docx技能包可用。
metadata: 
  node_type: memory
  type: project
  originSessionId: a9485d05-5d25-4f6e-ae21-6ea6ee359561
---

本项目已安装 LibreOffice 26.2.3.2（通过 winget），可进行 .doc → .docx 转换。
- `antiword -m UTF-8` 可提取 .doc 中文文本
- LibreOffice soffice 路径：`/c/Program Files/LibreOffice/program/soffice.exe`
- docx 技能包：解包→编辑XML→打包 工作流可用
- 注意：终端/Read工具均无法正确渲染中文，中文验证须通过 Python 解码(GDK→UTF-8)写入文件后读取
- 注意：Python脚本中反斜杠路径需用 raw string `r"..."` 或正斜杠，避免转义问题
- 注意：内联Python heredoc中 `'\\'` 会导致语法错误，复杂脚本应写入文件执行

**Why:** 这是后续处理文档类任务的基础环境配置
**How to apply:** 处理文档任务时直接使用上述工具链，不需要重新安装
