import psycopg2


def create_connection():
    connection = psycopg2.connect(
        database="meta-elite",
        user="postgres",
        host='localhost',
        password="postgres",
        port=5432)
    return connection



