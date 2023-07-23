import mysql.connector

# Credenciais de conexão
host = 'aws.connect.psdb.cloud'
dbname = 'vagas_trabalhos'  # replace with your database name
user = 'mcmo5l1e0qx8ejyff88z'  # replace with your MySQL user
password = 'pscale_pw_NCWzD65Yfk3JO2s0uWphzV8EWY6mQMTx15wJUc9YPSr'  # replace with your MySQL password

# Criando conexão com o banco
def conecta_db():
    conn = mysql.connector.connect(
        host=host,
        database=dbname,
        user=user,
        password=password,

    )
    return conn

# Consulta global
def consulta(sql):
    con = conecta_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    con.close()
    return recset

# Insert global
def inserir_dados(sql, values):
    con = conecta_db()
    cur = con.cursor()
    cur.execute(sql, values)
    con.commit()
    con.close()
