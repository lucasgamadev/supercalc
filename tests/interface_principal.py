import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import sys
import os

TESTES = [
    ("Calculadora Padrão", "test_interface_padrao.py"),
    ("Calculadora de Juros", "test_interface_juros.py"),
    ("Calculadora de Desconto", "test_interface_desconto.py"),
    #("Calculadora de Unidades", "test_interface_unidades.py"),
]

class InterfacePrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SuperCalc - Testes das Calculadoras")
        self.geometry("600x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Testes das Calculadoras", font=("Arial", 18, "bold")).pack(pady=10)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        for nome, script in TESTES:
            btn = tk.Button(btn_frame, text=f"Iniciar testes: {nome}", width=30, command=lambda s=script, n=nome: self.run_test(s, n))
            btn.pack(pady=5)
        self.output = scrolledtext.ScrolledText(self, width=70, height=15, font=("Consolas", 10))
        self.output.pack(padx=10, pady=10)
        self.output.config(state=tk.DISABLED)

    def run_test(self, script, nome):
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Executando testes para: {nome}\n\n")
        self.output.update()
        script_path = os.path.join(os.path.dirname(__file__), script)
        if not os.path.exists(script_path):
            self.output.insert(tk.END, f"Arquivo de teste não encontrado: {script}\n")
            self.output.config(state=tk.DISABLED)
            return
        try:
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=120)
            self.output.insert(tk.END, result.stdout)
            if result.returncode == 0:
                self.output.insert(tk.END, f"\nTestes finalizados com sucesso para {nome}!\n")
            else:
                self.output.insert(tk.END, f"\nAlguns testes falharam para {nome}.\n")
                self.output.insert(tk.END, result.stderr)
        except Exception as e:
            self.output.insert(tk.END, f"Erro ao executar os testes: {e}\n")
        self.output.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = InterfacePrincipal()
    app.mainloop()