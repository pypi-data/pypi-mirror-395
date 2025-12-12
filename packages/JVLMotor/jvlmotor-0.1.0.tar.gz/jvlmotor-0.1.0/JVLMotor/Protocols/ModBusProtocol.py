from .Communications.SerialCommunication import *
from .TemplateProtocol import *
from .MacTalkProtocol import *

from pymodbus.client import ModbusSerialClient
from pymodbus.client import ModbusUdpClient
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
from pymodbus.exceptions import ModbusIOException
from pymodbus.transaction import ModbusSocketFramer
from pymodbus.pdu import ModbusRequest

import libscrc
import math
import socket
import struct

import logging
import os

INITIATE_FILE_TRANSFER_REQUEST = 0x64
INITIATE_FILE_TRANSFER_RESPONSE = 0x65
TRANSFER_DATA_BLOCK_REQUEST = 0x66
TRANSFER_DATA_BLOCK_RESPONSE = 0x67
GET_FILE_STATUS_REQUEST = 0x68
GET_FILE_STATUS_RESPONSE = 0x69
START_FLASHING_REQUEST = 0x6A
START_FLASHING_RESPONSE = 0x6B

FIRMWARE_TRANSFER_UNLOCK = 995
FIRMWARE_TRANSFER_LOCK = 996
FILE_TRANSFER_UNLOCK = 997
FILE_TRANSFER_LOCK = 998

MODULE_REGISTER_ADDRESS = 0x8000

class ModBusProtocol(TemplateProtocol):
    # TODO: Parity
    def __init__(self,com_type="Serial",port=None, ip = None,
                 baudrate=115200,parity="E",motor_address = 254,motor="MAC",
                 motor_version="0",netX=50,update=False):
        super().__init__(motor=motor)
        self.motor_address = motor_address
        self.com_type = com_type
        self.netX = netX

        if com_type == "Serial":

            self.communication = ModbusSerialClient(
            port=port, 
            baudrate=baudrate, 
            timeout=0.5, 
            stopbits=1, 
            bytesize=8, 
            parity=parity)

            self.communication.connect()

        
        if com_type == "Ethernet":
            self.ip = ip
            if update:
                self.port = port
                self.setIP(motor=motor)
            self.communication = ModbusTcpClient(host=ip,
                                              port=502,
                                              auto_open=True)
            if(self.communication.connect()):
                self.communication.socket.setblocking(True)
            else:
                print("No connection")
                assert False


        #self.command_register = self.motor.registers["command"][0]

        self.file_id = {
            "mot_firmware" : [0x01,1],
            "eth_firmware" : [0x02,1],
            "enc_firmware" : [0x03,1],
            "fpga_image" : [0x10,1],
            "ePLC_program" : [0x11,2],
            "app_firmware_image" : [0x12,1],
            "com_firmware_image" : [0x13,1],
            "factory_defaults" : [0x14,2],
            "OEM_defaults" : [0x15,2],
            "scope_data" : [0x16,0],
            "CAM_table" : [0x17,2],
            "enc_calib" : [0x18,2],
            "reg_min_val" : [0x19,2],
            "reg_max_val" : [0x1A,2],
            "html_pages" : [0x1B,2],
            "app_com_firmware": [0x1C,1],
            "min_max_defaults" : [0x1D,1],
            "motor_event_log" : [0x1E,0],
            "module_event_log" : [0x1F,0],
            "units_scaling" : [0x20,2]
        }

    def __del__(self):
        self.communication.close()

    def setIP(self,motor):
        mt = MacTalkProtocol(port=self.port, motor=motor)
        if (mt.readModule(self.motor.module_registers["ip"]) & 0xFFFFFFFF) == self.ipTouint32(self.ip):
            return
        mt.writeModule(self.motor.module_registers["ip"],self.ipTouint32(self.ip))
        mt.writeModule(self.motor.module_registers["command"],
                       self.motor.module_cmd_register["save2flash"])
        mt.writeModule(self.motor.module_registers["command"],
                       self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def write(self,reg_num,data,length=4,no_response=False):
        def split_64bit_int(num):
            b3 = (num >> 48) & 0xFFFF
            b2 = (num >> 32) & 0xFFFF
            b1 = (num >> 16) & 0xFFFF
            b0 = num & 0xFFFF
            return [b0, b1, b2, b3]

        def split_32bit_int(num):
            high = (num >> 16) & 0xFFFF
            low = num & 0xFFFF
            return [low, high]

        reg = reg_num
        values16 = []

        try:
            if length>4:
                values16 += split_64bit_int(data)
                reg+= 2
            else:
                values16 += split_32bit_int(data)
                reg += 1
            self.communication.write_registers(
                address=reg_num*2, values=values16, slave=self.motor_address
                )
            
            return 0
            
        except ConnectionException as e:
            print(f"Connection error: {e}")
            return

    def read(self,reg_num,length=4):
        try:
            result =  self.communication.read_holding_registers(
                    address=reg_num * 2, count= 2*int(length/4), slave=self.motor_address
                )
            if result.isError():
                print(f"Read Error: {result}")
                return 

            received_values = result.registers 
            if isinstance(received_values,list):
                received_bytes = b''.join(value.to_bytes(2, byteorder='little') for value in received_values)
            else:
                received_bytes = received_values
            value = int.from_bytes(received_bytes,byteorder='little',signed=True)
            return value
            
        except ConnectionException as e:
            print(f"Connection error: {e}")
            return
        
    def writeModule(self,reg_num,data,length=4,no_response=False):
        def split_64bit_int(num):
            b3 = (num >> 48) & 0xFFFF
            b2 = (num >> 32) & 0xFFFF
            b1 = (num >> 16) & 0xFFFF
            b0 = num & 0xFFFF
            return [b0, b1, b2, b3]

        def split_32bit_int(num):
            high = (num >> 16) & 0xFFFF
            low = num & 0xFFFF
            return [low, high]

        reg = reg_num
        values16 = []

        try:
            if length>4:
                values16 += split_64bit_int(data)
                reg+= 2
            else:
                values16 += split_32bit_int(data)
                reg += 1
            
            self.communication.write_registers(
                address=MODULE_REGISTER_ADDRESS+reg_num*2, 
                values=values16, slave=self.motor_address
                )
            
            return 0
            
        except ConnectionException as e:
            print(f"Connection error: {e}")
            return

    def readModule(self,reg_num,length=4):
        try:
            result =  self.communication.read_holding_registers(
                    address=MODULE_REGISTER_ADDRESS+reg_num * 2, count= 2*int(length/4), slave=self.motor_address
                )
            if result.isError():
                print(f"Read Error: {result}")
                return 

            received_values = result.registers 
            if isinstance(received_values,list):
                received_bytes = b''.join(value.to_bytes(2, byteorder='little') for value in received_values)
            else:
                received_bytes = received_values
            value = int.from_bytes(received_bytes,byteorder='little',signed=True)
            return value
            
        except ConnectionException as e:
            print(f"Connection error: {e}")
            return
        
    def writeModuleCommand(self,data,length=4,no_response=False):
        return self.writeModule(self.motor.module_registers["command"],data,length=length,no_response=no_response)
            
    def readSeveralRegisters(self,register_start,count):
        try:
            if self.com_type == "Serial":
                result =  self.communication.read_holding_registers(
                    address=register_start * 2, count=count * 2, slave=self.motor_address
                )  # Read three registers (R2 R3 R4)
                if result.isError():
                    print(f"Read Error: {result}")
                    return

                received_values = result.registers 

                return received_values
            elif self.com_type == "Ethernet":
                result = self.communication.read_holding_registers(
                    reg_addr=register_start * 2, reg_nb=2*count 
                )
                return result
        except ConnectionException as e:
            print(f"Connection error: {e}")
            return
    
    def readSBUF(self):
        if self.com_type == "Serial" or self.netX != 50:
            return self.getFile(self.file_id["scope_data"][0])
        else:
            client = ModbusUdpClient(host=self.ip,port=47100)
            client.connect()
            buffer =  bytes([0x53,0x53,0x53] + [0xFF, self.computeComplement(0xFF)]+ [0xAA,0xAA])
            client.socket.sendto(buffer,(self.ip,47100))
            client.socket.setblocking(True)
            buffer = client.socket.recvfrom(1024)
            recpt_adress = buffer[1]
            buffer = buffer[0]
            length = buffer[5]
            buffer = buffer[7:2*(length)+7:2]
            return buffer

    def close(self):
        self.communication.close()

    def fileTransferUnlock(self):
        self.writeModule(self.motor.module_registers["command"],FILE_TRANSFER_UNLOCK)
        self.write(self.motor.registers["command"][0],FILE_TRANSFER_UNLOCK)


    def initFileReadRequest(self,file_id):
        message = [self.motor_address,INITIATE_FILE_TRANSFER_REQUEST,0x00,0x07,(file_id | 0x80),0x00,0x00,0x00,0x00,0x00,0x00]
        reply = self.comm(message)
        self.datalen = reply[2]*256+reply[3]
        self.response_code = reply[4]
        if self.response_code != 0:
            self.responseCode()
            return
        self.block_count = reply[5]*256+reply[6]
        self.total_length = ((reply[7]*256+reply[8])*256+reply[9])*256+reply[10]
        self.file_crc = reply[11]*256+reply[12]
        return reply
    
    def initFileWriteRequest(self,file_id,file_size):
        block_count = self.to_2x8bit(math.ceil(file_size/1024))
        file_size = self.to_4x8bit(file_size)
        message = [self.motor_address,INITIATE_FILE_TRANSFER_REQUEST,0x00,0x07,file_id] + block_count + file_size
        reply = self.comm(message)
        self.datalen = reply[2]*256+reply[3]
        self.response_code = reply[4]
        self.block_count = reply[5]*256+reply[6]
        self.total_length = ((reply[7]*256+reply[8])*256+reply[9])*256+reply[10]
        self.file_crc = reply[11]*256+reply[12]
        return reply
    
    def requestBlock(self,block_number):
        block_n = self.to_2x8bit(block_number)
        req_read_block = [self.motor_address, TRANSFER_DATA_BLOCK_REQUEST, 0x00, 0x02]
        req_read_block += block_n
        reply = self.comm(req_read_block)
        self.response_code = reply[4]
        self.block_number = reply[5]*256+reply[6]
        self.block_data = reply[7:-2]
        crc = reply[-2:]
        return reply
    
    def setBlock(self,block_number,data):
        block_n = self.to_2x8bit(block_number)
        req_write_block = [self.motor_address, TRANSFER_DATA_BLOCK_REQUEST]
        data_len = len(data) + 2
        data_len = self.to_2x8bit(data_len)
        req_write_block += data_len + block_n + data
        self.comm(req_write_block)

    def startFlashingRequest(self,transmitted_file,file_size):
        crc = libscrc.modbus(bytes(transmitted_file))
        file_crc = [(crc >> 8) & 0xFF,crc & 0xFF]
        file_size = self.to_4x8bit(file_size)
        transfer_date = [0x00,0x00,0x00,0x00]
        transfer_time = [0x00,0x00]
        req_flashing = [self.motor_address,START_FLASHING_REQUEST,0x00,0x1D] + file_size + [0x00,0x00,
                        0x00,0x00] + [0x00,0x00,0x00,0x00] + transfer_date + transfer_time + [0x00,0x00,
                        0x00,0x00] + [0x00,0x00] + [0x00] + file_crc + [0x00] + [0x00]
        reply = self.comm(req_flashing)
        self.response_code = reply[4]
        

    def getFileStatusRequest(self):
        req = [self.motor_address, GET_FILE_STATUS_REQUEST, 0x00, 0x00] 
        return self.comm(req)
        
    def getFile(self,file_id):
        self.fileTransferUnlock()
        time.sleep(0.2)
        self.initFileReadRequest(file_id)
        if (self.response_code != 0):
            self.responseCode()
        self.file = bytearray()
        for i in range(self.block_count):
            self.requestBlock(i)
            if(self.response_code != 0):
                self.responseCode()
            if self.block_number != i:
                print("Bad block number")
                return -1
            self.file += self.block_data
        return self.file
    
    def setFile(self,file_id,file_path=None,file=None):
        self.fileTransferUnlock()
        time.sleep(0.2)
        if file is None:
            file = []
        if file_path:
            file = self.binaryToHexList(file_path=file_path)
        self.initFileWriteRequest(file_id=file_id,file_size=len(file))
        if (self.response_code != 0):
            self.responseCode()
            return
        for i in range(self.block_count+1):
            data = file[i*1024:(i+1)*1024]
            self.setBlock(i,data)
        self.getFileStatusRequest()
        self.startFlashingRequest(file,len(file))
        if (self.response_code != 0):
            return self.responseCode()
        else:
            return 0


    def comm(self,data):
        crc = libscrc.modbus(bytes(data))
        crc_lsb = crc & 0xFF
        crc_msb = (crc >> 8) & 0xFF
        data.append(crc_lsb)
        data.append(crc_msb)
        reply_data = bytearray()
        if self.com_type == "Serial":
            hex_list = [f"{byte:02X}" for byte in data]
            self.communication.socket.write(data)
            #time.sleep(0.2)
            while True:
                chunk = self.communication.socket.read()
                if not chunk:
                    break
                reply_data += chunk
            hex_list = [f"{byte:02X}" for byte in reply_data]
            return reply_data
        elif self.com_type == "Ethernet":
            if self.communication.socket:  
                self.communication.socket.setblocking(True)
                self.communication.socket.sendall(bytes(data))  
                chunk = self.communication.socket.recv(1024)
                reply_data += chunk
                return reply_data
            else:
                print("Socket is not open.")
                return None

    def responseCode(self):
        if (self.response_code == 0x01):
            print("Not enough free heap memory.")
        elif (self.response_code == 0x02):
            print("Unknown file.")
        elif (self.response_code == 0x03):
            print("Attempt to read WO file or write RO file.")
        elif (self.response_code == 0x04):
            print("Attempt to access a password protected file.")
        elif (self.response_code == 0x05):
            print("File are empty(read only).")
        elif (self.response_code == 0x10):
            print("File codes is locked. Unlock first.")
        return self.response_code
    
	    
    def to_2x8bit(self,a):
        lsb = a & 0xFF
        msb = (a >> 8) & 0xFF
        return [msb, lsb]

    def to_4x8bit(self,a):
        b1 = a & 0xFF
        b2 = (a >> 8) & 0xFF
        b3 = (a >> 16) & 0xFF
        b4 = (a >> 24) & 0xFF
        return [b4, b3, b2, b1]

    def binaryToHexList(self,file_path):
        try:
            with open(file_path, 'rb') as file:  
                binary_data = file.read()       
            hex_list = [f"{byte:02x}" for byte in binary_data]
            return hex_list
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        
    def ipTouint32(self,ip):
        packed_ip = socket.inet_aton(ip)
        return struct.unpack("!I", packed_ip)[0]