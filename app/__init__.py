from flask import Flask

def create_app():
    app = Flask(__name__)

    # 配置从 config.py 中读取（包括 Gemini、API keys）
    app.config.from_pyfile("../config.py", silent=True)

    from app.routes import main
    app.register_blueprint(main)

    return app

