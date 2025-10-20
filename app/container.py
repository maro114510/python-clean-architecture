from dependency_injector import containers, providers
from app.datastore.item import ItemDatastore
from app.interactor.item import ItemInteractor


class Container(containers.DeclarativeContainer):
    """DI Container - Dependency Injection Container"""

    config = providers.Configuration()

    # Repository Layer
    item_repository = providers.Singleton(ItemDatastore)

    # Usecase Layer
    item_usecase = providers.Factory(
        ItemInteractor,
        repo=item_repository,
    )

    # Router Layer (not needed since we use function-based routers)
