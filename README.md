# Flask Cloudflare Login
The Flask Cloudflare Login module provides a Flask-Login user class from Cloudfare Access JWT token and Cloudflare identity API.

## Installation
Flask Cloudflare Login is available from PyPI and can be installed by running:

```sh
pip install flask-cloudflare-login
```

## Usage example - Dash App

### Cloudflare Settings

Configure your Cloudflare settings in in examples/dash/.env

```sh
CF_TEAM_DOMAIN=<company>.cloudflareaccess.com
CF_POLICY_AUD=
```

In order to make the application work locally you need to set CF_TEST_TOKEN with the CF_Authorization cookie value.

```sh
CF_TEST_TOKEN=
```

### Start the Dash App

```sh
make build run
```

## How to contribute?

- clone this repo or pull the latest changes
- create a new branch feature/\<feature\>
- run `make test` to auto format code, make sure all tests are passed
- push the code and create a merge request to main branch
- get the pull request reviewed and approved, the branch should be removed once merged.
- create a new git tag version, following semantic versioning praxis MAJOR.MINOR.PATCH
