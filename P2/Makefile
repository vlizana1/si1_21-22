DIR = app/sql/
AUTH = -U alumnodb -h 127.0.0.1
PSSWRD =  PGPASSWORD=alumnodb
DB_NAME = si1
DB = $(PSSWRD) psql $(AUTH) $(DB_NAME)

all: reset_db unzip_db actualiza

reset_db:
	$(PSSWRD) dropdb --if-exists $(AUTH) $(DB_NAME)
	$(PSSWRD) createdb $(AUTH) $(DB_NAME)

unzip_db:
	gunzip -c $(DIR)dump_v1.4.sql.gz | $(DB)

actualiza:
	cat $(DIR)actualiza.sql | $(DB)

run:
	python3 -m app
