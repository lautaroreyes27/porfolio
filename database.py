import pymysql
from pymysql.cursors import DictCursor
from config import Config

class Database:

    def __init__(self):
        self.__params = dict(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset="utf8mb4",
            cursorclass=DictCursor,
        )

    def consultar(self, sql, params=None):
        conexion = pymysql.connect(**self.__params)
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        finally:
            conexion.close()

    def ejecutar(self, sql, params=None):
        conexion = pymysql.connect(**self.__params)
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, params or ())
            conexion.commit()
            return cursor.lastrowid
        finally:
            conexion.close()
