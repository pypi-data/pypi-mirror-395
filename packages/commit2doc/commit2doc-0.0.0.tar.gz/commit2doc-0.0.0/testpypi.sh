curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r testpypi.txt
uv pip freeze > testpypi.lock
python3 -m build
python3 -m twine upload --repository testpypi dist/*
deactivate
rm -rf .venv
rm -rf dist
