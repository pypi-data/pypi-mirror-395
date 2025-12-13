from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


@dataclass
class Credentials:
    """
    # Database credentials container.

    Attributes
        db_type: Type of database (sqlite, mysql, postgres, sql_server)
        host: Database host (not needed for sqlite)
        port: Database port (not needed for sqlite)
        user: Database user (not needed for sqlite)
        password: Database password (not needed for sqlite)
        database: Database name (not needed for sqlite)
        database_path: Path to SQLite database file
        odbc_driver: ODBC driver version for SQL Server (default: 17)

    ## MySQL performance options (optional)
        mysql_driver: Preferred driver, 'mysqldb' (mysqlclient) or 'pymysql'.
        mysql_charset: Connection charset (default 'utf8mb4').
        pool_size: Base connections kept in the pool.
        max_overflow: Extra transient connections allowed above pool_size.
        pool_timeout: Seconds to wait for a connection before timeout.
        pool_recycle: Seconds to recycle connections (avoid MySQL idle timeouts).
        isolation_level: Default transaction isolation for connections.

    ## PostgreSQL performance options (optional)
        postgres_driver: Preferred driver, 'psycopg2' or 'psycopg'.
        pg_executemany_mode: Mode for executemany() (psycopg2), e.g. 'values'.
        pg_executemany_values_page_size: Page size for values batching (psycopg2).
        pg_stream_results: If True, enable streaming of large result sets.

    ## SQL Server performance and connection options (optional)
        fast_executemany: Enable fast path for executemany() with pyodbc.
        encrypt: Add 'Encrypt=yes' to ODBC string (use per security policy).
        trust_server_certificate: Add 'TrustServerCertificate=yes' to ODBC string.
        connection_timeout: Add 'Connection Timeout=XX' to ODBC string.
        application_intent_read_only: Add 'Application Intent=ReadOnly' (AG/read replicas).
        sqlserver_isolation_level: Default isolation ('READ COMMITTED' or 'SNAPSHOT').
    """

    db_type: Literal["sqlite", "mysql", "postgres", "sql_server"]
    host: str | None = None
    port: int | None = None
    user: str | None = None
    password: str | None = None
    database: str | None = None
    database_path: str | None = None
    odbc_driver: int | str | None = None

    # MySQL-specific performance configuration
    mysql_driver: Literal["mysqldb", "pymysql"] | None = None
    mysql_charset: str | None = None
    pool_size: int | None = None
    max_overflow: int | None = None
    pool_timeout: int | None = None
    pool_recycle: int | None = None
    isolation_level: Literal["READ COMMITTED", "READ UNCOMMITTED"] | None = None

    # PostgreSQL-specific performance configuration
    postgres_driver: Literal["psycopg2", "psycopg"] | None = None
    pg_executemany_mode: Literal["values"] | None = None
    pg_executemany_values_page_size: int | None = None
    pg_stream_results: bool | None = None

    # SQL Server-specific performance and connection configuration
    fast_executemany: bool | None = None
    encrypt: bool | None = None
    trust_server_certificate: bool | None = None
    connection_timeout: int | None = None
    application_intent_read_only: bool | None = None
    sqlserver_isolation_level: Literal["READ COMMITTED", "SNAPSHOT"] | None = None

    @classmethod
    def sqlite(cls, database_path: str | None = None) -> "Credentials":
        """Create SQLite credentials."""
        return cls(db_type="sqlite", database_path=database_path)

    @classmethod
    def mysql(cls, host: str, port: int, user: str, password: str, database: str) -> "Credentials":
        """
        Create MySQL credentials.

        Parameters
        ----------
        host : str
            Host do banco MySQL.
        port : int
            Porta do MySQL (geralmente 3306).
        user : str
            Usuário de conexão.
        password : str
            Senha de conexão.
        database : str
            Nome do banco.

        Performance e comportamento (opcionais)
        --------------------------------------
        mysql_driver : Literal['mysqldb', 'pymysql'], default 'pymysql'
            Driver de conexão. 'mysqldb' (mysqlclient) costuma ser mais rápido que 'pymysql',
            porém requer a dependência mysqlclient instalada. Use 'pymysql' para compatibilidade
            ampla sem dependências nativas.
        mysql_charset : str, default 'utf8mb4'
            Charset da conexão. 'utf8mb4' garante suporte completo a Unicode.
        pool_size : int, default 10
            Número de conexões mantidas no pool. Aumente para cargas com alta concorrência.
        max_overflow : int, default 20
            Conexões extras além de pool_size permitidas temporariamente.
        pool_timeout : int, default 30
            Tempo (segundos) aguardando por uma conexão livre antes de erro.
        pool_recycle : int, default 1800
            Tempo (segundos) para reciclar conexões e evitar timeouts de idle do MySQL.
        isolation_level : Literal['READ COMMITTED', 'READ UNCOMMITTED'], default 'READ COMMITTED'
            Nível de isolamento padrão. 'READ UNCOMMITTED' pode reduzir bloqueios em leituras
            não críticas (permite dirty reads). 'READ COMMITTED' é seguro para a maioria dos casos.

        Notes
        -----
        As opções acima serão utilizadas pelo `Connection` ao construir o `Engine`,
        aplicando tuning de pool e isolamento transacional específico para MySQL,
        além de incluir `?charset=` na URL.
        """
        return cls(
            db_type="mysql",
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            mysql_driver="pymysql",
            mysql_charset="utf8mb4",
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
            isolation_level="READ COMMITTED",
        )

    @classmethod
    def postgres(
        cls,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        *,
        postgres_driver: Literal["psycopg2", "psycopg"] = "psycopg2",
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_timeout: int = 30,
        pool_recycle: int = 1800,
        isolation_level: Literal["READ COMMITTED", "READ UNCOMMITTED"] = "READ COMMITTED",
        pg_executemany_mode: Literal["values"] = "values",
        pg_executemany_values_page_size: int = 2000,
        pg_stream_results: bool = False,
    ) -> "Credentials":
        """
        Create PostgreSQL credentials.

        Parameters
        ----------
        host : str
            Host do banco PostgreSQL.
        port : int
            Porta do PostgreSQL (geralmente 5432).
        user : str
            Usuário de conexão.
        password : str
            Senha de conexão.
        database : str
            Nome do banco.

        Performance e comportamento (opcionais)
        --------------------------------------
        postgres_driver : Literal['psycopg2','psycopg'], default 'psycopg2'
            Driver de conexão. 'psycopg' (psycopg3) tem ganhos modernos; 'psycopg2' é muito sólido
            e mantém ampla compatibilidade. Ajuste conforme ambiente e dependências.
        pool_size : int, default 10
            Número de conexões mantidas no pool.
        max_overflow : int, default 20
            Conexões extras além de pool_size permitidas temporariamente.
        pool_timeout : int, default 30
            Tempo (segundos) aguardando por uma conexão livre antes de erro.
        pool_recycle : int, default 1800
            Tempo (segundos) para reciclar conexões (boa prática geral).
        isolation_level : Literal['READ COMMITTED','READ UNCOMMITTED'], default 'READ COMMITTED'
            Nível de isolamento padrão. 'READ UNCOMMITTED' pode reduzir bloqueios em leituras não críticas
            (permite dirty reads).
        pg_executemany_mode : Literal['values'], default 'values'
            Modo de executemany para psycopg2, faz batching via VALUES com grande ganho em inserts em lote.
        pg_executemany_values_page_size : int, default 2000
            Tamanho de página para values batching com psycopg2 (ajuste conforme volume: 1000~5000).
        pg_stream_results : bool, default False
            Se True, habilita streaming de resultados grandes via execution_options.

        Notes
        -----
        As opções acima serão utilizadas pelo `Connection` ao construir o `Engine`,
        aplicando tuning de pool, isolamento, batching para executemany e streaming.
        """
        return cls(
            db_type="postgres",
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            postgres_driver=postgres_driver,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            isolation_level=isolation_level,
            pg_executemany_mode=pg_executemany_mode,
            pg_executemany_values_page_size=pg_executemany_values_page_size,
            pg_stream_results=pg_stream_results,
        )

    @classmethod
    def sql_server(
        cls,
        host: str,
        user: str,
        password: str,
        database: str,
        odbc_driver: int | str | None = None,
    ) -> "Credentials":
        """
        Create SQL Server credentials.

        Args:
            host: SQL Server host
            user: Username
            password: Password
            database: Database name
            odbc_driver: ODBC driver version (17, 13) or driver name ("SQL Server").
                        If None, will auto-detect the best available driver.
        Performance e comportamento (opcionais)
        --------------------------------------
        fast_executemany : bool, default True
            Habilita caminho de alta performance para executemany() (pyodbc), ideal para
            operações em lote (inserts/updates) com grande ganho de throughput.
        pool_size : int, default 10
            Número de conexões persistentes mantidas no pool.
        max_overflow : int, default 20
            Conexões extras além de pool_size permitidas temporariamente.
        pool_timeout : int, default 30
            Tempo (segundos) aguardando por uma conexão livre antes de erro.
        pool_recycle : int, default 1800
            Tempo (segundos) para reciclar conexões e evitar problemas de idle/keepalive.
        isolation_level : Literal['READ COMMITTED', 'SNAPSHOT'], default 'READ COMMITTED'
            Nível de isolamento padrão. 'SNAPSHOT' reduz bloqueios de leitura mas exige
            habilitação no servidor (database com ALLOW_SNAPSHOT_ISOLATION/READ_COMMITTED_SNAPSHOT).
        encrypt : bool, default False
            Adiciona 'Encrypt=yes' ao ODBC connect string.
        trust_server_certificate : bool, default False
            Adiciona 'TrustServerCertificate=yes' ao ODBC connect string.
        connection_timeout : int | None, default 30
            Define 'Connection Timeout=XX' no ODBC connect string.
        application_intent_read_only : bool, default False
            Adiciona 'Application Intent=ReadOnly' (útil para AG/réplicas em workloads de leitura).

        Notes
        -----
        As opções acima serão utilizadas pelo `Connection` ao construir o `Engine`,
        aplicando tuning de pool, isolamento e codificação da string ODBC via quote_plus.
        """
        return cls(
            db_type="sql_server",
            host=host,
            user=user,
            password=password,
            database=database,
            odbc_driver=odbc_driver,
            fast_executemany=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
            sqlserver_isolation_level="READ COMMITTED",
            encrypt=False,
            trust_server_certificate=False,
            connection_timeout=30,
            application_intent_read_only=False,
        )


class Connection:
    """
    Database connection manager with context manager support.

    Supports multiple database types with simplified credential management.

    Usage with Credentials class:
        # SQLite
        creds = Credentials.sqlite("test.db")
        with Connection(creds) as db:
            result = db.session.execute(text("SELECT 1"))
            db.session.commit()

        # MySQL
        creds = Credentials.mysql("localhost", 3306, "user", "pass", "mydb")
        with Connection(creds) as db:
            result = db.session.execute(text("SELECT * FROM users"))
            db.session.commit()

        # PostgreSQL
        creds = Credentials.postgres("localhost", 5432, "user", "pass", "mydb")
        with Connection(creds) as db:
            result = db.session.execute(text("SELECT * FROM users"))
            db.session.commit()

        # SQL Server
        creds = Credentials.sql_server("server", "user", "pass", "mydb")
        with Connection(creds) as db:
            result = db.session.execute(text("SELECT * FROM users"))
            db.session.commit()

        # SQL Server with specific ODBC driver
        creds = Credentials.sql_server("server", "user", "pass", "mydb", odbc_driver=17)
        with Connection(creds) as db:
            result = db.session.execute(text("SELECT * FROM users"))
            db.session.commit()

    Get engine directly:
        conn = Connection(Credentials.sqlite("test.db"))
        engine = conn.get_engine()
    """

    def __init__(self, credentials: Credentials) -> None:
        """
        Initialize database connection.

        Args:
            credentials: Credentials object containing database connection details
        """
        self.db_type = credentials.db_type
        self.host = credentials.host
        self.port = credentials.port
        self.user = credentials.user
        self.password = credentials.password
        self.database = credentials.database
        self.database_path = credentials.database_path
        self.odbc_driver = credentials.odbc_driver

        # MySQL performance options
        self.mysql_driver = credentials.mysql_driver or "pymysql"
        self.mysql_charset = credentials.mysql_charset or "utf8mb4"
        self.pool_size = credentials.pool_size or 10
        self.max_overflow = credentials.max_overflow or 20
        self.pool_timeout = credentials.pool_timeout or 30
        self.pool_recycle = credentials.pool_recycle or 1800
        self.isolation_level = credentials.isolation_level or "READ COMMITTED"

        # PostgreSQL performance options
        self.postgres_driver = credentials.postgres_driver or "psycopg2"
        self.pg_executemany_mode = credentials.pg_executemany_mode or "values"
        self.pg_executemany_values_page_size = credentials.pg_executemany_values_page_size or 2000
        self.pg_stream_results = credentials.pg_stream_results or False

        # SQL Server performance and connection options
        self.fast_executemany = (
            credentials.fast_executemany if credentials.fast_executemany is not None else True
        )
        self.sqlserver_isolation_level = (
            credentials.sqlserver_isolation_level
            if credentials.sqlserver_isolation_level is not None
            else "READ COMMITTED"
        )
        self.encrypt = credentials.encrypt if credentials.encrypt is not None else False
        self.trust_server_certificate = (
            credentials.trust_server_certificate
            if credentials.trust_server_certificate is not None
            else False
        )
        self.connection_timeout = (
            credentials.connection_timeout if credentials.connection_timeout is not None else 30
        )
        self.application_intent_read_only = (
            credentials.application_intent_read_only
            if credentials.application_intent_read_only is not None
            else False
        )

        self._engine: Engine | None = None
        self._connection_string: str | None = None
        self.session: Session | None = None

        # Test connection on initialization
        self._test_connection()

    def _create_connection_string(self) -> str:
        """Create database connection string based on db_type."""
        msg_requirements = "{} requires user, password, host, port, and database"
        msg_unsupported = "Unsupported database type."
        if self.db_type == "sqlite":
            return f"sqlite:///{self.database_path}" if self.database_path else "sqlite:///:memory:"

        if self.db_type == "mysql":
            if not all([self.user, self.password, self.host, self.port, self.database]):
                raise ValueError(msg_requirements.format("MySQL"))
            driver = self.mysql_driver if self.mysql_driver else "pymysql"
            charset = self.mysql_charset if self.mysql_charset else "utf8mb4"
            return (
                f"mysql+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/"
                f"{self.database}?charset={charset}"
            )

        if self.db_type == "postgres":
            if not all([self.user, self.password, self.host, self.port, self.database]):
                raise ValueError(msg_requirements.format("PostgreSQL"))
            driver = self.postgres_driver if self.postgres_driver else "psycopg2"
            return (
                f"postgresql+{driver}://{self.user}:{self.password}@{self.host}:{self.port}/"
                f"{self.database}"
            )

        if self.db_type == "sql_server":
            if not all([self.user, self.password, self.host, self.database]):
                raise ValueError(msg_requirements.format("SQL Server"))

            # Auto-detect ODBC driver if not specified
            driver = self.odbc_driver if self.odbc_driver else self._detect_odbc_driver()
            parts = [
                f"DRIVER={{{driver}}}",
                f"SERVER={self.host}",
                f"DATABASE={self.database}",
                f"UID={self.user}",
                f"PWD={self.password}",
            ]
            if self.encrypt:
                parts.append("Encrypt=yes")
            if self.trust_server_certificate:
                parts.append("TrustServerCertificate=yes")
            if self.connection_timeout:
                parts.append(f"Connection Timeout={self.connection_timeout}")
            if self.application_intent_read_only:
                parts.append("Application Intent=ReadOnly")

            connection_string = ";".join(parts)
            return f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"

        raise ValueError(msg_unsupported)

    def _detect_odbc_driver(self) -> str:
        """
        Auto-detect available ODBC driver for SQL Server.

        Tests drivers in order of preference: 17, 13, "SQL Server"

        Returns:
            str: The first available ODBC driver string

        Raises:
            ConnectionError: If no compatible ODBC driver is found
        """
        not_specific_drive = (
            "No compatible ODBC driver found. Please install one of: "
            "ODBC Driver 17 for SQL Server, ODBC Driver 13 for SQL Server, or SQL Server driver"
        )

        drivers_to_test = [
            "ODBC Driver 17 for SQL Server",
            "ODBC Driver 13 for SQL Server",
            "SQL Server",
        ]

        for driver in drivers_to_test:
            try:
                # Test connection string with this driver
                test_connection_string = (
                    f"DRIVER={{{driver}}};SERVER={self.host};"
                    f"DATABASE={self.database};UID={self.user};PWD={self.password};"
                )
                test_url = f"mssql+pyodbc:///?odbc_connect={test_connection_string}"

                # Try to create engine and test connection
                test_engine = create_engine(
                    test_url, pool_pre_ping=True, pool_recycle=3600, echo=False
                )

                # Test the connection
                with test_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))

                # If we get here, the driver works
                test_engine.dispose()
                return driver
            except Exception as e:
                # This driver doesn't work, try the next one
                continue

        # If no driver worked, raise an error
        raise ConnectionError(not_specific_drive)

    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine."""
        if not self._engine:
            self._connection_string = self._create_connection_string()

            connect_args = {}
            if self.db_type == "sqlite":
                connect_args = {"check_same_thread": False}

            engine_kwargs = {
                "connect_args": connect_args,
                "pool_pre_ping": True,
            }

            # Apply MySQL-specific performance options
            if self.db_type == "mysql":
                engine_kwargs.update({
                    "pool_size": self.pool_size,
                    "max_overflow": self.max_overflow,
                    "pool_timeout": self.pool_timeout,
                    "pool_recycle": self.pool_recycle,
                    "isolation_level": self.isolation_level,
                })

            # Apply PostgreSQL-specific performance and pooling options
            if self.db_type == "postgres":
                engine_kwargs.update({
                    "pool_size": self.pool_size,
                    "max_overflow": self.max_overflow,
                    "pool_timeout": self.pool_timeout,
                    "pool_recycle": self.pool_recycle,
                    "isolation_level": self.isolation_level,
                })
                # executemany tuning for psycopg2
                if self.postgres_driver == "psycopg2":
                    engine_kwargs.update({
                        "executemany_mode": self.pg_executemany_mode,
                        "executemany_values_page_size": self.pg_executemany_values_page_size,
                    })
                # psycopg (psycopg3) may leverage insertmanyvalues automatically; left default
                # streaming results for large queries
                if self.pg_stream_results:
                    engine_kwargs.update({"execution_options": {"stream_results": True}})

            # Apply SQL Server-specific performance and pooling options
            if self.db_type == "sql_server":
                engine_kwargs.update({
                    "fast_executemany": self.fast_executemany,
                    "pool_size": self.pool_size,
                    "max_overflow": self.max_overflow,
                    "pool_timeout": self.pool_timeout,
                    "pool_recycle": self.pool_recycle,
                    "isolation_level": self.sqlserver_isolation_level,
                })

            self._engine = create_engine(self._connection_string, **engine_kwargs)

        return self._engine

    def get_engine(self) -> Engine:
        """Get SQLAlchemy engine instance."""
        if not self._engine:
            self._create_engine()
        return self._engine

    def _test_connection(self) -> None:
        """
        Test database connection silently.
        Only raises exception if connection fails.
        """
        error_msg = "Failed to connect to {} database: {}"
        try:
            engine = self._create_engine()

            with engine.connect() as connection:
                # Simple test query for all database types
                connection.execute(text("SELECT 1"))

        except Exception as e:
            raise ConnectionError(error_msg.format(self.db_type, e)) from e

    def __enter__(self) -> "Connection":
        """Enter context manager - create session."""
        if not self._engine:
            self._create_engine()

        session_maker = sessionmaker(bind=self._engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager - cleanup session and engine."""
        if self.session:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()
            self.session = None

        # Keep engine alive for reuse, only dispose on explicit cleanup
        # self._engine remains available for future use

    def close(self) -> None:
        """Explicitly close and dispose of the engine."""
        if self.session:
            self.session.close()
            self.session = None

        if self._engine:
            self._engine.dispose()
            self._engine = None
