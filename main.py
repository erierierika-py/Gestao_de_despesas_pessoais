"""Menu principal do Gestor de Despesas Pessoais."""

from src import ajuda, backup, dados, login, pesquisa, poupanca, rendimentos, saldo, subscricoes
from src.despesas import adicionar_despesa, consultar_despesas, editar_despesa, eliminar_despesa
from src.utilitarios import confirmar

def confirmar_saida():
    """Pergunta ao utilizador se quer mesmo sair da aplicação.

    Returns:
        bool: True se o utilizador confirmar a saída, False caso contrário.
    """
    return confirmar("Queres mesmo sair?")


def menu_subscricoes():
    """Submenu das subscrições."""
    while True:
        print("\n*** SUBSCRIÇÕES ***")
        print("1 - Adicionar")
        print("2 - Listar")
        print("3 - Remover")
        print("0 - Voltar")
        opcao = input("Escolhe uma opção: ").strip()
        if opcao == "1":
            subscricoes.adicionar_subscricao()
        elif opcao == "2":
            subscricoes.listar_subscricoes()
        elif opcao == "3":
            subscricoes.remover_subscricao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida")


def menu_backup():
    """Submenu do backup."""
    while True:
        print("\n*** BACKUP ***")
        print("1 - Criar backup")
        print("2 - Ver backups")
        print("3 - Restaurar backup")
        print("0 - Voltar")
        opcao = input("Escolhe uma opção: ").strip()
        if opcao == "1":
            backup.criar_backup()
        elif opcao == "2":
            backup.mostrar_backups()
        elif opcao == "3":
            backup.restaurar_backup()
        elif opcao == "0":
            break
        else:
            print("Opção inválida")

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
        print("8 - Pesquisar despesas")
        print("9 - Filtrar por categoria")
        print("10 - Gasto por categoria")
        print("11 - Subscrições")
        print("12 - Backup")
        print("13 - Ajuda")
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

        elif opcao == "8":
            pesquisa.menu_pesquisar()

        elif opcao == "9":
            pesquisa.menu_filtrar()

        elif opcao == "10":
            pesquisa.menu_gasto_categoria()

        elif opcao == "11":
            menu_subscricoes()

        elif opcao == "12":
            menu_backup()

        elif opcao == "13":
            ajuda.mostrar_ajuda()

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