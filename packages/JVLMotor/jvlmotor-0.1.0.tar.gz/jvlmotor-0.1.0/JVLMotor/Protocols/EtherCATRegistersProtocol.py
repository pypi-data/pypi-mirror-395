from .TemplateProtocol import *
from .Communications.Drivers.CifXDriver import *

from .MacTalkProtocol import *

import socket
import struct
import time

CIFX_NUM = 0
CIFX_CH_NUM = 0

ECM_DEST = 0x20
ECM_OBJ_INDEX = 0x2012
ECM_MODUL_OBJ_INDEX = 0x2011
ECM_MODUL_CMD_INDEX = 0x2010
ECM_CMD_INDEX = 0x2010

ECM_IF_COE_TRANSPORT_COE = 0
ECM_SDO_TIMEOUT_COE = 1000

ECM_IF_CMD_COE_SDO_UPLOAD_REQ = 0x9A02
ECM_IF_CMD_COE_SDO_DOWNLOAD_REQ = 0x9A00

READ_IO_NUM = 2 
READ_ACYCLIC_NUM = 1

STATION_TIMING = 1e-3
class EtherCATRegistersProtocol(TemplateProtocol):
    def __init__(self, motor, motor_version="0",station_address = 0x100, update=False):
        super().__init__(motor)
        self.station_address = station_address
        if update:
            firmware_path = r"\JVLMotor\Protocols\Communications\Drivers\Firmwares\ECM\cifxecm.nxf" 
            current_dir = os.getcwd()
            if os.path.basename(current_dir) == "JVLMotor":
                firmware_path = firmware_path.replace(r"\JVLMotor", "")
            # Only Freerun is supported for this version
            if motor == "MIS":
                    config_path = r"JVL_MIS\config.nxd"

            if motor == "MAC":
                if int(motor_version) == 0:
                    motor_version = input("Please provide a motor version: ")

                elif int(motor_version) >= 400:
                    config_path = r"JVL_MAC_400\config.nxd"
                
                elif 50 <= int(motor_version) <= 141:
                    config_path = r"JVL_MAC_50\config.nxd"
            update_firmware_path = "./JVLMotor/Protocols/Communications/Drivers/Firmwares/ECM/updateECMFirmware.py"
            if os.path.basename(current_dir) == "JVLMotor":
                update_firmware_path = firmware_path.replace(r"/JVLMotor", "")
            subprocess.run(["python",
                            update_firmware_path,
                            "--firmware_path",firmware_path,"--config_path",config_path],
                            check=True)
            time.sleep(5)
        self.driver = CifXDriver()

        self.channel, err = self.driver.openChannel(CIFX_NUM,CIFX_CH_NUM)
        self.driver.setHostStateChannel(self.channel)
        if (err != CIFX_NO_ERROR):
            print("Open channel error: ", self.driver.getErrorDescriptionDriver(err))
       
        self.driver.onBusStateChannel(self.channel)

        if update:
            self.setupJVLProfile()

    def __del__(self):
        self.close()

    def readIO(self,reg_num,length=4):
        time.sleep(4*STATION_TIMING)
        for i in range(READ_IO_NUM):
            offset = self.motor.io_read_words.index(reg_num)*4
            value,err = self.driver.readIOChannel(self.channel,0,offset,length)
            if (err != CIFX_NO_ERROR):
                print("Error I/O reading:", self.driver.getErrorDescriptionDriver(err))
                return
        return int.from_bytes(value,byteorder='little',signed=True) 
    
    def writeIO(self,reg_num,data,length=4):
        offset = self.motor.io_write_words.index(reg_num)*4
        bytes_data = data.to_bytes(length,byteorder='little')
        err = self.driver.writeIOChannel(self.channel,0,offset,bytes_data,length)
        if (err != CIFX_NO_ERROR):
            print("Error I/O writing:", self.driver.getErrorDescriptionDriver(err))
            return
        time.sleep(4*STATION_TIMING)
        return CIFX_NO_ERROR
    
    def readSDO(self,index,subindex,size):
        packet = CIFX_PACKET()     
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 18
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = ECM_IF_CMD_COE_SDO_UPLOAD_REQ

        usStationAddress = self.station_address
        usTransportType = ECM_IF_COE_TRANSPORT_COE
        usAoEPort = 0
        usObjIndex = index
        bSubIndex = subindex
        if (bSubIndex > 0xFF):
            usObjIndex = usObjIndex + 1
            bSubIndex = bSubIndex - 0xFF
        fCompleteAccess = False
        ulTimeoutMs = ECM_SDO_TIMEOUT_COE
        ulMaxTotalBytes = size

        packet.abData[0:2] = usStationAddress.to_bytes(2,byteorder='little')
        packet.abData[2:4] = usTransportType.to_bytes(2,byteorder='little')
        packet.abData[4:6] = usAoEPort.to_bytes(2,byteorder='little')
        packet.abData[6:8] = usObjIndex.to_bytes(2,byteorder='little')
        packet.abData[8:9] = bSubIndex.to_bytes(1,byteorder='little')
        packet.abData[9:10] = fCompleteAccess.to_bytes(1,byteorder='little')
        packet.abData[10:14] = ulTimeoutMs.to_bytes(4,byteorder='little')
        packet.abData[14:18] = ulMaxTotalBytes.to_bytes(4,byteorder='little')

        
        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Read error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Read error: ", self.driver.getErrorDescriptionDriver(err))
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print("Read Status: ", hex(status))
            return

        data = rcv_packet.abData[18:18+size]
        value = int.from_bytes(data,byteorder='little',signed=True)
        return value

    def writeSDO(self,index,subindex,data,size,no_response=False):
        packet = CIFX_PACKET()     
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 18+size
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = ECM_IF_CMD_COE_SDO_DOWNLOAD_REQ

        usStationAddress = self.station_address
        usTransportType = ECM_IF_COE_TRANSPORT_COE
        usAoEPort = 0
        usObjIndex = index
        bSubIndex = subindex
        if (bSubIndex > 0xFF):
            usObjIndex = usObjIndex + 1
            bSubIndex = bSubIndex - 0xFF
        fCompleteAccess = False
        ulTimeoutMs = ECM_SDO_TIMEOUT_COE
        ulTotalBytes = size

        packet.abData[0:2] = usStationAddress.to_bytes(2,byteorder='little')
        packet.abData[2:4] = usTransportType.to_bytes(2,byteorder='little')
        packet.abData[4:6] = usAoEPort.to_bytes(2,byteorder='little')
        packet.abData[6:8] = usObjIndex.to_bytes(2,byteorder='little')
        packet.abData[8:9] = bSubIndex.to_bytes(1,byteorder='little')
        packet.abData[9:10] = fCompleteAccess.to_bytes(1,byteorder='little')
        packet.abData[10:14] = ulTotalBytes.to_bytes(4,byteorder='little')
        packet.abData[14:18] = ulTimeoutMs.to_bytes(4,byteorder='little')
        packet.abData[18:18+size] = data.to_bytes(size,byteorder='little')

        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Write error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Write error: ", self.driver.getErrorDescriptionDriver(err))
            return
        if(not no_response):
            status = rcv_packet.tHeader.ulState
            if (status != CIFX_NO_ERROR):
                print("Write Status: ", hex(status))
                return
        return CIFX_NO_ERROR

    def readProductCode(self):
        return self.readSDO(0x1018,2,4)
    
    def readMotorSDO(self,reg_num,length=4):
       return self.readSDO(ECM_OBJ_INDEX,reg_num,length)
    
    def writeMotorSDO(self,reg_num,data,length=4,no_response=False):
        return self.writeSDO(ECM_OBJ_INDEX,reg_num,data,length,no_response=no_response)

    def readModule(self,reg_num,length=4):
        return self.readSDO(ECM_MODUL_OBJ_INDEX,reg_num,length)
    
    def writeModule(self,reg_num,data,length=4,no_response=False):
        return self.writeSDO(ECM_MODUL_OBJ_INDEX,reg_num,data,length,no_response=no_response)
    
    def writeModuleCommand(self,data,length=4,no_response=False):
        return self.writeSDO(ECM_MODUL_CMD_INDEX,0,data,length,no_response=no_response)

    def read(self,reg_num,length=4):
        if reg_num in self.motor.io_read_words:
            return  self.readIO(reg_num,length)
        else:
            return self.readMotorSDO(reg_num,length)
        
    def write(self,reg_num,data,length=4,no_response=False):
        if reg_num in self.motor.io_write_words:
            return self.writeIO(reg_num,data,length)
        else:
            return self.writeMotorSDO(reg_num,data,length)
        
    def enable8IO(self):
        setup_bits = self.readModule(self.motor.module_registers["setup_bits"])
        self.writeModule(self.motor.module_registers["setup_bits"],setup_bits | (1 << self.motor.module_setup_bits["pdo_8"]))
        self.writeModuleCommand(self.motor.module_cmd_register["save2flash"])
        self.writeModuleCommand(self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def disableDSP(self):
        setup_bits = self.readModule(self.motor.module_registers["setup_bits"])
        setup_bits &= ~(1 << self.motor.module_setup_bits["enable_drive_profile"])
        self.writeModule(self.motor.module_registers["setup_bits"], setup_bits)
        self.writeModuleCommand(self.motor.module_cmd_register["save2flash"])
        self.writeModuleCommand(self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def setupJVLProfile(self):
        setup_bits = self.readModule(self.motor.module_registers["setup_bits"])
        setup_bits |= (1 << self.motor.module_setup_bits["pdo_8"])
        setup_bits &= ~(1 << self.motor.module_setup_bits["enable_drive_profile"])
        self.writeModule(self.motor.module_registers["setup_bits"],setup_bits)
        self.writeModuleCommand(self.motor.module_cmd_register["save2flash"])
        self.writeModuleCommand(self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def close(self):
        self.driver.closeChannel(self.channel)
        self.driver.closeDriver()
        
        