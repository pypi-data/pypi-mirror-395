import logging
import os
import time
from typing import Union

from cosmotech.orchestrator.utils.logger import get_logger

LOGGER = get_logger(
    "Supplychain/Timer",
    os.environ.get('LOG_LEVEL', 'INFO'),
)


class Timer:

    @property
    def current_split_time(self) -> float:
        return time.time() - self.last_split_time

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time

    @staticmethod
    def fast_print(message, log_level="INFO"):
        _log_level = logging.getLevelNamesMapping().get(log_level.upper(), logging.INFO)
        for _r in message.split("\n"):
            LOGGER.log(_log_level, _r)

    def display_message(self, message: str = "Time since started: {time_since_start}", level="INFO"):
        current_time = time.time()
        values = {"time_since_start": current_time - self.start_time,
                  "time_since_last_split": current_time - self.last_split_time,
                  "current_split": self.total_splits,
                  "average_time_per_split": (current_time - self.start_time) / max(self.total_splits, 1)}
        try:
            message = message.format(**values)
            if self.prefix is not None:
                message = '\n'.join(f"{self.prefix} {m}" for m in message.split('\n'))
        except KeyError:
            self.fast_print(
                "Only accepted keys are :"
                "\n- time_since_start"
                "\n- time_since_last_split"
                "\n- current_split"
                "\n- average_time_per_split",
                log_level="ERROR"
            )
        self.fast_print(message, level)

    def split(self, message: Union[str, None] = "{current_split}: {time_since_last_split}", level="INFO"):
        self.total_splits += 1
        current_time = time.time()
        if message is not None:
            self.display_message(message, level)
        self.last_split_time = current_time

    def reset(self):
        self.start_time = time.time()
        self.last_split_time = self.start_time
        self.total_splits = 0

    def __enter__(self):
        """
        Initialize self.last_time
        Allows the usage of :
        with Converter(..) as ... :
            ...
        :return: self
        """
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):
        """
        More explications on __enter__ and __exit__ on :
        https://docs.python.org/2.5/whatsnew/pep-343.html#SECTION000910000000000000000
        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: exception stack trace
        :return: Boolean, do we suppress exceptions ?
        """
        message = ["Total elapsed time: {time_since_start:6.4f}"]
        if self.total_splits > 1:
            message += ["Number of splits: {current_split}",
                        "Average time per split: {average_time_per_split:6.4f}"]
        self.display_message("\n".join(message), level="INFO")
        return exc_type is None

    def __init__(self, prefix: Union[str, None] = None):
        self.start_time = time.time()
        self.last_split_time = self.start_time
        self.total_splits = 0
        self.prefix = prefix
