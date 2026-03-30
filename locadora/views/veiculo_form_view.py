import tkinter as tk
from tkinter import ttk, messagebox

from model.veiculo import Categoria, VeiculoFactory
from model.ExcecoesPersonalizadas import PlacaInvalidaError


class VeiculoFormView(tk.Toplevel):

    def __init__(self, parent, on_save):
        super().__init__(parent)

        self._on_save = on_save

        self.title("Cadastrar Novo Veículo")
        self.resizable(False, False)
        self.grab_set()   # bloqueia a janela principal enquanto este formulário está aberto

        self._construir_tela()

    def _construir_tela(self):
        tk.Label(self, text="Cadastrar Novo Veículo", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Placa
        tk.Label(self, text="Placa:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self._entry_placa = tk.Entry(self, width=25)
        self._entry_placa.grid(row=1, column=1, padx=10, pady=5)

        # Tipo
        tk.Label(self, text="Tipo:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self._var_tipo = tk.StringVar(value="Carro")
        frame_tipo = tk.Frame(self)
        frame_tipo.grid(row=2, column=1, sticky="w", padx=10)
        tk.Radiobutton(frame_tipo, text="Carro",     variable=self._var_tipo, value="Carro").pack(side="left")
        tk.Radiobutton(frame_tipo, text="Motorhome", variable=self._var_tipo, value="Motorhome").pack(side="left")

        # Categoria
        tk.Label(self, text="Categoria:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self._var_categoria = tk.StringVar(value="ECONOMICO")
        ttk.Combobox(
            self,
            textvariable=self._var_categoria,
            values=["ECONOMICO", "EXECUTIVO"],
            state="readonly",
            width=22,
        ).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Taxa Diária
        tk.Label(self, text="Taxa Diária (R$):").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self._entry_taxa = tk.Entry(self, width=25)
        self._entry_taxa.grid(row=4, column=1, padx=10, pady=5)

        # Botão Salvar
        tk.Button(self, text="Salvar", width=15, command=self._salvar).grid(row=5, column=0, columnspan=2, pady=15)

    def _salvar(self):
        placa     = self._entry_placa.get().strip()
        tipo      = self._var_tipo.get()
        categoria = Categoria[self._var_categoria.get()]   # converte string → enum
        taxa_str  = self._entry_taxa.get().strip().replace(",", ".")

        # Validações
        if not placa:
            messagebox.showwarning("Campo obrigatório", "Informe a placa.", parent=self)
            return

        if not taxa_str:
            messagebox.showwarning("Campo obrigatório", "Informe a taxa diária.", parent=self)
            return

        try:
            taxa_diaria = float(taxa_str)
            if taxa_diaria < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Valor inválido", "Taxa diária deve ser um número positivo.", parent=self)
            return

        # Cria o veículo via Factory (a própria classe valida a placa)
        try:
            veiculo = VeiculoFactory.criar_veiculo(tipo, placa, categoria, taxa_diaria)
        except PlacaInvalidaError as e:
            messagebox.showerror("Placa inválida", str(e), parent=self)
            return

        # Avisa a Tela 1 e fecha o formulário
        self._on_save(veiculo)
        self.destroy()
