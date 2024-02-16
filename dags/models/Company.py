from airflow.providers.mysql.hooks.mysql import MySqlHook  
from airflow.providers.postgres.hooks.postgres import PostgresHook


class Company():

  def __init__(self,body):
    self.__name = body['name'],
    self.__catch_phrase = body['catchPhrase'],
    self.__bs = body['bs']

  def save(self):
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement = f"INSERT IGNORE INTO airflow_PI.companies(name, catchPhrase, bs) VALUES ('{self.__name[0]}','{self.__catch_phrase[0]}', '{self.__bs}');"
    
    mysql_hook.run(mysql_statement)

    postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')
    postgres_statement = f"INSERT INTO airflow_PI.companies(name, catchPhrase, bs) VALUES ('{self.__name[0]}','{self.__catch_phrase[0]}', '{self.__bs}') ON CONFLICT DO NOTHING;"
    
    postgres_hook.run(postgres_statement)
  
  @staticmethod
  def findId(name):
    mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement=f"SELECT id FROM airflow_PI.companies WHERE name = '{name}';"

    res = mysql_hook.get_records(mysql_statement)
    return res[0][0]