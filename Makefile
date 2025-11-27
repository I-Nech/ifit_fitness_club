dev:
	watchfiles --filter python --ignore-path .venv,__pycache__ "./.venv/Scripts/python.exe main.py"
active:
	source ./.venv/Scripts/activate