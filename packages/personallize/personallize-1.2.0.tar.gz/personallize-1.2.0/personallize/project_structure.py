"""
Módulo para criação de estrutura de projeto em camadas.

Este módulo fornece funcionalidades para criar automaticamente
uma estrutura de projeto organizada em camadas seguindo boas práticas.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectConfig:
    """Configuração para criação da estrutura do projeto."""

    project_name: str
    base_path: str = "./"
    create_git_files: bool = True
    create_docker_files: bool = False
    create_tests: bool = True
    python_version: str = "3.11"


class StructureManager:
    """Gerador de estrutura de projeto em camadas."""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.base_path = Path(config.base_path)

    def create_project_structure(self) -> str:
        """
        Cria a estrutura completa do projeto.

        Returns:
            str: Caminho do projeto criado
        """
        # Cria diretório base do projeto
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Cria estrutura de pastas
        self._create_folder_structure()

        # Cria arquivos base
        self._create_base_files()

        # Cria arquivos de configuração
        self._create_config_files()

        # Cria arquivos opcionais
        if self.config.create_git_files:
            self._create_git_files()

        if self.config.create_docker_files:
            self._create_docker_files()

        if self.config.create_tests:
            self._create_test_structure()

        return str(self.base_path)

    def _create_folder_structure(self) -> None:
        """Cria a estrutura de pastas do projeto."""
        folders = [
            "src",
            "src/configs",
            "src/controller",
            "src/main",
            "src/schemas",
            "src/models",
            "src/models/entities",
            "src/models/config",
            "src/models/repository",
            "src/services",
            "src/utils",
            "tests",
            "docs",
        ]

        for folder in folders:
            folder_path = self.base_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)

            # Cria __init__.py em pastas Python
            if folder.startswith("src") or folder == "tests":
                init_file = folder_path / "__init__.py"
                init_file.touch()

    def _create_base_files(self) -> None:
        """Cria arquivos base do projeto."""

        # src/main/__init__.py
        main_init = self.base_path / "src" / "main" / "__init__.py"
        main_init.write_text('"""Módulo principal da aplicação."""\n', encoding="utf-8")

        # src/main/app.py
        app_content = '''"""Aplicação principal."""

from src.configs.environments import get_settings
from src.configs.logs import setup_logging


def create_app():
    """Cria e configura a aplicação."""
    settings = get_settings()
    setup_logging(settings.log_level)

    # Configurar sua aplicação aqui

    return "app"


if __name__ == "__main__":
    app = create_app()
    print("Aplicação iniciada!")
'''
        (self.base_path / "src" / "main" / "app.py").write_text(app_content, encoding="utf-8")

        # requirements.txt
        requirements_content = """# Dependências principais
pydantic>=2.0.0
python-dotenv>=1.0.0

# Dependências de desenvolvimento
pytest>=7.0.0
blue>=0.9.0
ruff>=0.1.0
mypy>=1.0.0
"""
        (self.base_path / "requirements.txt").write_text(requirements_content, encoding="utf-8")

        # README.md
        readme_content = f"""# {self.config.project_name}

Descrição do projeto.

## Estrutura do Projeto

```
{self.config.project_name}/
├── src/
│   ├── configs/          # Configurações da aplicação
│   ├── controller/       # Controladores/Endpoints
│   ├── main/            # Aplicação principal
│   ├── schemas/         # Schemas de validação
│   ├── models/          # Modelos de dados
│   │   ├── entities/    # Entidades do domínio
│   │   ├── config/      # Configurações de modelo
│   │   └── repository/  # Repositórios
│   ├── services/        # Lógica de negócio
│   └── utils/           # Utilitários
├── tests/               # Testes
├── docs/                # Documentação
└── requirements.txt     # Dependências
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -m src.main.app
```

## Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements.txt

# Executar testes
pytest

# Formatação de código
blue src/ tests/

# Linting
ruff check src/ tests/
```
"""
        (self.base_path / "README.md").write_text(readme_content, encoding="utf-8")

        # src/models/config/connection.py
        connection_content = '''"""Configuração de conexão com banco de dados."""

from personallize import Connection, Credentials
from src.configs.environments import get_settings


def get_connection() -> Connection:
    """Retorna uma conexão configurada com o banco de dados."""
    settings = get_settings()

    # Criar credenciais baseadas nas configurações
    creds = Credentials(
        db_type=settings.db_type,
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_database,
        database_path=settings.db_database_path,
        odbc_driver=settings.db_odbc_driver
    )

    return Connection(creds)


# Instância global da conexão
connection = get_connection()
'''
        (self.base_path / "src" / "models" / "config" / "connection.py").write_text(
            connection_content, encoding="utf-8"
        )

    def _create_config_files(self) -> None:
        """Cria arquivos de configuração."""

        # src/configs/environments.py
        env_content = (
            '''"""Configurações de ambiente."""

import os
from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Configurações básicas
    app_name: str = "'''
            + self.config.project_name
            + '''"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # Configurações de log
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configurações de banco de dados (Credentials)
    db_type: str = "sqlite"
    db_host: str | None = None
    db_port: int | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_database: str | None = None
    db_database_path: str | None = "./app.db"
    db_odbc_driver: int | str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Retorna as configurações da aplicação."""
    return Settings()
'''
        )
        (self.base_path / "src" / "configs" / "environments.py").write_text(
            env_content, encoding="utf-8"
        )

        # src/configs/logs.py
        logs_content = '''"""Configuração de logs."""

from personallize import LogManager


def setup_logging() -> LogManager:
    """Configura o sistema de logs usando complex_log."""
    log_manager = LogManager()
    return log_manager.development()


def get_logger() -> LogManager:
    """Retorna um logger configurado."""
    return setup_logging()
'''
        (self.base_path / "src" / "configs" / "logs.py").write_text(logs_content, encoding="utf-8")

        # .env (exemplo)
        env_example = f"""# Configurações de ambiente para {self.config.project_name}

# Ambiente
ENVIRONMENT=development
DEBUG=true

# Logs
LOG_LEVEL=INFO

# Configurações de banco de dados (Credentials)
DB_TYPE=sqlite
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_DATABASE=database
DB_DATABASE_PATH=./app.db
DB_ODBC_DRIVER=17

"""
        (self.base_path / ".env.example").write_text(env_example, encoding="utf-8")

    def _create_git_files(self) -> None:
        """Cria arquivos relacionados ao Git."""

        gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
"""
        (self.base_path / ".gitignore").write_text(gitignore_content, encoding="utf-8")

    def _create_docker_files(self) -> None:
        """Cria arquivos Docker."""

        dockerfile_content = f"""FROM python:{self.config.python_version}-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY src/ src/

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "-m", "src.main.app"]
"""
        (self.base_path / "Dockerfile").write_text(dockerfile_content, encoding="utf-8")

        docker_compose_content = f"""version: '3.8'

services:
  {self.config.project_name}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      - ./logs:/app/logs
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: {self.config.project_name}
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
"""
        (self.base_path / "docker-compose.yml").write_text(docker_compose_content, encoding="utf-8")

    def _create_test_structure(self) -> None:
        """Cria estrutura de testes."""

        # tests/conftest.py
        conftest_content = '''"""Configuração dos testes."""

import pytest
from src.configs.environments import get_settings


@pytest.fixture
def settings():
    """Fixture para configurações de teste."""
    return get_settings()


@pytest.fixture
def sample_data():
    """Fixture com dados de exemplo para testes."""
    return {
        "test_data": "example"
    }
'''
        (self.base_path / "tests" / "conftest.py").write_text(conftest_content, encoding="utf-8")

        # tests/test_main.py
        test_main_content = '''"""Testes para o módulo principal."""

from src.main.app import create_app


def test_create_app():
    """Testa a criação da aplicação."""
    app = create_app()
    assert app is not None


def test_app_configuration(settings):
    """Testa a configuração da aplicação."""
    assert settings.app_name is not None
    assert settings.environment in ["development", "staging", "production"]
'''
        (self.base_path / "tests" / "test_main.py").write_text(test_main_content, encoding="utf-8")


def create_layered_project(project_name: str, base_path: str = "./", **kwargs) -> str:
    """
    Função de conveniência para criar um projeto em camadas.

    Args:
        project_name: Nome do projeto
        base_path: Caminho base onde criar o projeto
        **kwargs: Argumentos adicionais para ProjectConfig

    Returns:
        str: Caminho do projeto criado
    """
    config = ProjectConfig(project_name=project_name, base_path=base_path, **kwargs)

    generator = StructureManager(config)
    return generator.create_project_structure()
