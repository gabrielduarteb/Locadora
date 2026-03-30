"""
Ponto de entrada da aplicação Locadora de Veículos.
Execute: python main.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from views.veiculo_list_view import VeiculoListView


def main():
    app = VeiculoListView()
    app.mainloop()


if __name__ == "__main__":
    main()
