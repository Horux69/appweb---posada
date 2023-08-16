class ValidationLoginAdmin:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def validaLogin(self, correo, contrasena):
        consulta = f"SELECT nombres, correo, clave, rol, estado FROM operadores WHERE correo = '{correo}' AND clave = '{contrasena}' AND estado = 'activo'"
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado


