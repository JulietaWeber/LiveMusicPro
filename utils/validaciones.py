from datetime import datetime

def validar_texto(texto):

    return texto.strip() != ""

def validar_anio(anio):

    return anio > 1900

def validar_fecha(fecha):

    hoy = datetime.now().date()

    return fecha >= hoy