
import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv

from db import get_connection
from validators import validar_registro, validar_login, validar_contacto
from security import verificar_password
from email_service import enviar_correo_contacto
from models import Registro

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_temporal_desarrollo")

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
)

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])



@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "Backend Los Santos Customs activo",
        "proyecto": "Taller Mecánico Los Santos Customs"
    }), 200




@app.route("/registros", methods=["GET"])
def obtener_registros():
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registros ORDER BY id DESC")
        registros = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(registros), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al obtener registros: {str(e)}"}), 500


@app.route("/registros/<int:id>", methods=["GET"])
def obtener_registro(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre, categoria, descripcion, precio, activo, destacado FROM registros WHERE id = %s",
            (id,)
        )
        registro = cursor.fetchone()
        cursor.close()
        conexion.close()

        if not registro:
            return jsonify({"mensaje": "Registro no encontrado"}), 404

        return jsonify(registro), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al obtener registro: {str(e)}"}), 500


@app.route("/registros", methods=["POST"])
def agregar_registro():
    data = request.json

    errores = validar_registro(data)
    if errores:
        return jsonify({"errores": errores}), 400

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO registros (nombre, categoria, descripcion, precio, activo, destacado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            data.get("nombre"),
            data.get("categoria"),
            data.get("descripcion"),
            float(data.get("precio", 0)),
            bool(data.get("activo", 1)),
            bool(data.get("destacado", 0))
        )

        cursor.execute(sql, valores)
        conexion.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Servicio agregado correctamente",
            "id": nuevo_id
        }), 201
    except Exception as e:
        return jsonify({"mensaje": f"Error al agregar registro: {str(e)}"}), 500


@app.route("/registros/<int:id>", methods=["PUT"])
def actualizar_registro(id):
    data = request.json

    errores = validar_registro(data)
    if errores:
        return jsonify({"errores": errores}), 400

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            UPDATE registros
            SET nombre = %s, categoria = %s, descripcion = %s,
                precio = %s, activo = %s, destacado = %s
            WHERE id = %s
        """
        valores = (
            data.get("nombre"),
            data.get("categoria"),
            data.get("descripcion"),
            float(data.get("precio", 0)),
            bool(data.get("activo", True)),
            bool(data.get("destacado", False)),
            id
        )

        cursor.execute(sql, valores)
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        conexion.close()

        if filas == 0:
            return jsonify({"mensaje": "Registro no encontrado"}), 404

        return jsonify({"mensaje": "Servicio actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al actualizar registro: {str(e)}"}), 500


@app.route("/registros/<int:id>/desactivar", methods=["PUT"])
def desactivar_registro(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("UPDATE registros SET activo = 0 WHERE id = %s", (id,))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        conexion.close()

        if filas == 0:
            return jsonify({"mensaje": "Registro no encontrado"}), 404

        return jsonify({"mensaje": "Servicio desactivado correctamente"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al desactivar registro: {str(e)}"}), 500


@app.route("/registros/<int:id>", methods=["DELETE"])
def eliminar_registro(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM registros WHERE id = %s", (id,))
        conexion.commit()
        filas = cursor.rowcount
        cursor.close()
        conexion.close()

        if filas == 0:
            return jsonify({"mensaje": "Registro no encontrado"}), 404

        return jsonify({"mensaje": "Servicio eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al eliminar registro: {str(e)}"}), 500




@app.route("/login", methods=["POST"])
def login():
    from datetime import timedelta
    data = request.json

    errores = validar_login(data)
    if errores:
        return jsonify({"errores": errores}), 400

    correo   = data.get("correo")
    password = data.get("password")

    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()
    except Exception as e:
        return jsonify({"mensaje": f"Error de base de datos: {str(e)}"}), 500

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    if not verificar_password(password, usuario["password"]):
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    session.permanent = True
    session["usuario_id"]    = usuario["id"]
    session["nombreUsuario"] = usuario["nombre"]
    session["correo"]        = usuario["correo"]
    session["autenticado"]   = True

    return jsonify({
        "mensaje": "Sesión iniciada correctamente",
        "sesion": {
            "nombreUsuario": usuario["nombre"],
            "correo":        usuario["correo"],
            "autenticado":   True
        }
    }), 200


@app.route("/sesion", methods=["GET"])
def obtener_sesion():
    if session.get("autenticado"):
        return jsonify({
            "nombreUsuario": session.get("nombreUsuario"),
            "correo":        session.get("correo"),
            "autenticado":   True
        }), 200

    return jsonify({
        "nombreUsuario": "Invitado",
        "correo":        None,
        "autenticado":   False
    }), 200


@app.route("/logout", methods=["POST"])
def logout():
    """Cierra la sesión activa."""
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200




@app.route("/contacto", methods=["POST"])
def contacto():
    data = request.json

    errores = validar_contacto(data)
    if errores:
        return jsonify({"errores": errores}), 400

    try:
        enviar_correo_contacto(
            data.get("nombre"),
            data.get("correo"),
            data.get("mensaje")
        )
        return jsonify({
            "mensaje": "Tu mensaje fue enviado correctamente. El equipo de Los Santos Customs te contactará pronto."
        }), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al enviar correo: {str(e)}"}), 500




@app.route("/citas", methods=["POST"])
def agendar_cita():
    data = request.json

    errores = []
    if not data.get("nombre_cliente", "").strip():
        errores.append("El nombre del cliente es obligatorio")
    if not data.get("correo_cliente", "").strip():
        errores.append("El correo del cliente es obligatorio")
    if not data.get("fecha", "").strip():
        errores.append("La fecha es obligatoria")
    if not data.get("hora", "").strip():
        errores.append("La hora es obligatoria")
    if not data.get("servicio", "").strip():
        errores.append("El servicio es obligatorio")

    if errores:
        return jsonify({"errores": errores}), 400

    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO citas (nombre_cliente, correo_cliente, fecha, hora, servicio, notas, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'pendiente')
        """
        valores = (
            data.get("nombre_cliente"),
            data.get("correo_cliente"),
            data.get("fecha"),
            data.get("hora"),
            data.get("servicio"),
            data.get("notas", "")
        )

        cursor.execute(sql, valores)
        conexion.commit()
        nueva_id = cursor.lastrowid
        cursor.close()
        conexion.close()



        try:
            enviar_correo_contacto(
                data.get("nombre_cliente"),
                data.get("correo_cliente"),
                f"Confirmación de cita en AutoFix\n"
                f"Fecha: {data.get('fecha')} a las {data.get('hora')}\n"
                f"Servicio: {data.get('servicio')}\n"
                f"Notas: {data.get('notas', 'Sin notas adicionales')}"
            )
        except Exception:
            pass 

        return jsonify({
            "mensaje": "Cita agendada correctamente. Recibirás una confirmación por correo.",
            "id": nueva_id
        }), 201

    except Exception as e:
        return jsonify({"mensaje": f"Error al agendar cita: {str(e)}"}), 500


@app.route("/citas", methods=["GET"])
def obtener_citas():
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM citas ORDER BY fecha ASC, hora ASC")
        citas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(citas), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al obtener citas: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)