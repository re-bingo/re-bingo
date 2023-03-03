<h1>The <em>Bingo</em> Project, <strong>Reimplemented</strong>.</h1>

This repository contains the backend-end sources of *Bingo* application, our stack includes:

- GraphQL endpoint `/graphql` powered by *Strawberry*
- MySQL database connected using *Tortoise ORM*
- dependency management using *Poetry*

## Deployment

First, add a `sql.yaml` file under the `/config` folder, containing a db url like this:

```yaml
default: mysql://user:password@host:port/db
```

and generate a `salt` file under the `/config` folder:

```shell
openssl rand 1024 > salt
```

and add a `env.yaml` file under the `/config` folder, containing a *poster* url like this:

```yaml
poster: http://localhost:5000
```

Then, execute the command below:

```shell
poetry install
poetry run uvicorn src:app --reload --reload-exclude="migrations/**/*.py"
```