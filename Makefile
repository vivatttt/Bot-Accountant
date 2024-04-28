FLASK_APP = app/routes
PORT = 8000
DEBUG = --debug

run:
	@echo "Запуск Flask приложения..."
	FLASK_APP=$(FLASK_APP) flask run --port $(PORT) $(DEBUG)