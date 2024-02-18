from airflow.decorators import dag, task
from airflow.providers.mysql.hooks.mysql import MySqlHook  
from airflow.providers.redis.hooks.redis import RedisHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
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
    dag_id='ETL_From_an_API_to_MySQL_Postgres_and_Redis',
    default_args=default_arg,
    start_date=datetime(2024,1,2),
    schedule_interval='@weekly'
)
def api_load():

  mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')    
  postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')
  @task
  def db_creation():
    mysql_hook.run(db.get_sql_command())

  @task
  def cities_table_creation():
    mysql_hook.run(db.cities_c())
    postgres_hook.run(db.cities_c('postgres'))

  @task
  def companies_table_creation():
    mysql_hook.run(db.companies_c())
    postgres_hook.run(db.companies_c('postgres'))

  @task
  def users_table_creation():
    mysql_hook.run(db.users_c())
    postgres_hook.run(db.users_c('postgres'))

####################################################

  @task
  def getting_user_data_from_the_API(ti):
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
  def load_cities_to_MySQL_and_Postgres(ti):
    cities = ti.xcom_pull(task_ids='getting_user_data_from_the_API',key='cities_name')
    for x in cities:
      city_register = City({'name': x})
      city_register.save()

  @task
  def load_companies_to_MySQL_and_Postgres(ti):
    companies = ti.xcom_pull(task_ids='getting_user_data_from_the_API',key='companies_name')

    for x in companies:
      company_register = Company(x)
      company_register.save()

  @task
  def load_users_to_MySQL_and_Postgres(ti):
    users = ti.xcom_pull(task_ids='getting_user_data_from_the_API',key='user_body')
    
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
  def load_user_posts_to_Redis():
    res = requests.get(f"{API}/posts").json()
    hook = RedisHook(redis_conn_id='redis_connection').get_conn()
    
    hook.execute_command('SETEX', 'posts',604800, json.dumps({'content':res}))

  ddl_city = cities_table_creation()
  ddl_company = companies_table_creation()
  ddl_user = users_table_creation()

  users_info = getting_user_data_from_the_API()
  cities = load_cities_to_MySQL_and_Postgres() 
  companies = load_companies_to_MySQL_and_Postgres()
  users = load_users_to_MySQL_and_Postgres()

  post_info = load_user_posts_to_Redis()
  
  [ ddl_city, ddl_company ] >> ddl_user >> users_info >> [cities, companies] >> users >> post_info
  

  


api_dag = api_load()
