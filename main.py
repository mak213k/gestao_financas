from datetime import *
import locale
import sqlite3 as sql

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class DBFinancia:
    def __init__(self):
        self.__conexao = sql.connect('financias.db')
        self.__cursor = self.__conexao.cursor()
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS transacoes(id INTEGER PRIMARY KEY AUTOINCREMENT, titulo VARCHAR(50) NOT NULL, valor INTEGER NOT NULL, categoria TEXT CHECK(categoria IN ("despesa","receita")),data DATE NOT NULL)')

    def fechar(self):
        self.__conexao.close()
        
    def adicionar(self,valores):
        try:
            valores[3] = converter_data(valores[3]+' 00:00:00')
            valores[1] = converter_dinheiro(valores[1])
            self.__cursor.execute("INSERT INTO transacoes (titulo, valor, categoria, data) VALUES (?,?,?,?)",(valores[0],valores[1],valores[2],valores[3]))
            self.__conexao.commit()
            return'Nova transacao adicionada com sucesso'
        except sql.IntegrityError:
            return 'CAMPOS NÃO PREENCHIDOS, OU VALOR INVALIDO'
            
    def excluir(self,ind):
        self.__cursor.execute(f"DELETE FROM transacoes WHERE id == {ind}")
        self.__conexao.commit()
        return('Transacao excluida com sucesso')
        
    
    def editar(self,ind,valores):
        try:
            valores[3] = converter_data(valores[3]+' 00:00:00')
            valores[1] = converter_dinheiro(valores[1])
            sql_query = "UPDATE transacoes SET titulo = ?, valor = ?, categoria = ?, data = ? WHERE id = ?"
            self.__cursor.execute(sql_query,(valores[0], valores[1],valores[2],valores[3],ind))
            self.__conexao.commit()
            return 'Transacao editada com sucesso'
        except sql.IntegrityError:
            return 'CAMPOS NÃO PREENCHIDOS, OU VALOR INVALIDO'
        
    def selecionar(self,ind):
        dados = self.__cursor.execute(f"SELECT * FROM transacoes WHERE id = {ind}")
        return dados.fetchone()
    
    def listar(self,colunas="*",filtro=''):
        str_col = str(colunas).replace('(','')
        str_col = str_col.replace(')','')
        str_col = str_col.replace("'",'"')
        sql_query = f'SELECT {str_col} FROM transacoes ' + filtro
        coluna = self.__cursor.execute(sql_query)
        return coluna.fetchall()
    


def converter_data(string):
    try:
        if '/' in string:
            data = datetime.strptime(string, '%d/%m/%Y %H:%M:%S')
        elif '-' in string:
            data = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        return data
    except:
        return None


def converter_dinheiro(valor):
    if '.' in valor:
        valor = valor.replace('.','')
    elif ',' in valor:
        valor = valor.replace(',','')
    else:
        valor = valor+'00'
    try:
        return int(valor)
    except:
        return None



    