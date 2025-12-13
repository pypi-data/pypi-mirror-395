# cattle_grid

cattle_grid handles a few common tasks that plague Fediverse applications:

* Maintaining an actor document and associated endpoints like inbox
* Verifying HTTP signatures
* Determine if somebody is authorized to view something or not
* Manage follower collections

Furthermore with its [muck_out](https://bovine.codeberg.page/muck_out/) extension
it handles parsing ActivityPub objects.

cattle_grid relies on [faststream](https://faststream.ag2.ai/latest/) and
then [RabbitMQ](https://www.rabbitmq.com/) for message processing. If you
want to use cattle_grid, you will be faced with using __message queues__.

cattle_grid has an internal account system.

## Related links

### Applications using cattle_grid

* [comments](https://bovine.codeberg.page/comments/) allows one to add comments to a static site
* [fedi-herds](https://codeberg.org/bovine/fedi-herds/) allows list management
* [roboherd](https://bovine.codeberg.page/roboherd/) allows one to build automatic posting bots (these have no frontend)

### Related projects / utilities

* [almabtrieb](https://bovine.codeberg.page/almabtrieb/) implements one of the Client protocols used by cattle_grid
* [console](https://codeberg.org/bovine/console) provides a light weight frontend.

## Development

### Testing

You can run the pytest tests via

```bash
uv run pytest
```

or in watch mode

```bash
uv run ptw .
```

### Running behave tests

Build the container via

```bash
./update_docker.sh
```

This script uses the requirements from `pyproject.toml` via `uv export` to install
python dependencies in the container. This means this script needs to be rerun, if
you make changes to the dependencies. Startup the docker environment via

```bash
docker compose up
```

Open a runner container

```bash
docker compose run --rm --name runner cattle_grid_app /bin/sh
```

Inside this container, you now run

```bash
fediverse-features
behave
```

The first step downloads some features from [fediverse-features](https://codeberg.org/helge/fediverse-features)
and the second step runs the test suite.

### Building end 2 end reports  (as done by CI)

The process to build the end to end reports is described [here](./resources/report_builder/README.md). The reports should be published to [this repository](https://codeberg.org/helge/cattle_grid_reports) and then made available [here](https://helge.codeberg.page/cattle_grid_reports/).

### Running as stand alone

Create a requirements.txt file and start a virgin docker container

```bash
uv export --no-editable --no-emit-project --no-hashes --no-dev > requirements.txt
docker run --rm -ti -p 8000:8000\
    -v ./cattle_grid:/app/cattle_grid\
    -v ./requirements.txt:/app/requirements.txt \
    --workdir /app\
    helgekr/bovine:python3.13 /bin/sh
```

Once inside the docker container install dependencies

```sh
pip intall -r requirements.txt
```

and run `cattle_grid` via

```sh
uvicorn cattle_grid:create_app --factory --host 0.0.0.0
```

This currently fails.