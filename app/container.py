from dependency_injector import containers, providers
from app.datastore.item import ItemDatastore
from app.interactor.item import ItemInteractor
from app.config.app_config import AppConfig
from app.config.database_config import DatabaseConfig
from app.datastore.database import DatabaseFactory
from app.datastore.database.transaction_factory import TransactionManagerFactory


class Container(containers.DeclarativeContainer):
    """DI Container - Dependency Injection Container"""

    config = providers.Configuration()

    # Application configuration
    app_config = providers.Singleton(AppConfig.from_env)

    # Database configuration
    database_config = providers.Singleton(DatabaseConfig.from_env)

    # Database connection
    database_connection = providers.Singleton(
        DatabaseFactory.create_connection, config=database_config
    )

    # Transaction manager
    transaction_manager = providers.Singleton(
        TransactionManagerFactory.create_manager,
        connection=database_connection,
        config=database_config,
    )

    # Repository Layer
    item_repository = providers.Singleton(ItemDatastore)

    # Usecase Layer
    item_usecase = providers.Factory(
        ItemInteractor,
        repo=item_repository,
        transaction_manager=transaction_manager,
    )
