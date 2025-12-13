from faststream.rabbit import RabbitRouter


from .reporter import create_reporting_router


def test_create_reporting_router():
    router = create_reporting_router()

    assert isinstance(router, RabbitRouter)
