-- PESODU SLQ/PROCEDURE 
-- INPUT DESIRED_HIRE_DATE, DESIRED_Category_Id

-- Get `Vehicle_Id` 
-- that matchs: 
--     `DESIRED_Category_Id` 

--     AND 
    
--     NOT IN Booking.State = 1 -- CONFIREMED
--     OR 
--     IN Invoice AND Booking.State = 1 AND Booking.RerunDate <= DESIRED_HIRE_DATE
