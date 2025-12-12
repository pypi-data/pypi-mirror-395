# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
SRC=
DST=
DIRECTORIES=(
    digitalhub-sdk/digitalhub
    digitalhub-sdk-runtime-container/digitalhub_runtime_container
    digitalhub-sdk-runtime-dbt/digitalhub_runtime_dbt
    digitalhub-sdk-runtime-kfp/digitalhub_runtime_kfp
    digitalhub-sdk-runtime-hera/digitalhub_runtime_hera
    digitalhub-sdk-runtime-python/digitalhub_runtime_python
    digitalhub-sdk-runtime-modelserve/digitalhub_runtime_modelserve
    digitalhub-sdk-runtime-flower/digitalhub_runtime_flower
)
for dir in "${DIRECTORIES[@]}"; do
    cp -r $SRC/$dir $DST
done
echo "Done"

