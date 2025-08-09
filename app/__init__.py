import os
from flask import Flask
from .db import init_db_pool
from .blueprints.retos import retos_bp

def create_app():
    app = Flask(__name__)

    # Cargar SECRET_KEY desde variable de entorno
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_por_defecto_insegura')

    # DSN desde DATABASE_URL o desde variables individuales
    dsn = os.getenv("DATABASE_URL") or (
        f"dbname={os.getenv('PGDATABASE', 'mydb')} "
        f"user={os.getenv('PGUSER', 'postgres')} "
        f"password={os.getenv('PGPASSWORD', '')} "
        f"host={os.getenv('PGHOST', 'localhost')} "
        f"port={os.getenv('PGPORT', '5432')}"
    )

    sslmode = os.getenv("PGSSLMODE", "disable")
    minconn = int(os.getenv("PG_MINCONN", "1"))
    maxconn = int(os.getenv("PG_MAXCONN", "10"))

    # Inicializa el pool
    init_db_pool(dsn=dsn, sslmode=sslmode, minconn=minconn, maxconn=maxconn)

    # Registra blueprints
    app.register_blueprint(retos_bp)

    return app
