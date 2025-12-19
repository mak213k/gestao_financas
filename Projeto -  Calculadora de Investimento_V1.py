import pandas as pd
import numpy_financial as npf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def calcular_ir(meses):
    if meses <= 6:
        return 0.225
    elif meses <= 12: 
        return 0.20
    elif meses <= 24: 
        return 0.175
    else: 
        return 0.15

def simulador_investimentos():    
    
    #Entradas de Capital e Tempo
    cap_inicial = float(input("Capital Inicial (R$): "))
    aporte_mensal = float(input("Aporte Mensal (R$): "))
    meses = int(input("Prazo do investimento (meses): "))

    #Taxas de Referência 
    selic_aa = float(input("Taxa Selic (% a.a.) [Exemplo: 14.95]: ") or 14.95)/ 100
    cdi_aa = float(input("Taxa CDI (% a.a.) [Exemplo: 14.50]: ") or 14.50)/ 100
    ipca_aa = float(input("Inflação IPCA (% a.a.) [Exemplo: 4.50]: ") or 4.50)/ 100

    #Taxas de Custódia e Adm
    taxa_b3 = float(input("Taxa de Custódia B3 (% a.a.)[Exemplo: 0.20]: ") or 0.20) / 100
    taxa_adm_di = float(input("Taxa Adm Fundo DI (% a.a.)[Exemplo: 0.50]: ") or 0.50) / 100

    # Rentabilidades Específicas
    rent_fundo_di = float(input("Rentabilidade Fundo DI (% do CDI): ") or 100) / 100
    rent_poupanca_am = float(input("Rentabilidade Poupança (% a.m.): ") or 0.50) / 100
    rent_cdb = float(input("Rentabilidade CDB (% do CDI): ") or 110) / 100
    rent_lci_lca = float(input("Rentabilidade LCI/LCA (% do CDI): ") or 90) / 100

    #Cálculo
    taxa_ir = calcular_ir(meses)
    investimentos = ["Selic", "CDB", "LCI/LCA", "Fundo DI", "Poupança", "IPCA (Inflação)"]
    resultados = []

    total_investido = cap_inicial + (aporte_mensal * meses)

    for inv in investimentos:
        # Definir taxa anual bruta e custos
        custo_anual = 0
        isento_ir = False
        
        if inv == "Selic":
            taxa_bruta_aa = selic_aa
            custo_anual = taxa_b3
        elif inv == "CDB":
            taxa_bruta_aa = cdi_aa * rent_cdb
        elif inv == "LCI/LCA":
            taxa_bruta_aa = cdi_aa * rent_lci_lca
            isento_ir = True
        elif inv == "Fundo DI":
            taxa_bruta_aa = cdi_aa * rent_fundo_di
            custo_anual = taxa_adm_di
        elif inv == "Poupança":
            taxa_bruta_aa = (1 + rent_poupanca_am)**12 - 1
            isento_ir = True
        else: 
            taxa_bruta_aa = ipca_aa
            isento_ir = True

        # Cálculo de Juros Compostos (Mensal)   
        taxa_mensal = (1 + taxa_bruta_aa)**(1/12) - 1
        valor_bruto = npf.fv(taxa_mensal, meses, -aporte_mensal, -cap_inicial)
        
        # Custos (Simplificado: aplicado sobre o valor final proporcional ao ano)
        total_custos = valor_bruto * (custo_anual * (meses/12))
        
        # Imposto de Renda
        lucro_bruto = valor_bruto - total_investido
        valor_ir = 0 if isento_ir else (lucro_bruto * taxa_ir)
        
        valor_liquido = valor_bruto - total_custos - valor_ir
        rent_liquida_total = ((valor_liquido / total_investido) - 1) * 100

        resultados.append({
            "Investimento": inv,
            "Valor Bruto": valor_bruto,
            "Rent. Bruta (%)": ((valor_bruto/total_investido)-1)*100,
            "Custos": total_custos,
            "IR": valor_ir,
            "Valor Líquido": valor_liquido,
            "Rent. Líquida (%)": rent_liquida_total,
            "Ganho Real (R$)": valor_liquido - total_investido
        })


    df = pd.DataFrame(resultados)

    #Configurar o estilo do gráfico
    plt.figure(figsize=(14, 5))
    
    #Criar o gráfico de barras comparando o Valor Líquido    
    cores = ['#27ae60' if x != 'IPCA (Inflação)' else '#e74c3c' for x in df['Investimento']]
    barras = plt.bar(df['Investimento'], df['Valor Líquido'], color=cores)

    #Adicionar títulos e rótulos
    plt.title(f'Comparativo de Investimentos: Valor Líquido Final ({meses} meses)', fontsize=14, fontweight='bold')
    plt.ylabel('Valor Líquido Acumulado (R$)', fontsize=12)
    plt.xlabel('Tipo de Investimento', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    #Adicionar os valores exatos em cima de cada barra
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, yval, f'R$ {yval:,.2f}', 
                 va='bottom', ha='center', fontsize=10, fontweight='bold')

    
    plt.tight_layout()
    plt.show()

    df = pd.DataFrame(resultados)
    pd.options.display.float_format = '{:.2f}'.format
    print("\n--- Resultado da Simulação ---")
    print(df.to_string(index=False))
    
    #Gráfico Comparativo

    plt.plot(x=df["Investimento"], y=df["Valor Líquido"], name="Valor Líquido Acumulado", marker_color='teal')
    plt.update_layout(title="Comparativo de Valor Líquido Final (R$)", template="plotly_white")
    plt.show()

if __name__ == "__main__":
    simulador_investimentos()
    