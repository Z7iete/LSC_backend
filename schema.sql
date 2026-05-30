
CREATE DATABASE IF NOT EXISTS JCserver;
USE JCserver;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(80) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    destacado BOOLEAN  DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    correo_cliente VARCHAR(120) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    servicio VARCHAR(150) NOT NULL,
    notas TEXT DEFAULT NULL,
    estado ENUM(
        'pendiente',
        'confirmada',
        'en_proceso',
        'completada',
        'cancelada'
        ) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO registros (nombre, categoria, descripcion, precio, activo, destacado) VALUES
('Cambio de aceite y filtro', 'Servicios','Cambio de aceite de motor y filtro de aceite. Incluye revisión de niveles de fluidos.', 350.00, TRUE, TRUE),
('Alineación y balanceo', 'Servicios','Alineación computarizada de las 4 ruedas y balanceo de llantas para mayor estabilidad.',  480.00, TRUE, TRUE),
('Diagnóstico computarizado','Servicios', 'Escaneo electrónico completo del vehículo para detectar fallas en motor y sistemas eléctricos.', 300.00, TRUE, TRUE),
('Cambio de frenos delanteros', 'Servicios', 'Sustitución de pastillas y revisión del sistema de frenos delantero. Incluye revisión de discos.', 650.00, TRUE, FALSE),
('Revisión general preventiva', 'Servicios',   'Revisión de 25 puntos: motor, frenos, suspensión, luces, fluidos y más. Ideal cada 6 meses.',200.00, TRUE, FALSE),
('Cambio de llantas (juego de 4)', 'Productos', 'Suministro e instalación de 4 llantas nuevas. Precio varía según marca y medida del vehículo.', 2800.00, TRUE, TRUE),
('Aceite sintético 5W-30 (1L)','Productos','Aceite de motor sintético de alta calidad para motores modernos. Compatible con gasolina y diesel.', 120.00, TRUE, FALSE),
('Kit de filtros completo','Productos', 'Kit con filtro de aire, aceite y gasolina para mantenimiento preventivo completo del vehículo.', 280.00, TRUE, FALSE),
('Cita de diagnóstico inicial', 'Citas', 'Primera visita al taller para evaluar el estado general del vehículo y presupuestar reparaciones.', 0.00, TRUE, FALSE),
('Cita de servicio express','Citas', 'Cambio de aceite, revisión de llantas y fluidos. Servicio rápido en menos de 45 minutos.',350.00, TRUE, FALSE),
('Batería 12V 45AH','Inventario', 'Batería sellada libre de mantenimiento. Garantía de 18 meses. Compatible con la mayoría de vehículos compactos.', 950.00, TRUE, FALSE),
('Soporte técnico en ruta','Soporte', 'Asistencia mecánica de emergencia en carretera. Disponible en radio de 30 km del taller.', 500.00, TRUE, FALSE);

INSERT INTO citas (nombre_cliente, correo_cliente, fecha, hora, servicio, notas, estado) VALUES
('Diego Audelo', 'AudelosD@gmail.com','2026-06-02', '09:00:00', 'Cambio de aceite y filtro','Vehículo: Honda Civic 2019','pendiente'),
('Paola Inzunza','PaoPao123@hotmail.com','2026-06-03', '11:00:00', 'Alineación y balanceo', 'Vehículo: Toyota Corolla 2021','confirmada'),
('Francisco Mejia','FrancisMe@outlook.com','2026-06-05', '10:30:00', 'Diagnóstico computarizado', 'Luz de check engine encendida', 'pendiente'),
('Arturo Lizarraga', 'LizarragaArturo2003@gmail.com', '2026-06-06', '08:00:00', 'Revisión general preventiva', 'Vehículo: Nissan Versa 2020','confirmada'),
('Leonardo Aguilar','LeoAL@gmail.com','2026-06-10', '15:00:00', 'Cambio de frenos delanteros', 'Vehículo: Volkswagen Jetta 2018', 'pendiente');

-- Existe un usuario: jesciel.cabrales@hotmail.com
-- Contraseña Jesciel123
-- No se puede, aun, acceder a una cuenta con un insert convencional. El flask hashea la contraseña por lo que se escriba en texto
-- plano no va a funcionar porque no van a concordar. Lo que hice es que cree generar_hash para ver el hash del usuario, edite la tabla y puse
-- el hash, permitiendome usar la contraseña normal de texto plano en la aplicacion. Tambien se podrian crear ek usuario directo desde el create_user.py