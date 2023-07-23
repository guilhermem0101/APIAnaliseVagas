from flask import Blueprint, jsonify, request, send_file
from app.db import consulta, inserir_dados
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import io
bp = Blueprint('empregos', __name__)
site = "https://www.vagas.com.br"
class Vaga:
    def __init__(self, plataforma, titulo, empresa, descricao, data_publi, link):
        self.plataforma = plataforma
        self.titulo = titulo
        self.empresa = empresa
        self.descricao = descricao
        self.data_publi = data_publi
        self.link = site + link
        
def mineradorNoVagas():
    
    vagas = []

    # URL do arquivo a ser lido
    url = "https://www.vagas.com.br/vagas-de-analista-de-dados-em-sao-paulo?h%5B%5D=30&ordenar_por=mais_recentes"
    
    # Fazer a solicitação HTTP
    response = requests.get(url)
    content = response.content

    # Criar objeto BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")


    dados = soup.find_all(class_="vaga even")
    dados2 = soup.find_all(class_="vaga odd")

    todos_dados = dados + dados2
    


    for elemento in todos_dados:
        
        title=elemento.find(class_="link-detalhes-vaga").text.replace("\n", "")   
        data_publi = elemento.find(class_="data-publicacao").text
        empresa = elemento.find(class_="emprVaga").text.replace("\n", "")
        link = elemento.find(class_="link-detalhes-vaga")['href'] 
        descricao = elemento.find(class_="detalhes").text.replace("\n", "")
                   
        empresa = ' '.join(empresa.split())
        descricao = ' '.join(descricao.split())
        title = ' '.join(title.split())


        if data_publi == 'Hoje':
            data_publi = datetime.now().strftime('%Y-%m-%d')
        elif data_publi == 'Ontem':
            ontem = datetime.now() - timedelta(days=1)
            data_publi = ontem.strftime('%Y-%m-%d')
        elif data_publi.startswith('Há'):
            dias = int(data_publi.split()[1])
            nova_data = datetime.now() - timedelta(days=dias)
            data_publi = nova_data.strftime('%Y-%m-%d')
        else:
            data_publi = datetime.strptime(data_publi, '%d/%m/%Y').strftime('%Y-%m-%d')


        vaga = Vaga("Vagas", title, empresa, descricao, data_publi, link)

        vagas.append(vaga)
        
    return vagas


def mineradorNaGupy():
    
    vagas = []

    # URL do arquivo a ser lido
    url = "https://portal.gupy.io/job-search/term=analista%20de%20dados&state=S%C3%A3o%20Paulo"
    
    # Fazer a solicitação HTTP
    response = requests.get(url)
    content = response.content

    # Criar objeto BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")


    dados = soup.find_all(class_="sc-70b75bd4-0 hojCpd")
    


    for elemento in dados:
        
        title=elemento.find(class_="sc-llJcti bGqDEZ sc-70b75bd4-7 ftHylk").text.replace("\n", "")   
        data_publi = elemento.find(class_="sc-efBctP dpAAMR sc-70b75bd4-4 cpauqG").text
        empresa = elemento.find(class_="sc-efBctP dpAAMR sc-70b75bd4-5 dCVCel").text.replace("\n", "")
        link = elemento.find(class_="sc-70b75bd4-1 blwed")['href'] 
        descricao = ' '
                   
        empresa = ' '.join(empresa.split())       
        title = ' '.join(title.split())


        if data_publi == 'Hoje':
            data_publi = datetime.now().strftime('%Y-%m-%d')
        elif data_publi == 'Ontem':
            ontem = datetime.now() - timedelta(days=1)
            data_publi = ontem.strftime('%Y-%m-%d')
        elif data_publi.startswith('Há'):
            dias = int(data_publi.split()[1])
            nova_data = datetime.now() - timedelta(days=dias)
            data_publi = nova_data.strftime('%Y-%m-%d')
        else:
            data_publi = datetime.strptime(data_publi, '%d/%m/%Y').strftime('%Y-%m-%d')


        vaga = Vaga("Vagas", title, empresa, descricao, data_publi, link)

        vagas.append(vaga)
        
    return vagas






@bp.route('/minerar-vagas', methods=['POST'])
def insert_vaagas():
              
    data = mineradorNoVagas()  # Obtém os dados enviados na solicitação POST
    
    for item in data:  
        
        sql = "INSERT INTO vagas_contrato ( data_publi, plataforma, link, empresa, titulo) VALUES (%s, %s, %s, %s, %s)"
        values = (item.data_publi, item.plataforma, item.link, item.empresa, item.titulo)
        inserir_dados(sql, values)

    return jsonify({'message': 'Dados inseridos com sucesso!'}), 201




@bp.route('/vagas-de-emprego', methods=['GET'])
def get_vagas():
    sql = "SELECT * FROM vagas_contrato"  
    eixos_data = consulta(sql)
    return jsonify(eixos_data)


@bp.route('/vagas-por-dia', methods=['GET'])
def get_vagasQTDByDia():
    sql = "SELECT COUNT(idvaga) as n_vagas, data_publi  FROM vagas_contrato GROUP BY data_publi ORDER BY data_publi;"  
    vagas_data = consulta(sql)
    df = pd.DataFrame(vagas_data, columns=['n_vagas', 'date'])
    
    # generate plot
    df.plot(kind='bar', x='date', y='n_vagas')

    # Save the plot in a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Return the image directly as a response
    return send_file(img_buffer, mimetype='image/png')



@bp.route('/minerar-vagas-teste', methods=['POST'])
def insert_vaagasTeste():
    data = mineradorNoVagas()  # Obtém os dados enviados na solicitação POST

    # Converter a lista de objetos Vaga em uma lista de dicionários
    vagas_serializadas = []
    for vaga in data:
        vaga_dict = {
            'plataforma': vaga.plataforma,
            'titulo': vaga.titulo,
            'empresa': vaga.empresa,
            'descricao': vaga.descricao,
            'data_publi': vaga.data_publi,
            'link': vaga.link
        }
        vagas_serializadas.append(vaga_dict)

    return jsonify(vagas_serializadas)


@bp.route('/minerar-gupy-teste', methods=['POST'])
def insert_gupyTeste():
    data = mineradorNaGupy()  # Obtém os dados enviados na solicitação POST

    # Converter a lista de objetos Vaga em uma lista de dicionários
    vagas_serializadas = []
    for vaga in data:
        vaga_dict = {
            'plataforma': vaga.plataforma,
            'titulo': vaga.titulo,
            'empresa': vaga.empresa,
            'descricao': vaga.descricao,
            'data_publi': vaga.data_publi,
            'link': vaga.link
        }
        vagas_serializadas.append(vaga_dict)

    return jsonify(vagas_serializadas)