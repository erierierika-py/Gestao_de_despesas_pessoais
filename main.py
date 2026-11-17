from src import dados


def main():
    print("Gestor de Despesas")
    d = dados.carregar()
    print(f"{len(d['despesas'])} despesas registadas.")


if __name__ == "__main__":
    main()