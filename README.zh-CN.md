# Ability Runtime Seed

[English](README.md) | [简体中文](README.zh-CN.md)

📦 Semantic Robot Bundle 的构建输入与离线依赖缓存。虽然名称含 Runtime，本仓库**不是运行中的服务**、完整 Robot Bundle，也不是 Ability 源码仓库。

## 内容

| 路径 | 用途 |
|---|---|
| `AbilityFramework` | 本地源码编译的 Ability 宿主 |
| `ability_py-*.whl` | 本地构建的 Python Ability SDK |
| `ability_scaffold-*.whl` | 本地构建的打包工具 |
| `base-bundles/` | Bundle 种子配置与第三方 Wheel |
| `Makefile` | 文件存在检查与 scaffold 本地环境初始化 |

## 准备输入

使用 quick-start 的 **2.3、5.1、5.2** 步骤：下载第三方资产，从源码构建 AbilityFramework / ability-py / ability-scaffold，校验后复制到本仓库。

手动准备时，仅拉取剩余 LFS 资产：

```bash
git lfs pull -X "AbilityFramework,**/AbilityFramework,ability_py-*.whl,**/ability_py-*.whl,ability_scaffold-*.whl,**/ability_scaffold-*.whl"
```

随后从上述三个源码构建中复制匹配版本的二进制与 Wheel。SDK Wheel 既需要放在根目录，也需要放入选定 base bundle 的 `wheels/`。公开快照不包含这三类自产文件，完成构建和复制前不要执行 setup。

```bash
make check
make setup
```

setup 需要 uv 与 Python **3.13**，会生成包含 ability-scaffold 的 `.venv/`。`make check` 只检查文件存在；quick-start 还会验证 Wheel 压缩包并执行 AbilityFramework 版本检查。

## 使用与常见问题

Framework 刷新工作流使用这些输入生成激活的 Robot Bundle。当前缓存包含 Linux x86_64 / CPython 3.13 原生 Wheel，不是一套跨平台依赖集合。

“invalid wheel”常见原因是 LFS 指针或遗漏源码产物复制。共享库缺失可能是 ABI 不匹配，应保留 Bundle 锁定的依赖，不要盲目升级单个 Wheel。

本地 `.venv/` 和备份 `*.lfs-orig` 不属于发布输入。第三方 Wheel 保留内嵌许可，并提供[补充上游许可声明](third-party-licenses/README.md)。

[详细种子参考](README.reference.md) · [输入检查](Makefile)

## 许可证

Copyright 2026 InsightOS。自有代码采用 [Apache-2.0](LICENSE)；第三方组件与资产请查看 [NOTICE](NOTICE) 和[许可范围](LICENSE_SCOPE.md)。

## 三个平台的构建复现

参见 [glibc、musl 与 macOS 构建说明](README.build.md)：包含已锁定的源码版本、实际脚本入口、工具要求、本地与 CI 指令、产物位置和平台验证范围。
