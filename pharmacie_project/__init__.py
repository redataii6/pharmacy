# Ce fichier marque le répertoire comme un package Python.

# Utiliser PyMySQL comme connecteur MySQL à la place de mysqlclient
import pymysql
pymysql.install_as_MySQLdb()
