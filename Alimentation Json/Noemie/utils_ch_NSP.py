import postgresql
from postgresql import exceptions
import json
from datetime import datetime
from urllib.request import urlretrieve

##################################################################################
# Declaration des fonctions utiles


# Creation et verification de l'existance de la table
# Parametres:   param_db : sortie de l'ouverture de la connexion
#               param_sql_table: appel à la "create table" declaree par l'utilisateur
#               param_table_name: nom de la table declaree par l'utilisateur
#               param_database_name: nom de la database declaree par l'utilisateur
def create_table(param_db, param_sql_table, param_table_name, param_database_name):
    try:
        exe = param_db.execute(param_sql_table)
    except postgresql.exceptions.DuplicateTableError:
        print("La table « {}.{} » existe deja.".format(param_database_name, param_table_name))
    else:
        if exe is None:
            print("db.execute('{}') n'a pas renvoye d'erreur.".format(param_sql_table))


# Conversion Json en dictionnaire pour acceder facilement aux champs nommes
# Parametres:   data_json: data json deja charge
# Sortie: data json transforme en dictionnaire
def json_dict(data_json):
    if isinstance(data_json['values'][0], list):
        print('[load_json] Conversion list -> dict')
        val_list = list()
        l = 0
        while l < data_json['values'].__len__():
            dico = dict()
            for index in range(data_json['fields'].__len__()):
                dico[data_json['fields'][index]] = data_json['values'][l][index]
            val_list.append(dico)
            l += 1
        data_json['values'] = val_list
    res = data_json['values']
    return res


# Conversions dans les bons formats: en integers / float / date : pour tous les int / float / date a detecter a la main
# Parametres:   data_dict : data json ayant deja ete transforme en dictionnaire
#               param_set_int : set declare, comprenant les champs integer du json
#               param_set_float : set declare, comprenant les champs float du json
#               param_set_date : set declare, comprenant les champs de type du json
# Sortie: data_dict avec les bons formats
def conv_format(data_dict, param_set_int, param_set_float, param_set_date, param_format_date):
    for i in range(data_dict.__len__()):
        for key in param_set_float:
            data_dict[i][key] = float(data_dict[i][key])
        for key in param_set_int:
            try:
                data_dict[i][key] = int(data_dict[i][key])
            except ValueError as val_err:
                data_dict[i][key] = None
        for key in param_set_date:
            data_dict[i][key] = datetime.strptime(data_dict[i][key], param_format_date)
    return data_dict


# Chargement et modification du Json
# Parmetres:    file_path_json: url/chemin du json
#               online: booleen, True si le json est en ligne / False s'il est en local
# Sortie : data d
def data_create(file_path_json, online, param_set_int, param_set_float, param_set_date, param_format_date):
    if online:
        file_path_json, header = urlretrieve(file_path_json)
    json_data = open(file_path_json, mode='r')
    data = json.load(json_data)
    # Conversion en dictionnaire puis typage
    d = json_dict(data)
    d = conv_format(d, param_set_int, param_set_float, param_set_date, param_format_date)
    # print("Fichier charge et modifie avec succes")
    return data, d


# Construction de l'INSERT SQL
# Parametres:   param_table_name: table SQL deja creee
#               param_data: data json préalablement charge
# Sortie : statement necessaire a chaque appel d'insertion dans la table
def cons_insert(param_table_name, param_data):
    res = "INSERT INTO {} (".format(param_table_name)
    # parcours des champs declares dans fields
    for field in param_data['fields']:
        res += field + ", "
    res = res[:-2] + ") VALUES ("
    for indice in range(1, param_data['fields'].__len__() + 1):
        res += "${},".format(indice)
    res = res[:-1] + ")"
    # print("Construction de la requete d'insertion")
    return res


# Insertion
# Parametres:   data_param: data chargee comprenant encore les fields
#               d_param: json modifiee (mise en format)
#               statement_param: statement construit par la fonction cons_insert
def insertion(data_param, d_param, statement_param):
    c_ligne = 0
    for i in range(d_param.__len__()):
        li = list()
        for key in data_param['fields']:
            li.append(d_param[i][key])
        statement_param(*li)
        c_ligne += 1
    # print("Insertion des {} entrees pour {} lignes du json".format(c_ligne, d_param.__len__()))


