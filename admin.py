from datetime import datetime

class Administrador:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def consultarAdmin(self):
        sql = "SELECT * FROM operadores WHERE estado = 'activo'"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado

    def buscarAdmin(self, correo, cedula):
        consultaOperador = f"SELECT * FROM operadores WHERE correo = '{correo}' OR cedula = '{cedula}'"
        self.cursor.execute(consultaOperador)
        resultado = self.cursor.fetchone()
        self.conexion.commit()
        return resultado

    def agregarAdmin(self, operador, user_registro):

        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = f"INSERT INTO operadores (id, nombres, apellidos, cedula, correo, celular, rol, clave, estado, fecha_registro, user_registro) VALUES (NULL,'{operador[0]}','{operador[1]}','{operador[2]}','{operador[3]}','{operador[4]}','{operador[5]}','{operador[6]}','{operador[7]}', '{fecha_actual}', '{user_registro}')"
        self.cursor.execute(sql)
        self.conexion.commit()