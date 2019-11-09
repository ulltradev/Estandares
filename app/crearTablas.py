import sqlite3
def create_table_cliente():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS cliente_ (NitCliente integer PRIMARY KEY,"""\
                                                """NombreCliente text,"""\
                                                """TelefonoCliente text,"""\
                                                """DireccionCliente text,"""\
                                                """FechaNacimientoCliente date,"""\
                                                """GeneroCliente text)""")
    conn.commit()
    c.close()
    conn.close()

def create_table_carros():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS carros (LLaveCarro text PRIMARY KEY,"""\
                                                """NombreCarro text,"""\
                                                """ModeloCarro text)""")
    conn.commit()
    c.close()
    conn.close()

def create_table_ventas():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS ventas (Idventa INTEGER PRIMARY KEY,"""\
                                                """NombreCarro text,"""\
                                                """ModeloCarro text)""")
    conn.commit()
    c.close()
    conn.close()


def meter_Valores_en_carros():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    sql = ''' INSERT INTO carros (LLaveCarro,NombreCarro,ModeloCarro)'''\
          ''' VALUES(?,?,?) '''
    c.execute(sql, ['chevrolet_camaro2019','chevrolet_camaro','2019'])
    conn.commit()
    c.close()
    conn.close()
    return "success"

create_table_carros()
meter_Valores_en_carros()