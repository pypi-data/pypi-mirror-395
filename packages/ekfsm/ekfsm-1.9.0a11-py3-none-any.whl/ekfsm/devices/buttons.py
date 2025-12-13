import threading
from typing import Callable
from ekfsm.devices.utils import retry
from io4edge_client.binaryiotypeb import Pb
from ekfsm.devices.generic import Device
from ekfsm.devices.io4edge import GPIOArray
from ekfsm.log import ekfsm_logger
import io4edge_client.functionblock as fb

logger = ekfsm_logger(__name__)


class Button(Device):
    """
    Device class for handling a single button as part on array.
    """

    def __init__(
        self,
        name: str,
        parent: Device,
        children: list[Device] | None = None,
        abort: bool = False,
        channel_id: int = 0,
        *args,
        **kwargs,
    ):
        logger.debug(f"Initializing Button '{name}' on channel {channel_id}")

        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.channel_id = channel_id
        logger.debug(f"Button '{name}' assigned to channel {channel_id}")

        self._handler: Callable | None = None
        logger.info(f"Button '{name}' initialized on channel {channel_id}")

    def open(self) -> None:
        """
        Open connection to the button through parent device.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug(f"Opening connection to Button '{self.name}' via parent")
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, 'open'):
                parent.open()
                logger.info(f"Button '{self.name}' connection opened via parent")
            else:
                raise RuntimeError(f"Parent of Button '{self.name}' is None or does not have open method")
        except Exception as e:
            logger.error(f"Failed to open connection to Button '{self.name}' via parent: {e}")
            raise

    def close(self) -> None:
        """
        Close connection to the button through parent device.

        Note
        ----
        This delegates to the parent device's close method.
        """
        logger.debug(f"Closing connection to Button '{self.name}' via parent")
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, 'close'):
                parent.close()
                logger.info(f"Button '{self.name}' connection closed via parent")
            else:
                raise RuntimeError(f"Parent of Button '{self.name}' is None or does not have close method")
        except Exception as e:
            logger.error(f"Failed to close connection to Button '{self.name}' via parent: {e}")

    @property
    def connected(self) -> bool:
        """
        Check if the button is connected through parent device.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, 'connected'):
                return parent.connected
            else:
                logger.error(f"Parent of Button '{self.name}' is None or does not have connected property")
                return False
        except Exception as e:
            logger.error(f"Failed to check connection status for Button '{self.name}' via parent: {e}")
            return False

    @property
    def handler(self):
        """
        Handle button events with a callback function.
        """
        return self._handler

    @handler.setter
    def handler(self, func: Callable | None, *args, **kwargs):
        """
        Handle button events with a callback function.

        Parameters
        ----------
        func : Callable | None
            The function to call on button events. If None, no function is called.
        """
        if callable(func):
            self._handler = func
            logger.info(
                f"Handler set for button '{self.name}' on channel {self.channel_id}"
            )
            logger.debug(
                f"Handler function: {func.__name__ if hasattr(func, '__name__') else str(func)}"
            )
        else:
            self._handler = None
            logger.debug(
                f"Handler cleared for button '{self.name}' on channel {self.channel_id}"
            )

    def __repr__(self):
        return f"{self.name}; Channel ID: {self.channel_id}"


class ButtonArray(Device):
    """
    Device class for handling an io4edge gpio based button array.

    To read button events, call the `read` method in a separate thread.

    Note
    ----
        Button handlers are called in the context of the `read` method's thread and need to be set in the Button instances.
    """

    def __init__(
        self,
        name: str,
        parent: GPIOArray,
        children: list[Device] | None = None,
        abort: bool = False,
        keepaliveInterval: int = 10000,
        *args,
        **kwargs,
    ):
        logger.debug(
            f"Initializing ButtonArray '{name}' with parent device {parent.deviceId}"
        )

        super().__init__(name, parent, children, abort, *args, **kwargs)

        self.name = name

        self.service_addr = parent.service_addr
        self.client = parent.client

        logger.info(
            f"ButtonArray '{name}' configured with service address: {self.service_addr}"
        )

        self.subscriptionType = Pb.SubscriptionType.BINARYIOTYPEB_ON_RISING_EDGE
        self.stream_cfg = fb.Pb.StreamControlStart(
            bucketSamples=1,  # 1 sample per bucket, also ein event pro bucket
            keepaliveInterval=keepaliveInterval,
            bufferedSamples=2,  # 2 samples werden gepuffert
            low_latency_mode=True,  # schickt soweit moeglich sofort die Events
        )
        logger.debug(
            "Stream configuration initialized with rising edge subscription and low latency mode"
        )

        # Log button children count
        button_count = sum(1 for child in (children or []) if isinstance(child, Button))
        logger.info(f"ButtonArray '{name}' initialized with {button_count} button(s)")

    def open(self) -> None:
        """
        Open connection to the button array through parent GPIOArray.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug(f"Opening connection to ButtonArray '{self.name}' via parent")
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, 'open'):
                parent.open()
                logger.info(f"ButtonArray '{self.name}' connection opened via parent GPIOArray")
            else:
                raise RuntimeError(f"Parent of ButtonArray '{self.name}' is None or does not have open method")
        except Exception as e:
            logger.error(f"Failed to open connection to ButtonArray '{self.name}' via parent: {e}")
            raise

    def close(self) -> None:
        """
        Close connection to the button array through parent GPIOArray.

        Note
        ----
        This delegates to the parent GPIOArray's close method.
        """
        logger.debug(f"Closing connection to ButtonArray '{self.name}' via parent")
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, 'close'):
                parent.close()
                logger.info(f"ButtonArray '{self.name}' connection closed via parent GPIOArray")
            else:
                raise RuntimeError(f"Parent of ButtonArray '{self.name}' is None or does not have close method")
        except Exception as e:
            logger.error(f"Failed to close connection to ButtonArray '{self.name}' via parent: {e}")

    @property
    def connected(self) -> bool:
        """
        Check if the button array is connected through parent GPIOArray.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            parent = self.parent
            if parent is not None and hasattr(parent, 'connected'):
                return parent.connected
            else:
                logger.error(f"Parent of ButtonArray '{self.name}' is None or does not have connected property")
                return False
        except Exception as e:
            logger.error(f"Failed to check connection status for ButtonArray '{self.name}' via parent: {e}")
            return False

    def read(self, stop_event: threading.Event | None = None, timeout: float = 1):
        """
        Read all button events and dispatch to handlers.

        Parameters
        ----------
        stop_event : threading.Event, optional
            Event to signal stopping the reading loop. If None, the loop will run indefinitely.
        timeout : float, optional
            Timeout for reading from the stream in seconds. Default is 0.1 seconds.

        Note
        ----
            This method blocks and should be run in a separate thread.
        """
        button_channels = [
            button for button in self.children if isinstance(button, Button)
        ]

        if not button_channels:
            logger.warning(
                f"No button children found in ButtonArray '{self.name}', read operation will have no effect"
            )
            return

        logger.info(
            f"Starting button event reading for {len(button_channels)} buttons on '{self.name}'"
        )
        logger.debug(
            f"Read timeout: {timeout}s, stop_event provided: {stop_event is not None}"
        )
        # Prepare subscription channels
        subscribe_channels = tuple(
            Pb.SubscribeChannel(
                channel=button.channel_id,
                subscriptionType=self.subscriptionType,
            )
            for button in button_channels
        )

        channel_ids = [button.channel_id for button in button_channels]

        try:
            self._button_event_handling(
                stop_event,
                timeout,
                subscribe_channels,
                button_channels,
                channel_ids,
            )
        except Exception as e:
            logger.error(
                f"Failed to establish connection or start stream for ButtonArray '{self.name}': {e}"
            )
            raise

    @retry()
    def _button_event_handling(
        self,
        stop_event: threading.Event | None,
        timeout: float,
        subscribe_channels: tuple,
        button_channels: list,
        channel_ids: list,
    ):
        with self.client as client:
            logger.debug(f"IO4Edge client connected to service: {self.service_addr}")

            logger.debug(
                f"Subscribing to {len(subscribe_channels)} button channels: {channel_ids}"
            )

            client.start_stream(
                Pb.StreamControlStart(subscribeChannel=subscribe_channels),
                self.stream_cfg,
            )
            logger.info(f"Button event stream started for ButtonArray '{self.name}'")

            event_count = 0
            try:
                while not (stop_event and stop_event.is_set()):
                    try:
                        _, samples = client.read_stream(timeout=timeout)

                        for sample in samples.samples:
                            for button in button_channels:
                                pressed = bool(sample.inputs & (1 << button.channel_id))
                                if pressed:
                                    event_count += 1
                                    button_name = getattr(button, "name", "unnamed")
                                    logger.debug(
                                        f"Button press on channel {button.channel_id} ({button_name})"
                                    )

                                    if button.handler:
                                        try:
                                            logger.debug(
                                                f"Calling handler for button on channel {button.channel_id}"
                                            )
                                            button.handler()
                                        except Exception as e:
                                            logger.error(
                                                f"Error in button handler for channel {button.channel_id}: {e}"
                                            )
                                    else:
                                        logger.debug(
                                            f"No handler set for button on channel {button.channel_id}"
                                        )

                    except TimeoutError:
                        # Timeout is expected during normal operation
                        continue
                    except Exception as e:
                        logger.error(f"Error reading button events from stream: {e}")
                        break

            except KeyboardInterrupt:
                logger.info(f"Button reading interrupted for ButtonArray '{self.name}'")
            finally:
                logger.info(
                    f"Button event reading stopped for '{self.name}' after processing {event_count} events"
                )
                if stop_event:
                    stop_event.clear()
                    logger.debug("Stop event cleared")

    def __repr__(self):
        return f"{self.name}; Service Address: {self.service_addr}"
