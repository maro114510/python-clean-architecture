from dependency_injector import containers, providers
from app.datastore.item import ItemDatastore
from app.interactor.item import ItemInteractor
from app.config.database_config import DatabaseConfig
from app.datastore.database import DatabaseFactory

class Container(containers.DeclarativeContainer):
    """DI Container - Dependency Injection Container"""

    config = providers.Configuration()

    # Database configuration
    database_config = providers.Singleton(DatabaseConfig.from_env)

    # Database connection
    database_connection = providers.Singleton(
        DatabaseFactory.create_connection,
        config=database_config
    )

    # Repository Layer
    item_repository = providers.Singleton(
        ItemDatastore,
        db_connection=database_connection
    )

    # Usecase Layer
    item_usecase = providers.Factory(
        ItemInteractor,
        repo=item_repository,
    )

    # Router Layer (not needed since we use function-based routers)
