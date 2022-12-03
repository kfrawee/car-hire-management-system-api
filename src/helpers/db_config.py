from flask_mysqldb import MySQL

from app import app


# configurations
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "dev_password"
app.config["MYSQL_DATABASE_DB"] = "Car_Hire_Management_System"
app.config["MYSQL_HOST"] = "localhost"

mysql = MySQL(app)
