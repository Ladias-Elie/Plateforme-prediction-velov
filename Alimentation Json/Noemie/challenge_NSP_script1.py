import postgresql
import utils_challenge_NSP
from postgresql import exceptions
import time
import datetime
import sys

####################################
## Declaration des var utiles

# lien du site pour la recuperation des donnees
lienF = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'

# script sql necessaire creation de la table velov
sql_table = "CREATE TABLE {} (" \
            "id SERIAL PRIMARY KEY," \
            "number INTEGER NOT NULL," \
            "name VARCHAR(36) NOT NULL," \
            "address VARCHAR(65) NOT NULL," \
            "address2 VARCHAR(48)," \
            "commune VARCHAR(16) NOT NULL," \
            "nmarrond INTEGER," \
            "bonus VARCHAR(3) NOT NULL," \
            "pole VARCHAR(61) NOT NULL," \
            "lat DECIMAL(18) NOT NULL," \
            "lng DECIMAL(18) NOT NULL," \
            "bike_stands INTEGER NOT NULL," \
            "status VARCHAR(6) NOT NULL," \
            "available_bike_stands INTEGER NOT NULL," \
            "available_bikes INTEGER NOT NULL," \
            "availabilitycode INTEGER NOT NULL," \
            "availability VARCHAR(6) NOT NULL," \
            "banking VARCHAR(5) NOT NULL," \
            "gid INTEGER NOT NULL," \
            "last_update TIMESTAMP WITHOUT TIME ZONE NOT NULL," \
            "last_update_fme TIMESTAMP WITHOUT TIME ZONE NOT NULL)".format('velov')

# declaration de set pour la transformation avant insert
set_int = {'available_bike_stands', 'gid', 'nmarrond', 'availabilitycode',
                    'bike_stands', 'available_bikes', 'number'}
set_float = {'lat', 'lng'}
set_date = {'last_update', 'last_update_fme'}


def main():
    if len(sys.argv) != 6:
        print("Erreur dans les arguments")
        sys.exit(1)
    else:
        # recuperation des arguments
        host = sys.argv[1]
        database_name = sys.argv[2]
        table_name = sys.argv[3]
        user = sys.argv[4]
        pwd = sys.argv[5]
        IRI = 'pq://'+user+':'+pwd+'@'+host+'/'
        start_time = time.time()
        db = postgresql.open(IRI + database_name)
        # Creation de la table 'velov'
        utils_Json_Postgres.create_table(db, sql_table, table_name, database_name)
        if db.closed:
            db = postgresql.open(IRI + database_name)
        # chargement et modification du json pour preparation a l'insertion en bdd
        data, d = utils_Json_Postgres.data_create(lienF, True, set_int, set_float, set_date, "%Y-%m-%d %H:%M:%S")
        # Declaration  et preparation de la requete d'insertion
        sql_insert = utils_Json_Postgres.cons_insert(table_name, data)
        statement = None
        try:
            statement = db.prepare(sql_insert)
        except exceptions.DuplicateTableError:
            print("Une exception est soulevee!!! Erreur sur la requete d'insertion")
        # insertion
        utils_Json_Postgres.insertion(data, d, statement)
        tmp = time.time() - start_time
        tmp = str(datetime.timedelta(seconds=tmp))
        print(" Tps execution --- %s  ---" % tmp)

if __name__ == '__main__':
    main()






