#!/usr/bin/env python3
"""
Módulo principal para execução via linha de comando.
Permite executar: python -m personallize --init [path]
"""

import argparse
import sys
from pathlib import Path

from personallize.project_structure import ProjectConfig, StructureManager


def create_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        prog="personallize",
        description="Gerador de estrutura de projetos Python em camadas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m personallize --init                    # Cria projeto no diretório atual
  python -m personallize --init ./meu_projeto      # Cria projeto em ./meu_projeto
  python -m personallize --init /path/to/project   # Cria projeto no path especificado
        """,
    )

    parser.add_argument(
        "--init",
        nargs="?",
        const=".",
        default=None,
        metavar="PATH",
        help="Inicializa um novo projeto no path especificado (padrão: diretório atual)",
    )

    parser.add_argument(
        "--name", type=str, default="my_project", help="Nome do projeto (padrão: my_project)"
    )

    parser.add_argument(
        "--no-git", action="store_true", help="Não criar arquivos Git (.gitignore, etc.)"
    )

    parser.add_argument(
        "--docker",
        action="store_true",
        help="Criar arquivos Docker (Dockerfile, docker-compose.yml)",
    )

    parser.add_argument("--no-tests", action="store_true", help="Não criar estrutura de testes")

    parser.add_argument(
        "--python-version",
        type=str,
        default="3.11",
        help="Versão do Python para o projeto (padrão: 3.11)",
    )

    return parser


def init_project(
    path: str,
    project_name: str,
    create_git_files: bool = True,
    create_docker_files: bool = False,
    create_tests: bool = True,
    python_version: str = "3.11",
) -> None:
    """
    Inicializa um novo projeto na estrutura especificada.

    Args:
        path: Caminho onde criar o projeto
        project_name: Nome do projeto
        create_git_files: Se deve criar arquivos Git
        create_docker_files: Se deve criar arquivos Docker
        create_tests: Se deve criar estrutura de testes
        python_version: Versão do Python
    """
    try:
        # Resolve o path absoluto
        target_path = Path(path).resolve()

        # Cria a configuração do projeto
        config = ProjectConfig(
            project_name=project_name,
            base_path=str(target_path),
            create_git_files=create_git_files,
            create_docker_files=create_docker_files,
            create_tests=create_tests,
            python_version=python_version,
        )

        # Cria o gerenciador de estrutura
        manager = StructureManager(config)

        # Cria a estrutura do projeto
        print(f"Criando projeto '{project_name}' em: {target_path}")
        created_path = manager.create_project_structure()

        print(f"✅ Projeto criado com sucesso em: {created_path}")
        print("\nPróximos passos:")
        print(f"  cd {target_path}")
        print("  pip install -r requirements.txt")
        print("  # Configurar .env baseado em .env.example")

    except Exception as e:
        print(f"❌ Erro ao criar projeto: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Função principal da CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Se --init não foi especificado, mostra ajuda
    if args.init is None:
        parser.print_help()
        return

    # Executa a inicialização do projeto
    init_project(
        path=args.init,
        project_name=args.name,
        create_git_files=not args.no_git,
        create_docker_files=args.docker,
        create_tests=not args.no_tests,
        python_version=args.python_version,
    )


if __name__ == "__main__":
    main()
