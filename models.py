
class Registro:
    def __init__(self, id, nombre, categoria, descripcion, precio=0.0, activo=True, destacado=False):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.activo = activo
        self.destacado = destacado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "activo": self.activo,
            "destacado": self.destacado
        }

    def __repr__(self):
        return (
            f"<Registro id={self.id} nombre='{self.nombre}' "
            f"categoria='{self.categoria}' precio={self.precio} "
            f"activo={self.activo} destacado={self.destacado}>"
        )


class Usuario:
    def __init__(self, id, nombre, correo, password=None):
        self.id = id
        self.nombre= nombre
        self.correo = correo
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo
        }

    def __repr__(self):
        return f"<Usuario id={self.id} nombre='{self.nombre}' correo='{self.correo}'>"


class Cita:
    ESTADOS = ['pendiente', 'confirmada', 'en_proceso', 'completada', 'cancelada']

    def __init__(self, id, nombre_cliente, correo_cliente, fecha, hora,
                 servicio, notas="", estado="pendiente"):
        self.id = id
        self.nombre_cliente = nombre_cliente
        self.correo_cliente = correo_cliente
        self.fecha = fecha
        self.hora = hora
        self.servicio = servicio
        self.notas = notas
        self.estado = estado if estado in self.ESTADOS else "pendiente"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_cliente": self.nombre_cliente,
            "correo_cliente": self.correo_cliente,
            "fecha": str(self.fecha),
            "hora":str(self.hora),
            "servicio": self.servicio,
            "notas": self.notas,
            "estado":self.estado
        }

    def __repr__(self):
        return (
            f"<Cita id={self.id} cliente='{self.nombre_cliente}' "
            f"fecha={self.fecha} hora={self.hora} estado='{self.estado}'>"
        )