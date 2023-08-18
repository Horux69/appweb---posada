from datetime import datetime

class SitiosTuristicos:
    def __init__(self, miBD):
        self.mysql = miBD
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def agregarSitio(self, sitio):
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = f"INSERT INTO `sitios`(`id`, `nombre`, `direccion`, `descripcion`, `fk_categorias`, `fk_fotos`, `fk_busqueda`, `latitud`, `longitud`, `fecha_registro`, `user_registro`, `estado`, `parriba_izquierda_lat`, `parriba_izquierda_lon`, `parriba_derecha_lat`, `parriba_derecha_lon`, `pabajo_izquierda_lat`, `pabajo_izquierda_lon`, `pabajo_derecha_lat`, `pabajo_derecha_lon`) VALUES (NULL, )"


