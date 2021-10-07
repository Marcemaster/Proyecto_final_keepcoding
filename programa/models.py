import sqlite3


class DBManager():
    def __init__(self, ruta_basedatos):
        self.ruta_basedatos = ruta_basedatos

    def consultaSQL(self, consulta, params=[]):
        conexion = sqlite3.connect(self.ruta_basedatos)

        cur = conexion.cursor()
        cur.execute(consulta, params)

        keys = []
        for item in cur.description:
            keys.append(item[0])

        registros = []
        for registro in cur.fetchall():
            ix_clave = 0
            d = {}
            for columna in keys:
                d[columna] = registro[ix_clave]
                ix_clave += 1
            registros.append(d)

        conexion.close()
        return registros

    def modificaSQL(self, consulta, params):
        conexion = sqlite3.connect(self.ruta_basedatos)

        cur = conexion.cursor()
        cur.execute(consulta, params)
        conexion.commit()
        conexion.close()
