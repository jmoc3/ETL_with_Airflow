from airflow.providers.mysql.hooks.mysql import MySqlHook  
from airflow.providers.postgres.hooks.postgres import PostgresHook

class City():

  def __init__(self,body):
    self.__name = body['name']

  def save(self):
    hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement = f"INSERT IGNORE INTO cities(name) VALUES ('{self.__name}');"
    
    hook.run(mysql_statement)
  
    postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')
    postgres_statement = f"INSERT INTO cities(name) VALUES ('{self.__name}') ON CONFLICT DO NOTHING;"
    
    postgres_hook.run(postgres_statement)
  

  @staticmethod
  def findId(name):
    hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement=f"SELECT id FROM cities WHERE name = '{name}';"

    res = hook.get_records(mysql_statement)
    return res[0][0]