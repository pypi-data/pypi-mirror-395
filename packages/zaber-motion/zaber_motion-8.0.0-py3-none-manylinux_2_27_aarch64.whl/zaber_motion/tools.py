# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import List
from .call import call, call_async, call_sync
from .dto import requests as dto


class Tools:
    """
    Class providing various utility functions.
    """

    @staticmethod
    def list_serial_ports() -> List[str]:
        """
        Lists all serial ports on the computer.

        Returns:
            Array of serial port names.
        """
        request = dto.EmptyRequest(
        )
        response = call(
            "tools/list_serial_ports",
            request,
            dto.ToolsListSerialPortsResponse.from_binary)
        return response.ports

    @staticmethod
    async def list_serial_ports_async() -> List[str]:
        """
        Lists all serial ports on the computer.

        Returns:
            Array of serial port names.
        """
        request = dto.EmptyRequest(
        )
        response = await call_async(
            "tools/list_serial_ports",
            request,
            dto.ToolsListSerialPortsResponse.from_binary)
        return response.ports

    @staticmethod
    def get_message_router_pipe_path() -> str:
        """
        Returns path of message router named pipe on Windows
        or file path of unix domain socket on UNIX.

        Returns:
            Path of message router's named pipe or unix domain socket.
        """
        request = dto.EmptyRequest(
        )
        response = call_sync(
            "tools/get_message_router_pipe",
            request,
            dto.StringResponse.from_binary)
        return response.value

    @staticmethod
    def get_db_service_pipe_path() -> str:
        """
        Returns the path for communicating with a local device database service.
        This will be a named pipe on Windows and the file path of a unix domain socket on UNIX.

        Returns:
            Path of database service's named pipe or unix domain socket.
        """
        request = dto.EmptyRequest(
        )
        response = call_sync(
            "tools/get_db_service_pipe",
            request,
            dto.StringResponse.from_binary)
        return response.value
