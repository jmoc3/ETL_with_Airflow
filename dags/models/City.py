from airflow.providers.mysql.hooks.mysql import MySqlHook  
from airflow.providers.postgres.hooks.postgres import PostgresHook

class City():

  def __init__(self,body):
    self.__name = body['name']

  def save(self):
    hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement = f"INSERT IGNORE INTO airflow_PI.cities(name) VALUES ('{self.__name}');"
    
    hook.run(mysql_statement)

  @staticmethod
  def findId(name):
    hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement=f"SELECT id FROM airflow_PI.cities WHERE name = '{name}';"

    res = hook.get_records(mysql_statement)
    return res[0][0]