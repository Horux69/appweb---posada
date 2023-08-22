string = "RELIGIOSOS"
cod_p1 = string[0:3]

string = "ORIENTE"
cod_p2 = string[0:3]

cod_p3 = 0

cod_p3 += 1
cod_p3 = str(cod_p3).zfill(4)


cod_sitio = cod_p1 + cod_p2 + cod_p3

print(cod_sitio)