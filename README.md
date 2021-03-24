# Python GitHub API Client

This is a simple API client for Github, written in Python.

The client implements **v3** of the API.


## Setup

The Github API Client works only with token authentication.
To use methods, requiring authentication, provide a token as environment variable `GITHUB_TOKEN`


## General Usage

The Github API Client defines model classes for each data type, which cover the response json.

The model classes don't allow you to assign attributes, not defined in the model, so they try to
protect you from typos.

The attributes follow 1:1 the json attribute names, provided by GitHub.


## users module


### general usage

`from github_api_client import users`


### get_user()

`users.get_user(login)`

[GitHub documentation](https://docs.github.com/en/rest/reference/users#get-a-user)

The method do **not** require authentication.
It raises exception on anything but 200 OK.
It returns users.User instance, which includes the following attributes:
- login
- id
- node_id
- avatar_url
- gravatar_id
- url
- html_url
- followers_url
- following_url
- gists_url
- starred_url
- subscriptions_url
- organizations_url
- repos_url
- events_url
- received_events_url
- type
- site_admin
- name
- company
- blog
- location
- email
- hireable
- bio
- twitter_username
- public_repos
- public_gists
- followers
- following
- created_at
- updated_at


### get_authenticated_user()

`users.get_authenticated_user()`

[GitHub documentation](https://docs.github.com/en/rest/reference/users#get-the-authenticated-user)

The method **requires** authentication.
It raises exception on anything but 200 OK.
It returns users.AuthenticatedUser instance, which include all User fields + the following
additional attributes:
- private_gists
- total_private_repos
- owned_private_repos
- disk_usage
- collaborators
- two_factor_authentication
- plan


## TODOs

- Implement rate limits
- Wrap HTTPError in GitHubClientError


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
