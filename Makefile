PYTHON ?= python

.PHONY: install init-db run test api mcp

install:
	$(PYTHON) -m pip install -r requirements.txt

init-db:
	PYTHONPATH=src $(PYTHON) scripts/init_db.py

run:
	PYTHONPATH=src $(PYTHON) scripts/run_daily.py

test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

api:
	PYTHONPATH=src $(PYTHON) scripts/run_api.py

mcp:
	PYTHONPATH=src $(PYTHON) scripts/run_mcp.py
