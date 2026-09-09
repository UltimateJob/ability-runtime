# Ability Runtime Seed

[English](README.md) | [简体中文](README.zh-CN.md)

📦 Build inputs and an offline dependency cache for Semantic Robot Bundles. Despite its name, this repository is **not a running service**, a complete Robot Bundle, or the Ability source repository.

## Contents

| Path | Use |
|---|---|
| `AbilityFramework` | Locally built Ability host |
| `ability_py-*.whl` | Locally built Python Ability SDK |
| `ability_scaffold-*.whl` | Locally built packaging tool |
| `base-bundles/` | Bundle seed configuration and third-party Wheels |
| `Makefile` | Presence checks and local scaffold environment setup |

## Prepare the inputs

Use quick-start stages **2.3, 5.1, and 5.2**. They fetch third-party assets, build AbilityFramework/ability-py/ability-scaffold from source, validate the outputs, and copy them into this repository.

For manual preparation, fetch only the remaining LFS assets:

```bash
git lfs pull -X "AbilityFramework,**/AbilityFramework,ability_py-*.whl,**/ability_py-*.whl,ability_scaffold-*.whl,**/ability_scaffold-*.whl"
```

Then copy the version-matched binary and Wheels from those three source builds. The SDK Wheel is needed both at the root and in the selected base bundle's `wheels/` directory. The public snapshot intentionally excludes these generated first-party files; do not run setup before building and copying them.

```bash
make check
make setup
```

Setup requires uv and Python **3.13** and creates `.venv/` with ability-scaffold. `make check` only checks file presence; quick-start additionally validates Wheel archives and runs AbilityFramework's version check.

## Use and troubleshoot

The Framework refresh workflow consumes these inputs to create an active Robot Bundle. The current cache includes Linux x86_64 / CPython 3.13 native Wheels; it is not a cross-platform dependency set.

An “invalid wheel” error often indicates an LFS pointer or a missing source-build copy. A missing shared library can indicate an ABI mismatch; retain the bundle's pinned dependencies instead of upgrading individual Wheels blindly.

Local `.venv/` and backup `*.lfs-orig` files are not release inputs. Cached Wheels retain their embedded licenses; see the [supplemental upstream notices](third-party-licenses/README.md).

[Detailed seed reference](README.reference.md) · [Input checks](Makefile)

## License

Copyright 2026 InsightOS. First-party code: [Apache-2.0](LICENSE). See [NOTICE](NOTICE) and [license scope](LICENSE_SCOPE.md) for third-party components and assets.
