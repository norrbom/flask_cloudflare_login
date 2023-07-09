# Flask Cloudflare

The Flask Cloudflare module provides authorization based on Cloudfare Access JWT token and Cloudflare identity API.
The module comes with a class `CfUser` that  that can be used as a Flask-Login user class, objects of the CfUser class has a `groups` variable that holds a list of groups the user belongs to.

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

Or set the email and groups values that is pulled from the token.

```sh
TEST_CF_EMAIL=
TEST_CF_GROUPS=
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
