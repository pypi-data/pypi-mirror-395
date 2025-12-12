from .TemplateProtocol import *
from .Communications.Drivers.CifXDriver import *
from .MacTalkProtocol import *
from .ModBusProtocol import *

import socket
import struct
import time

EIP_APS_SET_CONFIGURATION_PARAMETERS_REQ = 0x00003612
EIP_APS_SET_PARAMETER_REQ = 0x0000360A
EIP_APS_CONFIG_DONE_REQ = 0x00003614
EIP_OBJECT_MR_REGISTER_REQ = 0x00001A02
EIP_OBJECT_AS_REGISTER_REQ = 0x00001A0C
EIP_OBJECT_REGISTER_SERVICE_REQ = 0x00001A44
EIP_OBJECT_SET_PARAMETER_REQ = 0x00001AF2
EIP_OBJECT_CIP_SERVICE_REQ = 0x00001AF8
HIL_SET_WATCHDOG_TIME_REQ = 0x00002F04
HIL_REGISTER_APP_REQ = 0x00002F10
HIL_START_STOP_COMM_REQ = 0x00002F30
HIL_CHANNEL_INIT_REQ = 0x00002F80
EIP_OBJECT_UNCONNECT_MESSAGE_REQ = 0x00001A36
EIP_OBJECT_OPEN_CL3_REQ = 0x00001A38
EIP_OBJECT_CONNECT_MESSAGE_REQ = 0x00001A3A
EIP_OBJECT_CLOSE_CL3_REQ = 0x00001A3C
EIP_OBJECT_CC_SLAVE_ACTIVATE_REQ = 0x00001A48
EIP_ENCAP_LISTIDENTITY_REQ = 0x00001810
EIP_ENCAP_LISTSERVICES_REQ = 0x00001814
EIP_ENCAP_LISTINTERFACES_REQ = 0x00001818
HIL_GET_SLAVE_HANDLE_REQ = 0x00002F08
HIL_GET_SLAVE_CONN_INFO_REQ = 0x00002F0A
HIL_BUSSCAN_REQ = 0x00002F22
HIL_GET_DEVICE_INFO_REQ = 0x00002F24
EIP_OBJECT_CREATE_CC_INSTANCE_REQ = 0x00001A50

SERVICE_GET_ATTRIBUTE_SINGLE = 0x0E
SERVICE_SET_ATTRIBUTE_SINGLE = 0x10


CIFX_NUM = 0
CIFX_CH_NUM = 0
READ_IO_NUM = 25
READ_ACYCLIC_NUM = 10

EIP_MODULE_COMMAND_REGISTER = 15

RPI = 1/1e3

class EthernetIPProtocol(TemplateProtocol):
    def __init__(self,motor,port="XXX",product="", update=False):
        super().__init__(motor=motor,product=product)
        if update: 
            firmware_path = r"\JVLMotor\Protocols\Communications\Drivers\Firmwares\EIM"
            current_dir = os.getcwd()
            if os.path.basename(current_dir) == "JVLMotor":
                firmware_path = firmware_path.replace(r"\JVLMotor", "")
                
            if motor == "MAC":
                firmware_path += r"\MAC\cifxeim.nxf"
                self.ip = "192.168.0.49"
            elif motor == "MIS":
                firmware_path += r"\MIS\cifxeim.nxf"
                self.ip = "192.168.0.50"
            update_firmware_path = "./JVLMotor/Protocols/Communications/Drivers/Firmwares/EIM/updateEIMFirmware.py"
            if os.path.basename(current_dir) == "JVLMotor":
                update_firmware_path = firmware_path.replace(r"/JVLMotor", "")
            subprocess.run(["python",
                            update_firmware_path,
                            "--firmware_path",firmware_path],
                            check=True)
            time.sleep(8)
            self.port = port
            self.setup()

        self.driver = CifXDriver()

        self.channel, err = self.driver.openChannel(CIFX_NUM,CIFX_CH_NUM)
        self.driver.setHostStateChannel(self.channel)
        if (err != CIFX_NO_ERROR):
            print(f"Open channel error: {self.driver.getErrorDescriptionDriver(err)}")
        
        self.driver.onBusStateChannel(self.channel)
        self.openClass3Connection()
    
    def __del__(self):
        self.close()
        
    def ipTouint32(self):
        packed_ip = socket.inet_aton(self.ip)
        return struct.unpack("!I", packed_ip)[0]

    def openClass3Connection(self,max_retries=5):
        for attempt in range(1, max_retries+1):
            packet = CIFX_PACKET()
            packet.tHeader.ulDest = 0x20
            packet.tHeader.ulLen = 3*4
            packet.tHeader.ulState = 0
            packet.tHeader.ulCmd = EIP_OBJECT_OPEN_CL3_REQ

            ulIPAddr = self.ipTouint32()
            ulRpi = 1000000
            ulTimeoutMult = 2
            packet.abData[0:4] = ulIPAddr.to_bytes(4,byteorder='little')
            packet.abData[4:8] = ulRpi.to_bytes(4,byteorder='little')
            packet.abData[8:12] = ulTimeoutMult.to_bytes(4,byteorder='little')
            self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
            rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
            if err != CIFX_NO_ERROR:
                print(f"Open class 3 connection error: {err} - {self.driver.getErrorDescriptionDriver(err)}")
                continue

            status = rcv_packet.tHeader.ulState
            if (status != CIFX_NO_ERROR):
                print(f"Failed Attempt {attempt}: Open Status - {hex(status)}")
                time.sleep(1)

            if status == CIFX_NO_ERROR:
                self.connection_cl3 = int.from_bytes(rcv_packet.abData[0:4], byteorder='little')
                return  CIFX_NO_ERROR # Successfully connected
            #self.connection_cl3 = int.from_bytes(rcv_packet.abData[0:4],byteorder='little')

    def readModule(self,reg_num,length=4):
        packet = CIFX_PACKET()
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 12
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = EIP_OBJECT_CONNECT_MESSAGE_REQ

        ulConnection = self.connection_cl3
        bService = SERVICE_GET_ATTRIBUTE_SINGLE
        ulClass = 0x65
        ulInstance = reg_num
        ulAttribute = 0x1

        packet.abData[0:4] = ulConnection.to_bytes(4,byteorder='little')
        packet.abData[4] = bService
        packet.abData[6:8] = ulClass.to_bytes(2,byteorder='little')
        packet.abData[8:10] = ulInstance.to_bytes(2,byteorder='little') #OK
        packet.abData[10:12] = ulAttribute.to_bytes(2,byteorder='little')

        for i in range(1):
            err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
            if err != CIFX_NO_ERROR:
                print(f"Read module error: {self.driver.getErrorDescriptionDriver(err)}")
                return

            rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
            if err != CIFX_NO_ERROR:
                print(f"Read module error: {self.driver.getErrorDescriptionDriver(err)}")
                return

            status = rcv_packet.tHeader.ulState
            if (status != CIFX_NO_ERROR):
                print(f"Read Status: {hex(status)}")
                assert False, f"readModule failed with status: {hex(status)}"
                return

        data = rcv_packet.abData[12:12+length]
        value = int.from_bytes(data,byteorder='little',signed=True)
        return value
    
    def writeModule(self,reg_num,data,length=4,no_response=True):
        packet = CIFX_PACKET()
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 12 + length
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = EIP_OBJECT_CONNECT_MESSAGE_REQ

        ulConnection = self.connection_cl3
        bService = SERVICE_SET_ATTRIBUTE_SINGLE
        ulClass = 0x65
        ulInstance = reg_num
        ulAttribute = 0x1

        packet.abData[0:4] = ulConnection.to_bytes(4,byteorder='little')
        packet.abData[4] = bService
        packet.abData[6:8] = ulClass.to_bytes(2,byteorder='little')
        packet.abData[8:10] = ulInstance.to_bytes(2,byteorder='little')
        packet.abData[10:12] = ulAttribute.to_bytes(2,byteorder='little')
        packet.abData[12:12+length] = data.to_bytes(length,byteorder='little')


        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print(f"Write module error: {self.driver.getErrorDescriptionDriver(err)}")
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print(f"Write module error: {self.driver.getErrorDescriptionDriver(err)}")
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print(f"Write Module Status {reg_num} for {data}: {hex(status)}")
            return

        return CIFX_NO_ERROR
    
    def writeModuleCommand(self,data,length=4,no_response=False):
        return self.writeModule(EIP_MODULE_COMMAND_REGISTER,data,length=length,no_response=no_response)
    
    def readClass3(self, reg_num, length=4):
        packet = CIFX_PACKET()
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 12
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = EIP_OBJECT_CONNECT_MESSAGE_REQ

        ulConnection = self.connection_cl3
        bService = SERVICE_GET_ATTRIBUTE_SINGLE
        ulClass = 0x64
        ulInstance = reg_num
        ulAttribute = 0x1

        packet.abData[0:4] = ulConnection.to_bytes(4,byteorder='little')
        packet.abData[4] = bService
        packet.abData[6:8] = ulClass.to_bytes(2,byteorder='little')
        packet.abData[8:10] = ulInstance.to_bytes(2,byteorder='little') #OK
        packet.abData[10:12] = ulAttribute.to_bytes(2,byteorder='little')

        for i in range(READ_ACYCLIC_NUM):
            err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
            if err != CIFX_NO_ERROR:
                print(f"Read error: {self.driver.getErrorDescriptionDriver(err)}")
                return

            rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
            if err != CIFX_NO_ERROR:
                print(f"Read error: {self.driver.getErrorDescriptionDriver(err)}")
                return

            status = rcv_packet.tHeader.ulState
            if (status != CIFX_NO_ERROR):
                print(f"Read Status: {hex(status)}")
                if (status == 0xc01e001e):
                    print("Communication issue probably due to timeout - Reopening Class3")
                    self.openClass3Connection()
                    time.sleep(0.1)
                return

        data = rcv_packet.abData[12:12+length]
        value = int.from_bytes(data,byteorder='little',signed=True)
        return value
    
    def writeClass3(self,reg_num,data,length=4,no_response = False):
        packet = CIFX_PACKET()
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 12 + length
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = EIP_OBJECT_CONNECT_MESSAGE_REQ

        ulConnection = self.connection_cl3
        bService = SERVICE_SET_ATTRIBUTE_SINGLE
        ulClass = 0x64
        ulInstance = reg_num
        ulAttribute = 0x1

        packet.abData[0:4] = ulConnection.to_bytes(4,byteorder='little')
        packet.abData[4] = bService
        packet.abData[6:8] = ulClass.to_bytes(2,byteorder='little')
        packet.abData[8:10] = ulInstance.to_bytes(2,byteorder='little')
        packet.abData[10:12] = ulAttribute.to_bytes(2,byteorder='little')
        packet.abData[12:12+length] = data.to_bytes(length,byteorder='little')


        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print(f"Read error: {self.driver.getErrorDescriptionDriver(err)}")
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print(f"Read error: {self.driver.getErrorDescriptionDriver(err)}")
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print(f"Write Status: {hex(status)}")
            if (status == 0xc01e001e):
                print("Communication issue probably due to timeout - Reopening Class3")
                self.openClass3Connection()
                time.sleep(0.1)
            return

        return CIFX_NO_ERROR

    def readClass1(self,reg_num,length=4):
        #Ensuring a complete IO run
        # time.sleep(1)
        time.sleep(4*RPI)
        for i in range(2):
            offset = self.motor.io_read_words.index(reg_num)*4
            value,err = self.driver.readIOChannel(self.channel,0,offset,length)
            if (err != CIFX_NO_ERROR):
                print(f"Error I/O reading: {self.driver.getErrorDescriptionDriver(err)}")
                return
        return int.from_bytes(value,byteorder='little',signed=True)
    
    def writeClass1(self,reg_num,data,length=4):
        offset = self.motor.io_write_words.index(reg_num)*4
        bytes_data = data.to_bytes(length,byteorder='little')
        err = self.driver.writeIOChannel(self.channel,0,offset,bytes_data,length)
        if (err != CIFX_NO_ERROR):
            print(f"Error I/O writing: {self.driver.getErrorDescriptionDriver(err)}")
            return
        time.sleep(4*RPI)
        return CIFX_NO_ERROR
        
    def read(self,reg_num,length=4):
        if reg_num in self.motor.io_read_words:
            return  self.readClass1(reg_num,length)
        else:
            return self.readClass3(reg_num,length)
        
    def write(self,reg_num,data,length=4,no_response=False):
        if reg_num in self.motor.io_write_words:
            return self.writeClass1(reg_num,data,length)
        else:
            return self.writeClass3(reg_num,data,length)
        
    def enable8IO(self):
        setup_bits = self.readModule(self.motor.module_registers["setup_bits"])
        self.writeModule(self.motor.module_registers["setup_bits"],setup_bits | (1 << self.motor.module_setup_bits["pdo_8"]))
        self.writeModule(self.motor.module_registers["command"],self.motor.module_cmd_register["save2flash"])
        self.writeModule(self.motor.module_registers["command"],self.motor.module_cmd_register["reset"])
        time.sleep(8)
        
    def setIP(self,motor):
        mt = MacTalkProtocol(port=self.port, motor=motor)
        mt.writeModule(self.motor.module_registers["ip"],self.ipTouint32())
        mt.writeModule(self.motor.module_registers["command"],
                       self.motor.module_cmd_register["save2flash"])
        mt.writeModule(self.motor.module_registers["command"],
                       self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def setup(self):
        if self.product == "404" or self.product == "1004":
            mt = ModBusProtocol(port=self.port)
        else:
            mt = MacTalkProtocol(port=self.port)
        mt.writeModule(self.motor.module_registers["ip"],self.ipTouint32())
        setup_bits = mt.readModule(self.motor.module_registers["setup_bits"])
        mt.writeModule(self.motor.module_registers["setup_bits"],setup_bits | (1 << self.motor.module_setup_bits["pdo_8"]))
        mt.writeModule(self.motor.module_registers["command"],
                       self.motor.module_cmd_register["save2flash"])
        mt.writeModule(self.motor.module_registers["command"],
                       self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def close(self):
        self.driver.closeChannel(self.channel)
        self.driver.closeDriver()








        

        