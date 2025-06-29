from loguru import logger
import sys

_Address = None

def _get_Address():
    global _Address
    if _Address is None:
        from el_analysis import Address
        _Address = Address
    return _Address

# Watched Addresses filter
_watched_addresses = set()


def _address_filter(record) -> bool:
    _Address = _get_Address()
    item = record["extra"].get("item", None)
    item_address = None
    if isinstance(item, _Address):
        item_address = item

    elif item is not None:
        item_address = getattr(item, "address", None)

    return (item_address is not None) and (item_address in _watched_addresses)


def watch_address(address: "Address"): # type: ignore
    global _watched_addresses
    _watched_addresses.add(address)

def stop_watching_address(address: "Address"): # type: ignore
    global _watched_addresses
    _watched_addresses.remove(address)

def reset_watched_addresses():
    global _watched_addresses
    _watched_addresses = set()

def activate_address_logging():
    reset_watched_addresses()
    logger.add(
            sink=sys.stdout,
            level="DEBUG",
            filter=_address_filter,
            # format="<green>{extra[item]}</green> <level>{level}</level> <u>{module}</u> - {message}",
            format="<green>Watched Address</green> <level>{level}</level> <u>{module}</u> - {message}",
            catch=True
        )