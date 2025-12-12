from .Communications.SerialCommunication import *
from .TemplateProtocol import *
from pymodbus.client import ModbusUdpClient

import socket
import struct
import logging
import os

PING_MODULE = [0x80,0x80,0x80]
WRITE = [0x52,0x52,0x52]
WRITE_MODULE = [0x83,0x83,0x83]
READ = [0x50,0x50,0x50]
READ_MODULE = [0x84,0x84,0x84]
READ_BUF = [0x53,0x53,0x53]
END = [0xAA,0xAA]
ACCEPTED = [0x11,0x11,0x11]

WRITE_LEN = 3
READ_LEN = 3
END_LEN = 2
ACCEPTED_LEN = 3
ADDRESS_LEN = 2
REG_LEN = 2
LEN_LEN = 2

#TODO: Try catch for error handling 

class MacTalkProtocol(TemplateProtocol):
    def __init__(self,com_type="Serial",port=None,ip=None,baudrate=19200,
                 motor_address=254,motor="MAC"):
        super().__init__(motor=motor)
        self.motor_address = motor_address
        self.com_type = com_type

        if com_type == "Serial":
            self.communication = SerialCommunication(port,baudrate,timeout=10)
            self.communication.open()

        if com_type == "Ethernet":
            self.ip = ip
            self.port = int(port)
            self.setIP(motor=motor)
            client = ModbusUdpClient(host=self.ip,port=self.port)
            client.connect()
            client.socket.connect((self.ip,self.port))
            self.communication = client.socket

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
        reg_len = (reg_num.bit_length() + 7) // 8
        data_bytes = data.to_bytes(length, byteorder='little')
        reg_bytes = reg_num.to_bytes(reg_len, byteorder='little')
         
        data_buffer = []
        for byte in data_bytes:
            data_buffer.append(byte)
            data_buffer.append(self.computeComplement(byte))

        reg_buffer = []
        for byte in reg_bytes:
            reg_buffer.append(byte)
            reg_buffer.append(self.computeComplement(byte))

        if (reg_len > 1):
            reg_buffer = [0xff,self.computeComplement(0xff),
                    reg_buffer[0]+reg_buffer[2],
                    self.computeComplement(reg_buffer[0]+reg_buffer[2])]
        if length > 4:
            reg_next = reg_num+1
            reg_next_len = (reg_next.bit_length() + 7) // 8
            reg_next_bytes = reg_next.to_bytes(reg_next_len, byteorder='little')

            reg_next_buffer = []
            for byte in reg_next_bytes:
                reg_next_buffer.append(byte)
                reg_next_buffer.append(self.computeComplement(byte))

            buffer_1 = bytes(WRITE + [self.motor_address, self.computeComplement(self.motor_address)] + 
                            reg_buffer + [4, self.computeComplement(4)]
                            + data_buffer[0:length] + END)
            buffer_2 = bytes(WRITE + [self.motor_address, self.computeComplement(self.motor_address)] + 
                            reg_next_buffer + [4, self.computeComplement(4)]
                            + data_buffer[length:2*length] + END)
            if self.com_type == "Serial":          
                self.communication.send(buffer_1)
                if not no_response:
                    accepted_1 = self.communication.receive(ACCEPTED_LEN)
                self.communication.send(buffer_2)
                if not no_response:
                    accepted_2 = self.communication.receive(ACCEPTED_LEN)
                if not no_response:
                    if accepted_1 == None or accepted_2 == None:
                        return 
                    else:
                        accepted_1 =  int.from_bytes(accepted_1,byteorder="little")
                        accepted_2 =  int.from_bytes(accepted_2,byteorder="little")
                    if accepted_1 != int.from_bytes(bytes(ACCEPTED),byteorder="little") or accepted_2 != int.from_bytes(bytes(ACCEPTED),byteorder="little"):
                        return 
                    else:
                        return 0
                else:
                    return 0
            elif self.com_type == "Ethernet":
                self.communication.send(buffer_1)
                if not no_response:
                    self.communication.setblocking(True)
                    accepted_1 = self.communication.recv(1024)
                self.communication.send(buffer_2)
                if not no_response:
                    self.communication.setblocking(True)
                    accepted_2 = self.communication.recv(1024)
                if not no_response:
                    if accepted_1 == None or accepted_2 == None:
                        return 
                    else:
                        accepted_1 =  int.from_bytes(accepted_1,byteorder="little")
                        accepted_2 =  int.from_bytes(accepted_2,byteorder="little")
                    if accepted_1 != int.from_bytes(bytes(ACCEPTED),byteorder="little") or accepted_2 != int.from_bytes(bytes(ACCEPTED),byteorder="little"):
                        return 
                    else:
                        return 0
                else:
                    return 0
        else:
            buffer = bytes(WRITE + [self.motor_address, self.computeComplement(self.motor_address)] + 
                            reg_buffer + [length, self.computeComplement(length)]
                            + data_buffer + END)
            if self.com_type == "Serial":
                self.communication.send(buffer)
                if not no_response:
                    accepted = self.communication.receive(ACCEPTED_LEN)
                    if accepted == None:
                        return 
                    else:
                        accepted =  int.from_bytes(accepted,byteorder="little")
                    if accepted != int.from_bytes(bytes(ACCEPTED),byteorder="little"):
                        return 
                    else:
                        return 0
                else:
                    return 0
            elif self.com_type == "Ethernet":
                self.communication.send(buffer)
                if not no_response:
                    accepted = self.communication.recv(ACCEPTED_LEN)
                    if accepted == None:
                        return -1
                    else:
                        accepted =  int.from_bytes(accepted,byteorder="little")
                    if accepted != int.from_bytes(bytes(ACCEPTED),byteorder="little"):
                        return -1
                    else:
                        return 0
                else:
                    return 0

    def read(self,reg_num,length=4): 
        reg_len = (reg_num.bit_length() + 7) // 8
        reg_bytes = reg_num.to_bytes(reg_len,byteorder='little')
        reg_buffer = []
        for byte in reg_bytes:
            reg_buffer.append(byte)
            reg_buffer.append(self.computeComplement(byte))
        
        if (reg_len > 1):
            reg_buffer = [0xff,self.computeComplement(0xff),
                    reg_buffer[0]+reg_buffer[2],
                    self.computeComplement(reg_buffer[0]+reg_buffer[2])]
        
        buffer = bytes(READ + [self.motor_address, self.computeComplement(self.motor_address)] +
                        reg_buffer + END)
        self.communication.send(buffer)
        if self.com_type == "Serial":
            try:
                buffer = self.communication.receive(WRITE_LEN+ADDRESS_LEN+len(reg_buffer)+LEN_LEN)
                data_len = buffer[WRITE_LEN+ADDRESS_LEN+len(reg_buffer)]
                buffer = self.communication.receive(2*data_len+END_LEN)
                buffer = buffer[:2*data_len:2]
            except:
                # print(f"Unknown Communication Problem on register {reg_num}")
                return
            
        elif self.com_type == "Ethernet":
            try: 
                buffer = self.communication.recv(1024)
                length = buffer[WRITE_LEN+ADDRESS_LEN+len(reg_buffer)]
                offset = WRITE_LEN+ADDRESS_LEN+len(reg_buffer)+LEN_LEN
                buffer = buffer[offset:2*length+offset:2]
            except:
                print(f"Unknown Communication Problem on register {reg_num}")
                return

        data = int.from_bytes(buffer,byteorder="little",signed=True)
        return data
    
    def pingModule(self):
        hex_buffer = PING_MODULE+ [0xFF,0x00] + END
        buffer = bytes(hex_buffer)
        self.communication.send(buffer)
        rcv_buffer = self.communication.receive(9)
        data = rcv_buffer[3:6:2]
        return int.from_bytes(data,byteorder='big')
    
    def writeModule(self,reg_num,data,length=4,no_response=False):
        reg_num = reg_num << 16
        reg_len = 4
        data_bytes = data.to_bytes(length, byteorder='big')
        reg_bytes = reg_num.to_bytes(reg_len, byteorder='big')
         
        data_buffer = []
        for byte in data_bytes:
            data_buffer.append(byte)
            data_buffer.append(self.computeComplement(byte))

        reg_buffer = []
        for byte in reg_bytes:
            reg_buffer.append(byte)
            reg_buffer.append(self.computeComplement(byte))


        hex_buffer = WRITE_MODULE + [0xFF, 
                                     self.computeComplement(0xFF)] + [2*length, 
                                    self.computeComplement(2*length)] + reg_buffer  + data_buffer + END
        buffer = bytes(hex_buffer)
        if self.com_type == "Serial":
            self.communication.send(buffer)
            if not no_response:
                accepted = self.communication.receive(ACCEPTED_LEN)
                if accepted == None:
                    return 
                else:
                    accepted =  int.from_bytes(accepted,byteorder="little")
                if accepted != int.from_bytes(bytes(ACCEPTED),byteorder="little"):
                    return 
                else:
                    return 0
            else:
                return 0
        elif self.com_type == "Ethernet":
            self.communication.send(buffer)
            if not no_response:
                accepted = self.communication.recv(ACCEPTED_LEN)
                if accepted == None:
                    return 
                else:
                    accepted =  int.from_bytes(accepted,byteorder="little")
                if accepted != int.from_bytes(bytes(ACCEPTED),byteorder="little"):
                    return 
                else:
                    return 0
            else:
                return 0
                
    def readModule(self,reg_num,length=4):
        reg_num = reg_num << 16
        reg_len = 4
        reg_bytes = reg_num.to_bytes(reg_len,byteorder='big')
        reg_buffer = []
        for byte in reg_bytes:
            reg_buffer.append(byte)
            reg_buffer.append(self.computeComplement(byte))
        
        
        hex_buffer = READ_MODULE + [0xFF, self.computeComplement(0xFF), 
                        reg_len, self.computeComplement(reg_len)] + reg_buffer + END
        buffer = bytes(hex_buffer)

        hex_buffer = READ_MODULE + [0xff, 0x00, 0x04, 0xfb, 0x00, 0xff,
                                     0x2f, 0xd0, 0x00, 0xff, 0x00, 0xff] + END

        self.communication.send(buffer)
        if self.com_type == "Serial":
            try: 
                buffer = self.communication.receive(WRITE_LEN+ADDRESS_LEN+LEN_LEN)
                data_len = buffer[WRITE_LEN+ADDRESS_LEN]
                buffer = self.communication.receive(2*data_len+END_LEN)
                buffer = buffer[:2*data_len:2]
            except: 
                print(f"Unknown Communication Problem on register {reg_num}")
                return

        elif self.com_type == "Ethernet":
            try: 
                buffer = self.communication.recv(1024)
                length = buffer[WRITE_LEN+ADDRESS_LEN+len(reg_buffer)]
                offset = WRITE_LEN+ADDRESS_LEN+len(reg_buffer)+LEN_LEN
                buffer = buffer[offset:2*length+offset:2]
            except:
                print(f"Unknown Communication Problem on register {reg_num}")
                return
        data = int.from_bytes(buffer,byteorder="big",signed=True)
        return data
    
    def writeModuleCommand(self,data,length=4,no_response=False):
        return self.writeModule(self.motor.module_registers["command"],data,length=length,no_response=no_response)
    
    def readSBUF(self):
        buffer = bytes(READ_BUF +  [0xFF, self.computeComplement(0xFF)] + END)
        self.communication.send(buffer)

        if self.com_type == "Serial":
            buffer = self.communication.receive(WRITE_LEN+ADDRESS_LEN+LEN_LEN)
            len = buffer[WRITE_LEN+ADDRESS_LEN]
            buffer = self.communication.receive(2*len+END_LEN)
            buffer = buffer[:2*len:2]
        elif self.com_type == "Ethernet":
            buffer = self.communication.recv(1024)
            len = buffer[WRITE_LEN+ADDRESS_LEN]
            buffer = buffer[WRITE_LEN+ADDRESS_LEN+LEN_LEN:2*len+WRITE_LEN+ADDRESS_LEN+LEN_LEN:2]
        return buffer
    
    def ipTouint32(self,ip):
        packed_ip = socket.inet_aton(ip)
        return struct.unpack("!I", packed_ip)[0]