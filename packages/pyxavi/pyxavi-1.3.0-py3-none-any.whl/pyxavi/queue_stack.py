from __future__ import annotations
from pyxavi import Storage, Dictionary
from typing import Protocol
import logging


class QueueItemProtocol(Protocol):

    def to_dict(self) -> dict:
        """Convert the object into a dict"""

    @staticmethod
    def from_dict(dictionary: dict) -> QueueItemProtocol:
        """Instantiates this class from a given dictionary"""

    def sort_value(self, param: any = None) -> any:
        """Returns a value that will be used to sort the collection of self items"""

    def unique_value(self, param: any = None) -> any:
        """Returns a value that will be used to deduplicate the collection of self items"""


class SimpleQueueItem(QueueItemProtocol):

    item: dict = None

    def __init__(self, item: dict) -> None:
        self.item = item

    def to_dict(self) -> dict:
        return self.item

    @staticmethod
    def from_dict(dictionary: dict) -> QueueItemProtocol:
        return SimpleQueueItem(item=dictionary)

    def sort_value(self, param: str = None) -> any:
        return self.item[param] if param in self.item else None

    def unique_value(self, param: str = None) -> any:
        return self.item[param] if param in self.item else None


class Queue:

    DEFAULT_LOGGER_NAME = "pyxavi-queue"
    _queue = []

    def __init__(
        self,
        logger: logging.Logger = None,
        storage_file: str = None,
        queue_item_object: QueueItemProtocol = SimpleQueueItem
    ) -> None:
        self._logger = logger if logger is not None\
            else logging.getLogger(self.DEFAULT_LOGGER_NAME)
        self.__storage_file = storage_file
        self._queue_item_object = queue_item_object
        self.load()

    def load(self) -> int:
        if self.__storage_file is not None:
            # If we have a storage file defined we'll
            #   then have a place to save the state.
            self._queue_manager = Storage(filename=self.__storage_file)
        else:
            # If we don't have a storage file defined we'll
            #   then use a Dictionary and won't allow to save the state
            self._queue_manager = Dictionary({"queue": []})

        self._queue = list(
            map(
                lambda x: self._queue_item_object.from_dict(x),
                self._queue_manager.get("queue", [])
            )
        )
        return self.length()

    def append(self, item: QueueItemProtocol) -> None:
        self._queue.append(item)

    def sort(self, param: str = None) -> None:
        self._logger.debug("Sorting queue by date ASC")
        self._queue = sorted(self._queue, key=lambda x: x.sort_value(param=param))

    def deduplicate(self, param: str = None) -> None:
        self._logger.debug("Deduplicating queue")
        uniques_queue = []
        output_queue = []
        for item in self._queue:
            unique = item.unique_value(param=param)
            if unique is None:
                raise RuntimeError("The unique value can't be None while deduplicating.")
            if unique not in uniques_queue:
                output_queue.append(item)
                uniques_queue.append(unique)
        self._queue = output_queue

    def save(self) -> None:
        if isinstance(self._queue_manager, Storage):
            self._logger.debug("Saving the queue")
            self._queue_manager.set("queue", list(map(lambda x: x.to_dict(), self._queue)))
            self._queue_manager.write_file()
        elif isinstance(self._queue_manager, Dictionary):
            self._logger.warning(
                "This queue has no state and a call to save() is received. Ignoring"
            )

    def is_empty(self) -> bool:
        return False if self._queue else True

    def get_all(self) -> list:
        return self._queue

    def clean(self) -> None:
        self._queue = []

    def length(self) -> int:
        return len(self._queue)

    def pop(self) -> QueueItemProtocol:
        return self._queue.pop(0) if not self.is_empty() else None

    def unpop(self, item: QueueItemProtocol) -> None:
        if self.is_empty():
            self._queue = []

        self._queue = [item] + self._queue

    def first(self) -> QueueItemProtocol:
        return self._queue[0] if not self.is_empty() else None

    def last(self) -> QueueItemProtocol:
        return self._queue[-1] if not self.is_empty() else None
