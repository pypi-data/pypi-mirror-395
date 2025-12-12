import serial
import struct
import time

class APSController:
    def __init__(self, port, baudrate=19200, timeout=1,device_id=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.device_id = device_id

        self.instructions = {
            "output_status" : 0x30,
            "target_frequency" : 0x31,
            "he_target_voltage" : 0x32,
            "auto_target_voltage" : 0x33,
            "max_out_current" : 0x34,
            "control_output" : 0x35,
            "control_output_status" : 0x36,
            "serial_no" : 0x4A,
            "i_rms" : 0x60,
            "v_rms" : 0x61,
            "i_peak" : 0x62,
            "v_peak" : 0x63,
            "p_va" : 0x64,
            "p_w" : 0x65,
            "p_f" : 0x66,
            "f_req" : 0x67
        }

    def connect(self):
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS
            )
        except serial.SerialException as e:
            self.serial_connection = None

    def setup(self,voltage,frequency,max_current):
        self.connect()
        time.sleep(1)
        self.writeControlOutput(False)
        self.writeAutoTargetVoltage(voltage)
        self.writeTargetFrequency(frequency)
        self.writeMaxOutCurrent(max_current)
        self.writeControlOutput(True)
        time.sleep(5)

    def checksum(self, data):
        """Calculate the checksum by summing the first 7 bytes."""
        return sum(data[:7]) & 0xFF

    def sendCommand(self, command_code, operation_code, data):
        """Send a command following the device's protocol."""
        command = struct.pack('B', self.device_id) + struct.pack('B', command_code) + struct.pack('B', operation_code) + data
        checksum = struct.pack('B', self.checksum(command))
        full_command = command + checksum
        
        # Send the command
        try:
            self.serial_connection.write(full_command)
        except Exception as e:
            print(f"Failed to send command: {e}")

    def readResponse(self, num_bytes=8):
        """Read the response from the device."""
        try:
            response = self.serial_connection.read(num_bytes)  # Adjust the number of bytes based on expected response size
            if response:
                return int.from_bytes(response[3:7],byteorder="little")
        except Exception as e:
            print(f"Failed to read response: {e}")
        return None
    
    def readOutputStatus(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["output_status"],data=data)
        return self.readResponse()
    
    def writeOutputStatus(self,output_status):
        data = struct.pack("<I",int(output_status))
        self.sendCommand(command_code=0x57,operation_code=self.instructions["output_status"],data=data)
        return self.readResponse()
    
    def readTargetFrequency(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["target_frequency"],data=data)
        return self.readResponse()/10
    
    def writeTargetFrequency(self,value_to_write):
        data = struct.pack("<I",int(10*value_to_write))
        self.sendCommand(command_code=0x57,operation_code=self.instructions["target_frequency"],data=data)
        return self.readResponse()/10
    
    def readHighEndTargetVoltage(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["he_target_voltage"],data=data)
        return self.readResponse()/10
    
    def writeHighEndTargetVoltage(self,value_to_write):
        data = struct.pack("<I",int(10*value_to_write))
        self.sendCommand(command_code=0x57,operation_code=self.instructions["he_target_voltage"],data=data)
        return self.readResponse()/10
    
    def readAutoTargetVoltage(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["auto_target_voltage"],data=data)
        return self.readResponse()/10
    
    def writeAutoTargetVoltage(self,value_to_write):
        data = struct.pack("<I",int(10*value_to_write))
        self.sendCommand(command_code=0x57,operation_code=self.instructions["auto_target_voltage"],data=data)
        return self.readResponse()/10
    
    def readMaxOutCurrent(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["max_out_current"],data=data)
        return self.readResponse()/1000
    
    def writeMaxOutCurrent(self,value_to_write):
        data = struct.pack("<I",int(1000*value_to_write))
        self.sendCommand(command_code=0x57,operation_code=self.instructions["max_out_current"],data=data)
        return self.readResponse()/1000
    
    def readControlOutput(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["control_output"],data=data)
        return self.readResponse()
    
    def writeControlOutput(self,value_to_write):
        data = struct.pack("<I",int(value_to_write))
        if value_to_write:
            self.sendCommand(command_code=0x57,operation_code=self.instructions["control_output"],data=data)
        else:
            self.sendCommand(command_code=0x57,operation_code=self.instructions["control_output_status"],data=data)
        return self.readResponse()
    
    def readSerialNumber(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["serial_no"],data=data)
        return self.readResponse()
    
    def readIRMS(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["i_rms"],data=data)
        return self.readResponse()/1000

    def readVRMS(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["v_rms"],data=data)
        return self.readResponse()/10
    
    def readIPeak(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["i_peak"],data=data)
        return self.readResponse()/1000
    
    def readVPeak(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["v_peak"],data=data)
        return self.readResponse()/10
    
    def readPVA(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["p_va"],data=data)
        return self.readResponse()/10
    
    def readPW(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["p_w"],data=data)
        return self.readResponse()/10
    
    def readPF(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["p_f"],data=data)
        return self.readResponse()/1000
    
    def readFreq(self):
        data = struct.pack("<I",0)
        self.sendCommand(command_code=0x52,operation_code=self.instructions["f_req"],data=data)
        return self.readResponse()/10
    
    def flushBuffers(self):
        """Flush the serial buffers to ensure clean communication."""
        if self.serial_connection:
            self.serial_connection.reset_input_buffer()
            self.serial_connection.reset_output_buffer()

    def close(self):
        """Close the serial connection."""
        if self.serial_connection:
            self.serial_connection.close()
            print("Serial connection closed.")