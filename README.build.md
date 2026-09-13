# ability-runtime: reproducible platform builds

## Versions, tools and build layout

The glibc installer pins component tag **v0.4.0-insightos.2026.2** at `f3dad56a28f177421fd56cca8d593e1f29fc0b49`.
This guide pins the current build-script snapshot at `e99797ebc7ad1b28b1bb7b13ffef7399b6909881`.
To reconstruct another published release, read its `release.json` and select
both `source_commit` and `build_recipe_commit`; a source tag alone may predate
the CI scripts. This recipe reproduces the build steps, not historical archive bytes.

Prerequisites: Python 3 and Git LFS; the input is a versioned binary-wheel inventory, not a native compiler project.

The release scripts expect **two sibling checkouts**, `automation/` for build
scripts and `source/` for the component. Run these commands from a fresh working
directory (the scripts themselves are not standalone copies):

```bash
REPRO_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ability-runtime-repro.XXXXXXXX")"
git clone --no-checkout https://github.com/insightos-community/ability-runtime.git "$REPRO_ROOT/automation"
GIT_LFS_SKIP_SMUDGE=1 git -C "$REPRO_ROOT/automation" checkout --detach e99797ebc7ad1b28b1bb7b13ffef7399b6909881
git clone --no-checkout https://github.com/insightos-community/ability-runtime.git "$REPRO_ROOT/source"
GIT_LFS_SKIP_SMUDGE=1 git -C "$REPRO_ROOT/source" checkout --detach v0.4.0-insightos.2026.2
cd "$REPRO_ROOT/source"
test "$(git rev-parse HEAD)" = f3dad56a28f177421fd56cca8d593e1f29fc0b49
export TARGET_TAG=v0.4.0-insightos.2026.2
export COMPONENT=ability-runtime
export GITHUB_SHA=e99797ebc7ad1b28b1bb7b13ffef7399b6909881
```

```bash
git lfs install --local
git lfs pull
git lfs fsck
```

## Linux glibc / standard component Release

The executable build entry is [`.github/scripts/build.sh`](.github/scripts/build.sh);
archive validation is [`.github/scripts/package.py`](.github/scripts/package.py).
From `source/` in the layout above:

```bash
bash ../automation/.github/scripts/build.sh
python3 ../automation/.github/scripts/package.py 
(cd .output/release && sha256sum -c SHA256SUMS)
```

Artifacts: `source/.output/release/` (archives/wheels, `release.json`, checksum
inventory and license notices). `release.json` records source and recipe revisions.
The local commands do not publish or overwrite a GitHub Release.

The existing release inventories Linux Python wheels, including native Linux
ABI artifacts. Do not label the entire archive as platform-independent simply
because its packaging script is Python.

## Linux musl

The Linux wheelhouse/runtime pack must be replaced, not copied into musl.
The complete musl assembly is maintained in quick-start; it pins the Python 3.13
Runtime adaptation in `artifacts/musl/upstream.json` and compiles the application
wheels against the verified musl dependency releases. It does not run this
repository’s Python 3.10 Linux release command unchanged.

For the complete musl build and offline checks, use the [quick-start musl commands](https://github.com/insightos-community/quick-start/blob/main/README.build.md#linux-musl-x86_64).

## macOS / macosx

Do not install the native Linux wheel inventory on macOS. quick-start’s
`artifacts/macos/installer-requirements.lock` selects CPython 3.13 macOS arm64
wheels and `artifacts/macos/relocate_wheels.py` repairs and records Mach-O paths.
The macOS assembler intentionally does not consume this Linux ability-runtime
archive. Use that assembler to reproduce the macOS dependency runtime.

The complete macOS installer targets Apple Silicon/macOS 15.5+; see the [locked assembly instructions](https://github.com/insightos-community/quick-start/blob/main/README.build.md#macos-apple-silicon).

## GitHub workflow reproduction

The repository’s [CI workflow](.github/workflows/ci.yml) implements the two-checkout
layout. To build a source tag without publishing, create a reproduction branch at the
pinned automation commit. GitHub dispatch expects a branch/tag ref; both tag refs
and default-branch dispatches can enter this workflow’s publishing job. The following
commands require repository write access and use a non-default branch:

```bash
gh auth setup-git
REPRO_BRANCH=reproduce/platform-builds
git -C "$REPRO_ROOT/automation" push origin e99797ebc7ad1b28b1bb7b13ffef7399b6909881:refs/heads/$REPRO_BRANCH
gh workflow run ci.yml --repo insightos-community/ability-runtime --ref "$REPRO_BRANCH" -f tag=v0.4.0-insightos.2026.2
gh run list --repo insightos-community/ability-runtime --workflow ci.yml --limit 5
# Set REPRO_RUN_ID to the selected run ID.
gh run watch "$REPRO_RUN_ID" --repo insightos-community/ability-runtime --exit-status
gh run download "$REPRO_RUN_ID" --repo insightos-community/ability-runtime --name release-assets --dir downloaded-release
```

## Reproduction evidence

Build in a fresh checkout and a separate output directory for each ABI. Preserve
source commits, compiler/tool versions, dependency locks, package inventories and
test logs. Fixed source revisions and a container digest reproduce the recipe;
unlocked OS packages, runner images, timestamps and build tools can still change
archive bytes. Compare a downloaded release against its published `SHA256SUMS`;
do not expect a local rebuild to have the same digest.

See the [complete installer and repository index](https://github.com/insightos-community/quick-start/blob/main/README.build.md) for assembly order,
platform locks and end-to-end validation. Local build commands do not publish a
Release. Publishing requires repository write access and a new version tag;
existing release tags/assets should not be replaced.
