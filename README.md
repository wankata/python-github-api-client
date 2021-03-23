# Python GitHub API Client

This is a simple API client for Github, written in Python.

The client implements **v3** of the API.


## For developers only

If you want to patch something, play around, run the tests, just follow the instructions below.

## Prerequisites

You need to have [Docker CE](https://docs.docker.com/install/ "Install Docker CE") and [Docker
Compose](https://docs.docker.com/compose/install/ "Install Docker Compose") installed.

If your environment is other than GNU/Linux, there may be some differences in the interaction with
Docker, so please follow the [Docker documentation](https://docs.docker.com/ "Docker documentation")
if something doesn't suits you.


## Setup Local Docker Environment

Under `environment/` you'll find all the configuration files, you need to run the
project on docker.

To prepare your environment, you need to cd `./environment` and:
- Sync the `.env.tmpl` file to `.env`. For now, you may, but you don't really need to change
  anything in the .env file.
- run `$ docker-compose up --build`

That's all!

## Utility scripts

To run all the linters and tests, you need to:
  - `$ cd environment`
  - `$ docker-compose exec app bash -c "./run_checks.py --help"`


## Basic conventions

To keep things clean, we use:
- [gitlint](https://jorisroovers.com/gitlint/ "gitlint documentation") to keep eye on our commit
  messages. See the .gitlint file for our custom rules.
- [flake8](https://flake8.pycqa.org/en/latest/index.html "flake8 documentation") to keep our code
  clean. See the .flake8 file for our custom rules.
- [mypy](https://mypy.readthedocs.io/en/stable/ "mypy documentation") to check our types statically.
