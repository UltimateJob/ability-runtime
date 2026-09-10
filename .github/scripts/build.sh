#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
mkdir -p .output/payload
git lfs fsck
python3 ../automation/.github/scripts/data.py
