# app.py
import os
from flask import Flask
from psycopg2 import connect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def test_db():
    try:
        conn = connect(
            dsn=os.getenv("DATABASE_URL"),
            sslmode=os.getenv("PGSSLMODE", "disable")
        )
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user, NOW();")
        db_name, db_user, db_time = cur.fetchone()
        cur.close()
        conn.close()
        return f"""✅ Conexión exitosa<br>
        Base de datos: {db_name}<br>
        Usuario: {db_user}<br>
        Fecha/Hora: {db_time}"""
    except Exception as e:
        return f"❌ Error de conexión: {e}"

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 3000)))
