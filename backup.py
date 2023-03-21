import mysql.connector
import subprocess
from datetime import datetime

# dados de conexão do banco de dados MySQL
config = {
  'user': 'root',
  'password': '1012',
  'host': 'localhost',
  'database': 'clinica'
}

# cria uma conexão com o banco de dados
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# obtém a data atual para incluir no nome do arquivo de backup
data_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
nome_arquivo = 'backup_{}.sql'.format(data_atual)

# executa o comando para fazer o backup do banco de dados
with open(nome_arquivo, 'w') as arquivo:
    subprocess.run(['mysqldump', '--user', config['user'], '--password', config['password'], 
                    '--host', config['host'], config['database']], stdout=arquivo)

# fecha a conexão com o banco de dados
cursor.close()
cnx.close()
