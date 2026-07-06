import os
import sys
import boto3
import pymysql

client = boto3.client("ssm", region_name="us-east-1")


def get_param(name):
    return client.get_parameter(
        Name=f"/application/banking/{name}",
        WithDecryption=True
    )["Parameter"]["Value"].strip()


conn = None

try:
    DB_HOST = get_param("DB_HOST")
    DB_PORT = int(get_param("DB_PORT"))
    DB_USER = get_param("DB_USER")
    DB_PASSWORD = get_param("DB_PASSWORD")
    DB_NAME = get_param("DB_NAME")

    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=10
    )

    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    cur.execute(f"USE `{DB_NAME}`")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(base_dir, "init.sql")

    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            cur.execute(statement)

    conn.commit()

    print(f"✅ Database `{DB_NAME}` created/initialized successfully")

except Exception as e:
    print("❌ Database init error:", e)
    sys.exit(1)

finally:
    if conn:
        conn.close()