import os
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

############################################################
# Declaration de variables nécessaire à l'exécution du code
###########################################################

# A modifier / chemin de creation du .credential
home_dir = 'C:/monChemin/'

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
# chemin de la branche principale pour la crzation du fichier credentials (droit d'acczs au drive)



def get_credentials():
    #dzclaration du chemin
    credential_dir = os.path.join(home_dir, '.credentials')
    #vzrification de l'existence du dossier, et crzation si besoin
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')
    #ouverture
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    #verification de la validitz des credential
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)

        print('credential crees: ' + credential_path)


def main():
    get_credentials()
    print("credential ok")


if __name__ == '__main__':
    main()