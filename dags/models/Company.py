from airflow.providers.mysql.hooks.mysql import MySqlHook  

class Company():

  def __init__(self,body):
    self.__name = body['name'],
    self.__catch_phrase = body['catchPhrase'],
    self.__bs = body['bs']

  def save(self):
    hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement = f"INSERT IGNORE INTO airflow_PI.companies(name, catchPhrase, bs) VALUES ('{self.__name[0]}','{self.__catch_phrase[0]}', '{self.__bs}')"
    
    hook.run(mysql_statement)
  
  @staticmethod
  def findId(name):
    hook = MySqlHook(mysql_conn_id='mysql_connection')
    mysql_statement=f"SELECT id FROM airflow_PI.companies WHERE name = '{name}'"

    res = hook.get_records(mysql_statement)
    return res[0][0]