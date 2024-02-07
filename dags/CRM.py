from airflow.decorators import dag, task
from airflow.providers.mysql.hooks.mysql import MySqlHook  
from airflow.providers.redis.hooks.redis import RedisHook
from airflow.providers.redis.operators.redis_publish import RedisPublishOperator

from datetime import datetime, timedelta
import requests
import json

from helpers.db_object import airflow_PI
from models.Company import Company
from models.City import City
from models.User import User

API = 'https://jsonplaceholder.typicode.com/'
db = airflow_PI()

default_arg = {
  'owner':'jmoc',
  'retries':5,
  'retry_delay': timedelta(minutes=2)
}

@dag(
    dag_id='Read_and_load_of_API_to_MySQLDB',
    default_args=default_arg,
    start_date=datetime(2024,1,2),
    schedule_interval='@weekly'
)
def api_load():

  hook = MySqlHook(mysql_conn_id='mysql_connection')    

  @task
  def db_creation():
    hook.run(db.get_sql_command())

  @task
  def cities_table():
    hook.run(airflow_PI.cities_c(db.get_name()))

  @task
  def companies_table():
    hook.run(airflow_PI.companies_c(db.get_name()))

  @task
  def users_table():
    hook.run(airflow_PI.users_c(db.get_name()))

####################################################

  @task
  def Get_API_users(ti):
    res = requests.get(f'{API}/users').json()
    cities = set()
    companies = []
    for x in res:
      cities.add(x['address']['city'])
      companies.append(x['company'])
    
    ti.xcom_push(key='cities_name', value=cities)
    ti.xcom_push(key='companies_name', value=companies)
    ti.xcom_push(key='user_body', value=res)
  
  @task
  def Load_cities_registers(ti):
    cities = ti.xcom_pull(task_ids='Get_API_users',key='cities_name')

    for x in cities:
      city_register = City({'name': x})
      city_register.save()

  @task
  def Load_companies_registers(ti):
    companies = ti.xcom_pull(task_ids='Get_API_users',key='companies_name')

    for x in companies:
      company_register = Company(x)
      company_register.save()

  @task
  def Load_users_registers(ti):
    users = ti.xcom_pull(task_ids='Get_API_users',key='user_body')
    
    for x in users:
      address = f"{x['address']['street']} {x['address']['suite']}"
      city_id = City.findId(x['address']['city'])
      company_id = Company.findId(x['company']['name'])
      
      x['address_str'] = address
      x['city_id'] = city_id
      x['company_id'] = company_id

      user_register = User(x)
      user_register.save()
  
  @task 
  def Load_API_posts():
    res = requests.get(f"{API}/posts").json()
    hook = RedisHook(redis_conn_id='redis_connection').get_conn()
    
    hook.execute_command('SETEX', 'posts',604800, json.dumps({'content':res}))

  ddl_db = db_creation()
  ddl_city = cities_table()
  ddl_company = companies_table()
  ddl_user = users_table()

  users_info = Get_API_users()
  cities = Load_cities_registers() 
  companies = Load_companies_registers()
  users = Load_users_registers()

  post_info = Load_API_posts()
  ddl_db >> [ ddl_city, ddl_company ] >> ddl_user >> users_info >> [cities, companies] >> users >> post_info
  

  


api_dag = api_load()
