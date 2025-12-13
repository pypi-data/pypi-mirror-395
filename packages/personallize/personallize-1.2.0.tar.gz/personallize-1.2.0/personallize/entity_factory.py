from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Constantes para tamanhos de string
STRING_LENGTH_SMALL = 50
STRING_LENGTH_MEDIUM = 100
STRING_LENGTH_STANDARD = 255
STRING_LENGTH_LARGE = 500
STRING_LENGTH_MAX = 1000

# Constantes para detecção de índices
MIN_UNIQUE_RATIO = 0.1
MAX_UNIQUE_RATIO = 0.8

# Margem de segurança para cálculo de tamanho de string
STRING_LENGTH_MARGIN = 1.5


@dataclass
class EntityConfig:
    """Configurações para geração de entities"""

    auto_add_id: bool = True
    id_column_name: str = "id"
    detect_relationships: bool = True
    add_indexes: bool = True
    string_max_length: int = STRING_LENGTH_STANDARD
    detect_nullable: bool = True
    add_timestamps: bool = False


class EntityFactory:
    """Factory para criação de entities SQLAlchemy a partir de DataFrames pandas"""

    def __init__(self, config: EntityConfig | None = None):
        self.config = config or EntityConfig()

        # Mapeamento de tipos pandas/numpy para SQLAlchemy
        self.type_mapping = {
            # Tipos Python básicos
            str: "String",
            int: "Integer",
            float: "Float",
            bool: "Boolean",
            datetime: "DateTime",
            # Tipos pandas/numpy
            pd.StringDtype(): "String",
            pd.Int64Dtype(): "Integer",
            pd.Float64Dtype(): "Float",
            pd.BooleanDtype(): "Boolean",
            # Tipos numpy
            np.int64: "Integer",
            np.int32: "Integer",
            np.float64: "Float",
            np.float32: "Float",
            np.bool_: "Boolean",
            np.object_: "String",
            # Tipos datetime
            np.datetime64: "DateTime",
            pd.Timestamp: "DateTime",
        }

    def analyze_dataframe(self, df: pd.DataFrame) -> dict[str, dict[str, Any]]:
        """Analisa um DataFrame e retorna informações sobre as colunas"""
        column_info = {}

        for col_name in df.columns:
            col_data = df[col_name]

            # Detecta o tipo da coluna
            col_type = self._detect_column_type(col_data)

            # Verifica se pode ser nula
            nullable = col_data.isna().any() if self.config.detect_nullable else True

            # Detecta se é chave estrangeira
            is_foreign_key = self._detect_foreign_key(col_name)

            # Detecta se precisa de índice
            needs_index = self._should_have_index(col_name, col_data)

            # Calcula tamanho máximo para strings
            max_length = self._calculate_string_length(col_data) if col_type is str else None

            column_info[col_name] = {
                "type": col_type,
                "nullable": nullable,
                "is_foreign_key": is_foreign_key,
                "needs_index": needs_index,
                "max_length": max_length,
                "unique_values": col_data.nunique(),
                "sample_values": col_data.dropna().head(3).tolist(),
            }

        return column_info

    def _detect_column_type(self, series: pd.Series) -> type:
        """Detecta o tipo mais apropriado para uma coluna"""
        # Remove valores nulos para análise
        clean_series = series.dropna()

        if clean_series.empty:
            return str

        # Verifica se é datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return datetime

        # Verifica se é numérico
        if pd.api.types.is_numeric_dtype(series):
            # Verifica se todos os valores são inteiros
            if pd.api.types.is_integer_dtype(series):
                return int
            return float

        # Verifica se é booleano
        if pd.api.types.is_bool_dtype(series):
            return bool

        # Tenta converter para datetime
        if series.dtype == "object":
            try:
                pd.to_datetime(clean_series.head(100))
            except (ValueError, TypeError):
                # Default para string se não conseguir converter
                return str
            else:
                return datetime

        # Default para string
        return str

    def _detect_foreign_key(self, col_name: str) -> bool:
        """Detecta se uma coluna é provavelmente uma chave estrangeira"""
        fk_patterns = ["_id", "id_", "fk_", "_fk"]
        return any(pattern in col_name.lower() for pattern in fk_patterns)

    def _should_have_index(self, col_name: str, series: pd.Series) -> bool:
        """Determina se uma coluna deveria ter um índice"""
        if not self.config.add_indexes:
            return False

        # Colunas com poucos valores únicos podem precisar de índice
        unique_ratio = series.nunique() / len(series) if len(series) > 0 else 0

        # Padrões de nomes que geralmente precisam de índice
        index_patterns = ["email", "username", "code", "slug", "name"]
        has_index_pattern = any(pattern in col_name.lower() for pattern in index_patterns)

        return has_index_pattern or (MIN_UNIQUE_RATIO <= unique_ratio <= MAX_UNIQUE_RATIO)

    def _calculate_string_length(self, series: pd.Series) -> int:
        """Calcula o tamanho máximo apropriado para uma coluna string"""
        if series.dtype != "object":
            return self.config.string_max_length

        # Remove valores nulos e calcula o tamanho máximo
        clean_series = series.dropna().astype(str)
        if clean_series.empty:
            return self.config.string_max_length

        max_len = clean_series.str.len().max()

        # Adiciona uma margem de segurança
        suggested_length = min(max_len * STRING_LENGTH_MARGIN, STRING_LENGTH_MAX)

        # Usa tamanhos padrão baseados em constantes
        length_thresholds = [
            (STRING_LENGTH_SMALL, STRING_LENGTH_SMALL),
            (STRING_LENGTH_MEDIUM, STRING_LENGTH_MEDIUM),
            (STRING_LENGTH_STANDARD, STRING_LENGTH_STANDARD),
            (STRING_LENGTH_LARGE, STRING_LENGTH_LARGE),
        ]

        for threshold, return_value in length_thresholds:
            if suggested_length <= threshold:
                return return_value

        return STRING_LENGTH_MAX

    def create_entity_from_dataframe(
        self, df: pd.DataFrame, entity_name: str, output_path: str = "./"
    ) -> str:
        """Cria um arquivo entity a partir de um DataFrame pandas"""

        # Analisa o DataFrame
        column_info = self.analyze_dataframe(df)

        # Adiciona coluna ID se necessário
        if self.config.auto_add_id and self.config.id_column_name not in column_info:
            column_info = {
                self.config.id_column_name: {
                    "type": int,
                    "nullable": False,
                    "is_foreign_key": False,
                    "needs_index": False,
                    "max_length": None,
                },
                **column_info,
            }

        # Adiciona timestamps se necessário
        if self.config.add_timestamps:
            timestamp_columns = {
                "created_at": {
                    "type": datetime,
                    "nullable": False,
                    "is_foreign_key": False,
                    "needs_index": False,
                    "max_length": None,
                },
                "updated_at": {
                    "type": datetime,
                    "nullable": True,
                    "is_foreign_key": False,
                    "needs_index": False,
                    "max_length": None,
                },
            }
            column_info.update(timestamp_columns)

        return self._generate_entity_file(entity_name, column_info, output_path)

    def create_entity_file(
        self, entity_name: str, columns: dict[str, type], output_path: str = "./"
    ) -> str:
        """Método de compatibilidade com a versão anterior"""
        # Converte o formato antigo para o novo
        column_info = {}
        for col_name, col_type in columns.items():
            column_info[col_name] = {
                "type": col_type,
                "nullable": col_name != self.config.id_column_name,
                "is_foreign_key": self._detect_foreign_key(col_name),
                "needs_index": False,
                "max_length": self.config.string_max_length if col_type is str else None,
            }

        return self._generate_entity_file(entity_name, column_info, output_path)

    def _generate_entity_file(
        self, entity_name: str, column_info: dict[str, dict[str, Any]], output_path: str
    ) -> str:
        """Gera o arquivo da entity"""

        # Imports necessários
        imports = [
            "from datetime import datetime",
            "from sqlalchemy import String, Integer, DateTime, Boolean, Float, Index, ForeignKey",
            "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column",
        ]

        # Verifica se precisa de ForeignKey
        has_foreign_keys = any(col["is_foreign_key"] for col in column_info.values())
        if has_foreign_keys:
            imports[2] += ", ForeignKey"

        content = "\n".join(imports) + "\n\n"

        # Base class
        content += "class Base(DeclarativeBase):\n    pass\n\n"

        # Entity class
        class_name = entity_name.capitalize()
        table_name = entity_name.lower()

        content += f"class {class_name}(Base):\n"
        content += f'    __tablename__ = "{table_name}"\n\n'

        # Colunas
        indexes = []
        for col_name, col_info in column_info.items():
            col_type = col_info["type"]
            nullable = col_info["nullable"]
            is_primary = col_name == self.config.id_column_name
            is_fk = col_info["is_foreign_key"]
            needs_index = col_info["needs_index"]
            max_length = col_info.get("max_length")

            # Tipo SQLAlchemy
            sqlalchemy_type = self.type_mapping.get(col_type, "String")

            # Adiciona tamanho para strings
            if sqlalchemy_type == "String" and max_length:
                sqlalchemy_type = f"String({max_length})"
            elif sqlalchemy_type == "String" and not max_length:
                sqlalchemy_type = f"String({self.config.string_max_length})"

            # Tipo Python para anotação
            python_type = col_type.__name__ if hasattr(col_type, "__name__") else str(col_type)

            # Monta a linha da coluna
            type_annotation = f"{python_type} | None" if nullable else python_type

            column_args = [sqlalchemy_type]

            if is_primary:
                column_args.append("primary_key=True")

            if is_fk and not is_primary:
                # Assume que a FK aponta para uma tabela com nome similar
                fk_table = col_name.replace("_id", "").replace("id_", "")
                column_args.append(f'ForeignKey("{fk_table}.id")')

            column_args.append(f"nullable={nullable}")

            content += f"    {col_name}: Mapped[{type_annotation}] = mapped_column({', '.join(column_args)})\n"

            # Adiciona à lista de índices se necessário
            if needs_index and not is_primary:
                indexes.append(col_name)

        # Adiciona índices
        if indexes:
            content += "\n    # Índices\n"
            content += "    __table_args__ = (\n"
            for idx_col in indexes:
                content += f'        Index("idx_{table_name}_{idx_col}", "{idx_col}"),\n'
            content += "    )\n"

        # Salva o arquivo
        file_path = Path(output_path) / f"{entity_name.lower()}.py"
        with Path(file_path).open("w", encoding="utf-8") as f:
            f.write(content)

        return str(file_path)
