# Personallize

Uma biblioteca Python com ferramentas essenciais para desenvolvimento de RPA (Robotic Process Automation) e ML (Machine Learning), oferecendo recursos para conexão com bancos de dados, logging, geração de estruturas de projeto e interface de linha de comando.

## ✨ Funcionalidades

- 🏗️ **CLI Project Generator**: Interface de linha de comando para criação de projetos
- 🗄️ **EntityFactory**: Geração automática de entidades SQLAlchemy a partir de DataFrames
- 🏗️ **ProjectStructureGenerator**: Criação automática de estrutura de projeto em camadas
- 🔌 **Connection**: Conexão simplificada com bancos de dados
- 📊 **Logging**: Sistema de logging simples e avançado
- 🌐 **WebDriver Factory**: Criação automatizada de drivers para automação web

## 📋 Requisitos

- Python >= 3.11
- SQLAlchemy >= 2.0.0
- Selenium >= 4.0.0
- Rich >= 12.0.0

## 📦 Instalação

### Com pip

```bash
pip install personallize
```

### Com uv (recomendado)

```bash
uv add personallize
```

### Para desenvolvimento

```bash
# Com pip
pip install personallize[dev]

# Com uv
uv add personallize --optional dev
```

## 🚀 Uso

### 🖥️ Interface de Linha de Comando (CLI)

Após a instalação, você pode usar o comando `personallize` diretamente no terminal:

```bash
# Criar projeto no diretório atual
personallize --init

# Criar projeto em um diretório específico
personallize --init ./meu_projeto

# Criar projeto com nome personalizado
personallize --init ./meu_projeto --name "nome_do_projeto"

# Ver todas as opções disponíveis
personallize --help
```

#### Opções da CLI

- `--init [PATH]`: Inicializa projeto no path especificado (padrão: diretório atual)
- `--name NAME`: Nome do projeto (padrão: my_project)
- `--no-git`: Não criar arquivos Git (.gitignore, etc.)
- `--docker`: Criar arquivos Docker (Dockerfile, docker-compose.yml)
- `--no-tests`: Não criar estrutura de testes
- `--python-version VERSION`: Versão do Python (padrão: 3.11)

#### Usando com Python

```bash
# Alternativa usando python -m
python -m personallize --init ./meu_projeto

# Com uv
uv run python -m personallize --init ./meu_projeto
```

### 🏗️ Estrutura de Projeto Gerada

O comando CLI cria uma estrutura completa de projeto:

```
meu_projeto/
├── .env.example              # Configurações de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação do projeto
├── requirements.txt         # Dependências (com blue formatter)
├── docs/                    # Documentação
├── src/                     # Código fonte
│   ├── __init__.py
│   ├── configs/             # Configurações
│   │   ├── __init__.py
│   │   └── environments.py  # Configurações de ambiente
│   ├── controller/          # Controladores
│   ├── main/               # Arquivos principais
│   ├── models/             # Modelos de dados
│   │   └── config/
│   │       └── connection.py # Conexão com BD
│   ├── schemas/            # Esquemas de dados
│   ├── services/           # Serviços de negócio
│   └── utils/              # Utilitários
│       └── logs.py         # Sistema de logging
└── tests/                  # Testes
    ├── __init__.py
    ├── conftest.py
    └── test_main.py
```

### 🗄️ EntityFactory - Geração Automática de Entidades

```python
import pandas as pd
from personallize.entity_factory import EntityFactory, EntityConfig

# Criar DataFrame de exemplo
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['João', 'Maria', 'Pedro'],
    'email': ['joao@email.com', 'maria@email.com', 'pedro@email.com'],
    'age': [25, 30, 35],
    'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])
})

# Configurar EntityFactory
config = EntityConfig(
    auto_add_id=True,
    detect_relationships=True,
    add_indexes=True,
    add_timestamps=True
)

# Criar factory e gerar entidade
factory = EntityFactory(config)
entity_path = factory.create_entity_from_dataframe(df, "User", "./models/")

print(f"Entidade criada em: {entity_path}")
```

### 🏗️ ProjectStructureGenerator - Programático

```python
from personallize.project_structure import create_layered_project, ProjectConfig

# Criar projeto com estrutura em camadas
project_path = create_layered_project(
    project_name="meu_projeto",
    base_path="./",
    create_git_files=True,
    create_docker_files=True,
    create_tests=True,
    python_version="3.11"
)

print(f"Projeto criado em: {project_path}")
```

### 🔌 Conexão com Banco de Dados

```python
from personallize import Connection, Credentials

# Configurar credenciais
credentials = Credentials(
    host='localhost',
    database='exemplo.db',
    username='user',
    password='password'
)

# Criar conexão
conn = Connection('sqlite', credentials)

# Usar conexão
with conn.get_connection() as db:
    result = db.execute("SELECT * FROM users")
    print(result.fetchall())
```

### 📊 Sistema de Logging

```python
from personallize import LogManager

# Logging simples para desenvolvimento
logger = LogManager().development()
logger.info("Aplicação iniciada")
logger.error("Erro encontrado")

# Logging para produção
logger = LogManager().production()
logger.info("Sistema em produção")
```

## 🚀 Recursos Detalhados

### 📊 Connection

Módulo flexível para conexão com diversos bancos de dados:

- SQLite
- MySQL
- PostgreSQL
- SQL Server

### 📝 Logs

Sistema de logging com duas opções:

**Simple Log (`simple_log`):**
- Logging básico e direto
- Ideal para projetos simples

**Complex Log (`complex_log`):**
- Sistema avançado com configurações flexíveis
- Presets: `simple()`, `development()`, `production()`
- Suporte a queue para logging assíncrono
- Gerar logs em arquivo
- Personalização completa de formatos e níveis de log
- Decorators para captura de exceções

### 🏗️ Gerador de Estruturas

**Características dos projetos gerados:**
- Estrutura MVC em camadas
- Configuração de ambiente com `.env.example`
- Sistema de logging integrado com `LogManager`
- Conexão com banco de dados configurada
- Formatação de código com `blue`
- Estrutura de testes com `pytest`
- Documentação básica

### 🌐 WebDriver

Ferramentas para automação web:
- Gerenciamento customizado do ChromeDriver
- Manipulação avançada de WebDriver
- Integração com Selenium

## 🔧 Desenvolvimento

### Executando testes

```bash
# Com pytest
pytest

# Com uv
uv run pytest
```

### Formatação de código

```bash
# Com blue (recomendado)
blue src/ tests/

# Com uv
uv run blue src/ tests/
```

### Linting

```bash
# Com ruff
ruff check src/ tests/

# Com uv
uv run ruff check src/ tests/
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Miguel Tenório**

- Email: `deepydev42@gmail.com`
- GitHub: [@MiguelTenorio42](https://github.com/MiguelTenorio42)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um Pull Request.

## 📝 Changelog

### v1.1.0
- ✨ **Nova funcionalidade**: Interface de linha de comando (CLI)
- 🏗️ **Melhoria**: Estrutura de projeto atualizada com `LogManager`
- 🔧 **Melhoria**: Configuração de ambiente com `Credentials`
- 🎨 **Melhoria**: Formatador alterado de `black` para `blue`
- 📦 **Melhoria**: Suporte para Python 3.11+
- 🐛 **Correção**: Estrutura de projeto agora cria arquivos no diretório correto

### v1.0.1
- 🐛 Correções de bugs menores
- 📚 Melhorias na documentação

### v1.0.0
- 🎉 Lançamento inicial
- 🗄️ EntityFactory
- 🔌 Sistema de conexão com bancos de dados
- 📊 Sistema de logging
- 🌐 WebDriver Factory
