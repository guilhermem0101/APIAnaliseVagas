from flask import Blueprint, jsonify, request
from app.db import consulta, inserir_dados

bp = Blueprint('eixos', __name__)

@bp.route('/eixos', methods=['GET'])
def get_eixos():
    sql = "SELECT * FROM eixos"  # replace with your actual SQL query
    eixos_data = consulta(sql)
    return jsonify(eixos_data)



@bp.route('/eixosn', methods=['POST'])
def insert_eixo():
    # data = request.get_json()  # Obtém os dados enviados na solicitação POST
    ideixos = 4
    nome = "Emprego"
    carga_horaria = 40
    
    # Constrói o comando SQL para inserir os dados na tabela
    sql = "INSERT INTO eixos (ideixos, nome, carga_horaria) VALUES (%s, %s, %s)"
    values = (ideixos, nome, carga_horaria)
    inserir_dados(sql, values)

    return jsonify({'message': 'Dados inseridos com sucesso!'}), 201