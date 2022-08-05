export FLASK_APP=index.py

run: db
	flask run --host=0.0.0.0

db:
	rm -f db/database.db
	sqlite3 db/database.db < db/database.sql

.PHONY: db
