-- MySQL dump 10.16  Distrib 10.1.28-MariaDB, for Win32 (AMD64)
--
-- Host: 127.0.0.1    Database: diner
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `ID` varchar(32) NOT NULL,
  `DisplayName` varchar(255) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Phone` varchar(100) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `PostCode` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `ID` varchar(32) NOT NULL,
  `DisplayName` varchar(25) NOT NULL,
  `ContactID` varchar(32) DEFAULT NULL,
  `EmailUpdates` bit(1) NOT NULL DEFAULT b'0',
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `customer_contact_FK` (`ContactID`),
  CONSTRAINT `customer_contact_FK` FOREIGN KEY (`ContactID`) REFERENCES `contact` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dish`
--

DROP TABLE IF EXISTS `dish`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dish` (
  `ID` varchar(32) NOT NULL,
  `DisplayName` varchar(255) NOT NULL,
  `Vegan` bit(1) NOT NULL,
  `Vegetarian` bit(1) NOT NULL,
  `Lowfat` bit(1) NOT NULL,
  `Created` date NOT NULL,
  `LastUsed` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meal`
--

DROP TABLE IF EXISTS `meal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meal` (
  `ID` varchar(32) NOT NULL,
  `DisplayName` varchar(255) NOT NULL,
  `Vegan` bit(1) NOT NULL,
  `Vegetarian` bit(1) NOT NULL,
  `Lowfat` bit(1) NOT NULL,
  `Created` date NOT NULL,
  `LastUsed` date DEFAULT NULL,
  `SideID` varchar(32) DEFAULT NULL,
  `DishID` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `meal_side_FK` (`SideID`),
  KEY `meal_dish_FK` (`DishID`),
  CONSTRAINT `meal_dish_FK` FOREIGN KEY (`DishID`) REFERENCES `dish` (`ID`) ON DELETE SET NULL,
  CONSTRAINT `meal_side_FK` FOREIGN KEY (`SideID`) REFERENCES `side` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `ID` varchar(32) NOT NULL,
  `Date` date NOT NULL,
  `OrderLimit` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu_item`
--

DROP TABLE IF EXISTS `menu_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu_item` (
  `ID` varchar(32) NOT NULL,
  `MenuID` varchar(32) DEFAULT NULL,
  `Placing` int(11) NOT NULL,
  `Price` int(11) NOT NULL,
  `Note` text,
  `MealID` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `menu_item_menu_FK` (`MenuID`),
  KEY `menu_item_meal_FK` (`MealID`),
  CONSTRAINT `menu_item_meal_FK` FOREIGN KEY (`MealID`) REFERENCES `meal` (`ID`) ON DELETE SET NULL,
  CONSTRAINT `menu_item_menu_FK` FOREIGN KEY (`MenuID`) REFERENCES `menu` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `side`
--

DROP TABLE IF EXISTS `side`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `side` (
  `ID` varchar(32) NOT NULL,
  `DisplayName` varchar(255) NOT NULL,
  `Created` date NOT NULL,
  `LastUsed` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'diner'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-04 13:15:17
