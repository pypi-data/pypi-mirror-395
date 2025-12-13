from ekfsm.devices.generic import Device
from ekfsm.devices.io4edge import IO4Edge
from ekfsm.devices.utils import retry
from ekfsm.log import ekfsm_logger
from io4edge_client.colorLED import Client
from io4edge_client.api.colorLED.python.colorLED.v1alpha1.colorLED_pb2 import Color

logger = ekfsm_logger(__name__)


class LEDArray(Device):
    """
    Device class for handling a LED array.
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
            f"Initializing LEDArray '{name}' with parent device {parent.deviceId}"
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
            f"LEDArray '{name}' configured with service address: {self.service_addr}"
        )

        try:
            self.client = Client(self.service_addr, connect=False)
            logger.debug(f"LEDArray client created for service: {self.service_addr}")
        except Exception as e:
            logger.error(
                f"Failed to create LEDArray client for {self.service_addr}: {e}"
            )
            raise

    def open(self) -> None:
        """
        Open connection to the LED array.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug(f"Opening connection to LEDArray '{self.name}'")
        try:
            self.client.open()
            logger.info(f"LEDArray '{self.name}' connection opened successfully")
        except Exception as e:
            logger.error(f"Failed to open connection to LEDArray '{self.name}': {e}")
            raise

    def close(self) -> None:
        """
        Close connection to the LED array.

        Note
        ----
        Always call this method to properly cleanup resources and terminate background threads.
        """
        logger.debug(f"Closing connection to LEDArray '{self.name}'")
        try:
            self.client.close()
            logger.info(f"LEDArray '{self.name}' connection closed successfully")
        except Exception as e:
            logger.error(f"Failed to close connection to LEDArray '{self.name}': {e}")

    @property
    def connected(self) -> bool:
        """
        Check if the LED array is connected.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            return self.client.connected
        except Exception as e:
            logger.error(
                f"Failed to check connection status for LEDArray '{self.name}': {e}"
            )
            return False

    def __repr__(self):
        return f"{self.name}; Service Address: {self.service_addr}"


class ColorLED(Device):
    """
    Device class for handling a color LED.
    """

    def __init__(
        self,
        name: str,
        parent: "LEDArray",
        children: list[Device] | None = None,
        abort: bool = False,
        channel_id: int = 0,
        *args,
        **kwargs,
    ):
        logger.debug(f"Initializing ColorLED '{name}' on channel {channel_id}")

        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.name = name
        self.channel_id = channel_id

        self.client = parent.client
        logger.info(
            f"ColorLED '{name}' initialized on channel {channel_id} with parent LEDArray"
        )

    def open(self) -> None:
        """
        Open connection to the color LED through parent LEDArray.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug(f"Opening connection to ColorLED '{self.name}' via parent")
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, "open"):
                parent.open()
                logger.info(
                    f"ColorLED '{self.name}' connection opened via parent LEDArray"
                )
            else:
                raise RuntimeError(
                    f"Parent of ColorLED '{self.name}' is None or does not have open method"
                )
        except Exception as e:
            logger.error(
                f"Failed to open connection to ColorLED '{self.name}' via parent: {e}"
            )
            raise

    def close(self) -> None:
        """
        Close connection to the color LED through parent LEDArray.

        Note
        ----
        This delegates to the parent LEDArray's close method.
        """
        logger.debug(f"Closing connection to ColorLED '{self.name}' via parent")
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, "close"):
                parent.close()
                logger.info(
                    f"ColorLED '{self.name}' connection closed via parent LEDArray"
                )
            else:
                raise RuntimeError(
                    f"Parent of ColorLED '{self.name}' is None or does not have close method"
                )
        except Exception as e:
            logger.error(
                f"Failed to close connection to ColorLED '{self.name}' via parent: {e}"
            )

    @property
    def connected(self) -> bool:
        """
        Check if the color LED is connected through parent LEDArray.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, "connected"):
                return parent.connected
            else:
                logger.error(
                    f"Parent of ColorLED '{self.name}' is None or does not have connected property"
                )
                return False
        except Exception as e:
            logger.error(
                f"Failed to check connection status for ColorLED '{self.name}' via parent: {e}"
            )
            return False

    @retry()
    def describe(self):
        pass

    @retry()
    def get(self) -> tuple[Color, bool]:
        """
        Get color LED state.

        Returns
        -------
            Current color and blink state.

        Raises
        ------
        RuntimeError
            if the command fails
        TimeoutError
            if the command times out
        """
        logger.info(
            "Getting color LED state for '%s' on channel %s", self.name, self.channel_id
        )
        try:
            result = self.client.get(self.channel_id)
            color, blink = result
            logger.info(
                "ColorLED '%s' state: color=%s, blink=%s", self.name, color, blink
            )
            return result
        except Exception as e:
            logger.error(
                "Failed to get ColorLED '%s' state on channel %s: %s",
                self.name,
                self.channel_id,
                e,
            )
            raise

    @retry()
    def set(self, color: Color, blink: bool) -> None:
        """
        Set the color of the color LED.

        Parameters
        ----------
        color : :class:`~io4edge_client.api.colorLED.python.colorLED.v1alpha1.colorLED_pb2.Color`
            The color to set the LED to.
        blink : bool
            Whether to blink the LED.

        Raises
        ------
        RuntimeError
            if the command fails
        TimeoutError
            if the command times out
        """
        logger.info(
            f"Setting ColorLED '{self.name}' on channel {self.channel_id}: color={color}, blink={blink}"
        )
        try:
            self.client.set(self.channel_id, color, blink)
            logger.debug(
                f"ColorLED '{self.name}' successfully set to color={color}, blink={blink}"
            )
        except Exception as e:
            logger.error(
                f"Failed to set ColorLED '{self.name}' on channel {self.channel_id}: {e}"
            )
            raise

    def __repr__(self):
        return f"{self.name}; Channel ID: {self.channel_id}"
