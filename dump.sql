-- MySQL dump 10.13  Distrib 5.7.23, for Win64 (x86_64)
--
-- Host: localhost    Database: shoppingcart
-- ------------------------------------------------------
-- Server version	5.7.23-log

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
-- Table structure for table `store_order`
--


LOCK TABLES `store_product` WRITE;
/*!40000 ALTER TABLE `store_product` DISABLE KEYS */;
INSERT INTO `store_product` VALUES (1,'Headphones',179.99,0,'headphones.jpg'),(2,'Mount of Olives Book',14.67,0,'book.jpg'),(3,'Project Source Code',19.99,1,'sourcecode.jpg'),(4,'Watch',259,0,'watch.jpg'),(5,'Shoes',89.99,0,'shoes.jpg'),(6,'T-Shirt',25.99,0,'shirt.jpg'),(7,'Iphone 11 Pro Max',890,0,'iphone.jpg'),(8,'AMD Ryzen Processor',385,0,'AMD-Ryzen-5-3600-3rd-Gen-Desktop-Processor-1.jpg'),(9,'Miniso Ear Buds',124,0,'Miniso_Earbuds.jpg');
/*!40000 ALTER TABLE `store_product` ENABLE KEYS */;
UNLOCK TABLES;