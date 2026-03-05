import datetime
import calendar
import tkinter as tk
from tkinter import messagebox

def calcular():
    try:
        salario = float(entry_salario.get())
        produto = float(entry_produto.get())

        hoje = datetime.date.today()
        ano = hoje.year
        mes = hoje.month

        dias_no_mes = calendar.monthrange(ano, mes)[1]

        dias_uteis = 0
        for dia in range(1, dias_no_mes + 1):
            data = datetime.date(ano, mes, dia)
            if data.weekday() < 5:
                dias_uteis += 1

        valor_dia = salario / dias_uteis
        valor_hora = valor_dia / 8
        horas_para_comprar = produto / valor_hora
        dias_para_comprar = produto / valor_dia

        resultado = f"""
Dias úteis no mês: {dias_uteis}
Valor de um dia de trabalho: R$ {valor_dia:.2f}
Valor de uma hora de trabalho: R$ {valor_hora:.2f}
Horas necessárias para comprar: {horas_para_comprar:.2f} horas
Dias necessários para comprar: {dias_para_comprar:.2f} dias
"""

        label_resultado.config(text=resultado)

    except ValueError:
        messagebox.showerror("Erro", "Digite valores corretos.")

# Janela
janela = tk.Tk()
janela.title("Calculadora de Horas de Trabalho")
janela.geometry("350x350")


# Salário
tk.Label(janela, text="Salário líquido mensal:").pack(pady=5)
entry_salario = tk.Entry(janela)
entry_salario.pack()

# Produto
tk.Label(janela, text="Valor do produto:").pack(pady=5)
entry_produto = tk.Entry(janela)
entry_produto.pack()

# Botão
tk.Button(janela, text="Calcular", command=calcular).pack(pady=15)

# Resultado
label_resultado = tk.Label(janela, text="", justify="left")
label_resultado.pack()

janela.mainloop()
