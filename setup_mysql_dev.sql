-- A script that prepares mysql server for the AirBnB_clone_v2 project

-- Creates database if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creates new user if user does not exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the database to the user above
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on the database peprformance_schema
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';

-- Grant USAGE privilege on all databases
GRANT USAGE ON *.* TO 'hbnb_dev'@'localhost';
