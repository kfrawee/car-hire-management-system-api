CREATE TABLE IF NOT EXISTS `Car_Hire_Management_System`.`Booking` (
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


DELIMITER //
CREATE TRIGGER before_insert_booking BEFORE INSERT ON Booking
FOR EACH ROW
BEGIN
-- Validate ReturnDate <= HireDate + 7 days
   if NEW.ReturnDate > DATE_ADD(NEW.HireDate, INTERVAL 6 DAY)  then
   SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid ReturnDate. Customer cannot hire a car for longer than a week';
  end if;
--Validate BookingDate <= HireDate + 7 
   if NEW.HireDate > DATE_ADD(NEW.BookingDate, INTERVAL 6 DAY)  then
   SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid HireDate. Booking can only 7 days in advance depending on availability.';
  end if;
END//


DELIMITER //
CREATE TRIGGER post_confirmation AFTER UPDATE ON Booking
FOR EACH ROW
BEGIN
   -- Create new invoice
   if NEW.State = 1 then

    INSERT INTO Invoice (Customer_Id, Booking_Id, Amount, CreatedOn)
    VALUES (NEW.Customer_Id, NEW.Booking_Id, (SELECT PricePerDay FROM Vehicle WHERE Vehicle.Vehicle_Id = NEW.Vehicle_Id), NOW());
    
    UPDATE Booking SET Invoice_id=LAST_INSERT_ID() WHERE Booking_Id=NEW.new_invoice_id;
  	
    -- email confirmation letter
  	if NEW.BookingDate < NEW.HireDate then
    INSERT INTO Email(email, body) 
    VALUES ((SELECT CustomerEmail from Customer where Customer_Id = NEW.Customer_Id),'SOME CONFIRMATION LETTER WITH DATA');
  	end if;
  	
  end if;

END//