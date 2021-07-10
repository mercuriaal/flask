import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
SALT = 'gc48956347g'
conn = psycopg2.connect(DATABASE_URL, sslmode='require')