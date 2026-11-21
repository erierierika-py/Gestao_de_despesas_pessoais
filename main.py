"""Menu principal do Gestor de Despesas Pessoais."""

from src import dados, login, poupanca, rendimentos, saldo
from src.despesas import adicionar_despesa, consultar_despesas, editar_despesa, eliminar_despesa
from src.utilitarios import confirmar

def confirmar_saida():
    """Pergunta ao utilizador se quer mesmo sair da aplicação.

    Returns:
        bool: True se o utilizador confirmar a saída, False caso contrário.
    """
    return confirmar("Queres mesmo sair?")

def main():
    """Pede o login e, se for válido, mostra o menu principal em ciclo."""
    if not login.fazer_login():
        return

    while True:
        print("\nGESTÃO DE DESPESAS PESSOAIS")

        d = dados.carregar()
        print(f"{len(d['despesas'])} despesas registadas.")
        saldo.aviso_saldo_baixo(d)

        print("1 - Adicionar despesa")
        print("2 - Consultar despesas")
        print("3 - Editar despesa")
        print("4 - Remover despesa")
        print("5 - Rendimentos")
        print("6 - Saldo e histórico")
        print("7 - Poupança")
        print("0 - Sair")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            adicionar_despesa()

        elif opcao == "2":
            consultar_despesas()

        elif opcao == "3":
            editar_despesa()

        elif opcao == "4":
            eliminar_despesa()

        elif opcao == "5":
            rendimentos.menu_rendimentos()

        elif opcao == "6":
            saldo.menu_saldo()

        elif opcao == "7":
            poupanca.menu_poupanca()

        elif opcao == "0":
            if confirmar_saida():
                print("Os teus dados estão guardados. Até à próxima!")
                break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nAplicação terminada. Os teus dados estão guardados.")