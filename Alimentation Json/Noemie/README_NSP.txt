# Noémie SALAUN-PENQUER
# Mars 2016
# Integration velov
# en python 3.4

# 3 scripts disponibles:
	# 1/ Chargement et integration du Json velov (disponible en ligne)
	# 2/ Integration des json disponible sur un Drive 
	# 3/ Integration des json disponible dans un dossier

######### SCRIPT 1 ###########
# challenge_NSP_script1 

# Prérequis:
	# Adresse de récupération du fichier: 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json'
	# Schéma de la table : intégré au code mais qui pourrait être stocké dans un fichier.txt et passé en paramètre
	# Vérification de tous les packages nécessaires à l'exécution du code 
	# import utils_ch_NSP


# 1 fichiers python:
	# challenge_NSP_script1 (host database_name table_name user pwd)
		# host : adresse de la base de données avec le numéro de port
        	# database_name : nom de la base de données
        	# table_name : nom de la table où insérer les données
        	# user : nom d'utilisateur pour se connecter à la base de données
        	# pwd : mot de passe pour se connecter à la base de données

	# MAIN:		
		# Récupération des paramètres
		# Vérification de l'existence de la table
		# Récupération du fichier en ligne
		# Intégration (après manipulations, tests)
			
# Exemple exécution :
	# >C:\Python34\python challenge_NSP_script1.py "localhost:5432" "velov" "velov" "admin" "admin"
	# >La table « velov.velov » existe déjà.
	# >Fichier chargé et modifié avec succès
	# >Construction de la requête d'insertion
	# >Insertion des 348 entrées pour 348 lignes du json
	# >Tps execution --- 0:00:01.727544  ---

######### SCRIPT 2 ###########
# challenge_NSP_script2

# Prérequis:
	# client secret de l'adresse gmail: 'ldsa.velov@gmail.com' (demander le pwd)
	# Schéma de la table : intégré au code mais qui pourrait être stocké dans un fichier.txt et passé en paramètre
	# Vérification de tous les packages nécessaires à l'exécution du code 
	# import utils_ch_NSP
	# execution de createCredential.py 
	# Dans les 2 .py passer en paramètre le chemin du fichier client_secret.json : *home_dir*

# 1 fichiers python:
	# challenge_NSP_script2 (host database_name table_name user pwd)
		# host : adresse de la base de données avec le numéro de port
        	# database_name : nom de la base de données
        	# table_name : nom de la table où insérer les données
        	# user : nom d'utilisateur pour se connecter à la base de données
        	# pwd : mot de passe pour se connecter à la base de données
	# MAIN:		
		# Récupération des paramètres
		# Vérification de l'existence de la table
		# Connexion au Drive
		# Tant qu'il y a des json :
			# Chargement d'un fichier
			# Intégration (après manipulations, tests)

# Exemple exécution : (seulement json du mois de février pour test)
	# >C:\Python34\python createCredential.py
	# 
	# >C:\Python34\python challenge_NSP_script2.py "localhost:5432" "velov" "velov" "admin" "admin"
	# >...
	# >nb tot: 4622
 	# >Fin du script en --- 1:46:16.271047  ---

######### SCRIPT 3 ###########
	# challenge_NSP_script3
# Prérequis:
	# Chemin du dossier dans lequel se trouvent les json (var folder)
	# Schéma de la table : intégré au code mais qui pourrait être stocké dans un fichier.txt et passé en paramètre
	# Vérification de tous les packages nécessaires à l'exécution du code 
	# import utils_ch_NSP


# 1 fichiers python:
	# challenge_NSP_script3 (host database_name table_name user pwd)
		# host : adresse de la base de données avec le numéro de port
        	# database_name : nom de la base de données
        	# table_name : nom de la table où insérer les données
        	# user : nom d'utilisateur pour se connecter à la base de données
        	# pwd : mot de passe pour se connecter à la base de données

	# MAIN:		
		# Récupération des paramètres
		# Vérification de l'existence de la table
		# Pour tous les fichiers de type json du dossier:
			# Récupération du fichier en ligne
			# Intégration (après manipulations, tests)
			
# Exemple exécution :
	# >C:\Python34\python challenge_NSP_script3.py "localhost:5432" "velov" "velov" "admin" "admin"
	# >La table « velov.velov » existe déjà.
	# >...
	# >...