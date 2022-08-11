from query import select_ora
import base64
import cx_Oracle
import datetime


user = input(str('Digite o usuario: ')).strip()
password = input(str('Digite a senha do banco: '))
host = input(str('Digite o nome do HOST: '))


def connOra(user, password, host, select_ora):
    diretorio = ('arquivos/')

    conn = cx_Oracle.connect(user=user, password=password, dsn=host)
    cursor = conn.cursor()
    cursor.prefetchrows = 1000
    cursor.arraysize = 1000

    def output_type_handler(cursor, name, default_type, size, precision, scale):
        if default_type == cx_Oracle.DB_TYPE_CLOB:
            return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)

    conn.outputtypehandler = output_type_handler
    
    start = datetime.datetime.now()
    cursor.execute(select_ora)
    
    while True:
        
        row = cursor.fetchone()
        if not row:
            break
        res = bytes(row[2], 'utf-8')

        bt = base64.decodebytes(res)

        with open(diretorio + row[1], "wb+") as f:
            f.write(bt)
        

       
    conn.close()
    
    
   

if __name__=='__main__':
    print('Inicio do processo')
    connOra(user, password, host, select_ora)