
from src.despesas import adicionar_despesa, consultar_despesas


def main():
    while True:
        print("\nGESTÃO DE DESPESAS PESSOAIS")
        print("1 - Adicionar despesa")
        print("2 - Consultar despesas")
        print("0 - Sair")

        opcao = input("Escolhe uma opção: ")

        if opcao == "1":
            adicionar_despesa()

        elif opcao == "2":
            consultar_despesas()

        elif opcao == "0":
            print("Ata a procima")
            break

        else:
            print("Opção invalida.")


if __name__ == "__main__":
    main()
