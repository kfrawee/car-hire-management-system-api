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

