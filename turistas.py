class Turistas:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def buscarTuristas(self, correo, cedula):
        consulta = f"SELECT * FROM turistas WHERE correo = '{correo}' OR cedula = '{cedula}'"
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado

    def agregarTurista(self, turista, user_registro):
        sql = "INSERT INTO turistas (id, nombres, apellidos, cedula, correo, foto, celular, rol, clave, estado, latitud, longitud, fecha_registro, user_registro) VALUES (NULL, )"
        