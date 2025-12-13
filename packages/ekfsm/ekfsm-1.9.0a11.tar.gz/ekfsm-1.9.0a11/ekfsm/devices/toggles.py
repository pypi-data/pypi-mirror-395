from ekfsm.devices.utils import retry
from io4edge_client.binaryiotypeb import Client
from ekfsm.devices.generic import Device
from ekfsm.devices.io4edge import GPIOArray
from ekfsm.log import ekfsm_logger

logger = ekfsm_logger(__name__)


class BinaryToggle(Device):
    """
    Device class for handling a binary toggle switch.
    """

    def __init__(
        self,
        name: str,
        parent: GPIOArray,
        children: list[Device] | None = None,
        abort: bool = False,
        channel_id: int = 0,
        *args,
        **kwargs,
    ):
        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.channel_id = channel_id
        self.name = name
        self.service_addr = parent.service_addr
        self.client: Client = parent.client

        logger.debug(
            f"Initializing BinaryToggle '{name}' with parent device {parent.deviceId}"
        )
        logger.info(
            f"BinaryToggle '{name}' configured with service address: {self.service_addr} on channel {channel_id}"
        )

    def open(self) -> None:
        """
        Open connection to the binary toggle through parent GPIOArray.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug(f"Opening connection to BinaryToggle '{self.name}' via parent")
        try:
            if isinstance(self.parent, GPIOArray):
                self.parent.open()
                logger.info(f"BinaryToggle '{self.name}' connection opened via parent GPIOArray")
            else:
                raise RuntimeError(f"Parent of BinaryToggle '{self.name}' is not a GPIOArray")
        except Exception as e:
            logger.error(f"Failed to open connection to BinaryToggle '{self.name}' via parent: {e}")
            raise

    def close(self) -> None:
        """
        Close connection to the binary toggle through parent GPIOArray.

        Note
        ----
        This delegates to the parent GPIOArray's close method.
        """
        logger.debug(f"Closing connection to BinaryToggle '{self.name}' via parent")
        try:
            if isinstance(self.parent, GPIOArray):
                self.parent.close()
                logger.info(f"BinaryToggle '{self.name}' connection closed via parent GPIOArray")
            else:
                raise RuntimeError(f"Parent of BinaryToggle '{self.name}' is not a GPIOArray")
        except Exception as e:
            logger.error(f"Failed to close connection to BinaryToggle '{self.name}' via parent: {e}")

    @property
    def connected(self) -> bool:
        """
        Check if the binary toggle is connected through parent GPIOArray.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            if isinstance(self.parent, GPIOArray):
                return self.parent.connected
            else:
                logger.error(f"Parent of BinaryToggle '{self.name}' is not a GPIOArray")
                return False
        except Exception as e:
            logger.error(f"Failed to check connection status for BinaryToggle '{self.name}' via parent: {e}")
            return False

    @retry()
    def set(self, state: bool):
        """
        Set the state of the toggle switch.

        Parameters
        ----------
            state
                state to set. a "true" state turns on the toggle switch, a "false" state turns it off.
        """
        logger.info(
            f"Setting BinaryToggle '{self.name}' on channel {self.channel_id} to state {state}"
        )
        self.client.set_output(self.channel_id, state)
        logger.info(
            f"BinaryToggle '{self.name}' on channel {self.channel_id} set to state {state}"
        )

    @retry()
    def get(self) -> bool:
        """
        Get the current state of the toggle switch.

        Returns
            The current state of the toggle switch.
        """
        state = self.client.get_input(self.channel_id)
        logger.info(
            f"Retrieved state {state} for BinaryToggle '{self.name}' on channel {self.channel_id}"
        )
        return state

    def on(self):
        """
        Turn the toggle switch on.
        """
        self.set(True)

    def off(self):
        """
        Turn the toggle switch off.
        """
        self.set(False)

    def __repr__(self):
        return f"{self.name}; Channel ID: {self.channel_id}"
