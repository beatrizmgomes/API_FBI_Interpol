from flask import Flask, jsonify, request
import requests
import cx_Oracle

# Substitua os valores abaixo pelos seus próprios
username = "rm96016"
password = "040998"
dsn = "oracle.fiap.com.br:1521/orcl"

try:
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    print("Conexão bem-sucedida ao Oracle Database")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Erro de conexão:", error.message)

# Faça operações no banco de dados usando a conexão
app = Flask(__name__)

# Endpoint para puxar dados do FBI e popula o banco de dados
@app.route('/')
def index():
    return "Bem-vindo à API do FBI e da Interpol"

@app.route('/atualizar-dados', methods=['GET'])
def atualizar_dados():
    try:
        # Faça uma requisição à API do FBI
        fbi_url = "https://api.fbi.gov/wanted/v1/list"
        fbi_response = requests.get(fbi_url)
        fbi_data = fbi_response.json()
        print("Dados do FBI:", fbi_data)

        # Faça uma requisição à API da Interpol
        interpol_url = "https://ws-public.interpol.int/notices/v1/red?resultPerPage=20&page=3"
        interpol_response = requests.get(interpol_url)
        interpol_data = interpol_response.json()
        print("Dados da Interpol:", interpol_data)

        # Agora, você pode processar os dados e inseri-los no banco de dados em tempo real
        # Substitua "sua_tabela" pelo nome da tabela real que você deseja inserir os dados
        response_data = {
            "dados_fbi": fbi_data,
            "dados_interpol": interpol_data
        }

        # Configurar as informações de conexão
        connection = cx_Oracle.connect(
            user="rm96016",
            password="040998",
            dsn="oracle.fiap.com.br:1521/orcl"
        )

        # Criar um cursor
        cursor = connection.cursor()

        # Executar uma consulta SQL
        cursor.execute("SELECT * FROM sua_tabela")
        result = cursor.fetchall()

        # Exibir os resultados
        for row in result:
            print(row)

        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

        return jsonify({"message": "Dados atualizados com sucesso!"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
