.PHONY: run clean

run: .venv/bin/activate
	(source .venv/bin/activate && python3 tram.py)

.venv/bin/activate: requirements.txt
	make clean
	(python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)

clean:
	rm -rf .venv
