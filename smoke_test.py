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
        database=DB_NAME,
        connect_timeout=10
    )

    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()

    print("✅ DB connected successfully")
    print("✅ Tables found:")
    for table in tables:
        print(table[0])

except Exception as e:
    print("❌ DB ERROR:", e)
    sys.exit(1)

finally:
    if conn:
        conn.close()