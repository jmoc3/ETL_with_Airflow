from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

class User():

  def __init__(self,body):
    self.__name = body['name'],
    self.__username = body['username'],
    self.__email = body['email'],
    self.__address = body['address_str'],
    self.__city_id = body['city_id'],
    self.__zipcode = body['address']['zipcode'],
    self.__latitud = body['address']['geo']['lat'],
    self.__longitud = body['address']['geo']['lng'],
    self.__phone = body['phone'],
    self.__website = body['website'],
    self.__company_id = body['company_id']
  
  def save(self):
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement = f"INSERT IGNORE INTO airflow_PI.users(name, username, email, address, city_id, zipcode, latitud, longitud, phone, website, company_id) VALUES ('{self.__name[0]}','{self.__username[0]}','{self.__email[0]}','{self.__address[0]}','{self.__city_id[0]}','{self.__zipcode[0]}','{self.__latitud[0]}','{self.__longitud[0]}','{self.__phone[0]}','{self.__website[0]}','{self.__company_id}');"
    
    mysql_hook.run(mysql_statement)

    postgres_hook = PostgresHook(postgres_conn_id = 'postgres_connection')
    postgres_statement = f"INSERT INTO airflow_PI.users (name, username, email, address, city_id, zipcode, latitud, longitud, phone, website, company_id) VALUES ('{self.__name[0]}','{self.__username[0]}','{self.__email[0]}','{self.__address[0]}','{self.__city_id[0]}','{self.__zipcode[0]}','{self.__latitud[0]}','{self.__longitud[0]}','{self.__phone[0]}','{self.__website[0]}','{self.__company_id}') ON CONFLICT (email) DO NOTHING;"

    postgres_hook.run(postgres_statement)


