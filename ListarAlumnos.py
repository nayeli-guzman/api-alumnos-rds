import boto3
import pymysql
import json
import os

def lambda_handler(event, context):
    secret_name = os.environ['SECRET_NAME']  # ejemplo: rds_mysql_alumnos_user_dev
    region_name = os.environ['AWS_REGION']   # ejemplo: us-east-1

    # Obtener secretos desde Secrets Manager
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        secret_dict = json.loads(get_secret_value_response['SecretString'])

        host = os.environ['DB_HOST']  # nombre DNS del RDS, o puedes guardarlo también como secreto
        user = secret_dict['username']
        password = secret_dict['password']
        database = os.environ['DB_NAME']

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos;")
            results = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": results
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    finally:
        if 'connection' in locals() and connection:
            connection.close()
