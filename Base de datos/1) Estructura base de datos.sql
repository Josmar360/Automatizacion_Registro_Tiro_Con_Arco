CREATE SCHEMA Tiro_Con_Arco;

USE Tiro_Con_Arco;

CREATE TABLE Entrenador (
	PK_ID_Entrenador INT AUTO_INCREMENT PRIMARY KEY,
	Primer_Nombre VARCHAR(50) NOT NULL,
	Segundo_Nombre VARCHAR(50) NULL,
    Primer_Apellido VARCHAR(50) NOT NULL,
    Segundo_Apellido VARCHAR(50) NOT NULL,
    Correo_Electronico VARCHAR(100) NOT NULL,
    Numero_Telefono VARCHAR(10) NOT NULL,
    Fecha_Nacimiento DATE NOT NULL
);

CREATE TABLE Unidad_Academica (
	PK_Iniciales_Unidad VARCHAR(50) NOT NULL PRIMARY KEY,
    Nombre_Unidad VARCHAR(500) NOT NULL
);

CREATE TABLE Arco (
    PK_ID_Arco INT AUTO_INCREMENT PRIMARY KEY,
    Tipo_Arco VARCHAR(50) NOT NULL, 
    Marca VARCHAR(50) NOT NULL, 
    Modelo VARCHAR(50) NOT NULL, 
    Peso_Arco DECIMAL(5,2), 
    Libraje DECIMAL(5,2), 
    Longitud_Arco DECIMAL(5,2), 
    Material_Arco VARCHAR(50), 
    Ano_Fabricacion YEAR, 
    Numero_Serie VARCHAR(100), 
    Estado_Arco VARCHAR(20) NOT NULL, 
    Accesorios_Incluidos VARCHAR(250), 
    Fecha_Compra DATE, 
    Propietario_Actual VARCHAR(100), 
    Historial_Mantenimiento VARCHAR(500), 
    Uso_Actual VARCHAR(50), 
    Comentarios_Adicionales VARCHAR(500)
);

CREATE TABLE Atleta (
	PK_ID_Atleta INT AUTO_INCREMENT PRIMARY KEY,
	Primer_Nombre VARCHAR(50) NOT NULL,
	Segundo_Nombre VARCHAR(50) NULL,
    Primer_Apellido VARCHAR(50) NOT NULL,
    Segundo_Apellido VARCHAR(50) NOT NULL,
    FK_Unidad_Academica VARCHAR(50) NOT NULL,
    Correo_Electronico VARCHAR(100) NOT NULL,
    Numero_Telefono VARCHAR(10) NOT NULL,
    Fecha_Nacimiento DATE NOT NULL,
    FK_ID_Arco INT NOT NULL,
    FK_Entrenador_Cargo INT NOT NULL,
    FOREIGN KEY (FK_Unidad_Academica) REFERENCES Unidad_Academica(PK_Iniciales_Unidad),
    FOREIGN KEY (FK_ID_Arco) REFERENCES Arco(PK_ID_Arco),
    FOREIGN KEY (FK_Entrenador_Cargo) REFERENCES Entrenador(PK_ID_Entrenador)
);

CREATE TABLE Entrenamientos (
    PK_ID_Entrenamiento INT AUTO_INCREMENT PRIMARY KEY,
    FK_ID_Atleta INT NOT NULL,
    Titulo VARCHAR(50),
    Fecha DATE,
    Serie_estandar VARCHAR(50),
    Interior VARCHAR(50),
    Arco VARCHAR(50),
    Flecha VARCHAR(50),
    Distancia VARCHAR(20),
    Blanco VARCHAR(50),
    FOREIGN KEY (FK_ID_Atleta) REFERENCES Atleta(PK_ID_Atleta)
);

CREATE TABLE Disparo (
	FK_ID_Entrenamiento INT,
    PK_ID_Disparo INT,
    Serie INT,
    Tanda INT,
    Hora TIME,
    Puntos VARCHAR(10),
    Equivalencia INT,
    Acumulado INT,
    X DECIMAL(20, 18),
    Y DECIMAL(20, 18),
	PRIMARY KEY (FK_ID_Entrenamiento, PK_ID_Disparo),
    FOREIGN KEY (FK_ID_Entrenamiento) REFERENCES Entrenamientos(PK_ID_Entrenamiento)
);