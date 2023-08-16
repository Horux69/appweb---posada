class ValidationLoginAdmin:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def validaLogin(self, correo, contrasena):

        consulta = f"SELECT nombres, rol FROM operadores WHERE correo = '{correo}' AND clave = '{contrasena}'"

        self.cursor.execute(consulta)

        resultado = self.cursor.fetchall()

        self.conexion.commit()

        return resultado


    def buscarMedico(self, id):
        consultaMedicos = f"SELECT * FROM medicos WHERE idmedico = '{id}'"
        self.cursor.execute(consultaMedicos)
        resultado = self.cursor.fetchone()
        self.conexion.commit()
        return resultado
