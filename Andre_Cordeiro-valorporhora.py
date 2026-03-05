import datetime
import calendar


salario = float(input("Digite seu salário líquido mensal: "))
produto = float(input("Digite o valor do produto: "))


hoje = datetime.date.today()
ano = hoje.year
mes = hoje.month

# Quantidade de dias no mes
dias_no_mes = calendar.monthrange(ano, mes)[1]

# dias uteis
dias_uteis = 0

for dia in range(1, dias_no_mes + 1):
    data = datetime.date(ano, mes, dia)
    
    # weekday(): segunda=0 ... domingo=6
    if data.weekday() < 5:  
        dias_uteis += 1

# Calculos
valor_dia = salario / dias_uteis
valor_hora = valor_dia / 8
horas_para_comprar = produto / valor_hora

# Resultados
print("\n----- RESULTADO -----")
print(f"Dias úteis no mês: {dias_uteis}")
print(f"Valor de um dia de trabalho: R$ {valor_dia:.2f}")
print(f"Valor de uma hora de trabalho: R$ {valor_hora:.2f}")
print(f"Horas necessárias para comprar o produto: {horas_para_comprar:.2f} horas")