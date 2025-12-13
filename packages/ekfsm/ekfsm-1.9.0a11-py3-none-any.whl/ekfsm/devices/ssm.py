from typing import TYPE_CHECKING
from ekfsm.devices.generic import Device
from ekfsm.devices.utils import retry
from ekfsm.log import ekfsm_logger
from io4edge_client.ssm import Client
import io4edge_client.api.ssm.python.ssm.v1.ssm_pb2 as Pb

if TYPE_CHECKING:
    from ekfsm.devices.io4edge import IO4Edge

logger = ekfsm_logger(__name__)


class SSM(Device):
    """
    Device class for handling System State Manager (SSM) functionality.

    The SSM manages system state transitions and provides watchdog functionality
    for io4edge devices.
    """

    def __init__(
        self,
        name: str,
        parent: "IO4Edge",
        children: list[Device] | None = None,
        abort: bool = False,
        service_suffix: str | None = None,
        keepaliveInterval: int = 10000,
        *args,
        **kwargs,
    ):
        logger.debug(
            "Initializing SSM '%s' with parent device %s", name, parent.deviceId
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
            "SSM '%s' configured with service address: %s",
            name,
            self.service_addr,
        )

        try:
            self.client = Client(
                self.service_addr, command_timeout=self.timeout, connect=False
            )
            logger.debug("SSM client created for service: %s", self.service_addr)
        except Exception as e:
            logger.error("Failed to create SSM client for %s: %s", self.service_addr, e)
            raise

    def open(self) -> None:
        """
        Open connection to the System State Manager.

        Raises
        ------
        RuntimeError
            If connection fails
        """
        logger.debug("Opening connection to SSM '%s'", self.name)
        try:
            self.client.open()
            logger.info("SSM '%s' connection opened successfully", self.name)
        except Exception as e:
            logger.error("Failed to open connection to SSM '%s': %s", self.name, e)
            raise

    def close(self) -> None:
        """
        Close connection to the System State Manager.

        Note
        ----
        Always call this method to properly cleanup resources and terminate background threads.
        """
        logger.debug("Closing connection to SSM '%s'", self.name)
        try:
            self.client.close()
            logger.info("SSM '%s' connection closed successfully", self.name)
        except Exception as e:
            logger.error("Failed to close connection to SSM '%s': %s", self.name, e)

    @property
    def connected(self) -> bool:
        """
        Check if the System State Manager is connected.

        Returns
        -------
        bool
            True if connected, False otherwise
        """
        try:
            return self.client.connected
        except Exception as e:
            logger.error("Failed to check connection status for SSM '%s': %s", self.name, e)
            return False

    @retry()
    def describe(self) -> Pb.ConfigurationDescribeResponse:
        """
        Get the description from the System State Manager functionblock.

        Returns
        -------
        Pb.ConfigurationDescribeResponse
            Description from the SSM functionblock

        Raises
        ------
        RuntimeError
            if the command fails
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        """
        logger.info("Getting SSM description for '%s'", self.name)
        try:
            result = self.client.describe()
            logger.debug("SSM '%s' description retrieved successfully", self.name)
            return result
        except Exception as e:
            logger.error("Failed to get SSM '%s' description: %s", self.name, e)
            raise

    @retry()
    def kick(self) -> None:
        """
        Kick the System State Manager to prevent a timeout.

        This method should be called periodically to indicate that the system
        is still alive and prevent the watchdog from triggering.

        Raises
        ------
        RuntimeError
            if the command fails
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        """
        logger.debug("Kicking SSM watchdog for '%s'", self.name)
        try:
            self.client.kick()
            logger.debug("SSM '%s' watchdog kicked successfully", self.name)
        except Exception as e:
            logger.error("Failed to kick SSM '%s' watchdog: %s", self.name, e)
            raise

    @retry()
    def state(self) -> Pb.SystemState:
        """
        Get the current system state from the SSM.

        Returns
        -------
        Pb.SystemState
            Current system state (OFF, ON, ERROR, etc.)

        Raises
        ------
        RuntimeError
            if the command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        """
        logger.info("Getting system state for SSM '%s'", self.name)
        try:
            state = self.client.state
            logger.info("SSM '%s' current state: %s", self.name, state)
            return state
        except Exception as e:
            logger.error("Failed to get SSM '%s' state: %s", self.name, e)
            raise

    @retry()
    def error(self, message: str) -> None:
        """
        Set the system to error state with the given message.

        Parameters
        ----------
        message : str
            Error message to log

        Raises
        ------
        RuntimeError
            if command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        InvalidStateError
            if operation attempted in an invalid state
        UnknownError
            if unknown error occurs while setting error state
        """
        logger.warning("Setting SSM '%s' to error state: %s", self.name, message)
        try:
            self.client.error(message)
            logger.info("SSM '%s' error state set successfully", self.name)
        except Exception as e:
            logger.error("Failed to set SSM '%s' error state: %s", self.name, e)
            raise

    @retry()
    def resolve(self, message: str) -> None:
        """
        Resolve the current error state.

        Parameters
        ----------
        message : str
            Resolution message

        Raises
        ------
        RuntimeError
            if command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        InvalidStateError
            if operation attempted in an invalid state
        UnknownError
            if unknown error occurs while resolving error
        """
        logger.info("Resolving SSM '%s' error state: %s", self.name, message)
        try:
            self.client.resolve(message)
            logger.info("SSM '%s' error resolved successfully", self.name)
        except Exception as e:
            logger.error("Failed to resolve SSM '%s' error: %s", self.name, e)
            raise

    @retry()
    def fatal(self, message: str) -> None:
        """
        Signal a fatal error to the SSM.

        Parameters
        ----------
        message : str
            Fatal error message

        Raises
        ------
        RuntimeError
            if command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        InvalidStateError
            if operation attempted in an invalid state
        UnknownError
            if unknown error occurs signaling fatal error
        """
        logger.critical("Setting SSM '%s' fatal error: %s", self.name, message)
        try:
            self.client.fatal(message)
            logger.info("SSM '%s' fatal error set successfully", self.name)
        except Exception as e:
            logger.error("Failed to set SSM '%s' fatal error: %s", self.name, e)
            raise

    @retry()
    def shutdown(self) -> None:
        """
        Indicate system shutdown to the SSM.

        Raises
        ------
        RuntimeError
            if command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        InvalidStateError
            if operation attempted in an invalid state
        UnknownError
            if unknown error occurs while signaling shutdown
        """
        logger.info("Signaling shutdown to SSM '%s'", self.name)
        try:
            self.client.shutdown()
            logger.info("SSM '%s' shutdown signal sent successfully", self.name)
        except Exception as e:
            logger.error("Failed to signal shutdown to SSM '%s': %s", self.name, e)
            raise

    @retry()
    def on(self) -> None:
        """
        Signal ON state to the SSM.

        Raises
        ------
        RuntimeError
            if command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        InvalidStateError
            if operation attempted in an invalid state
        UnknownError
            if unknown error occurs while turning on
        """
        logger.info("Turning on SSM '%s'", self.name)
        try:
            self.client.on()
            logger.info("SSM '%s' turned on successfully", self.name)
        except Exception as e:
            logger.error("Failed to turn on SSM '%s': %s", self.name, e)
            raise

    @retry()
    def reboot(self) -> None:
        """
        Signal a reboot to the SSM.

        Raises
        ------
        RuntimeError
            if command fails or unhandled response
        TimeoutError
            if the command times out
        ConnectionError
            if not connected to the device
        InvalidStateError
            if operation attempted in an invalid state
        UnknownError
            if unknown error occurs while signaling reboot
        """
        logger.info("Signaling reboot to SSM '%s'", self.name)
        try:
            self.client.reboot()
            logger.info("SSM '%s' reboot signal sent successfully", self.name)
        except Exception as e:
            logger.error("Failed to signal reboot to SSM '%s': %s", self.name, e)
            raise

    def __repr__(self):
        return f"SSM({self.name}; Service Address: {self.service_addr})"
