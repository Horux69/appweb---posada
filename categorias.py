from datetime import datetime

class Categorias:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def consulta_categorias(self):

        sql = "SELECT * FROM `categorias`"
        self.cursor.execute(sql)
        resultado_categorias = self.cursor.fetchall()
        self.conexion.commit()
        return resultado_categorias
    
    def agregar_categorias(self, categoria, user_registro):

        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = f"INSERT INTO categorias (id, nombre, fecha_registro, user_registro) VALUES (NULL,'{categoria[0]}', '{fecha_actual}', '{user_registro}')"
        self.cursor.execute(sql)
        self.conexion.commit()