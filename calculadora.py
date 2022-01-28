import tkinter as tk

FONTE_GRANDE = ("IBM Plex Sans", 40, "bold")
FONTE_PEQUENA = ("IBM Plex Sans", 16)
FONTE_DIGITOS = ("IBM Plex Sans", 24, "bold")
FONTE_PADRAO = ("IBM Plex Sans", 20)

COR_BOTAO_OPERADORES = "#c9e2f5"
COR_BOTAO_NUMEROS = "#dedede"
COR_BOTAO_IGUAL = "#b08080"
COR_DISPLAY = "#ffefd5"
COR_NUMEROS = "#4B0082"


class Calculadora:
    def __init__(self):
        self.calc_display = tk.Tk()
        self.calc_display.geometry("375x667")
        self.calc_display.resizable(0, 0)
        self.calc_display.title("Calculadora")

        self.expressao_total = ""
        self.expressao_atual = ""
        self.tela_display = self.cria_tela_display()

        self.total_label, self.label = self.cria_display_labels()

        self.digitos = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2),
            ".": (4, 1),
        }
        self.operacoes = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.botoes_tela = self.cria_botoes_tela()

        self.botoes_tela.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.botoes_tela.rowconfigure(x, weight=1)
            self.botoes_tela.columnconfigure(x, weight=1)
        self.cria_botoes_digitos()
        self.cria_botoes_operadores()
        self.cria_botoes_especiais()
        self.teclado()

    def teclado(self):
        self.calc_display.bind("<Return>", lambda event: self.resolver())
        for key in self.digitos:
            self.calc_display.bind(
                str(key), lambda event, digit=key: self.add_para_expressao(digit)
            )

        for key in self.operacoes:
            self.calc_display.bind(
                key, lambda event, operator=key: self.acrescenta_operador(operator)
            )

    def cria_botoes_especiais(self):
        self.cria_botao_limpar()
        self.cria_botao_igual()
        self.cria_botao_quadrado()
        self.cria_botao_raiz_quadrada()

    def cria_display_labels(self):
        total_label = tk.Label(
            self.tela_display,
            text=self.expressao_total,
            anchor=tk.E,
            bg=COR_DISPLAY,
            fg=COR_NUMEROS,
            padx=24,
            font=FONTE_PEQUENA,
        )
        total_label.pack(expand=True, fill="both")

        label = tk.Label(
            self.tela_display,
            text=self.expressao_atual,
            anchor=tk.E,
            bg=COR_DISPLAY,
            fg=COR_NUMEROS,
            padx=24,
            font=FONTE_GRANDE,
        )
        label.pack(expand=True, fill="both")

        return total_label, label

    def cria_tela_display(self):
        frame = tk.Frame(self.calc_display, height=221, bg=COR_DISPLAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_para_expressao(self, value):
        self.expressao_atual += str(value)
        self.update_label()

    def cria_botoes_digitos(self):
        for digit, grid_value in self.digitos.items():
            button = tk.Button(
                self.botoes_tela,
                text=str(digit),
                bg=COR_BOTAO_NUMEROS,
                fg=COR_NUMEROS,
                font=FONTE_DIGITOS,
                borderwidth=1,
                command=lambda x=digit: self.add_para_expressao(x),
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def acrescenta_operador(self, operator):
        self.expressao_atual += operator
        self.expressao_total += self.expressao_atual
        self.expressao_atual = ""
        self.update_total_label()
        self.update_label()

    def cria_botoes_operadores(self):
        for i, (operator, symbol) in enumerate(self.operacoes.items()):
            button = tk.Button(
                self.botoes_tela,
                text=symbol,
                bg=COR_BOTAO_OPERADORES,
                fg=COR_NUMEROS,
                font=FONTE_PADRAO,
                borderwidth=1,
                command=lambda x=operator: self.acrescenta_operador(x),
            )
            button.grid(row=i, column=4, sticky=tk.NSEW)

    def limpar(self):
        self.expressao_atual = ""
        self.expressao_total = ""
        self.update_label()
        self.update_total_label()

    def cria_botao_limpar(self):
        button = tk.Button(
            self.botoes_tela,
            text="C",
            bg=COR_BOTAO_OPERADORES,
            fg=COR_NUMEROS,
            font=FONTE_PADRAO,
            borderwidth=1,
            command=self.limpar,
        )
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def quadrado(self):
        self.expressao_atual = str(eval(f"{self.expressao_atual}**2"))
        self.update_label()

    def cria_botao_quadrado(self):
        button = tk.Button(
            self.botoes_tela,
            text="x\u00b2",
            bg=COR_BOTAO_OPERADORES,
            fg=COR_NUMEROS,
            font=FONTE_PADRAO,
            borderwidth=1,
            command=self.quadrado,
        )
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def raiz_quadrada(self):
        self.expressao_atual = str(eval(f"{self.expressao_atual}**0.5"))
        self.update_label()

    def cria_botao_raiz_quadrada(self):
        button = tk.Button(
            self.botoes_tela,
            text="\u221ax",
            bg=COR_BOTAO_OPERADORES,
            fg=COR_NUMEROS,
            font=FONTE_PADRAO,
            borderwidth=1,
            command=self.raiz_quadrada,
        )
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def resolver(self):
        self.expressao_total += self.expressao_atual
        self.update_total_label()
        try:
            self.expressao_atual = str(eval(self.expressao_total))

            self.expressao_total = ""
        except Exception:
            self.expressao_atual = "Error"
        finally:
            self.update_label()

    def cria_botao_igual(self):
        button = tk.Button(
            self.botoes_tela,
            text="=",
            bg=COR_BOTAO_IGUAL,
            fg=COR_NUMEROS,
            font=FONTE_PADRAO,
            borderwidth=1,
            command=self.resolver,
        )
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def cria_botoes_tela(self):
        frame = tk.Frame(self.calc_display)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.expressao_total
        for operator, symbol in self.operacoes.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.expressao_atual[:11])

    def run(self):
        self.calc_display.mainloop()


if __name__ == "__main__":
    calc = Calculadora()
    calc.run()
