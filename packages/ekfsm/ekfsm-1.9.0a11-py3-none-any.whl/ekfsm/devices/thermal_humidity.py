from ekfsm.devices.generic import Device
from ekfsm.devices.io4edge import IO4Edge
from ekfsm.devices.utils import retry
from ekfsm.log import ekfsm_logger
from io4edge_client.analogintypeb import Client

logger = ekfsm_logger(__name__)


class ThermalHumidity(Device):
    """
    Device class for handling a thermal humidity sensor.
    """

    def __init__(
        self,
        name: str,
        parent: IO4Edge,
        children: list[Device] | None = None,
        abort: bool = False,
        service_suffix: str | None = None,
        *args,
        **kwargs,
    ):
        logger.debug(
            f"Initializing ThermalHumidity sensor '{name}' with parent device {parent.deviceId}"
        )

        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.name = name

        if service_suffix is not None:
            self.service_suffix = service_suffix
            logger.debug(f"Using custom service suffix: {service_suffix}")
        else:
            self.service_suffix = name
            logger.debug(f"Using default service suffix: {name}")

        self.service_addr = f"{parent.deviceId}-{self.service_suffix}"
        logger.info(
            f"ThermalHumidity '{name}' configured with service address: {self.service_addr}"
        )

        try:
            self.client = Client(self.service_addr, connect=False)
            logger.debug(
                f"ThermalHumidity client created for service: {self.service_addr}"
            )
        except Exception as e:
            logger.error(
                f"Failed to create ThermalHumidity client for {self.service_addr}: {e}"
            )
            raise

    def open(self) -> None:
        """
        Open connection to the thermal humidity sensor.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug(f"Opening connection to ThermalHumidity sensor '{self.name}'")
        try:
            self.client.open()
            logger.info(f"ThermalHumidity sensor '{self.name}' connection opened successfully")
        except Exception as e:
            logger.error(f"Failed to open connection to ThermalHumidity sensor '{self.name}': {e}")
            raise

    def close(self) -> None:
        """
        Close connection to the thermal humidity sensor.

        Note
        ----
        Always call this method to properly cleanup resources and terminate background threads.
        """
        logger.debug(f"Closing connection to ThermalHumidity sensor '{self.name}'")
        try:
            self.client.close()
            logger.info(f"ThermalHumidity sensor '{self.name}' connection closed successfully")
        except Exception as e:
            logger.error(f"Failed to close connection to ThermalHumidity sensor '{self.name}': {e}")

    @property
    def connected(self) -> bool:
        """
        Check if the thermal humidity sensor is connected.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            return self.client.connected
        except Exception as e:
            logger.error(f"Failed to check connection status for ThermalHumidity sensor '{self.name}': {e}")
            return False

    @retry()
    def temperature(self) -> float:
        """
        Get the temperature in Celsius.

        Raises
        ------
        RuntimeError
            if the command fails
        TimeoutError
            if the command times out
        """
        logger.info(f"Reading temperature from ThermalHumidity sensor '{self.name}'")
        try:
            temp = self.client.value()
            logger.info(f"ThermalHumidity '{self.name}' temperature: {temp}°C")
            return temp
        except Exception as e:
            logger.error(
                f"Failed to read temperature from ThermalHumidity '{self.name}': {e}"
            )
            raise

    def __repr__(self):
        return f"{self.name}; Service Address: {self.service_addr}"
