export FLASK_APP=index.py

run: db
	flask run --host=0.0.0.0

db:
	rm -f db/database.db
	sqlite3 db/database.db < db/database.sql

install:
	sudo apt install python-virtualenv 2>/dev/null ; python3 -m venv INM5151-virtualenv ; source INM5151-virtualenv/bin/activate
	sudo pip install -r requirements.txt

.PHONY: db