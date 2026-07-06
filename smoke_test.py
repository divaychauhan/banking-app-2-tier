import os
import sys
import boto3
import pymysql

client = boto3.client("ssm", region_name="us-east-1")

params = {}

response = client.get_parameters_by_path(
    Path="/application/banking",
    WithDecryption=True,
    Recursive=True
)

for p in response["Parameters"]:
    key = os.path.basename(p["Name"])
    value = p["Value"].strip()
    params[key] = value

required = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT"]

missing = [k for k in required if k not in params]

for k in required:
    if k in params:
        print(k, "✅")
    else:
        print(k, "❌")

if missing:
    print(f"Failed: Missing parameters {missing}")
    sys.exit(1)

print("DB_HOST:", repr(params["DB_HOST"]))
print("DB_NAME:", params["DB_NAME"])
print("DB_USER:", params["DB_USER"])
print("DB_PORT:", params["DB_PORT"])

try:
    connection = pymysql.connect(
        host=params["DB_HOST"],
        user=params["DB_USER"],
        password=params["DB_PASSWORD"],
        database=params["DB_NAME"],
        port=int(params["DB_PORT"]),
        connect_timeout=10
    )

    cur = connection.cursor()
    cur.execute("SHOW TABLES")

    tables = [row[0] for row in cur.fetchall()]

    connection.close()

    print("Database:", params["DB_NAME"])
    print("Tables:", tables)

except Exception as e:
    print("DB ERROR ❌:", e)
    sys.exit(1)

print("✅ Smoke test Done")