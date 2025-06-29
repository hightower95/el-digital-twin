
# from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from el_analysis import Address

from loguru import logger

import sys


def _initial_setup():

    global _watched_addresses

    _watched_addresses = set()

    logger.remove()

    logger.add(
        sink=sys.stdout,
        level="INFO",
        format="{time: HH:mm:ss} | <level>{level}</level> | {module} | {message}",
        filter=_module_filter,
        enqueue=False,

    )

    logger.add(
        sink="e3-toolkit.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}",
        enqueue=False,
        mode="w"

    )

    logger.debug("Started logging")


# Module specific filters
_context_levels = {
    "scratch": logger.level("INFO"),
    "test": logger.level("ERROR"),
}


def _module_filter(record) -> bool:
    extra = record.get("extra", None)
    module = record["extra"].get("module", None) if extra else None

    if module is None:

        return True

    level = _context_levels.get(module, None)

    if level is None:

        return True

    return record["level"].no >= level.no




_initial_setup()


# if __name__ == "__main__":

#     print(f"Running in {__name__}")

#     # Example usage
#     _Address = _get_Address()

#     address1 = _Address.from_tuple(("C", "A1", "X1", None))
#     address2 = _Address.from_tuple(("D", "B1", "X2", None))
#     address3 = _Address.from_tuple(("C", "A1", "X1", None))  # same as address 1

#     watch_address(address1)

#     # Log some messages

#     logger.info("This is a general log message.")

#     logger.debug(
#         "1. This debug message won't be shown unless the address is being watched.", item=address1)

#     logger.debug(
#         "2. This debug message won't be shown unless the address2 is being watched.", item=address2)

#     # Example of addressing watched addresses

#     if address1 in _watched_addresses:

#         logger.debug("3. Address being watched: ", item=address1)

#         logger.debug("3.5. Address not being watched: ", item=address2)

#         logger.debug("3.75. Address also being watched: ", item=address3)

#     logger.debug(
#         "4. This debug message won't be shown unless the address is being watched.", item=address1)

#     # Optionally stop watching

#     stop_watching_address(address1)

#     logger.debug(
#         "5. This debug message won't be shown unless the address is being watched.", item=address1)
