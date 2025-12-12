# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
VERSION=${1:-latest}
HOME=
cp $HOME/[...]/run_handler.py .
docker build --no-cache --build-arg VERSION=$VERSION -t ghcr.io/scc-digitalhub/digitalhub-sdk-wrapper-hera/wrapper-hera:test  -f $HOME/_HERA.dockerfile .
docker build --no-cache --build-arg VERSION=$VERSION -t ghcr.io/scc-digitalhub/digitalhub-sdk-wrapper-dbt/wrapper-dbt:test  -f $HOME/_DBT.dockerfile .
docker build --no-cache --build-arg VERSION=$VERSION -t ghcr.io/scc-digitalhub/digitalhub-sdk-wrapper-kfp/wrapper-kfp:test  -f $HOME/_KFP.dockerfile .
docker build --no-cache --build-arg VERSION=$VERSION -t ghcr.io/scc-digitalhub/digitalhub-serverless/python-runtime:3.9-test -f $HOME/_PY9.dockerfile .
docker build --no-cache --build-arg VERSION=$VERSION -t ghcr.io/scc-digitalhub/digitalhub-serverless/python-runtime:3.10-test -f $HOME/_PY10.dockerfile .
docker build --no-cache --build-arg VERSION=$VERSION -t ghcr.io/scc-digitalhub/digitalhub-serverless/python-runtime:3.11-test -f $HOME/_PY11.dockerfile .
rm run_handler.py
