BEGIN;

-- =========================
-- 1. Alumnos
-- =========================
INSERT INTO alumno (nombre, apellidos, email, id_tarjeta)
VALUES
('Juan', 'Pérez', 'juan.perez@example.com', '73BAE212'),
('María', 'García', 'maria.garcia@example.com', 'B30E361C'),
('Carlos', 'López', 'carlos.lopez@example.com', 'A1B2C3D4'),
('Pedro', 'Ramírez', 'pedro.ramirez@example.com', 'Z1B2C3B0'),
('Lucía', 'Morales', 'lucia.morales@example.com', 'E1B443U4');


-- =========================
-- 2. Trabajadores
-- =========================
INSERT INTO trabajador (nombre, apellidos, email, rol_personal, id_tarjeta)
VALUES
('Ana', 'Martínez', 'ana.martinez@example.com', 'profesor', '63D7CD11'),
('Luis', 'Fernández', 'luis.fernandez@example.com', 'personalAux', 'D4E5F6G7');

-- =========================
-- 3. Profesor y Personal Auxiliar
-- =========================
INSERT INTO profesor (id_profesor) VALUES (1);
INSERT INTO personalAux (id_personal_aux) VALUES (2);

-- =========================
-- 4. Clase
-- =========================
INSERT INTO clase (id_clase, nombre, descripcion, id_profesor)
VALUES ('G5', 'Gestión Empresarial', 'Clase de gestión de empresas', 1);

-- =========================
-- 5. Horario
-- =========================
INSERT INTO horario (fecha, hora, aula, id_clase) VALUES
('2025-12-02', '18:00:00', 'Aula 101', 'G5'),
('2025-12-03', '18:00:00', 'Aula 101', 'G5'),
('2025-12-04', '18:00:00', 'Aula 101', 'G5'),
('2025-12-09', '18:00:00', 'Aula 101', 'G5'),
('2025-12-10', '18:00:00', 'Aula 101', 'G5'),
('2025-12-11', '18:00:00', 'Aula 101', 'G5'),
('2025-12-16', '18:00:00', 'Aula 101', 'G5'),
('2025-12-17', '18:00:00', 'Aula 101', 'G5'),
('2025-12-18', '18:00:00', 'Aula 101', 'G5');

INSERT INTO horario (fecha, hora, aula, id_clase) VALUES
('2026-01-06', '18:00:00', 'Aula 101', 'G5'),
('2026-01-07', '18:00:00', 'Aula 101', 'G5'),
('2026-01-08', '18:00:00', 'Aula 101', 'G5'),
('2026-01-13', '18:00:00', 'Aula 101', 'G5'),
('2026-01-14', '18:00:00', 'Aula 101', 'G5'),
('2026-01-15', '18:00:00', 'Aula 101', 'G5'),
('2026-01-20', '18:00:00', 'Aula 101', 'G5'),
('2026-01-21', '18:00:00', 'Aula 101', 'G5'),
('2026-01-22', '18:00:00', 'Aula 101', 'G5'),
('2026-01-27', '18:00:00', 'Aula 101', 'G5'),
('2026-01-28', '18:00:00', 'Aula 101', 'G5'),
('2026-01-29', '18:00:00', 'Aula 101', 'G5');