import PySimpleGUI as pg
from main import *
from criarRelatorio import criar_relatorio

    
objDb = DBFinancia()
pg.theme('DarkGrey13')

def validar(val):
    for v in val:
        if len(v)<1:
            return False
    return True

def atualizar():
    transacoes = []
    for t in objDb.listar(colunas=('titulo','valor','categoria','data')):
        t = list(t)
        t[1] = f"R$ {t[1]/100:.2f}"
        data = converter_data(t[3])
        t[3] = f"{data.day} / {data.month} / {data.year}"
        transacoes.append(t)
    return transacoes


def editar(val_salvos):
    cont_edit = [[pg.Text('Titulo'), pg.Input(val_salvos[1],key='edit_tit',size=(30,0))],
                 [pg.Text('Valor'),pg.Input(val_salvos[2]/100,key='edit_valor',size=(7,0))],
                 [pg.Radio('receita',group_id=1,default=True,key='REC_BUT_EDIT'),pg.Radio('despesa',group_id=1,key='DES_BUT_EDIT')],
                 [pg.Text('Data'), pg.Input(val_salvos[4][:11],key='edit_data',size=10)],
                 [pg.Button('salvar')]]
    
    janela_edit = pg.Window('editar', cont_edit)
    while True:
        eventos_edit,valores_edit = janela_edit.read()
        if eventos_edit==pg.WIN_CLOSED:
            break
        if eventos_edit=='salvar':
            if valores_edit['REC_BUT_EDIT']:
                edit_categoria = 'receita'
            elif valores_edit['DES_BUT_EDIT']:
                edit_categoria = 'despesa'
            editar_valores = [valores_edit['edit_tit'],valores_edit['edit_valor'],edit_categoria,valores_edit['edit_data']]
            if validar(editar_valores)==True:
                pg.Popup('',objDb.editar(salvos[0],editar_valores))
            else:
                pg.Popup('aviso', 'CAMPOS NÃO PREENCHIDOS, OU VALOR INVALIDO')
    janela_edit.close()






col_botoes = [[pg.Button('excluir')],[pg.Button('editar')]]
Tabela = [[pg.Table(atualizar(),headings=['Titulo','Valor','Categoria','Data'],pad=(10,0),key='TRANSACOES',enable_events=True,justification='center',row_height=20,num_rows=7,col_widths=[10],auto_size_columns=False)]]
Conj_transacoes = [[pg.Text('Ultimas Transacoes',pad=(10,10),font=('Arial', 12,'bold'))],
                   [pg.Column(Tabela),pg.Column(col_botoes)],
                   [pg.Text(f'Total transacoes {len(objDb.listar())}',pad=(13,0))]]
                   


Conj_cria_pdf = [[pg.Push(),pg.Text("Salvar as informações em um arquivo pdf",font=('Arial', 12,'bold')),pg.Push()],
                 [pg.Push(),pg.Text("Escolha um caminho para salvar"),pg.Push()],
                 [pg.Sizer(0,50)],
                 [pg.Push(),pg.Input(key='CAMINHOPDF',size=(25,0)),pg.SaveAs('procurar'),pg.Push()],
                 [pg.Push(),pg.Button('salvar pdf'),pg.Push()]]

Conj_adicionar = [[pg.Sizer(0,10)],
                 [pg.Text('Titulo'),pg.Input(key='ADD_TIT', size=(30,0))],
                 [pg.Sizer(0,15)],
                 [pg.Text('Valor'),pg.Input(key='ADD_VAL', size=(7,0))],
                 [pg.Sizer(0,15)],
                 [pg.Radio('receita',group_id=1,default=True,key='REC_BUTTON'),pg.Radio('despesa',group_id=1,key='DES_BUTTON')],
                 [pg.Sizer(0,15)],
                 [pg.Text("Obs: apenas os formatos de data: 'dd/mm/yyyy', 'yyyy-mm-dd' são suportados")],
                 [pg.Text("Data"),pg.Input(key='ADD_DATA', size=(10,0))],
                 [pg.Button("ADD",pad=((7,0),(10,8)))]]




layout_main = [[pg.TabGroup([[pg.Tab('visao geral',Conj_transacoes),pg.Tab('adicionar',Conj_adicionar),pg.Tab('salvar',Conj_cria_pdf)]])]]


janela = pg.Window('Gestão financeira', layout_main)


while True:
    eventos, valores = janela.read()
    if eventos==pg.WIN_CLOSED:
        break
            
    if eventos=='excluir':
        try:
            ind_t = valores['TRANSACOES'][0]
            id_selecionado = objDb.listar()[ind_t][0]
            pg.Popup('',objDb.excluir(id_selecionado))
            janela['TRANSACOES'].update(atualizar())
        except IndexError:
            pg.Popup('','selecione um item para excluir')       
    
    if eventos=='editar':
        try:
            ind_t = valores['TRANSACOES'][0]
            id_selecionado = objDb.listar()[ind_t][0]
            salvos = objDb.selecionar(id_selecionado)
            editar(salvos)
            janela['TRANSACOES'].update(atualizar())
        except IndexError:
            pg.Popup('','selecione um item para editar') 
    
    
    if eventos=='salvar pdf':
        if len(valores['CAMINHOPDF'])==0:
            pg.Popup('','Selecione um caminho para salvar')
        else:
            pg.Popup('',criar_relatorio(valores['CAMINHOPDF']))
        
    if eventos=='ADD':
        if valores['REC_BUTTON']:
            ADD_CAT = 'receita'
        elif valores['DES_BUTTON']:
            ADD_CAT = 'despesa'
        valores_add = [valores['ADD_TIT'],valores['ADD_VAL'],ADD_CAT,valores['ADD_DATA']]
        if validar(valores_add)==True:
            pg.Popup('',objDb.adicionar(valores_add))
            janela['TRANSACOES'].update(atualizar())
        else:
            pg.Popup('aviso', 'CAMPOS NÃO PREENCHIDOS, OU VALOR INVALIDO')
    
objDb.fechar()   
janela.close()