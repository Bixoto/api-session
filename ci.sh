#! /bin/bash -ex
[ ! -f pyproject.toml ] && exit 0

COV_ARGS=""

if [ -n "$HTMLCOV" ]; then
  COV_ARGS="$COV_ARGS --cov-report=html"
fi
if [ -n "$BRANCHCOV" ]; then
  COV_ARGS="$COV_ARGS --cov-branch"
fi

poetry run ruff check api_session
poetry run mypy --check-untyped-defs --explicit-package-bases ./*.py api_session/*.py
poetry run pytest --cov=. $COV_ARGS tests/
