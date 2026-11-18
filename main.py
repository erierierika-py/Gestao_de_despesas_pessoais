
from src import dados
from src.despesas import adicionar_despesa, consultar_despesas, editar_despesa


def main():
    while True:
        print("\nGESTÃO DE DESPESAS PESSOAIS")

        d = dados.carregar()
        print(f"{len(d['despesas'])} despesas registadas.")

        print("1 - Adicionar despesa")
        print("2 - Consultar despesas")
        print("3 - Editar despesa")
        print("0 - Sair")

        opcao = input("Escolhe uma opção: ")

        if opcao == "1":
            adicionar_despesa()

        elif opcao == "2":
            consultar_despesas()

        elif opcao == "3":
            editar_despesa()

        elif opcao == "0":
            print("Ate a proxima")
            break

        else:
            print("Opção invalida")


if __name__ == "__main__":
    main()
