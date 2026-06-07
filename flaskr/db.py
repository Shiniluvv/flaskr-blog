import sqlite3
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db_automatically(app):
    """Автоматически создаёт таблицы при запуске приложения (для Render)."""
    with app.app_context():
        db = get_db()
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='user' OR name='post');")
        tables = cursor.fetchall()
        if len(tables) < 2:
            init_db()
            app.logger.info("Database tables were missing and have been created automatically.")
        else:
            app.logger.info("Database tables already exist.")
    