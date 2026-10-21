# GitHub Actions

Projeto desenvolvido para o exercício **Implementando Integração Contínua (CI) com GitHub Actions**, que faz parte da disciplina de **Automação de Testes de Software**. O objetivo é criar uma API simples, automatizar seus testes e demonstrar como o CI impede que alterações com erro avancem no repositório.


## Estrutura do projeto

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── assets/
│   └── Exercício ATS12.pdf
├── main.py
├── requirements.txt
├── test_main.py
└── README.md
```

## Executando localmente

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute os testes:

```bash
pytest test_main.py
```

Inicie a API:

```bash
fastapi run main.py --port 8000
```

As rotas disponíveis são:

- `GET /` — verifica se a API está funcionando.
- `GET /somar/{a}/{b}` — soma dois números.
- `GET /multiplicar/{a}/{b}` — multiplica dois números.

## Pipeline de CI

O workflow [ci.yml](.github/workflows/ci.yml) é executado a cada `push`. O job `verificar-api`:

1. Faz o checkout do código.
2. Configura Python nas versões 3.10, 3.11 e 3.12 usando uma `strategy matrix`.
3. Instala as dependências.
4. Executa os testes automatizados com Pytest.
5. Inicia a API em segundo plano.
6. Usa `curl -f` para fazer requisições reais às rotas `/` e `/somar/10/20`.

Se qualquer teste ou requisição falhar, o workflow falha e sinaliza que a alteração precisa ser corrigida.

## Passo a passo dos commits

Os commits abaixo seguem a sequência proposta no enunciado, disponível em [assets/Exercício ATS12.pdf](assets/Exercício%20ATS12.pdf).

### 1. Primeira versão da API e do CI

**Commit:** `d2eb925 feat: subindo primeira versão`

Foi criada a base do projeto:

- API FastAPI em `main.py`.
- Rota `/`.
- Rota `/somar/{a}/{b}`.
- Testes para as rotas existentes em `test_main.py`.
- Dependências em `requirements.txt`.
- Workflow inicial do GitHub Actions, usando Python 3.11 e executando o Pytest.

Depois desse commit, o código foi enviado ao repositório remoto para verificar a primeira execução bem-sucedida do workflow.

### 2. Simulação de um erro na função de soma

**Commit:** `5b97556 feat: subindo erro na função somar`

A função de soma foi alterada intencionalmente de:

```python
return {"resultado": a + b}
```

para:

```python
return {"resultado": a - b}
```

O teste continuou esperando o resultado correto da soma. Por isso, o GitHub Actions falhou no passo `Rodar testes`.

O diagnóstico esperado do Pytest é:

- Para `/somar/5/3`, o teste esperava `{"resultado": 8}`.
- A API retornou `{"resultado": 2}`.

Esse commit demonstrou que o CI identifica o bug antes que ele seja aceito como código válido.

### 3. Correção da função de soma

**Commit:** `53dc29f fix: corrigindo função somar`

A implementação foi corrigida, restaurando a operação de adição. Com isso, os testes voltaram a passar e a branch principal ficou verde novamente.

### 4. Criação da funcionalidade de multiplicação em uma branch

**Branch:** `feature-multiplicacao`

**Commit:** `356d997 feat: subindo erro na função multiplicar`

Foi criada a rota `/multiplicar/{a}/{b}` e adicionado um teste para ela. O teste foi enviado propositalmente com a expectativa incorreta:

```python
assert response.json() == {"resultado": 5}
```

Como `3 * 2` resulta em `6`, o CI falhou no Pull Request. Isso demonstrou o bloqueio do merge enquanto o status check `verificar-api` estivesse com erro.

### 5. Correção do teste e merge do Pull Request

**Commit:** `6c709fe fix: corrigindo erro no teste da função multiplicar`

A expectativa do teste foi corrigida para:

```python
assert response.json() == {"resultado": 6}
```

O workflow passou, o Pull Request foi atualizado automaticamente e pôde ser integrado à branch `master` no commit de merge:

**Merge:** `e4bed7c Merge pull request #1 from Felipewv93/feature-multiplicacao`

### 6. Execução em múltiplas versões do Python

**Commit:** `c0d6e3a ci: att ci que usa strategy matrix`

O workflow deixou de testar somente Python 3.11 e passou a executar o mesmo job nas versões:

```yaml
python-version: ['3.10', '3.11', '3.12']
```

A configuração dinâmica utilizada pelo `setup-python` é:

```yaml
python-version: ${{ matrix.python-version }}
```

Assim, o pipeline verifica a compatibilidade da API sem duplicar o arquivo YAML.

### 7. Adição do teste de integração

**Commit:** `f563634 ci: att ci com teste de integração`

Além dos testes unitários, o workflow passou a iniciar a API no runner e fazer requisições HTTP reais:

```yaml
fastapi run main.py --port 8000 &
sleep 3
curl -f http://localhost:8000/
curl -f http://localhost:8000/somar/10/20
```

O parâmetro `-f` faz o `curl` retornar erro quando a resposta HTTP indica falha, permitindo que o GitHub Actions também valide o funcionamento da aplicação em execução.

## Resultado final

Ao final do exercício, o projeto possui:

- Testes automatizados para as rotas da API.
- CI executado automaticamente a cada `push`.
- Validação em Python 3.10, 3.11 e 3.12.
- Proteção demonstrada por falhas intencionais nos testes.
- Fluxo de desenvolvimento com branch e Pull Request.
- Teste de integração com a API em execução no runner.

## Autor

**Felipe Viana**