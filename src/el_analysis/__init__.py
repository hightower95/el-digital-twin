
from el_analysis.config import summarize_config, config
from el_analysis.utils.setup_logging import logger as logging # type: ignore
from el_analysis.utils.address_logging import activate_address_logging
activate_address_logging()
# from .core import logging

# from .core import Address
from el_analysis.core import Address, Project, Location

from el_analysis.models import Device, Interface#, Interface, Connector, Pin

#, Connector, Interface, Pin
# from .models import Device
# summarize_config(do_print=True)  # Print the configuration summary at module load


from el_analysis.connector_toolkit.utils import get_connector_from_part_number