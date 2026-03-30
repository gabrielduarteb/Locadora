import tkinter as tk
from tkinter import ttk, messagebox

from model.veiculo import Veiculo, Categoria, VeiculoFactory
from model.estados_veiculo import DisponivelState, AlugadoState, ManutencaoState
from views.veiculo_form_view import VeiculoFormView


def _nome_tipo(veiculo):
    return type(veiculo).__name__


def _nome_estado(veiculo):
    estados = {
        DisponivelState: "Disponível",
        AlugadoState:    "Alugado",
        ManutencaoState: "Manutenção",
    }
    return estados.get(type(veiculo.estado_atual), "—")


class VeiculoListView(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Locadora de Veículos")
        self.geometry("700x400")

        self._veiculos = []
        self._popular_dados_exemplo()

        self._construir_tela()
        self._atualizar_tabela()

    def _popular_dados_exemplo(self):
        self._veiculos = [
            VeiculoFactory.criar_veiculo("Carro",     "ABC1234", Categoria.ECONOMICO,  89.90),
            VeiculoFactory.criar_veiculo("Motorhome", "XYZ5678", Categoria.EXECUTIVO, 320.00),
            VeiculoFactory.criar_veiculo("Carro",     "DEF9012", Categoria.EXECUTIVO, 175.00),
        ]

    def _construir_tela(self):
        # Título
        tk.Label(self, text="Veículos Cadastrados", font=("Arial", 14, "bold")).pack(pady=10)

        # Tabela (Treeview)
        colunas = ("placa", "tipo", "categoria", "taxa", "estado")
        self._tree = ttk.Treeview(self, columns=colunas, show="headings", height=10)

        self._tree.heading("placa",     text="Placa")
        self._tree.heading("tipo",      text="Tipo")
        self._tree.heading("categoria", text="Categoria")
        self._tree.heading("taxa",      text="Taxa Diária")
        self._tree.heading("estado",    text="Estado")

        self._tree.column("placa",     width=120, anchor="center")
        self._tree.column("tipo",      width=120, anchor="center")
        self._tree.column("categoria", width=110, anchor="center")
        self._tree.column("taxa",      width=120, anchor="center")
        self._tree.column("estado",    width=110, anchor="center")

        self._tree.pack(padx=10, pady=5)

        # Frame com os 3 botões no rodapé
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Novo",            width=15, command=self._abrir_formulario).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Ver Informações", width=15, command=self._ver_informacoes).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Remover",         width=15, command=self._remover).grid(row=0, column=2, padx=5)

    def _atualizar_tabela(self):
        # Limpa a tabela e reinsere todos os veículos
        for item in self._tree.get_children():
            self._tree.delete(item)

        for v in self._veiculos:
            self._tree.insert("", "end", values=(
                v.placa,
                _nome_tipo(v),
                v.categoria.value,
                f"R$ {v.taxa_diaria:.2f}",
                _nome_estado(v),
            ))

    def _ver_informacoes(self):
        selecionado = self._tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo na lista.")
            return

        # Descobre o índice da linha selecionada
        indice = self._tree.index(selecionado[0])
        v = self._veiculos[indice]

        info = (
            f"Placa:       {v.placa}\n"
            f"Tipo:        {_nome_tipo(v)}\n"
            f"Categoria:   {v.categoria.value}\n"
            f"Taxa Diária: R$ {v.taxa_diaria:.2f}\n"
            f"Seguro:      R$ {v.valor_seguro:.2f}\n"
            f"Estado:      {_nome_estado(v)}"
        )
        messagebox.showinfo(f"Informações — {v.placa}", info)

    def _remover(self):
        selecionado = self._tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo na lista.")
            return

        indice = self._tree.index(selecionado[0])
        v = self._veiculos[indice]

        confirmou = messagebox.askyesno("Confirmar", f"Remover o veículo {v.placa}?")
        if confirmou:
            self._veiculos.pop(indice)
            self._atualizar_tabela()

    def _abrir_formulario(self):
        VeiculoFormView(self, on_save=self._ao_salvar_veiculo)

    def _ao_salvar_veiculo(self, novo_veiculo):
        self._veiculos.append(novo_veiculo)
        self._atualizar_tabela()
