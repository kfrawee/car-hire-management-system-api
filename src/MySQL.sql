CREATE TABLE `Vehicle Category` (
  `Category_Id` INT NOT NULL AUTO_INCREMENT,
  `CategoryName` VARCHAR(10),
  `CategoryDescription` VARCHAR(255),
  PRIMARY KEY (`Category_Id`)
);

CREATE TABLE `Vehicle` (
  `Vehicle_Id` INT NOT NULL AUTO_INCREMENT,
  `Category_Id` INT,
  `VehicleName` VARCHAR(50),
  `PricePerDay` FLOAT,
  PRIMARY KEY (`Vehicle_Id`),
  FOREIGN KEY (`Category_Id`) REFERENCES `Vehicle Category`(`Category_Id`)
);

CREATE TABLE `Customer` (
  `Customer_Id` VARCHAR(36) NOT NULL, -- uuid
  `FirstName` VARCHAR(50) NOT NULL,
  `LastName` VARCHAR(50) NOT NULL,
  `CustomerEmail` VARCHAR(50) NOT NULL,
  `CustomerPhone` VARCHAR(11) NOT NULL,
  `CustomerAddress` VARCHAR(255) NOT NULL,
  `CreatedOn` DATETIME DEFAULT NOW(),
  `UpdatedOn` DATETIME DEFAULT NULL,
  PRIMARY KEY (`Customer_Id`)
);

CREATE TABLE `Booking` (
  `Booking_Id` INT NOT NULL AUTO_INCREMENT,
  `Customer_Id ` INT,
  `Vehicle_Id` INT,
  `BookingDate` DATETIME DEFAULT NOW(),
  `HireDate` DATETIME DEFAULT NOW(),
  `ReturnDate` DATETIME,
  PRIMARY KEY (`Booking_Id`),
  FOREIGN KEY (`Customer_Id `) REFERENCES `Customer`(`Customer_Id`)
);

CREATE TABLE `Invoice` (
  `Invoice_Id` INT NOT NULL AUTO_INCREMENT,
  `Customer_Id` INT,
  `Booking_Id` INT,
  `Amount` FLOAT,
  `CreatedOn` DATETIME DEFAULT NOW(),
  `HireDate` DATETIME,
  `RerunDate` DATETIME,
  PRIMARY KEY (`Invoice_Id`),
  FOREIGN KEY (`Customer_Id`) REFERENCES `Customer`(`Customer_Id`)
);

