# Flask Cloudflare

Flask Cloudflare provides additional authorization on top of Cloudfare Access by checking if a user is part of a group.
Groups are fetched from Cloudflare identity API.

## Installation

### Create a venv

```sh
python3 -m venv ./venv
. ./venv/bin/activate && \
pip install --upgrade pip build
deactivate
```

### Build the package:

```sh
. ./venv/bin/activate && \
python -m build --wheel .
deactivate
```

### Install the package and dependencies with pip:

```sh
. ./venv/bin/activate && \
pip install -r examples/dash/requirements.txt && \
pip install --no-index --find-links ./dist flask_cloudflare && \
deactivate
```

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

Or set the email and groups values that is pulled from the token.

```sh
TEST_CF_EMAIL=
TEST_CF_GROUPS=
```

### Run the example Dash App

```sh
sh -c '. ./venv/bin/activate && cd examples/dash && export ENVIRONMENT=local export SECRET_KEY=changeme && python app.py'
```
