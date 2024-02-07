class airflow_PI():

  def __init__(self):
    self.__sql_create_command =  """CREATE DATABASE IF NOT EXISTS airflow_PI"""
    self.__name = 'airflow_PI'

  def get_name(self):
    return self.__name

  def get_sql_command(self):
    return self.__sql_create_command

  @staticmethod
  def cities_c(db):
    return f"""
            CREATE TABLE IF NOT EXISTS {db}.cities(
              id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
              name VARCHAR(25) NOT NULL UNIQUE  
            )

           """

  @staticmethod
  def companies_c(db):
    return  f"""
            CREATE TABLE IF NOT EXISTS {db}.companies(
              id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
              name VARCHAR(25) NOT NULL UNIQUE  ,
              catchPhrase VARCHAR(225) NOT NULL,
              bs VARCHAR(50) NOT NULL 
            )
            """
  
  @staticmethod
  def users_c(db):
    return f"""
            CREATE TABLE IF NOT EXISTS {db}.users(
              id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
              name VARCHAR(25) NOT NULL,
              username VARCHAR(25) NOT NULL,
              email VARCHAR(255) NOT NULL UNIQUE,
              address VARCHAR(50),
              city_id INT,
              zipcode VARCHAR(10),
              latitud VARCHAR(20),
              longitud VARCHAR(20),
              phone VARCHAR(15),
              website VARCHAR(50),
              company_id INT,
              FOREIGN KEY (city_id) REFERENCES cities(id),
              FOREIGN KEY (company_id) REFERENCES companies(id)
            )
            """