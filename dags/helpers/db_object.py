class airflow_PI():

  def __init__(self):
    self.__sql_create_command =  """CREATE DATABASE IF NOT EXISTS airflow;"""
    self.__name = 'airflow'

  def get_name(self):
    return self.__name

  def get_sql_command(self):
    return self.__sql_create_command

  def cities_c(self,dbm='MySQL'):

    id_type = 'BIGSERIAL' if dbm == 'postgres' else 'INT AUTO_INCREMENT '

    return f"""
            CREATE TABLE IF NOT EXISTS cities(
              id {id_type} PRIMARY KEY NOT NULL,
              name VARCHAR(25) NOT NULL UNIQUE  
            );

           """

  def companies_c(self,dbm='MySQL'):

    id_type = 'BIGSERIAL' if dbm == 'postgres' else 'INT AUTO_INCREMENT '

    return  f"""
            CREATE TABLE IF NOT EXISTS companies(
              id {id_type} PRIMARY KEY NOT NULL,
              name VARCHAR(25) NOT NULL UNIQUE  ,
              catchPhrase VARCHAR(225) NOT NULL,
              bs VARCHAR(50) NOT NULL 
            );
            """
  
  def users_c(self,dbm='MySQL'):

    id_type = 'BIGSERIAL' if dbm == 'postgres' else 'INT AUTO_INCREMENT '

    return f"""
            CREATE TABLE IF NOT EXISTS users(
              id {id_type} PRIMARY KEY NOT NULL,
              name VARCHAR(25) NOT NULL,
              username VARCHAR(25) NOT NULL,
              email VARCHAR(255) NOT NULL UNIQUE,
              address VARCHAR(50),
              city_id INT,
              zipcode VARCHAR(10),
              latitud VARCHAR(20),
              longitud VARCHAR(20),
              phone VARCHAR(30),
              website VARCHAR(50),
              company_id INT,
              FOREIGN KEY (city_id) REFERENCES cities(id),
              FOREIGN KEY (company_id) REFERENCES companies(id)
            );
            """