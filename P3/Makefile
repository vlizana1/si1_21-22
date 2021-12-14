DIR = app/
DIR_SQL = $(DIR)sql/
DIR_SQL_I = SQL/
AUTH = -U alumnodb -h 127.0.0.1
PSSWRD = PGPASSWORD=alumnodb
DB_NAME = si1
DB = $(PSSWRD) psql $(AUTH) $(DB_NAME)


# Comando para preparar y probar el apartado 1
apartado1: reset_db to_mongo

# Comando para preparar y probar el ejercicio H del apartado 3
apartado3_H: reset_db no_delete_on_cascade

# Comando para preparar y probar el ejercicio I del apartado 3
apartado3_I: reset_db updPromo


reset_db: clear_db unzip_db

clear_db:
	$(PSSWRD) dropdb --if-exists $(AUTH) $(DB_NAME)
	$(PSSWRD) createdb $(AUTH) $(DB_NAME)

unzip_db:
	gunzip -c $(DIR_SQL)dump_v1.5-P3.sql.gz | $(DB)

to_mongo:
	python3 $(DIR)createMongoDBFromPostgreSQLDB.py

no_delete_on_cascade:
	cat $(DIR_SQL)no_delete_on_cascade.sql | $(DB)

updPromo:
	cat $(DIR_SQL_I)updPromo.sql | $(DB)

run:
	python3 -m app
