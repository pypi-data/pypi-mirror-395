import serial
import time
from .TemplateCommunications import *
class SerialCommunication(TemplateCommunications):
    def __init__(self, port, baudrate=19200, timeout=1):
        super().__init__()
        """
        Initialize the SerialCommunication object.

        :param port: Serial port name (e.g., 'COM3' or '/dev/ttyUSB0')
        :param baudrate: Baud rate for the serial communication (default is 19200)
        :param timeout: Timeout for read operations in seconds (default is 1)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def open(self):
        """Open the serial port connection."""
        if self.serial_connection is not None and self.serial_connection.is_open:
            print("Serial port already open.")
            return -1

        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            return 0
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return -1

    def close(self):
        """Close the serial port connection."""
        if self.serial_connection is None or not self.serial_connection.is_open:
            print("Serial port is not open.")
            return -1

        try:
            self.serial_connection.close()
            return 0
        except serial.SerialException as e:
            print(f"Error closing serial port: {e}")
            return -1

    def send(self, data):
        """
        Send data through the serial port.

        :param data: Data to be sent (should be bytes or a string)
        """
        if self.serial_connection is None or not self.serial_connection.is_open:
            print("Serial port is not open.")
            return -1

        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes if necessary

        try:
            self.serial_connection.write(data)
            return 0
        except serial.SerialException as e:
            print(f"Error sending data: {e}")
            return -1

    def receive(self,n_bytes):
        """
        Receive data from the serial port.

        :return: Received data as bytes
        """
        if self.serial_connection is None or not self.serial_connection.is_open:
            print("Serial port is not open.")
            return None

        try:
            data = self.serial_connection.read(n_bytes)  # Read all available data
            return data
        except serial.SerialException as e:
            print(f"Error receiving data: {e}")
            return None

    def flush(self):
        """Flush the input and output buffers."""
        if self.serial_connection is None or not self.serial_connection.is_open:
            print("Serial port is not open.")
            return -1

        try:
            self.serial_connection.flush()
            return 0
        except serial.SerialException as e:
            print(f"Error flushing buffers: {e}")
            return -1