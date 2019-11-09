import re
import os
import json
import sqlite3
import configparser 
from app import app
from datetime import datetime
from werkzeug import secure_filename
from flask import render_template, url_for,request, redirect,jsonify

def generarlistaDeCarros():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT NombreCarro,ModeloCarro FROM carros")
    rows = c.fetchall()
    c.close()
    conn.close()
    return [row[0]+","+row[1] for row in rows]

def generarlistaDeExtra():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT Idextras,extraNombre FROM extras")
    rows = c.fetchall()
    c.close()
    conn.close()
    return [row for row in rows]

def generarlistaDeMecanicos():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT LLaveMecanico,NombreMecanico FROM mecanicos")
    rows = c.fetchall()
    c.close()
    conn.close()
    return [row for row in rows]

def generarlistaDeReparacionesRevisiones():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT LLaveReparacionLista,ReparaciosNombre,ReparacionTipo FROM reparacionesLista")
    rows = c.fetchall()
    c.close()
    conn.close()
    return [row for row in rows]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['pdf']

def checkearSiUsuarioExiste(NitCliente):
    if NitCliente:
        conn = sqlite3.connect("estandar_calidad.db")
        c = conn.cursor()
        c.execute("SELECT * FROM cliente_ WHERE NitCliente = "+str(NitCliente))
        rows = c.fetchall()
        c.close()
        conn.close()
        return rows
    return None

def checkearSiReparoExiste(LLaveReparacion):
    if LLaveReparacion:
        conn = sqlite3.connect("estandar_calidad.db")
        c = conn.cursor()
        c.execute("SELECT * FROM reparacionesFacts WHERE LLaveReparacion = "+str(LLaveReparacion))
        rows = c.fetchall()
        c.close()
        conn.close()
        return rows
    return None


def checkearSiVentaExiste(Idventa):
    if Idventa:
        conn = sqlite3.connect("estandar_calidad.db")
        c = conn.cursor()
        c.execute("SELECT * FROM ventas WHERE Idventa = "+str(Idventa))
        rows = c.fetchall()
        c.close()
        conn.close()
        return rows
    return None


def indicarElIdDeVentaRecienIngresada():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT IdVenta FROM ventas ORDER BY IdVenta DESC LIMIT 1")
    valor = c.fetchone()
    c.close()
    conn.close()
    return valor[0]


@app.route('/moduloVentas')
def method_for_sales():
    carros = generarlistaDeCarros()
    extras = generarlistaDeExtra()
    return render_template('pagGuardarVenta.html', title='Home',carros=carros,extras=extras,numExtras=len(extras))

@app.route('/moduloActualizarVentas')
def method_for_updatingsales():
    carros = generarlistaDeCarros()
    extras = generarlistaDeExtra()
    return render_template('pagActualizarVenta.html', title='Home',carros=carros,extras=extras,numExtras=len(extras))


@app.route('/moduloReparacion')
def method_for_fixes():
    mecanicos = generarlistaDeMecanicos()
    reparevi = generarlistaDeReparacionesRevisiones()
    return render_template('pagGuardarReparaciones.html', title='Home',mecanicos=mecanicos,reparevi=reparevi)



@app.route('/matchesEncontrada', methods=['POST'])
def extracting():
    m = re.findall(request.form.get("reguExpre").replace("\\n","\n"), request.form.get("texto").replace("\\n","\n"), flags=re.MULTILINE)
    if m:
        textAReemplazar = request.form.get("texto")
        matchesEncontados = set(m)
        for match in matchesEncontados:
            textAReemplazar = textAReemplazar.replace(match,'<span style="background-color: red">'+match+'</span>') 
        return jsonify({'lista':m,'regex':request.form.get("reguExpre"),'textoResaltado':textAReemplazar})
    else:
        return jsonify("patron no encontrado")


@app.route('/addicionDeEntradaEnSeccion', methods=['POST'])
def agregandoEntradaEnSeccionDeArchivoConig():
    try:
        config = configparser.ConfigParser()
        config.read("app/config.ini")  # Add this line
        cnfFile = open("app/config.ini", "w")
        config.set(request.form.get("seccionName"),request.form.get("nombreDeVariable"), r''+request.form.get("reguExpre"))
        config.write(cnfFile)
        cnfFile.close()
        return "veamos"
    except Exception as e:
        if 'No section' in str(e):
            return "esa seccion aun no existe"



@app.route('/logicaIngresarUpdateClientes', methods=['POST'])
def method_for_creating_users_logic():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    if checkearSiUsuarioExiste(request.form.get("nitCliente")):
        sql = '''UPDATE  cliente_
                 SET NombreCliente =?,
                     TelefonoCliente=?,
                     DireccionCliente=?,
                     FechaNacimientoCliente=?,
                     GeneroCliente=?
                 WHERE NitCliente = ?'''
        c.execute(sql, [request.form.get("nombreCliente"),request.form.get("telefonoCliente"),request.form.get("direccionCliente"),\
                        request.form.get("fechaNacimientoCliente"),request.form.get("generoCliente[]"),request.form.get("nitCliente")])
        conn.commit()
        c.close()
        conn.close()
        return ({"accion realizada":"usuario actualizado",\
                 "Nit":request.form.get("nitCliente"),\
                 "Nombre":request.form.get("nombreCliente"),\
                 "telefono":request.form.get("telefonoCliente"),\
                 "direccion":request.form.get("direccionCliente"),\
                 "fecha":request.form.get("fechaNacimientoCliente"),\
                 "genero":request.form.get("generoCliente[]")})

    else:
        sql = ''' INSERT INTO cliente_(NitCliente,NombreCliente,TelefonoCliente,DireccionCliente,FechaNacimientoCliente,GeneroCliente)'''\
            ''' VALUES(?,?,?,?,?,?) '''
        c.execute(sql, [request.form.get("nitCliente"),request.form.get("nombreCliente"),request.form.get("telefonoCliente"),\
                        request.form.get("direccionCliente"),request.form.get("fechaNacimientoCliente"),request.form.get("generoCliente[]")])
        conn.commit()
        c.close()
        conn.close()
        return ({"accion realizada":"usuario ingresado",\
                 "Nit":request.form.get("nitCliente"),\
                 "Nombre":request.form.get("nombreCliente"),\
                 "telefono":request.form.get("telefonoCliente"),\
                 "direccion":request.form.get("direccionCliente"),\
                 "fecha":request.form.get("fechaNacimientoCliente"),\
                 "genero":request.form.get("generoCliente[]")})
    
@app.route('/logicaIngresarUpdateVentas', methods=['POST'])
def method_for_creating_cars_logic():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    if checkearSiUsuarioExiste(request.form.get("nitCliente")):
        if checkearSiVentaExiste(request.form.get("idVenta")):
            sql = '''UPDATE  ventas
                     SET NombreCarro =?,
                         ModeloCarro=?,
                         ExtrasCarro=?,
                         IdCliente=?,
                         IdVendedor=?,
                         HoraVenta=?,
                         fechaVenta=?
                     WHERE Idventa = ?'''
            c.execute(sql, [request.form.get("modeloVehiculo[]").split(",")[0],request.form.get("modeloVehiculo[]").split(",")[1],\
                            request.form.get("elExtra[]"),request.form.get("nitCliente"),"1","00:00",request.form.get("FechaDeLaVenta"),\
                            request.form.get("idVenta")])
            conn.commit()
            c.close()
            conn.close()
            return ({"accion realizada":"venta actualizada",\
                 "Nit":request.form.get("nitCliente"),\
                 "modeloVehiculo":request.form.get("modeloVehiculo[]"),\
                 "fecha venta":request.form.get("FechaDeLaVenta"),\
                 "idVenta":request.form.get("idVenta"),\
                 "asignaIdVenta":"no",\
                 "elExtra":request.form.get("elExtra[]")})
        else:
            sql = ''' INSERT INTO ventas(NombreCarro,ModeloCarro,ExtrasCarro,IdCliente,IdVendedor,HoraVenta,fechaVenta)'''\
                  ''' VALUES(?,?,?,?,?,?,?) '''
            c.execute(sql, [request.form.get("modeloVehiculo[]").split(",")[0],request.form.get("modeloVehiculo[]").split(",")[1],\
                            request.form.get("elExtra[]"),request.form.get("nitCliente"),"1","00:00",datetime.now()])
            conn.commit()
            c.close()
            conn.close()
            return ({"accion realizada":"venta ingresada",\
                 "Nit":request.form.get("nitCliente"),\
                 "modeloVehiculo":request.form.get("modeloVehiculo[]"),\
                 "idVenta":str(indicarElIdDeVentaRecienIngresada()),\
                 "asignaIdVenta":"si",\
                 "elExtra":request.form.get("elExtra[]")})
    else:
        return "no existe el cliente"



@app.route('/logicaIngresarUpdateRepaRevi', methods=['POST'])
def method_for_fixin_cars_logic():
    return str(request.form)

@app.route('/obtenerListaDeVentas', methods=['GET'])
def traigamosTodasLasVentas():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT * FROM ventas")
    rows = c.fetchall()
    c.close()
    conn.close()
    return render_template('data-tablesCarros.html', title='mostrarVentas',rows=rows)


@app.route('/obtenerListaDeReparacinesLista', methods=['GET'])
def traigamosTodasLasReparacinesLista():
    conn = sqlite3.connect("estandar_calidad.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reparacionesLista")
    rows = c.fetchall()
    c.close()
    conn.close()
    return render_template('data-tablesReparaciones.html', title='mostrarReparaciones',rows=rows)
    #return str(request.form)
            # return ({"accion realizada":"venta actualizada",\
            #      "Nit":request.form.get("nitCliente"),\
            #      "modeloVehiculo":request.form.get("modeloVehiculo[]"),\
            #      "fecha venta":request.form.get("FechaDeLaVenta"),\
            #      "idVenta":request.form.get("idVenta"),\
            #      "asignaIdVenta":"no",\
            #      "elExtra":request.form.get("elExtra[]")}) 
    # conn = sqlite3.connect("estandar_calidad.db")
    # c = conn.cursor()
    # if checkearSiUsuarioExiste(request.form.get("nitCliente")):
    #     if checkearSiReparoExiste(request.form.get("idVenta")):
    #         sql = '''UPDATE  ventas
    #                  SET NombreCarro =?,
    #                      ModeloCarro=?,
    #                      ExtrasCarro=?,
    #                      IdCliente=?,
    #                      IdVendedor=?,
    #                      HoraVenta=?,
    #                      fechaVenta=?
    #                  WHERE Idventa = ?'''
    #         c.execute(sql, [request.form.get("modeloVehiculo[]").split(",")[0],request.form.get("modeloVehiculo[]").split(",")[1],\
    #                         request.form.get("elExtra[]"),request.form.get("nitCliente"),"1","00:00",request.form.get("FechaDeLaVenta"),\
    #                         request.form.get("idVenta")])
    #         conn.commit()
    #         c.close()
    #         conn.close()
    #         return ({"accion realizada":"venta actualizada",\
    #              "Nit":request.form.get("nitCliente"),\
    #              "modeloVehiculo":request.form.get("modeloVehiculo[]"),\
    #              "fecha venta":request.form.get("FechaDeLaVenta"),\
    #              "idVenta":request.form.get("idVenta"),\
    #              "asignaIdVenta":"no",\
    #              "elExtra":request.form.get("elExtra[]")})
    #     else:
    #         sql = ''' INSERT INTO ventas(NombreCarro,ModeloCarro,ExtrasCarro,IdCliente,IdVendedor,HoraVenta,fechaVenta)'''\
    #               ''' VALUES(?,?,?,?,?,?,?) '''
    #         c.execute(sql, [request.form.get("modeloVehiculo[]").split(",")[0],request.form.get("modeloVehiculo[]").split(",")[1],\
    #                         request.form.get("elExtra[]"),request.form.get("nitCliente"),"1","00:00",datetime.now()])
    #         conn.commit()
    #         c.close()
    #         conn.close()
    #         return ({"accion realizada":"venta ingresada",\
    #              "Nit":request.form.get("nitCliente"),\
    #              "modeloVehiculo":request.form.get("modeloVehiculo[]"),\
    #              "idVenta":str(indicarElIdDeVentaRecienIngresada()),\
    #              "asignaIdVenta":"si",\
    #              "elExtra":request.form.get("elExtra[]")})
    # else:
    #     return "no existe el cliente"
