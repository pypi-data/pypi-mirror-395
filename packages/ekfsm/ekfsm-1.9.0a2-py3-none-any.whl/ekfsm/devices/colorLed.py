from ekfsm.devices.generic import Device
from ekfsm.devices.ledArray import LEDArray
from ekfsm.devices.utils import retry
from ekfsm.log import ekfsm_logger
from io4edge_client.api.colorLED.python.colorLED.v1alpha1.colorLED_pb2 import Color

logger = ekfsm_logger(__name__)


class ColorLED(Device):
    """
    Device class for handling a color LED.
    """

    def __init__(
        self,
        name: str,
        parent: LEDArray,
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
