from datetime import date, datetime


def limpiar_texto(texto, campo="El campo"):
    valor = str(texto).strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacío.")
    return valor


def validar_texto(texto):
    return bool(str(texto).strip())


def validar_anio(anio):
    try:
        valor = int(anio)
    except (TypeError, ValueError) as error:
        raise ValueError("El año debe ser un número entero.") from error
    if valor <= 0 or valor > date.today().year + 1:
        raise ValueError("El año debe ser positivo y no puede superar el año próximo.")
    return valor


def validar_fecha(fecha):
    if isinstance(fecha, date):
        return fecha.isoformat()
    try:
        return datetime.strptime(str(fecha), "%Y-%m-%d").date().isoformat()
    except ValueError as error:
        raise ValueError("La fecha debe ser válida y tener formato AAAA-MM-DD.") from error
