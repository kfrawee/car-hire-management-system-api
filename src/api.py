import traceback
from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from flask import jsonify, request
from flask_cors import CORS
from marshmallow import ValidationError
from helpers import generate_customer_data
from app import app
from db_config import mysql
from schemas import CreateOrUpdateCustomer

CORS(app)
create_or_update_customer_schema = CreateOrUpdateCustomer()


@app.before_first_request
def create_table():
    try:
        # create customer table
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"""
            -- DROP DATABASE Car_Hire_Management_System; -- reset

            CREATE DATABASE IF NOT EXISTS Car_Hire_Management_System;

            USE `Car_Hire_Management_System`;
 
            CREATE TABLE IF NOT EXISTS `Car_Hire_Management_System`.`Customer` (
                `Customer_Id` VARCHAR(36) NOT NULL, -- uuid
                `FirstName` VARCHAR(50) NOT NULL,
                `LastName` VARCHAR(50) NOT NULL,
                `CustomerEmail` VARCHAR(50) NOT NULL,
                `CustomerPhone` VARCHAR(11) NOT NULL,
                `CustomerAddress` VARCHAR(255) NOT NULL,
                `CreatedOn` DATETIME DEFAULT CURRENT_TIMESTAMP,
                `UpdatedOn` DATETIME NULL,
                PRIMARY KEY (`Customer_Id`)
                );
        """
        )
    except:
        pass


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/customer/", methods=["POST", "GET"])
def customer():
    """Handler for /customer/
    Create a new customer or retrieve all customers
    """
    if request.method.upper() == "POST":
        data = request.get_json() or {}
        try:
            # 1st Validation on body request
            clear_data = create_or_update_customer_schema.load(data)
        except ValidationError as e:
            response_body = {
                "error": {
                    "message": "Invalid request body",
                    "details": e.normalized_messages(),
                }
            }

            response = jsonify(response_body)
            response.status_code = HTTPStatus.BAD_REQUEST
            return response

        customer_id = str(uuid4())
        created_on = datetime.utcnow()
        clear_data.update(customer_id=customer_id, created_on=created_on)

        # GET the values to update the BD

        Customer_Id = clear_data.get("customer_id")
        FirstName = clear_data.get("first_name")
        LastName = clear_data.get("last_name")
        CustomerEmail = clear_data.get("email")
        CustomerPhone = clear_data.get("phone_number")
        CustomerAddress = clear_data.get("address")
        CreatedOn = clear_data.get("created_on")
        UpdatedOn = clear_data.get("updated_on")

        # 2nd validation: either a unique email, or a unique phone number - should be both.
        # I will check for email only
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                f"""SELECT Customer_Id FROM Car_Hire_Management_System.Customer WHERE CustomerEmail = '{CustomerEmail}';"""
            )

            results = cursor.fetchall()
            if results:  # ALREADY EXISTS
                cursor.close()
                existing_customer_id = results[0]
                response_body = {
                    "error": {
                        "message": "Invalid request body",
                        "details": f"This email is already associated with a customer_id: {existing_customer_id[0]}",
                    }
                }
                response = jsonify(response_body)
                response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
                return response

            else:
                # INSERT NEW CUSTOMER
                try:
                    insert_customer = (
                        """INSERT INTO Car_Hire_Management_System.Customer"""
                        """(Customer_Id, FirstName, LastName, CustomerEmail, CustomerPhone, CustomerAddress, CreatedOn, UpdatedOn)"""
                        """VALUES( %s, %s, %s, %s, %s, %s, %s, %s ); """
                    )

                    cursor.execute(
                        insert_customer,
                        (
                            Customer_Id,
                            FirstName,
                            LastName,
                            CustomerEmail,
                            CustomerPhone,
                            CustomerAddress,
                            CreatedOn,
                            UpdatedOn,
                        ),
                    )
                    mysql.connection.commit()

                except Exception as e:
                    cursor.close()

                    response_body = {
                        "error": {
                            "message": "Internal Server Error",
                            "details": {
                                "exception_type": type(e).__name__,
                                "traceback": traceback.format_exc(),
                            },
                        }
                    }

                    response = jsonify(response_body)
                    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    return response

                cursor.close()
                response = jsonify(create_or_update_customer_schema.dump(clear_data))
                response.status_code = HTTPStatus.CREATED
                return response

        except Exception as e:
            cursor.close()
            response_body = {
                "error": {
                    "message": "Internal Server Error",
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc(),
                    },
                }
            }

            response = jsonify(response_body)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response

    else:  # GET - retrieve all customers
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                f"""SELECT Customer_Id, FirstName, LastName, CustomerEmail FROM Car_Hire_Management_System.Customer; """
            )

            results = cursor.fetchall()
            if results:
                cursor.close()
                response_body = {
                    "Count": len(results),
                    "Customers": [
                        generate_customer_data(customer, full=False)
                        for customer in results
                    ],
                }
                response = jsonify(response_body)
                response.status_code = HTTPStatus.OK
                return response

            else:

                cursor.close()
                response_body = {
                    "message": "No customers were found.",
                }
                response = jsonify(response_body)
                response.status_code = HTTPStatus.NOT_FOUND
                return response

        except Exception as e:
            cursor.close()
            response_body = {
                "error": {
                    "message": "Internal Server Error",
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc(),
                    },
                }
            }

            response = jsonify(response_body)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response


@app.route("/customer/<string:customer_id>", methods=["PUT", "GET", "DELETE"])
def a_customer(customer_id):
    """Handles request to /customer/<customer_id>
    Get, Update or Delete a customer"""
    if request.method.upper() == "PUT":
        try:
            cursor = mysql.connection.cursor()
            pass

        except Exception as e:
            cursor.close()
            response_body = {
                "error": {
                    "message": "Internal Server Error",
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc(),
                    },
                }
            }

            response = jsonify(response_body)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
    elif request.method.upper() == "GET":
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                f"""SELECT * FROM Car_Hire_Management_System.Customer WHERE Customer_Id = '{customer_id}';"""
            )

            results = cursor.fetchall()
            if results:

                cursor.close()
                response_body = {"Customer": generate_customer_data(results[0])}

                response = jsonify(response_body)
                response.status_code = HTTPStatus.OK
                return response
            else:
                cursor.close()
                response_body = {
                    "message": f"Customer with id: '{customer_id}' was not found.",
                }
                response = jsonify(response_body)
                response.status_code = HTTPStatus.NOT_FOUND
                return response
        except Exception as e:
            cursor.close()
            response_body = {
                "error": {
                    "message": "Internal Server Error",
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc(),
                    },
                }
            }

            response = jsonify(response_body)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
    else:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                f"""SELECT * FROM Car_Hire_Management_System.Customer WHERE Customer_Id = '{customer_id}';"""
            )

            results = cursor.fetchall()
            if results:
                cursor.execute(
                    f"""DELETE FROM Car_Hire_Management_System.Customer WHERE Customer_Id = '{customer_id}';"""
                )
                mysql.connection.commit()
                cursor.close()

                response = jsonify()
                response.status_code = HTTPStatus.NO_CONTENT
                return response
            else:
                cursor.close()
                response_body = {
                    "message": f"Customer with id: '{customer_id}' was not found.",
                }
                response = jsonify(response_body)
                response.status_code = HTTPStatus.NOT_FOUND
                return response

        except Exception as e:
            cursor.close()
            response_body = {
                "error": {
                    "message": "Internal Server Error",
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc(),
                    },
                }
            }

            response = jsonify(response_body)
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response


if __name__ == "__main__":
    app.run()
