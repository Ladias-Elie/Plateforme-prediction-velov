import io
import os
import httplib2
import googleapiclient
from googleapiclient import discovery
import oauth2client
from oauth2client import file
import postgresql
import utils_ch_NSP
from postgresql import exceptions
import time
import datetime
import sys


############################################################
# Declaration de variables necessaire à l'execution du code
###########################################################


# chemin de la branche principale pour la creation du fichier credentials (droit d'acces au drive)
home_dir = 'C:/Users/lata/PycharmProjects/LDSA_velov_JSON_to_SQL/'

# script sql creation de la table velov
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


def get_credentials():
    #declaration du chemin
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')
    #ouverture
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    #verification de la validite des credential
    if not credentials or credentials.invalid:
        print("erreur! veuillez relancer createCredential.py")
        sys.exit(1)
    return credentials


# fonction principale de chargement et insertion du fichier dans la base
def dl_insert(param_results, param_s_f, param_outpath, param_IRI, param_database_name, param_table_name):
    start_time = time.time()
    db = postgresql.open(param_IRI + param_database_name)
    nb_files = 0
    items = param_results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            file_id = item['id']
            file_name = item['name']
            nb_files += 1
            print("*******Chargement et traitement du fichier******", file_name)
            # chargement get_media
            request = param_s_f.get_media(fileId=file_id)
            outfilename = param_outpath+"_temp.json"
            outfile = io.FileIO(outfilename, mode='w+')
            downloader = googleapiclient.http.MediaIoBaseDownload(outfile, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            if db.closed:
                print("!!Connexion reouverte!!")
                db = postgresql.open(param_IRI + param_database_name)
            data, d = utils_Json_Postgres.data_create(outfilename, False, set_int, set_float, set_date, "%Y-%m-%d %H:%M:%S")
            # Declaration  et preparation de la requete d'insertion
            sql_insert = utils_Json_Postgres.cons_insert(param_table_name, data)
            statement = None
            try:
                statement = db.prepare(sql_insert)
            except exceptions.DuplicateTableError:
                print("Une exception est soulevee!!! Erreur sur la requete d'insertion")
            utils_Json_Postgres.insertion(data, d, statement)
    print("Tps execution pour le chargement et l'insertion des %s fichiers" % nb_files)
    print(" --- %s seconds ---" % (time.time() - start_time))
    return nb_files



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

    start_time = time.time()
    nb_files_tot = 0
    # Ouverture et connexion a la bd
    db = postgresql.open(IRI + database_name)
    # Creation de la table 'velov'
    utils_Json_Postgres.create_table(db, sql_table, table_name, database_name)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http, credentials=credentials)
    s_f = service.files()
    results = s_f.list(pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    # id de la page suivante pour n'oublier aucun fichier
    n_p_t = results.get('nextPageToken')
    nb_files_tot = nb_files_tot + dl_insert(results, s_f, home_dir, IRI, database_name,table_name)
    while n_p_t is not None :
        print("************Nouvelle page du Drive**************")
        results = s_f.list(pageSize=1000, pageToken = n_p_t, fields="nextPageToken, files(id, name)").execute()
        # id de la page suivante pour n'oublier aucun fichier
        n_p_t = results.get('nextPageToken')
        nb_files_tot = nb_files_tot + dl_insert(results, s_f, home_dir, IRI, database_name,table_name)
    print("nb tot: %s" % nb_files_tot)
    tmp = time.time() - start_time
    tmp = str(datetime.timedelta(seconds=tmp))
    print(" Fin du script en --- %s  ---" % tmp)


if __name__ == '__main__':
    main()