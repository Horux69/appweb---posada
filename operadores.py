from datetime import datetime

class Operadores:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def consultarOperador(self):
        sql = "SELECT * FROM operadores WHERE estado = 'activo' AND rol = 'op'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado
    
    def buscarOperador(self, correo, cedula):
        consulta = f"SELECT * FROM operadores WHERE correo = '{correo}' OR cedula = '{cedula}'"
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado
    
    def agregarOperadores(self, operador, user_registro):

        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = f"INSERT INTO operadores (id, nombres, apellidos, cedula, correo, celular, rol, clave, estado, fecha_registro, user_registro) VALUES (NULL, '{operador[0]}','{operador[1]}','{operador[2]}','{operador[3]}','{operador[4]}','{operador[5]}','{operador[6]}','{operador[7]}','{fecha_actual}', '{user_registro}')"
        self.cursor.execute(sql)
        self.conexion.commit()

    def desactivarOpe(self, id):
        sql = f"UPDATE `operadores` SET `estado`='inactivo' WHERE `id` = '{id}'"
        self.cursor.execute(sql)
        self.conexion.commit()

    def eliminarOpe(self, id):
        sql = f"DELETE FROM operadores WHERE id = '{id}'"
        self.cursor.execute(sql)
        self.conexion.commit()