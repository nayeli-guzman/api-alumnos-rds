import boto3
import pymysql
import os
import json


def lambda_handler(event, context):
    # Parámetros de conexión (puedes usar Parameter Store o Secrets Manager para mayor seguridad)
    SSM_host = os.environ['DB_HOST']
    user = os.environ['DB_USER']
    SSM_password = os.environ['DB_PASSWORD']
    database = os.environ['DB_NAME']
    secret_name = "rds_mysql_alumnos_user_" + database
    region_name = 'us-east-1'

    # Recuperar los secretos
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(get_secret_value_response['SecretString'])

    user = secret['username']
    password = secret['password']
    host = "alumnos.cdqnwdkgx7px.us-east-1.rds.amazonaws.com"

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos;")  # Ajusta el nombre de la tabla según tu caso
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
        if connection is not None:
            connection.close()