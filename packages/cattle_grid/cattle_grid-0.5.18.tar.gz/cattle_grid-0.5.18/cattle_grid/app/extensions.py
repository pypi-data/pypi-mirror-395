from cattle_grid.extensions.load import (
    load_extensions,
    set_globals,
    collect_method_information,
)
from cattle_grid.exchange.info import exchange_method_information
from cattle_grid.dependencies.globals import global_container


def init_extensions(settings):
    extensions = load_extensions(settings)

    set_globals(extensions)

    global_container.method_information = (
        collect_method_information(extensions) + exchange_method_information
    )

    return extensions
