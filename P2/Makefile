DIR = app/sql/
AUTH = -U alumnodb -h 127.0.0.1
PSSWRD =  PGPASSWORD=alumnodb
DB_NAME = si1
DB = $(PSSWRD) psql $(AUTH) $(DB_NAME)

all: reset_db unzip_db actualiza set update

get: getTopSales getTopActors

reset_db:
	$(PSSWRD) dropdb --if-exists $(AUTH) $(DB_NAME)
	$(PSSWRD) createdb $(AUTH) $(DB_NAME)

unzip_db:
	gunzip -c $(DIR)dump_v1.4.sql.gz | $(DB)

actualiza:
	cat $(DIR)actualiza.sql | $(DB)

set:
	cat $(DIR)setPrice.sql | $(DB)
	cat $(DIR)setOrderAmount.sql | $(DB)

update:
	cat $(DIR)updOrders.sql | $(DB)

update2:
	cat $(DIR)updInventoryAndCustomer.sql | $(DB)

getTopSales:
	cat $(DIR)getTopSales.sql | $(DB)

getTopActors:
	cat $(DIR)getTopActors.sql | $(DB)

run:
	python3 -m app
