---
name: rust-mingw-env
description: Rust + MinGW 构建环境配置——USTC镜像、GCC MinGW路径
metadata: 
  node_type: memory
  type: project
  originSessionId: 809b763d-77a9-4721-ad2c-7c6f36eee7a2
---

本机 Rust 开发环境已配置完成，可用于构建 Windows 原生程序（Tauri 等）。

**Rust:**
- 版本: rustc 1.96.0, cargo 1.96.0
- 工具链: `stable-x86_64-pc-windows-gnu` (默认)
- 安装位置: `~/.cargo/bin/`
- 镜像源: USTC (`sparse+https://mirrors.ustc.edu.cn/crates.io-index/`)
- 配置文件: `~/.cargo/config.toml`

**MinGW-w64 (GCC):**
- 来源: WinLibs (Brecht Sanders), GCC 16.1.0
- 类型: POSIX threads, UCRT runtime, SEH 异常
- 路径: `/d/mingw64/bin/` (2026-06-06 重新安装到此)
- PATH 已持久化: `export PATH="/d/mingw64/bin:$PATH"` 写入 ~/.bashrc
- 关键 DLL: `libgcc_s_seh-1.dll` 提供 -lgcc_eh

**构建命令模板:**
```bash
export PATH="/d/mingw64/bin:$PATH"
cd /d/some-ascii-path  # 不能有中文!
cargo build --release
```

**Why:** 后续任何 Rust/Tauri 开发都依赖这套环境
**How to apply:** 构建前设置 PATH，项目路径必须纯 ASCII
