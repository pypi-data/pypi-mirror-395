# Feature testing

Cattle_grid is feature tested using [behave](https://behave.readthedocs.io/en/latest/).
The packages below contain useful general functions.
Individual steps are described in [Steps](./steps.md).

## Use in your project

The tools provided here are meant to be reusable. Generally, the
aim is to use [almabtrieb](https://bovine.codeberg.page/almabtrieb/) to
talk to a compatible server. Then one can use the steps and tools
provided here to write tests. I have done this a few times,
see [comments](https://codeberg.org/bovine/comments/) and its
feature tests.

### Setup

First, the test code reads the following two values from the cattle_grid
configuration file:

```toml title="cattle_grid.toml"
amqp_url = "amqp://guest:guest@rabbitmq:5672/"
db_url = "postgresql+asyncpg://postgres:pass@cattle_grid_db/"

[frontend]
base_urls = ["http://abel"]
```

The `amqp_url` is used by almabtrieb. The `db_url` is currently needed
to create and delete accounts to use almabtrieb with.

## Project layout

Assuming one locates the feature tests in the `features` directory,
we will need to create the following structure:

```tree
features/
├── basic.feature
├── environment.py
└── steps
    ├── custom.py
    └── import.py
```

where `basic.feature` is the Gherkin for some test and
`custom.py` represents custom steps. The file `environment.py`
is described [here](https://behave.readthedocs.io/en/stable/tutorial/#environmental-controls)
in the behave documentation and should take the form

```python title="features/environment.py"
from cattle_grid.testing.features.environment import (
    before_all,  
    before_scenario,  
    after_scenario,  
)
```

similarly `import.py` makes the steps available:

```python title="features/steps/import.py"
from cattle_grid.testing.features.steps import *
```

#### Custom setup steps

If you have to run custom setup steps, you can do it as follows:

```python title="features/environment.py"
from cattle_grid.testing.features.environment import (
    before_all,  
    before_scenario as cg_bs,  
    after_scenario,  
)

def before_scenario(context, scenario):
    cg_bs(context, scenario)

    # your setup
```

## Usage

One thing these tools do for you is managing actors for this to work, one
needs to create actors using our methods

```gherkin
Given A new user called "Alice"
```

this ensures that the `context.actors["Alice"]` and `context.connections["Alice"]`
variables have the appropriate values.

:::cattle_grid.testing.features

:::cattle_grid.testing.features.environment
