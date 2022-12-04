CREATE DATABASE IF NOT EXISTS Car_Hire_Management_System;

USE `Car_Hire_Management_System`;

CREATE TABLE `Car_Hire_Management_System`.`Vehicle Category` (
  `Category_Id` INT NOT NULL AUTO_INCREMENT,
  `CategoryName` VARCHAR(10),
  `CategoryDescription` VARCHAR(255),
  PRIMARY KEY (`Category_Id`)
);

CREATE TABLE `Car_Hire_Management_System`.`Vehicle` (
  `Vehicle_Id` INT NOT NULL AUTO_INCREMENT,
  `Category_Id` INT,
  `VehicleName` VARCHAR(50),
  `PricePerDay` FLOAT,
  PRIMARY KEY (`Vehicle_Id`),
  FOREIGN KEY (`Category_Id`) REFERENCES `Vehicle Category`(`Category_Id`)
);

CREATE TABLE `Car_Hire_Management_System`.`Customer` (
  `Customer_Id` VARCHAR(36) NOT NULL, -- uuid
  `FirstName` VARCHAR(50) NOT NULL,
  `LastName` VARCHAR(50) NOT NULL,
  `CustomerEmail` VARCHAR(50) NOT NULL,
  `CustomerPhone` VARCHAR(11) NOT NULL,
  `CustomerAddress` VARCHAR(255) NOT NULL,
  `CreatedOn` DATETIME DEFAULT NOW() NOT NULL,
  `UpdatedOn` DATETIME DEFAULT NULL,
  PRIMARY KEY (`Customer_Id`)
);

CREATE TABLE `Car_Hire_Management_System`.`Booking` (
  `Booking_Id` INT NOT NULL AUTO_INCREMENT,
  `Customer_Id ` INT,
  `Vehicle_Id` INT,
  `State` INT NOT NULL DEFAULT 0 CHECK (State IN (0, 1)), 
  `BookingDate` DATETIME DEFAULT NOW(),
  `HireDate` DATETIME DEFAULT NOW(),
  `ReturnDate` DATETIME,
  PRIMARY KEY (`Booking_Id`),
  FOREIGN KEY (`Customer_Id `) REFERENCES `Customer`(`Customer_Id`),
  FOREIGN KEY (`Vehicle_Id`) REFERENCES `Vehicle`(`Vehicle_Id`)

);

CREATE TABLE `Car_Hire_Management_System`.`Invoice` (
  `Invoice_Id` INT NOT NULL AUTO_INCREMENT,
  `Customer_Id` INT,
  `Booking_Id` INT,
  `Amount` FLOAT,
  `CreatedOn` DATETIME DEFAULT NOW(),
  PRIMARY KEY (`Invoice_Id`),
  FOREIGN KEY (`Customer_Id`) REFERENCES `Customer`(`Customer_Id`),
  FOREIGN KEY (`Booking_Id`) REFERENCES `Booking`(`Booking_Id`),
);

CREATE TABLE IF NOT EXISTS `Car_Hire_Management_System`.`Email`(
  `Email_Id` int AUTO_INCREMENT NOT NULL,
	`CustomerEmail` varchar(25) NOT NULL,
	`EmailBody` varchar(300) NOT NULL, 
	`CreatedOn` datetime DEFAULT NOW(), 
	PRIMARY KEY (Email_Id));
	PRIMARY KEY (Email_Id));
