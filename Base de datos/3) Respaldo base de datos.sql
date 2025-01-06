-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: tiro_con_arco
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `arco`
--

DROP TABLE IF EXISTS `arco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arco` (
  `PK_ID_Arco` int NOT NULL AUTO_INCREMENT,
  `Tipo_Arco` varchar(50) NOT NULL,
  `Marca` varchar(50) NOT NULL,
  `Modelo` varchar(50) NOT NULL,
  `Peso_Arco` decimal(5,2) DEFAULT NULL,
  `Libraje` decimal(5,2) DEFAULT NULL,
  `Longitud_Arco` decimal(5,2) DEFAULT NULL,
  `Material_Arco` varchar(50) DEFAULT NULL,
  `Ano_Fabricacion` year DEFAULT NULL,
  `Numero_Serie` varchar(100) DEFAULT NULL,
  `Estado_Arco` varchar(20) NOT NULL,
  `Accesorios_Incluidos` varchar(250) DEFAULT NULL,
  `Fecha_Compra` date DEFAULT NULL,
  `Propietario_Actual` varchar(100) DEFAULT NULL,
  `Historial_Mantenimiento` varchar(500) DEFAULT NULL,
  `Uso_Actual` varchar(50) DEFAULT NULL,
  `Comentarios_Adicionales` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`PK_ID_Arco`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arco`
--

LOCK TABLES `arco` WRITE;
/*!40000 ALTER TABLE `arco` DISABLE KEYS */;
/*!40000 ALTER TABLE `arco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `atleta`
--

DROP TABLE IF EXISTS `atleta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atleta` (
  `PK_ID_Atleta` int NOT NULL AUTO_INCREMENT,
  `Primer_Nombre` varchar(50) NOT NULL,
  `Segundo_Nombre` varchar(50) DEFAULT NULL,
  `Primer_Apellido` varchar(50) NOT NULL,
  `Segundo_Apellido` varchar(50) NOT NULL,
  `FK_Unidad_Academica` varchar(50) NOT NULL,
  `Correo_Electronico` varchar(100) NOT NULL,
  `Numero_Telefono` varchar(10) NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `FK_ID_Arco` int NOT NULL,
  `FK_Entrenador_Cargo` int NOT NULL,
  PRIMARY KEY (`PK_ID_Atleta`),
  KEY `FK_Unidad_Academica` (`FK_Unidad_Academica`),
  KEY `FK_ID_Arco` (`FK_ID_Arco`),
  KEY `FK_Entrenador_Cargo` (`FK_Entrenador_Cargo`),
  CONSTRAINT `atleta_ibfk_1` FOREIGN KEY (`FK_Unidad_Academica`) REFERENCES `unidad_academica` (`PK_Iniciales_Unidad`),
  CONSTRAINT `atleta_ibfk_2` FOREIGN KEY (`FK_ID_Arco`) REFERENCES `arco` (`PK_ID_Arco`),
  CONSTRAINT `atleta_ibfk_3` FOREIGN KEY (`FK_Entrenador_Cargo`) REFERENCES `entrenador` (`PK_ID_Entrenador`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atleta`
--

LOCK TABLES `atleta` WRITE;
/*!40000 ALTER TABLE `atleta` DISABLE KEYS */;
/*!40000 ALTER TABLE `atleta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disparo`
--

DROP TABLE IF EXISTS `disparo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disparo` (
  `FK_ID_Entrenamiento` int NOT NULL,
  `PK_ID_Disparo` int NOT NULL,
  `Serie` int DEFAULT NULL,
  `Tanda` int DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Puntos` varchar(10) DEFAULT NULL,
  `Equivalencia` int DEFAULT NULL,
  `Acumulado` int DEFAULT NULL,
  `X` decimal(20,18) DEFAULT NULL,
  `Y` decimal(20,18) DEFAULT NULL,
  PRIMARY KEY (`FK_ID_Entrenamiento`,`PK_ID_Disparo`),
  CONSTRAINT `disparo_ibfk_1` FOREIGN KEY (`FK_ID_Entrenamiento`) REFERENCES `entrenamientos` (`PK_ID_Entrenamiento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disparo`
--

LOCK TABLES `disparo` WRITE;
/*!40000 ALTER TABLE `disparo` DISABLE KEYS */;
/*!40000 ALTER TABLE `disparo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrenador`
--

DROP TABLE IF EXISTS `entrenador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrenador` (
  `PK_ID_Entrenador` int NOT NULL AUTO_INCREMENT,
  `Primer_Nombre` varchar(50) NOT NULL,
  `Segundo_Nombre` varchar(50) DEFAULT NULL,
  `Primer_Apellido` varchar(50) NOT NULL,
  `Segundo_Apellido` varchar(50) NOT NULL,
  `Correo_Electronico` varchar(100) NOT NULL,
  `Numero_Telefono` varchar(10) NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  PRIMARY KEY (`PK_ID_Entrenador`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrenador`
--

LOCK TABLES `entrenador` WRITE;
/*!40000 ALTER TABLE `entrenador` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrenador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrenamientos`
--

DROP TABLE IF EXISTS `entrenamientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrenamientos` (
  `PK_ID_Entrenamiento` int NOT NULL AUTO_INCREMENT,
  `FK_ID_Atleta` int NOT NULL,
  `Titulo` varchar(50) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Serie_estandar` varchar(50) DEFAULT NULL,
  `Interior` varchar(50) DEFAULT NULL,
  `Arco` varchar(50) DEFAULT NULL,
  `Flecha` varchar(50) DEFAULT NULL,
  `Distancia` varchar(20) DEFAULT NULL,
  `Blanco` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`PK_ID_Entrenamiento`),
  KEY `FK_ID_Atleta` (`FK_ID_Atleta`),
  CONSTRAINT `entrenamientos_ibfk_1` FOREIGN KEY (`FK_ID_Atleta`) REFERENCES `atleta` (`PK_ID_Atleta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrenamientos`
--

LOCK TABLES `entrenamientos` WRITE;
/*!40000 ALTER TABLE `entrenamientos` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrenamientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidad_academica`
--

DROP TABLE IF EXISTS `unidad_academica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidad_academica` (
  `PK_Iniciales_Unidad` varchar(50) NOT NULL,
  `Nombre_Unidad` varchar(500) NOT NULL,
  PRIMARY KEY (`PK_Iniciales_Unidad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidad_academica`
--

LOCK TABLES `unidad_academica` WRITE;
/*!40000 ALTER TABLE `unidad_academica` DISABLE KEYS */;
/*!40000 ALTER TABLE `unidad_academica` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-06 12:27:25
