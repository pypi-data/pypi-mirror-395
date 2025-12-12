from typing import Optional

from sqlalchemy.exc import IntegrityError
from daomodel import DAOModel


class Conflict(Exception):
    """Indicates that the store could not be updated due to an existing conflict."""
    def __init__(self, model: Optional[DAOModel] = None, msg: Optional[str] = None, error: Optional[Exception] = None):
        self.detail = msg if msg else f'Conflict for {model.__class__.doc_name()} {model}'
        self.original_error = error


class TransactionMixin:
    """A mixin that provides transaction management functionality.

    self.db must be set in the extending class before calling any methods.
    """
    @property
    def _auto_commit(self) -> bool:
        """Determines if auto-commit is enabled.

        This is based on whether the session is in transaction mode -
        if in transaction mode, auto-commit is disabled.

        :return: True if auto-commit is enabled, False otherwise
        """
        if not hasattr(self.db, '_in_transaction'):
            self.db._in_transaction = False
        return not self.db._in_transaction

    def start_transaction(self) -> None:
        """Starts a transaction by setting transaction_mode to True.

        This disables auto_commit until the transaction is committed or rolled back.
        """
        self.db._in_transaction = True

    def _end_transaction(self) -> None:
        """Resets the transaction state after a transaction is committed or rolled back."""
        self.db._in_transaction = False

    def _commit_if_not_transaction(self):
        if self._auto_commit:
            self.commit()

    def commit(self, *models_to_refresh: DAOModel) -> None:
        """Commits all pending changes to the database.

        'Pending changes' includes data changes made to models that were fetched from the database.
        Use dao.start_transaction() to avoid automatically calling this method following each insert, upsert, and remove.
        This will commit all changes within the session and is not limited to this DAO.
        Following the DB commit, DAOModels will be detached, needing to be refreshed.

        If this DAO was in transaction mode, it will be reset to auto-commit mode after committing.

        :param models_to_refresh: The DAOModels to refresh after committing
        :raises Conflict: if a unique constraint is violated
        :raises IntegrityError: if a database constraint is violated (e.g., NOT NULL, foreign key)
        """
        try:
            self.db.commit()
            for model in models_to_refresh:
                self.db.refresh(model)
            self._end_transaction()
        except IntegrityError as e:
            error_msg = str(e).lower()
            if any(text in error_msg for text in ('unique constraint', 'unique violation', 'duplicate key')):
                raise Conflict(msg=f"Unique constraint violation: {str(e)}", error=e)
            raise

    def rollback(self) -> None:
        """Reverts all pending database changes of a transaction.

        This will discard all changes that have not yet been committed.

        :raises RuntimeError: if not in transaction mode
        """
        if self._auto_commit:
            raise RuntimeError('Cannot rollback while not in transaction mode')
        self.db.rollback()
        self._end_transaction()
