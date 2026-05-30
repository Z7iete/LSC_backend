def validar_registro(data):
    errores = []

    if not data:
        errores.append("No se recibieron datos.")
        return errores

    if not str(data.get("nombre", "")).strip():
        errores.append("El nombre del servicio es obligatorio.")

    if not str(data.get("categoria", "")).strip():
        errores.append("La categoría es obligatoria.")

    categorias_validas = ['Servicios', 'Productos', 'Citas', 'Clientes', 'Inventario', 'Soporte']
    categoria = str(data.get("categoria", "")).strip()
    if categoria and categoria not in categorias_validas:
        errores.append(f"Categoría inválida. Opciones: {', '.join(categorias_validas)}.")

    if not str(data.get("descripcion", "")).strip():
        errores.append("La descripción del servicio es obligatoria.")

    if len(str(data.get("descripcion", "")).strip()) < 5:
        errores.append("La descripción debe tener al menos 5 caracteres.")

    try:
        precio = float(data.get("precio", 0))
        if precio <= 0:
            errores.append("El precio debe ser mayor que 0.")
    except (ValueError, TypeError):
        errores.append("El precio debe ser un número válido.")

    return errores


def validar_login(data):
    errores = []

    if not data:
        errores.append("No se recibieron datos.")
        return errores

    correo = str(data.get("correo", "")).strip()
    if not correo:
        errores.append("El correo es obligatorio.")
    elif "@" not in correo or "." not in correo.split("@")[-1]:
        errores.append("El correo no tiene un formato válido.")

    password = str(data.get("password", "")).strip()
    if not password:
        errores.append("La contraseña es obligatoria.")
    elif len(password) < 4:
        errores.append("La contraseña debe tener al menos 4 caracteres.")

    return errores


def validar_contacto(data):
    errores = []

    if not data:
        errores.append("No se recibieron datos.")
        return errores

    if not str(data.get("nombre", "")).strip():
        errores.append("El nombre es obligatorio.")

    correo = str(data.get("correo", "")).strip()
    if not correo:
        errores.append("El correo es obligatorio.")
    elif "@" not in correo or "." not in correo.split("@")[-1]:
        errores.append("El correo no tiene un formato válido.")

    mensaje = str(data.get("mensaje", "")).strip()
    if not mensaje:
        errores.append("El mensaje es obligatorio.")
    elif len(mensaje) < 10:
        errores.append("El mensaje debe tener al menos 10 caracteres.")

    return errores


def validar_cita(data):
    errores = []

    if not data:
        errores.append("No se recibieron datos.")
        return errores

    if not str(data.get("nombre_cliente", "")).strip():
        errores.append("El nombre del cliente es obligatorio.")

    correo = str(data.get("correo_cliente", "")).strip()
    if not correo:
        errores.append("El correo del cliente es obligatorio.")
    elif "@" not in correo or "." not in correo.split("@")[-1]:
        errores.append("El correo del cliente no tiene un formato válido.")

    if not str(data.get("fecha", "")).strip():
        errores.append("La fecha de la cita es obligatoria.")

    if not str(data.get("hora", "")).strip():
        errores.append("La hora de la cita es obligatoria.")

    if not str(data.get("servicio", "")).strip():
        errores.append("El servicio solicitado es obligatorio.")

    return errores