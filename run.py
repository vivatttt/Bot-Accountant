from app import app
from app.routes import routes

if __name__ == '__main__':
    app.register_blueprint(routes)
    app.run(debug=True, port=8000)