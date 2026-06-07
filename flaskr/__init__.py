import os
from flask import Flask

def create_app(test_config=None):
    # создаём экземпляр приложения
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # загружаем конфигурацию из config.py, если он есть (необязательно)
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # убеждаемся, что папка instance существует
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # регистрируем db
    from . import db
    db.init_app(app)
    db.init_db_automatically(app)


    # регистрируем auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # регистрируем blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
