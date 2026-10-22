# Desafio QA Automation

Automação do DemoQA em Python. A parte 1 testa a API; a parte 2 testa a interface com Selenium e Page Object Model.

## Estrutura

```text
api/            Chamadas da API de contas e livros
pages/          Ações e seletores das páginas
tests/api/      Fluxo da API
tests/ui/       Cenários de interface
tests/fixtures/ Arquivo usado no upload do Practice Form
features/       Cenário BDD com 12 registros
```

O arquivo [`tests/fixtures/natalia teste.txt`](tests/fixtures/natalia%20teste.txt) é usado no upload do cenário **Forms → Practice Form**.

## Preparação no Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se `.venv` já existir, execute apenas o comando de instalação. Para o teste de interface, tenha o Chrome instalado. O Selenium gerencia o driver automaticamente quando o ambiente permite.

## Execução

Para depurar um teste no VS Code, abra a pasta `desafio`, abra o arquivo de teste, selecione **Python: arquivo atual** em *Run and Debug* e pressione F5.

Para executar o fluxo de API diretamente no PowerShell:

```powershell
.\.venv\Scripts\python.exe tests\api\test_book_flow.py
```

Para executar todos os testes de API e interface pelo pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Para executar o cenário BDD:

```powershell
.\.venv\Scripts\python.exe -m behave features\web_tables_12_records.feature --no-capture
```

No VS Code, selecione **BDD: 12 registros** no Debug e pressione F5.

O teste de API cria um usuário novo a cada execução, gera um token, confirma a autorização, escolhe dois livros disponíveis, adiciona os livros e verifica a coleção final do usuário. Os testes de interface também dependem de acesso ao DemoQA. Se o serviço mudar ou ficar indisponível, a falha deve ser analisada antes de alterar as asserções.

## Cenário BDD

O arquivo `features/web_tables_12_records.feature` descreve o cenário em português. Cada frase chama uma função em `features/steps/web_tables_steps.py`. O arquivo `features/environment.py` abre o Chrome antes do cenário e o fecha no final.

O cenário cria 12 registros com e-mails diferentes e confere os 12. Ele reutiliza as ações de `pages/web_tables_page.py`. O [Behave](https://cucumber.io/docs/installation/python/) é a implementação de BDD/Gherkin para Python listada pelo Cucumber.

A exclusão dos 12 registros, indicada como bônus no desafio, não faz parte deste cenário.

