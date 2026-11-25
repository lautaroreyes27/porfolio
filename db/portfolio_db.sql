DROP DATABASE IF EXISTS portfolio;
CREATE DATABASE portfolio
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE portfolio;

CREATE TABLE usuario (
    id_usuario     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(50)  NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    creado_en      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE persona (
    id_persona  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario  INT UNSIGNED NOT NULL UNIQUE,
    nombre      VARCHAR(60)  NOT NULL,
    apellido    VARCHAR(60)  NOT NULL,
    titulo      VARCHAR(100) NOT NULL,
    resumen     TEXT,
    objetivo    TEXT,
    email       VARCHAR(120) NOT NULL,
    telefono    VARCHAR(30),
    ciudad      VARCHAR(80),
    foto        VARCHAR(255),
    cv_pdf      VARCHAR(255),
    CONSTRAINT fk_persona_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE educacion (
    id_educacion  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_persona    INT UNSIGNED NOT NULL,
    institucion   VARCHAR(120) NOT NULL,
    titulo        VARCHAR(120),
    nivel         ENUM('inicial','primario','secundario','terciario',
                       'universitario','curso') NOT NULL,
    fecha_inicio  YEAR NOT NULL,
    fecha_fin     YEAR NULL,
    descripcion   TEXT,
    CONSTRAINT fk_educacion_persona
        FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
        ON DELETE CASCADE,
    CONSTRAINT chk_educacion_fechas
        CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
) ENGINE=InnoDB;

CREATE TABLE experiencia (
    id_experiencia  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_persona      INT UNSIGNED NOT NULL,
    puesto          VARCHAR(100) NOT NULL,
    empresa         VARCHAR(100) NOT NULL,
    fecha_inicio    DATE NOT NULL,
    fecha_fin       DATE NULL,
    descripcion     TEXT,
    CONSTRAINT fk_experiencia_persona
        FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
        ON DELETE CASCADE,
    CONSTRAINT chk_experiencia_fechas
        CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
) ENGINE=InnoDB;

CREATE TABLE categoria_tecnologia (
    id_categoria  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(60) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE tecnologia (
    id_tecnologia  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_categoria   INT UNSIGNED NOT NULL,
    nombre         VARCHAR(60)  NOT NULL UNIQUE,
    icono          VARCHAR(80),   
    CONSTRAINT fk_tecnologia_categoria
        FOREIGN KEY (id_categoria) REFERENCES categoria_tecnologia(id_categoria)
) ENGINE=InnoDB;

CREATE TABLE persona_tecnologia (
    id_persona     INT UNSIGNED NOT NULL,
    id_tecnologia  INT UNSIGNED NOT NULL,
    nivel          TINYINT UNSIGNED NOT NULL DEFAULT 50,  
    PRIMARY KEY (id_persona, id_tecnologia),
    CONSTRAINT fk_pt_persona
        FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
        ON DELETE CASCADE,
    CONSTRAINT fk_pt_tecnologia
        FOREIGN KEY (id_tecnologia) REFERENCES tecnologia(id_tecnologia)
        ON DELETE CASCADE,
    CONSTRAINT chk_pt_nivel CHECK (nivel BETWEEN 0 AND 100)
) ENGINE=InnoDB;

CREATE TABLE habilidad_blanda (
    id_habilidad  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_persona    INT UNSIGNED NOT NULL,
    descripcion   VARCHAR(150) NOT NULL,
    CONSTRAINT fk_habilidad_persona
        FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE proyecto (
    id_proyecto  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_persona   INT UNSIGNED NOT NULL,
    titulo       VARCHAR(120) NOT NULL,
    descripcion  TEXT,
    url_repo     VARCHAR(255),
    url_demo     VARCHAR(255),
    imagen       VARCHAR(255),
    CONSTRAINT fk_proyecto_persona
        FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE proyecto_tecnologia (
    id_proyecto    INT UNSIGNED NOT NULL,
    id_tecnologia  INT UNSIGNED NOT NULL,
    PRIMARY KEY (id_proyecto, id_tecnologia),
    CONSTRAINT fk_prt_proyecto
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto)
        ON DELETE CASCADE,
    CONSTRAINT fk_prt_tecnologia
        FOREIGN KEY (id_tecnologia) REFERENCES tecnologia(id_tecnologia)
        ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO categoria_tecnologia (nombre) VALUES
    ('Lenguajes'),
    ('Frameworks y librerías'),
    ('Bases de datos'),
    ('Herramientas');

INSERT INTO tecnologia (id_categoria, nombre, icono) VALUES
    (1, 'Python',     'fa-brands fa-python'),
    (1, 'HTML',       'fa-brands fa-html5'),
    (1, 'CSS',        'fa-brands fa-css3-alt'),
    (1, 'JavaScript', 'fa-brands fa-js'),
    (2, 'Flask',      'fa-solid fa-flask'),
    (2, 'React',      'fa-brands fa-react'),
    (3, 'MySQL',      'fa-solid fa-database'),
    (4, 'Git',        'fa-brands fa-git-alt'),
    (4, 'Figma',      'fa-brands fa-figma'),
    (4, 'Kdenlive',   'fa-solid fa-film');
