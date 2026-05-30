
from db import get_connection
from security import generar_hash


def crear_usuario(nombre, correo, password):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
    existente = cursor.fetchone()

    if existente:
        print(f"Ya existe un usuario con el correo: {correo}")
        cursor.close()
        conexion.close()
        return

    password_hash = generar_hash(password)

    cursor.execute(
        "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)",
        (nombre, correo, password_hash)
    )

    conexion.commit()
    cursor.close()
    conexion.close()
    print(f"✅ Usuario '{nombre}' creado correctamente con correo: {correo}")


if __name__ == "__main__":
    crear_usuario("adminLSC", "LSCadmon@gmail.com", "LCS_1234")