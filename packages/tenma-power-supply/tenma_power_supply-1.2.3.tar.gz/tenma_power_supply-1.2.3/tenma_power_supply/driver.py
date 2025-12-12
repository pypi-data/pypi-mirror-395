"""
TENMA power supply
==================

Simple driver for a cheap 60V / 15A power supply, controllable over ethernet.

"""
import logging
import select
import socket

import retry
from generic_scpi_driver import GenericDriver
from generic_scpi_driver.session import Session

logger = logging.getLogger(__name__)
BUFFER_SIZE = 1024


class UDPSession(Session):
    """
    Interface for GenericSCPIDriver using a UDP connection

    Constructing this object opens a UDP connection to the given TENMA power supply.

    The TENMA supplies don't implement UDP properly: they always send messages
    to the same port as they listen on, regardless of the source port of the
    request. So, we must explicitly set up a socket that listens on the same
    port as it sends.
    """

    def __init__(self, id, port, baud_rate=None, timeout=1.0) -> None:
        self._ip = id
        self._port = port
        self._timeout = timeout

        logger.debug("Opening UDP connection to %s, %s", id, port)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)

        @retry.retry(exceptions=OSError, tries=10, jitter=0.5, logger=logger)
        def open_connection(sock: socket.socket):
            # The host IP will be narrowed down to the correct host IP as soon as
            # the other end is "connect"ed
            sock.bind(("0.0.0.0", port))
            sock.connect((id, port))

        open_connection(self._sock)

        logger.debug("UDP socket established")

    def write(self, s: str) -> None:
        msg = s.strip() + "\n"
        logger.debug("Sending message %s", msg)

        self._sock.send(bytes(msg, "utf-8"))

    def query(self, s: str) -> str:
        msg = s.strip() + "\n"

        logger.debug("Querying message %s", msg)

        self._sock.send(bytes(msg, "utf-8"))
        return str(self._sock.recv(BUFFER_SIZE), "utf-8").strip()

    def close(self) -> None:
        self._sock.close()

    def flush(self) -> None:
        while True:
            readable, _, _ = select.select([self._sock], [], [], 0)
            if not readable:
                break
            self._sock.recv(BUFFER_SIZE)


class TENMAPowerSupply(GenericDriver):
    """
    Driver for a TENMA 72-13360 ethernet power supply. Communicates over ethernet.
    """

    session_factory = UDPSession

    def __init__(
        self,
        *args,
        id: str = None,
        port: int = None,
        simulation: bool = False,
        **kwargs
    ):
        super().__init__(
            *args,
            id=id,
            port=port,
            simulation=simulation,
            command_separator=":",
            **kwargs
        )


TENMAPowerSupply._register_query(
    "get_identity",
    "*IDN?",
    response_parser=str,
)
TENMAPowerSupply._register_query(
    "get_current",
    "ISET?",
    response_parser=float,
)
TENMAPowerSupply._register_query(
    "set_current",
    "ISET",
    response_parser=None,
)


TENMAPowerSupply._register_query(
    "set_current",
    "ISET",
    response_parser=None,
    args=[GenericDriver.Arg(name="current", validator=lambda x: str(float(x)))],
)


TENMAPowerSupply._register_query(
    "set_voltage",
    "VSET",
    response_parser=None,
    args=[GenericDriver.Arg(name="voltage", validator=lambda x: str(float(x)))],
)

TENMAPowerSupply._register_query(
    "get_voltage",
    "VSET?",
    response_parser=float,
)
