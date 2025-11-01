from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table, TableStyle
import sqlite3 as sql
from datetime import datetime
from decimal import Decimal



def criar_tabela(valores):
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Cor de fundo
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Cor do texto
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento do texto
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte em negrito
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Tamanho da fonte

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Cor de fundo
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Adicionar grade
         ])
        
    for linha in range(1,len(valores)):
        cor = colors.lightgrey if linha%2==0 else colors.beige
        table_style.add('BACKGROUND', (0, linha), (-1, -1), cor)
       
    
    tabela = Table(valores,hAlign='LEFT')
    tabela.setStyle(table_style)
    return tabela



def formatar_valores(valores):
    # formata o valor para monetario e a data para formato do brasil
    for l in valores:
        if 'TITULO' not in l:
            l[1] = f"R$ {Decimal(l[1]) / Decimal(100):.2f}"
            l[2] = datetime.strptime(l[2], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
    return valores


def criar_relatorio(caminho):
    con = sql.connect("financias.db")
    cur = con.cursor()
    despesas = cur.execute('SELECT titulo,valor,data FROM transacoes WHERE categoria="despesa"').fetchall()
    receitas = cur.execute("SELECT titulo,valor,data FROM transacoes WHERE  categoria='receita'").fetchall()
    
    if ".pdf" not in caminho:
        caminho_completo = f"{caminho}.pdf"
    else:
        caminho_completo = caminho
    
    pdf = SimpleDocTemplate(caminho_completo,pagesize=A4)

    data_hoje = Paragraph(f"data de criação: {datetime.now().strftime('%d/%m/%Y')}", ParagraphStyle(name='style_date',aligment=TA_LEFT))
    titulo_pdf =  Paragraph("GASTOS E GANHOS PESSOAIS", ParagraphStyle(name='style_tit',aligment=TA_CENTER))

    
    pdes = Paragraph("DESPESAS", ParagraphStyle(name='style_des',aligment=TA_LEFT))
    prec = Paragraph("RECEITAS", ParagraphStyle(name='style_des',aligment=TA_RIGHT))
    

    lista_tabela_gastos = [["TITULO", "VALOR", "DATA"]]
    
    try:
        #passa os valores da linha para uma lista
        for linha in despesas:
            lista_tabela_gastos.append(list(linha))
        
        formatar_valores(lista_tabela_gastos)
        tabela_des = criar_tabela(lista_tabela_gastos)
        
        # detalhes dos gastos (maior valor, periodo, total)
        cur.execute('SELECT MAX(valor) FROM transacoes WHERE categoria="despesa"')
        maior_valor_des = Paragraph(f"MAIOR VALOR: R$ {cur.fetchone()[0]/100}",ParagraphStyle(name='MVdes',aligment=TA_RIGHT))
        total_des = cur.execute('SELECT SUM(valor) FROM transacoes WHERE categoria="despesa"').fetchone()[0]
        total_valor_des = Paragraph(f"VALOR TOTAl: R$ {total_des/100}",ParagraphStyle(name='VTdes',aligment=TA_LEFT))
        cur.execute('SELECT MAX(data),MIN(data) FROM transacoes WHERE categoria="despesa"')
        datas = cur.fetchall()[0]
        periodo_des = Paragraph(f"PERIODO: {datetime.strptime(datas[1],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')}  à  {datetime.strptime(datas[0],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')}",ParagraphStyle(name='pdes',aligment=TA_CENTER))
            
        lista_tabela_ganhos = [["TITULO", "VALOR", "DATA"]]

        for linha in receitas:
            lista_tabela_ganhos.append(list(linha))
            
        formatar_valores(lista_tabela_ganhos)
        tabela_rec = criar_tabela(lista_tabela_ganhos)
        
        # detalhes dos ganhos (maior valor, periodo, total)
        cur.execute('SELECT MAX(valor) FROM transacoes WHERE categoria="receita"')
        maior_valor_rec = Paragraph(f"MAIOR VALOR: R$ {cur.fetchone()[0]/100}",ParagraphStyle(name='MVdes',aligment=TA_RIGHT))
        total_rec = cur.execute('SELECT SUM(valor) FROM transacoes WHERE categoria="receita"').fetchone()[0]
        total_valor_rec = Paragraph(f"VALOR TOTAl: R$ {total_rec/100}",ParagraphStyle(name='VTdes',aligment=TA_LEFT))
        cur.execute('SELECT MAX(data),MIN(data) FROM transacoes WHERE categoria="receita"')
        datas = cur.fetchall()[0]
        periodo_rec = Paragraph(f"PERIODO: {datetime.strptime(datas[1],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')}  à  {datetime.strptime(datas[0],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')}",ParagraphStyle(name='pdes',aligment=TA_CENTER))
        
        saldo_final = Paragraph(f"SALDO FINAL: R$ {(total_rec - total_des)/100:.2f}",ParagraphStyle(name='pdes',aligment=TA_CENTER))
    except TypeError:
        return "Você deve ter pelos menos um registros de cada categoria"
    
    
    pdf.build([data_hoje,Spacer(0,30),titulo_pdf,Spacer(0,40),pdes,Spacer(0,10),tabela_des,Spacer(0,10),total_valor_des,periodo_des,maior_valor_des,Spacer(0,60),prec,Spacer(0,10),tabela_rec,Spacer(0,10),total_valor_rec,periodo_rec,maior_valor_rec,Spacer(0,40),saldo_final])

    
    con.close()
    return "Registro salvo com sucesso"