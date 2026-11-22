# Gestor de Despesas Pessoais

Aplicação de consola em Python para gerir despesas, rendimentos e orçamento pessoal.
Permite registar o que gastas e o que recebes, acompanhar o saldo, definir um objetivo
de poupança e guardar tudo em ficheiro, protegido por palavra-passe.

Projeto desenvolvido no âmbito da U.C. Ambientes de Desenvolvimento Colaborativo
(ISE, Universidade do Algarve).

## Requisitos

- Python 3.10 ou superior
- Nenhuma biblioteca externa (só módulos que já vêm com o Python)
- Funciona apenas na consola de texto

## Como correr

1. Clonar o repositório:

```bash
git clone https://github.com/erierierika-py/Gestao_de_despesas_pessoais
cd Gestao_de_despesas_pessoais
```

2. Iniciar a aplicação a partir da pasta principal:

```bash
python main.py
```

Na **primeira execução** a aplicação pede para criar uma palavra-passe. Nas execuções
seguintes pede essa palavra-passe (máximo de 3 tentativas).

Os dados ficam guardados em `data/dados.json`, que é criado automaticamente.

## Funcionalidades

**Despesas**
- Adicionar, consultar, editar e remover despesas
- Pesquisar despesas pela descrição
- Filtrar despesas por categoria, com o total da categoria
- Ver o gasto por categoria (valor e percentagem), de todos os meses ou de um mês específico

**Rendimentos**
- Registar, listar, alterar e eliminar rendimentos

**Saldo e histórico**
- Total de rendimentos, despesas e saldo, por mês
- Histórico mês a mês
- Aviso quando o saldo está a ficar baixo
- Definir um limite de gastos mensal e ver quanto falta para o atingir

**Poupança e pagamentos regulares**
- Definir um objetivo de poupança e acompanhar o progresso (percentagem e valor em falta)
- Registar subscrições (Netflix, ginásio...) e ver o total mensal

**Dados e segurança**
- Backup dos dados, com listagem e restauro
- Login com palavra-passe (guardada como hash com salt, nunca em texto)
- Menu de ajuda com instruções de utilização
- Validação dos dados introduzidos, com mensagens de erro

## Estrutura do projeto

```
Gestao_de_despesas_pessoais/
├── main.py               # Menu principal e ponto de entrada
├── README.md
├── requirements.txt
├── data/
│   └── dados.json        # Dados da aplicação (criado automaticamente)
├── src/
│   ├── dados.py          # Ler e guardar o ficheiro JSON
│   ├── login.py          # Login com palavra-passe (hash com salt)
│   ├── despesas.py       # Adicionar, consultar, editar e remover despesas
│   ├── rendimentos.py    # Registar, listar, alterar e eliminar rendimentos
│   ├── saldo.py          # Saldo, histórico mensal e limite de gastos
│   ├── pesquisa.py       # Pesquisa, filtro e gasto por categoria
│   ├── poupanca.py       # Objetivo de poupança e progresso
│   ├── subscricoes.py    # Pagamentos regulares
│   ├── backup.py         # Criar, listar e restaurar backups
│   ├── ajuda.py          # Instruções de utilização
│   └── utilitarios.py    # Funções auxiliares (ex.: confirmação s/n)
├── tests/                # Testes unitários (unittest)
└── backups/              # Cópias de segurança (criada automaticamente)
```

## Formato dos dados

Todos os dados ficam num único ficheiro, `data/dados.json`, que é lido e gravado pelo módulo `src/dados.py`. Exemplo:

```json
{
  "categorias": ["Alimentação", "Transportes", "Lazer"],
  "despesas": [
    {"id": 1, "descricao": "Pingo Doce", "valor": 23.5, "categoria": "Alimentação", "data": "2026-11-10"}
  ],
  "rendimentos": [
    {"id": 1, "descricao": "Salário", "tipo": "Salário", "valor": 900, "data": "2026-11-01"}
  ],
  "orcamento": {"limite_mensal": 500},
  "poupanca": {"objetivo": 1000},
  "subscricoes": [
    {"id": 1, "nome": "Netflix", "valor": 12.99, "categoria": "Lazer", "dia": 15}
  ],
  "login": {"salt": "...", "hash": "..."}
}
```

| Chave | Conteúdo |
|---|---|
| `categorias` | Lista de nomes de categorias |
| `despesas` | Lista de despesas (id, descrição, valor, categoria, data AAAA-MM-DD) |
| `rendimentos` | Lista de rendimentos (id, descrição, tipo, valor, data) |
| `orcamento` | Limite de gastos mensal (`limite_mensal`) |
| `poupanca` | Objetivo de poupança |
| `subscricoes` | Pagamentos regulares (id, nome, valor, categoria, dia do mês) |
| `login` | Salt e hash da palavra-passe (nunca a palavra-passe em texto) |

O ficheiro `dados.json` não vai para o GitHub (está no `.gitignore`), por isso cada pessoa tem os seus dados locais.

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
| `tests/test_login.py` | hash com salt e verificação da palavra-passe |
| `tests/test_rendimentos.py` | registo de rendimentos |
| `tests/test_saldo.py` | resumo mensal e saldo |
| `tests/test_utilitarios.py` | confirmação s/n |
| `tests/test_main.py` | menu principal |

Os testes usam dados criados dentro de cada teste, por isso não dependem do `data/dados.json` e não o alteram.

## Documentação

**Código:** todas as funções têm docstrings. A documentação em HTML é gerada com o [Sphinx](https://www.sphinx-doc.org):

```bash
pip install sphinx
cd docs
make html
```

Abre depois `docs/_build/html/index.html` no browser.

**Wiki:** o fluxo de trabalho com Git, a estrutura dos dados, as user stories e as decisões do projeto estão na [Wiki do repositório](https://github.com/erierierika-py/Gestao_de_despesas_pessoais/wiki).

## Fluxo de trabalho

- `main`: versão estável
- `develop`: integração
- `feature/...`: uma por funcionalidade, com Pull Request revisto por outro membro para o `develop`

## Grupo

| Membro | Contribuições |
|---|---|
| Erika | Backup, ajuda, subscrições, objetivo de poupança, pesquisa, filtro e gasto por categoria, login, testes |
| Dalila | Rendimentos, saldo e histórico mensal, aviso de saldo baixo |
| Rodrigo | Despesas (adicionar, consultar, editar, remover), limite de gastos mensal |