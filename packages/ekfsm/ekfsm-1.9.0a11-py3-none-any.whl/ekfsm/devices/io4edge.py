from typing import Callable, Optional
from ekfsm.core.components import HWModule
from ekfsm.devices.generic import Device
from ekfsm.log import ekfsm_logger
import io4edge_client.core.coreclient as CClient
from io4edge_client.binaryiotypeb import Client

from re import sub

logger = ekfsm_logger(__name__)


class IO4Edge(Device):
    """
    Device class for handling IO4Edge devices.

    See https://docs.ci4rail.com/user-docs/io4edge/ for more information.
    """

    def __init__(
        self,
        name: str,
        parent: HWModule | None = None,
        children: list[Device] | None = None,
        abort: bool = False,
        *args,
        **kwargs,
    ):
        logger.debug("Initializing IO4Edge device '%s'", name)

        super().__init__(name, parent, children, abort, *args, **kwargs)

        attr = self.hw_module.slot.attributes
        if (
            attr is None
            or not hasattr(attr, "slot_coding")
            or getattr(attr, "slot_coding") is None
        ):
            logger.error(
                "Slot attributes for %s are not set or do not contain 'slot_coding'",
                self.hw_module.slot.name,
            )
            raise ValueError(
                f"Slot attributes for {self.hw_module.slot.name} are not set or do not contain 'slot_coding'."
            )
        else:
            geoaddr = int(attr.slot_coding)
            self._geoaddr = geoaddr
            logger.debug("IO4Edge '%s' geo address: %s", name, geoaddr)

        _, module_name = sub(r"-.*$", "", self.hw_module.board_type).split(maxsplit=1)
        self._module_name = module_name
        logger.debug("IO4Edge '%s' module name: %s", name, module_name)

        try:
            self.client = CClient.new_core_client(self.deviceId, connect=False)
            logger.info(
                "IO4Edge '%s' initialized with device ID: %s", name, self.deviceId
            )
        except Exception as e:
            logger.error("Failed to create IO4Edge core client for '%s': %s", name, e)
            raise

    @property
    def deviceId(self) -> str:
        """
        Returns the device ID for the IO4Edge device.
        The device ID is a combination of the module name and the geo address.
        """
        return f"{self._module_name}-geo_addr{self._geoaddr:02d}"

    def open(self) -> None:
        """
        Open connection to the IO4Edge device.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug("Opening connection to IO4Edge device '%s'", self.name)
        try:
            self.client.open()
            logger.info("IO4Edge device '%s' connection opened successfully", self.name)
        except Exception as e:
            logger.error("Failed to open connection to IO4Edge device '%s': %s", self.name, e)
            raise

    def close(self) -> None:
        """
        Close connection to the IO4Edge device.

        Note
        ----
        Always call this method to properly cleanup resources and terminate background threads.
        """
        logger.debug("Closing connection to IO4Edge device '%s'", self.name)
        try:
            self.client.close()
            logger.info("IO4Edge device '%s' connection closed successfully", self.name)
        except Exception as e:
            logger.error("Failed to close connection to IO4Edge device '%s': %s", self.name, e)

    @property
    def connected(self) -> bool:
        """
        Check if the IO4Edge device is connected.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            return self.client.connected
        except Exception as e:
            logger.error("Failed to check connection status for IO4Edge device '%s': %s", self.name, e)
            return False

    def identify_firmware(self) -> tuple[str, str]:
        """
        Identify the firmware on the IO4Edge device.

        Returns
        -------
            A tuple containing the firmware title and version.
        """
        response = self.client.identify_firmware()
        return (
            response.title,
            response.version,
        )

    def load_firmware(
        self, cfg: bytes, progress_callback: Optional[Callable[[float], None]] = None
    ) -> None:
        """
        Load firmware onto the IO4Edge device.

        cfg
            Firmware configuration bytes.
        progress_callback
            Optional callback for progress updates.
        """
        self.client.load_firmware(cfg, progress_callback)

    def restart(self) -> None:
        """
        Restart the IO4Edge device.

        Important
        ---------
            This will disconnect the client from the device.
        """
        self.client.restart()

    def load_parameter(self, name: str, value: str) -> None:
        """
        Set a parameter onto the IO4Edge device.

        cfg
            The name of the parameter to load.
        value
            The value to set for the parameter.
        """
        self.client.set_persistent_parameter(name, value)

    def get_parameter(self, name: str) -> str:
        """
        Get a parameter value from the IO4Edge device.

        Returns
            The value of the requested parameter.
        """
        return self.client.get_persistent_parameter(name)

    def __repr__(self):
        return f"{self.name}; DeviceId: {self.deviceId}"


class GPIOArray(Device):
    """
    Device class for handling an io4edge GPIO array.
    """

    def __init__(
        self,
        name: str,
        parent: IO4Edge,
        children: list[Device] | None = None,
        abort: bool = False,
        service_suffix: str | None = None,
        keepaliveInterval: int = 10000,
        *args,
        **kwargs,
    ):
        logger.debug(
            "Initializing GPIOArray '%s' with parent device %s", name, parent.deviceId
        )

        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.name = name
        if service_suffix is not None:
            self.service_suffix = service_suffix
            logger.debug("Using custom service suffix: %s", service_suffix)
        else:
            self.service_suffix = name
            logger.debug("Using default service suffix: %s", name)

        self.deviceId = parent.deviceId
        self.service_addr = f"{self.deviceId}-{self.service_suffix}"
        self.timeout = int(keepaliveInterval / 1000 + 5)

        logger.info(
            "GPIOArray '%s' configured with service address: %s",
            name,
            self.service_addr,
        )

        try:
            self.client = Client(
                self.service_addr, command_timeout=self.timeout, connect=False
            )
            logger.debug("IO4Edge client created for service: %s", self.service_addr)
        except Exception as e:
            logger.error(
                "Failed to create IO4Edge client for %s: %s", self.service_addr, e
            )
            raise

    def open(self) -> None:
        """
        Open connection to the GPIO array.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug("Opening connection to GPIOArray '%s'", self.name)
        try:
            self.client.open()
            logger.info("GPIOArray '%s' connection opened successfully", self.name)
        except Exception as e:
            logger.error("Failed to open connection to GPIOArray '%s': %s", self.name, e)
            raise

    def close(self) -> None:
        """
        Close connection to the GPIO array.

        Note
        ----
        Always call this method to properly cleanup resources and terminate background threads.
        """
        logger.debug("Closing connection to GPIOArray '%s'", self.name)
        try:
            self.client.close()
            logger.info("GPIOArray '%s' connection closed successfully", self.name)
        except Exception as e:
            logger.error("Failed to close connection to GPIOArray '%s': %s", self.name, e)

    @property
    def connected(self) -> bool:
        """
        Check if the GPIO array is connected.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            return self.client.connected
        except Exception as e:
            logger.error("Failed to check connection status for GPIOArray '%s': %s", self.name, e)
            return False

    def __repr__(self):
        return f"{self.name}; Service Address: {self.service_addr}"
