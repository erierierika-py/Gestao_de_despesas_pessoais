# Gestor de Despesas

Aplicação de consola em Python para gerir despesas, rendimentos e orçamento pessoal.

## Como correr
python main.py

## Grupo
- Erika
- Dalila
- Rodrigo

## Testes

Os testes unitários usam o módulo `unittest` (já vem com o Python, não é preciso instalar nada) e ficam na pasta `tests/`.

Para correr todos os testes, a partir da pasta principal do projeto:

```bash
python -m unittest discover tests -v
```

O `-v` mostra o nome de cada teste e se passou (`ok`) ou falhou.

Para correr só um ficheiro:

```bash
python -m unittest tests.test_pesquisa -v
```

| Ficheiro | O que testa |
|---|---|
| `tests/test_pesquisa.py` | pesquisa por descrição, filtro por categoria, gasto por categoria |
| `tests/test_poupanca.py` | cálculo do valor poupado |
| `tests/test_subscricoes.py` | total mensal das subscrições |

Os testes usam dados criados dentro de cada teste, por isso não dependem do `data/dados.json` e não o alteram.