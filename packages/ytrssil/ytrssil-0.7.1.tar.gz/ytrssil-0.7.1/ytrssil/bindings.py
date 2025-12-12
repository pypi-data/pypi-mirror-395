from inject import Binder, Injector, clear_and_configure, get_injector_or_die

from ytrssil.client import HttpClient
from ytrssil.config import Configuration, load_config
from ytrssil.protocols import Client


def dependency_configuration(binder: Binder) -> None:
    binder.bind(Configuration, load_config())
    binder.bind_to_constructor(Client, HttpClient)


def setup_dependencies() -> Injector:
    clear_and_configure(dependency_configuration)

    return get_injector_or_die()
