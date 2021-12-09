DIR = app/
DIR_SQL = $(DIR)sql/
AUTH = -U alumnodb -h 127.0.0.1
PSSWRD = PGPASSWORD=alumnodb
DB_NAME = si1
DB = $(PSSWRD) psql $(AUTH) $(DB_NAME)

all: reset_db unzip_db to_mongo

reset_db:
	$(PSSWRD) dropdb --if-exists $(AUTH) $(DB_NAME)
	$(PSSWRD) createdb $(AUTH) $(DB_NAME)

unzip_db:
	gunzip -c $(DIR_SQL)dump_v1.5-P3.sql.gz | $(DB)

to_mongo:
	python3 $(DIR)createMongoDBFromPostgreSQLDB.py

run:
	python3 -m app
