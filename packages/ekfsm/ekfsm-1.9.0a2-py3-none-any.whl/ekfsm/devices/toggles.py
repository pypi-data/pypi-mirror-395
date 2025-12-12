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

        logger.debug(
            f"Initializing BinaryToggle '{name}' with parent device {parent.deviceId}"
        )

        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.name = name

        self.service_addr = parent.service_addr

        logger.info(
            f"BinaryToggle '{name}' configured with service address: {self.service_addr} on channel {channel_id}"
        )

        self.client: Client = parent.client

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
