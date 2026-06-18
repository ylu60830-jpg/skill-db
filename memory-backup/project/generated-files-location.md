---
name: generated-files-location
description: "All generated files (images, HTML, animations, etc.) must be saved under the project directory, not loose in D drive root"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 053caba2-aa47-4475-bca2-9e4a6db41433
---

所有生成的输出文件（像素画 HTML、动画、图片、截图、文档等）必须保存在项目目录 `D:\新建1 CLAUDE` 下，按类型分到对应子目录，不要散落在 D 盘根目录。

**Why:** 用户注意到之前有文件直接扔在 D 盘，影响整洁。项目目录就是为此准备的。

**How to apply:** 每次 Write 生成文件时，路径统一用 `D:\新建1 CLAUDE/<子目录>/<文件名>`。子目录按类型分：pixel-card/（像素画）、photos/（图片）、clawd-ref/（clawd 动画参考）、docs/（文档）等。
