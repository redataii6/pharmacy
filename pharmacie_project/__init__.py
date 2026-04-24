# Ce fichier marque le répertoire comme un package Python.

# Utiliser PyMySQL comme connecteur MySQL à la place de mysqlclient
# import pymysql
# pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import DatabaseWrapper
def check_database_version_supported(self):
    pass
DatabaseWrapper.check_database_version_supported = check_database_version_supported
