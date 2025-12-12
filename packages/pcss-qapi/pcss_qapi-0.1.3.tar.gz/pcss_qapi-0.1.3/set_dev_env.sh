#!/bin/bash

echo "[============Preparing developer setup==============]"
{
    uv venv
    uv sync
} || {
    echo "[================uv is not installed================]" &&
    python3 -m pip install uv &&
    python3 -m uv venv
    uv sync
}
source .venv/bin/activate

echo "[==============Installing requirements==============]"
#uv pip install -r requirements.txt
#uv pip install -r requirements-dev.txt
#uv pip install -r requirements-ql.txt
{
    echo "[===========Adding pre-commit as git hook===========]" &&
    pre-commit install &&

    echo "[===================Running Tests===================]" &&
    pytest tests &&

    echo "[===================Running Linter===================]" &&
    pylint pcss_qapi
} || {
    echo "[]==============!!Something went wrong!!==============]"
}