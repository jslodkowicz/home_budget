deps:
	sudo apt-get install python3.7-dev libmysqlclient-dev && pip install -r requirements.txt
data:
	docker exec -it home_budget_app_1 python manage.py loaddata sample_data.json
test:
	docker exec -it home_budget_app_1 python manage.py test
	docker exec -it home_budget_app_1 python -m flake8
build:
	docker-compose build
up:
	docker-compose up
