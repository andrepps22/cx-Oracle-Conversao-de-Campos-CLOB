##########################################
###   Desenvolvido por Andre de Paula ####
###          DT 10/08/2022            ####
##########################################

from query import select_ora  # Arquivo aonde está armazenado o select do banco.
import base64
import cx_Oracle
import datetime


user = input(str('Digite o usuario: ')).strip()
password = input(str('Digite a senha do banco: '))
host = input(str('Digite o nome do HOST: '))


# Função que vai conectar ao Oracle.
def connOra(user, password, host, select_ora):
    diretorio = ('arquivos/')  # Diretorio existente

    conn = cx_Oracle.connect(user=user, password=password, dsn=host)
    cursor = conn.cursor()

    # Filtrando a quantidade de linhas que vem do banco para a variavel
    cursor.prefetchrows = 1000
    cursor.arraysize = 1000

    # Faz a checagem do tipo da conexão e caso seja do typo CLOB retorna os dados em tipo STRING
    def output_type_handler(cursor, name, default_type, size, precision, scale):
        if default_type == cx_Oracle.DB_TYPE_CLOB:
            return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)

    conn.outputtypehandler = output_type_handler

    start = datetime.datetime.now()
    cursor.execute(select_ora)

    # Transforma as linhas que vieram do banco em arquivos.
    while True:

        row = cursor.fetchone()
        if not row:
            break
        res = bytes(row[2], 'utf-8')  #'ROW[2]' são os dados brutos quem vem em forma de testo, a variavel 'res' recebe o arquivo tranformado em bytes

        bt = base64.decodebytes(res)  # A variavel bt recebi os bytes decodificados.

        with open(diretorio + row[1], "wb+") as f:  # Gera os arquivs que vem  'ROW[1]' nome e tipo do arquivo
            f.write(bt)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    print('Inicio do processo')
    connOra(user, password, host, select_ora)
