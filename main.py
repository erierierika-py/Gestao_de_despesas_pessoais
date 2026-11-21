
from src import dados, poupanca, rendimentos, saldo
from src.despesas import adicionar_despesa, consultar_despesas, editar_despesa, eliminar_despesa


def main():
    """Mostra o menu principal em ciclo e executa a opção escolhida."""
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

        opcao = input("Escolhe uma opção: ")

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
            print("Até à próxima")
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()
