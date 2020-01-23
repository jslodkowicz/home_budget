make deps:
	sudo apt-get install python3.7-dev libmysqlclient-dev && pip install -r requirements.txt
make data:
	python manage.py loaddata sample_data.json
