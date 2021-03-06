# Home Budget
[![Build Status](https://travis-ci.org/jslodkowicz/home_budget.svg?branch=master)](https://travis-ci.org/jslodkowicz/home_budget)

Simple web app for managing home budget.

# Installing

### Requirements:
* python 3.7
* docker

### Usage

- `make deps` will install all necessary dependencies
- `make build` will build an app instance
- `make up` will run the app
- `make data` will load fixtures with sample data
- `make test` will run unittests and flake8 code check

[Mailhog](http://localhost:8025) service is used for handling mail functionality of an app.

For test purposes there are 3 user instances, credentials are listed below:

- _admin@example.com / admin_
- _henry@test.com / Haslo123_
- _anna@test.com / Haslo123_

To use AWS and currency converter features, you must copy .env file to `home_budget/home_budget` directory.

### API

[Swagger UI](http://localhost:8000/swagger) is used as a default tool for API documentation and testing.

### pip-tools

For managing packages we use pip-tools. To add a package, simply add a package name to requirements.in file
and run `pip-compile` command, after that requirements.txt file will be updated.