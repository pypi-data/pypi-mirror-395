# Bifrons

CLI para automação de versões SemVer baseada em títulos de PR/commit.

## Descrição

O Bifrons analisa o título de uma PR ou commit e incrementa automaticamente a versão seguindo as regras do [Semantic Versioning (SemVer)](https://semver.org/). Ele classifica o título em:
- **patch** (correções): títulos começando com "fix"
- **minor** (novos recursos): títulos começando com "feat" ou "feature"
- **major** (mudanças incompatíveis): títulos começando com "breaking", "major" ou contendo "breaking change"

A versão atual é lida/escrita no arquivo [`version.txt`](version.txt ) no diretório atual.

## Instalação

1. Certifique-se de ter Python 3.8+ instalado.
2. Clone o repositório e instale em modo editável:
   ```
   git clone https://github.com/Kalimbinha/Bifrons.git
   cd Bifrons
   pip install -e .
   ```

## Uso

Execute o comando com o título da PR/commit:

```
bifrons --title "fix: correção de bug"
```

### Exemplos

- **Patch (correção)**:
  ```
  bifrons --title "fix: resolve memory leak"
  ```
  Saída:
  ```
  [bifrons] versão anterior: 1.0.0
  [bifrons] nova versão: 1.0.1
  ```

- **Minor (novo recurso)**:
  ```
  bifrons --title "feat: add dark mode"
  ```
  Saída:
  ```
  [bifrons] versão anterior: 1.0.1
  [bifrons] nova versão: 1.1.0
  ```

- **Major (mudança incompatível)**:
  ```
  bifrons --title "breaking: remove deprecated API"
  ```
  Saída:
  ```
  [bifrons] versão anterior: 1.1.0
  [bifrons] nova versão: 2.0.0
  ```

- **Título inválido**:
  ```
  bifrons --title "random title"
  ```
  Saída:
  ```
  Erro: Título inválido! Use fix/feat/major
  ```

### Arquivo de Versão

- O arquivo [`version.txt`](version.txt ) é criado automaticamente se não existir (inicia com `0.0.0`).
- Ele contém apenas a versão atual (ex.: `1.2.3`).
- Execute no diretório onde deseja gerenciar a versão.

## Desenvolvimento

- **Estrutura do Projeto**:
  ```
  Bifrons/
  ├── bifrons/
  │   ├── __init__.py
  │   ├── cli.py       # Interface de linha de comando
  │   └── core.py      # Lógica principal
  ├── pyproject.toml   # Configuração do projeto
  ├── README.md        # Este arquivo
  └── version.txt      # Arquivo de versão (gerado)
  ```

- **Testes**: Execute `pytest` para rodar os testes em `tests/`.
- **Linting**: Use `black bifrons/` para formatar o código.

## Autor

Fernando Barreto (kalimbinhaa@gmail.com)

## Licença

MIT License. Veja o arquivo LICENSE para detalhes.
