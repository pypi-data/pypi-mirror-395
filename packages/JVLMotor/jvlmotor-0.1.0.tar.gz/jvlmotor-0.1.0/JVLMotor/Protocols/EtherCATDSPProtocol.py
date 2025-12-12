from .TemplateProtocol import *
from .Communications.Drivers.CifXDriver import *

import socket
import struct
import time

CIFX_NUM = 0
CIFX_CH_NUM = 0

READ_IO_NUM = 25

ECM_DEST = 0x20
ECM_OBJ_INDEX = 0x2012
ECM_MODUL_OBJ_INDEX = 0x2011
ECM_MODUL_CMD_INDEX = 0x2010
ECM_CMD_INDEX = 0x2010

ECM_IF_COE_TRANSPORT_COE = 0
ECM_SDO_TIMEOUT_COE = 100

ECM_IF_CMD_COE_SDO_UPLOAD_REQ = 0x9A02
ECM_IF_CMD_COE_SDO_DOWNLOAD_REQ = 0x9A00
ECM_IF_CMD_SET_SLAVE_TARGET_STATE_REQ = 0x9E04
ECM_IF_CMD_SET_MASTER_TARGET_STATE_REQ = 0x9E00
ECM_IF_STATE_INIT = 0x01
ECM_IF_STATE_PREOP = 0x02
ECM_IF_STATE_SAFEOP = 0x04
ECM_IF_STATE_OP = 0x08
ECM_IF_CMD_GET_SLAVE_CURRENT_STATE_REQ = 0x9E06
ECM_IF_CMD_GET_MASTER_CURRENT_STATE_REQ = 0x9E02
ECM_IF_CMD_GET_CYCLIC_SLAVE_MAPPING_REQ = 0x9E26

ECM_RPDO_MAP_INDEX = 0x1600
ECM_TPDO_MAP_INDEX = 0x1A00

ECM_MODE_PASSIVE = 0
ECM_MODE_PP = 1   # Profile Position mode
ECM_MODE_VELOCITY = 2   # (Not supported)
ECM_MODE_PV = 3   # Profile Velocity mode
ECM_MODE_PT = 4   # (Not supported)
ECM_MODE_HOMING = 6   # Homing mode
ECM_MODE_IP = 7   # Interpolated Position mode (Not supported)
ECM_MODE_CSP = 8   # Cyclic Synchron Position mode
ECM_MODE_CSV = 9   # Cyclic Synchron Velocity mode
ECM_MODE_CST = 10  # Cyclic Synchron Torque mode (Not supported in MIS and miniMAC motors)

CTL_WORD_SWITCH_ON = 0
CTL_WORD_ENA_VOLT = 1
CTL_WORD_QUICK_STOP = 2
CTL_WORD_ENABLE_OPERATION = 3

CTL_WORD_OFFSET = 0
TARGET_POSITION_OFFSET = 2
TARGET_VELOCITY_OFFSET = 6
TARGET_TORQUE_OFFSET = 10

STATUS_WORD_OFFSET = 0
ACTUAL_POSITION_OFFSET = 2
ACTUAL_VELOCITY_OFFSET = 6
ACTUAL_TORQUE_OFFSET = 10

READ_IO_NUM = 2 
STATION_TIMING = 1e-3

####################### WARNING: Hilscher board doesn't support dynamic allocation  #######################
####################### of PDO, each operation mode need a configuration download   #######################
####################### only made for distributed clock configuration.              #######################
class EtherCATDSPProtocol(TemplateProtocol):
    def __init__(self, motor, motor_version="0",station_address=0x100,update=False):
        super().__init__(motor)
        self.station_address = station_address
        if update:
            firmware_path = r"\JVLMotor\Protocols\Communications\Drivers\Firmwares\ECM\cifxecm.nxf" 
            
            current_dir = os.getcwd()
            if os.path.basename(current_dir) == "JVLMotor":
                firmware_path = firmware_path.replace(r"\JVLMotor", "")
            # Only Freerun is supported for this version

            if motor == "MIS":
                    config_path = r"DSP_MIS\config.nxd"

            if motor == "MAC":
                if int(motor_version) == 0:
                    motor_version = input("Please provide a motor version: ")

                if int(motor_version) >= 400:
                    config_path = r"DSP_MAC_400\config.nxd"
                
                elif 50 <= int(motor_version) <= 141:
                    config_path = r"DSP_MAC_50\config.nxd"

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
        #if update:
        #    err = self.driver.downloadConfigurationChannel(0,configuration_file)
        #    if(err != CIFX_NO_ERROR):
        #        err = self.driver.resetChannel(self.channel,CIFX_CHANNELINIT,CIFX_TO_FIRMWARE_START)
        #    err = self.driver.resetSysDevice(CIFX_NUM)
        self.driver.onBusStateChannel(self.channel)

        if update:
            self.enableDSP()


        self.dsp_od = {
            "synchronized_output": (0x1C32, 0, 1),  # U8
            "synchronization_type": (0x1C32, 1, 2),  # U16
            "cycle_time": (0x1C32, 2, 4),  # U32
            "synchronization_types_supported": (0x1C32, 4, 2),  # U16
            "minimum_cycle_time": (0x1C32, 5, 4),  # U32
            "calc_and_copy_time": (0x1C32, 6, 4),  # U32
            "delay_time": (0x1C32, 9, 4),  # U32
            "cycle_time_too_small": (0x1C32, 12, 2),  # U16
            "sync_error": (0x1C32, 32, 1),  # Boolean (assuming 1 byte)
            "synchronized_output_2": (0x1C33, 0, 1),  # U8
            "synchronization_type_2": (0x1C33, 1, 2),  # U16
            "cycle_time_2": (0x1C33, 2, 4),  # U32
            "synchronization_types_supported_2": (0x1C33, 4, 2),  # U16
            "minimum_cycle_time_2": (0x1C33, 5, 4),  # U32
            "calc_and_copy_time_2": (0x1C33, 6, 4),  # U32
            "cycle_time_too_small_2": (0x1C33, 12, 2),  # U16
            "sync_error_2": (0x1C33, 32, 1),  # Boolean (assuming 1 byte)
            "motor_type": (0x6402, 0, 2),  # U16
            "motor_catalogue_number": (0x6403, 0, "STR"),  # STR (string, length may vary)
            "motor_manufacturer": (0x6404, 0, "STR"),  # STR (string)
            "http_motor_catalogue_address": (0x6405, 0, "STR"),  # STR (string)
            "supported_drive_modes": (0x6502, 0, 4),  # U32
            "drive_catalogue_number": (0x6503, 0, "STR"),  # STR (string)
            "drive_manufacturer": (0x6504, 0, "STR"),  # STR (string)
            "http_drive_catalogue_address": (0x6505, 0, "STR"),  # STR (string)
            "analog_input_1": (0x2101, 0, 2),  # I16
            "motor_temperature": (0x2103, 0, 1),  # I8
            "digital_inputs": (0x60FD, 0, 4),  # U32
            "digital_outputs": (0x60FE, 0, 1),  # U8
            "physical_outputs": (0x60FE, 1, 4),  # U32
            "bit_mask": (0x60FE, 2, 4),  # U32
            "diagnosis_history": (0x10F3, 0, 1),  # U8
            "maximum_messages": (0x10F3, 1, 1),  # U8
            "newest_message": (0x10F3, 2, 1),  # U8
            "newest_acknowledged_message": (0x10F3, 3, 1),  # U8
            "new_message_available": (0x10F3, 4, 1),  # U8
            "flags": (0x10F3, 5, 2),  # U16
            "diagnosis_message": (0x10F3, (6, 37), "STR"),  # STR (string)
            "error_code": (0x603F, 0, 2),  # U16
            "control_word": (0x6040, 0, 2),  # U16
            "status_word": (0x6041, 0, 2),  # U16
            "quick_stop_option_code": (0x605A, 0, 2),  # I16
            "quick_stop_deceleration": (0x6085, 0, 4),  # U32
            "modes_of_operation": (0x6060, 0, 1),  # I8
            "modes_of_operation_display": (0x6061, 0, 1),  # I8
            "max_torque": (0x6072, 0, 2),  # U16
            "polarity": (0x607E, 0, 1),  # U8
            "position_actual_value": (0x6064, 0, 4),  # I32
            "position_window": (0x6067, 0, 4),  # U32
            "position_window_time": (0x6068, 0, 2),  # U16
            "target_position": (0x607A, 0, 4),  # I32
            "software_position_limit": (0x607D, 0, 1),  # U8
            "software_position_limit_min": (0x607D, 1, 4),  # I32
            "software_position_limit_max": (0x607D, 2, 4),  # I32
            "max_motor_speed": (0x6080, 0, 4),  # U32
            "profile_velocity": (0x6081, 0, 4),  # U32
            "profile_acceleration": (0x6083, 0, 4),  # U32
            "motion_profile_type": (0x6086, 0, 2),  # I16
            "following_error_actual_value": (0x60F4, 0, 4),  # I32
            "velocity_demand_value": (0x606B, 0, 4),  # I32
            "velocity_actual_value": (0x606C, 0, 4),  # I32
            "velocity_window": (0x606D, 0, 2),  # U16
            "velocity_window_time": (0x606E, 0, 2),  # U16
            "target_velocity": (0x60FF, 0, 4),  # U32
            "target_torque": (0x6071, 0, 2),  # I16
            "torque_actual_value": (0x6077, 0, 2),  # I16
            "homing_torque": (0x2100, 0, 2),  # U16
            "home_offset": (0x607C, 0, 4),  # I32
            "homing_method": (0x6098, 0, 1),  # I8
            "homing_speeds": (0x6099, 0, 1),  # U8
            "speed_search_switch": (0x6099, 1, 4),  # U32
            "speed_search_zero": (0x6099, 2, 4),  # U32
            "homing_acceleration": (0x609A, 0, 4),  # U32
            "position_encoder_resolution": (0x608F, 0, 1),  # U8
            "encoder_increments": (0x608F, 1, 4),  # U32
            "motor_revolutions": (0x608F, 2, 4),  # U32
            "gear_ratio": (0x6091, 0, 1),  # U8
            "gear_motor_revolutions": (0x6091, 1, 4),  # U32
            "gear_shaft_revolutions": (0x6091, 2, 4),  # U32
            "feed_constant": (0x6092, 0, 1),  # U8
            "feed": (0x6092, 1, 4),  # U32
            "feed_shaft_revolutions": (0x6092, 2, 4),  # U32
            "reset_pdo": (0x0000,0,0)
        }

        # Static specific IOs
        self.io_read_words = [STATUS_WORD_OFFSET,ACTUAL_POSITION_OFFSET,
                              ACTUAL_VELOCITY_OFFSET,ACTUAL_TORQUE_OFFSET]
        self.io_write_words = [CTL_WORD_OFFSET,TARGET_POSITION_OFFSET,
                               TARGET_VELOCITY_OFFSET,TARGET_TORQUE_OFFSET]

    def __del__(self):
        self.close()

    def getSlaveState(self):
        packet = CIFX_PACKET()     
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 2
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = ECM_IF_CMD_GET_SLAVE_CURRENT_STATE_REQ

        usStationAddress = self.station_address
        packet.abData[0:2] = usStationAddress.to_bytes(2,byteorder='little')

        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Init error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Init error: ", self.driver.getErrorDescriptionDriver(err))
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print("Init Status: ", hex(status))
            return

        current_state = rcv_packet.abData[2:3]
        current_state = int.from_bytes(current_state,byteorder='little',signed=False)
        target_state = rcv_packet.abData[3:4]
        target_state = int.from_bytes(target_state,byteorder='little',signed=False)
        active_error = rcv_packet.abData[4:8]
        active_error = int.from_bytes(active_error,byteorder='little')
        return current_state,target_state, active_error
       
    def setSlaveState(self,state):
        packet = CIFX_PACKET()     
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 3
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = ECM_IF_CMD_SET_SLAVE_TARGET_STATE_REQ

        usStationAddress = self.station_address
        bTargetState = state

        packet.abData[0:2] = usStationAddress.to_bytes(2,byteorder='little')
        packet.abData[2:3] = bTargetState.to_bytes(1,byteorder='little')

        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("State error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("State error: ", self.driver.getErrorDescriptionDriver(err))
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print("State Status: ", hex(status))
            return

    def getMasterState(self):
        packet = CIFX_PACKET()     
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 0
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = ECM_IF_CMD_GET_MASTER_CURRENT_STATE_REQ

        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Init error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Init error: ", self.driver.getErrorDescriptionDriver(err))
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print("Init Status: ", hex(status))
            return

        current_state = rcv_packet.abData[0:1]
        current_state = int.from_bytes(current_state,byteorder='little',signed=False)
        target_state = rcv_packet.abData[1:2]
        target_state = int.from_bytes(target_state,byteorder='little',signed=False)
        active_error = rcv_packet.abData[2:6]
        active_error = int.from_bytes(active_error,byteorder='little')
        return current_state,target_state, active_error

        
    def setMasterState(self,state):
        packet = CIFX_PACKET()     
        packet.tHeader.ulDest = 0x20
        packet.tHeader.ulLen = 1
        packet.tHeader.ulState = 0
        packet.tHeader.ulCmd = ECM_IF_CMD_SET_MASTER_TARGET_STATE_REQ

        packet.abData[0:1] = state.to_bytes(1,byteorder='little')
        err = self.driver.putPacketChannel(self.channel,packet,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("State error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("State error: ", self.driver.getErrorDescriptionDriver(err))
            return

        status = rcv_packet.tHeader.ulState
        if (status != CIFX_NO_ERROR):
            print("State Status: ", hex(status))
            return

    
    
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

        if data < 0:    
            data = (1 << (size * 8)) + data  

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
            print("Read error: ", self.driver.getErrorDescriptionDriver(err))
            return

        rcv_packet, err = self.driver.getPacketChannel(self.channel,PACKET_WAIT_TIMEOUT)
        if err != CIFX_NO_ERROR:
            print("Read error: ", self.driver.getErrorDescriptionDriver(err))
            return

        if(not no_response):
            status = rcv_packet.tHeader.ulState
            if (status != CIFX_NO_ERROR):
                print("Write Status: ", hex(status))
                return
        return CIFX_NO_ERROR

    def addRPDO(self,name,subindex):
        self.setSlaveState(ECM_IF_STATE_INIT)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_INIT:
            current_state,target_state,error = self.getSlaveState()

        self.setSlaveState(ECM_IF_STATE_PREOP)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_PREOP:
            current_state,target_state,error = self.getSlaveState()

        data = self.dsp_od[name][0] << 16 | self.dsp_od[name][1] << 8 | self.dsp_od[name][2]*8
        print(hex(data))
        self.writeSDO(ECM_RPDO_MAP_INDEX,subindex,data,4)

        self.setSlaveState(ECM_IF_STATE_SAFEOP)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_SAFEOP:
            current_state,target_state,error = self.getSlaveState()

        self.setSlaveState(ECM_IF_STATE_OP)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_OP:
            current_state,target_state,error = self.getSlaveState()
        

    def addTPDO(self,name,subindex):
        self.setSlaveState(ECM_IF_STATE_INIT)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_INIT:
            current_state,target_state,error = self.getSlaveState()

        self.setSlaveState(ECM_IF_STATE_PREOP)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_PREOP:
            current_state,target_state,error = self.getSlaveState()

        data = self.dsp_od[name][0] << 16 | self.dsp_od[name][1] << 8 | self.dsp_od[name][2]*8
        print(hex(data))
        self.writeSDO(ECM_TPDO_MAP_INDEX,subindex,data,4)

        self.setSlaveState(ECM_IF_STATE_SAFEOP)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_SAFEOP:
            current_state,target_state,error = self.getSlaveState()

        self.setSlaveState(ECM_IF_STATE_OP)
        current_state,target_state,error = self.getSlaveState()
        while current_state != ECM_IF_STATE_OP:
            current_state,target_state,error = self.getSlaveState() 

    def readDSPOD(self,name):
        return self.readSDO(self.dsp_od[name][0],
                            self.dsp_od[name][1],
                            self.dsp_od[name][2])

    def writeDSPOD(self,name,data,no_response=False):
        return self.writeSDO(self.dsp_od[name][0],
                      self.dsp_od[name][1],
                      data,
                      self.dsp_od[name][2],
                      no_response=no_response)

    def readProductCode(self):
        return self.readSDO(0x1018,2,4)
    
    def readMotorSDO(self,reg_num,length=4):
       return self.readSDO(ECM_OBJ_INDEX,reg_num,length)
    
    def writeMotorSDO(self,reg_num,data,length=4,no_response=False):
        return self.writeSDO(ECM_OBJ_INDEX,reg_num,data,length)

    def readModule(self,reg_num,length=4):
        return self.readSDO(ECM_MODUL_OBJ_INDEX,reg_num,length)
    
    def writeModule(self,reg_num,data,length=4,no_response=False):
        return self.writeSDO(ECM_MODUL_OBJ_INDEX,reg_num,data,length,no_response=no_response)
    
    def writeModuleCommand(self,data,length=4,no_response=False):
        return self.writeSDO(ECM_MODUL_CMD_INDEX,0,data,length,no_response=no_response)
    
    def readIO(self,start_byte,length=4):
        time.sleep(4*STATION_TIMING)
        for i in range(READ_IO_NUM):
            offset = start_byte
            value,err = self.driver.readIOChannel(self.channel,0,offset,length)
            if (err != CIFX_NO_ERROR):
                print("Error I/O reading:", self.driver.getErrorDescriptionDriver(err))
        return int.from_bytes(value,byteorder='little',signed=True) 
    
    def writeIO(self,start_byte,data,length=4):
        offset = start_byte
        bytes_data = data.to_bytes(length,byteorder='little')
        err = self.driver.writeIOChannel(self.channel,0,offset,bytes_data,length)
        if (err != CIFX_NO_ERROR):
            print("Error I/O writing:", self.driver.getErrorDescriptionDriver(err))
            return 
        time.sleep(4*STATION_TIMING)
        return CIFX_NO_ERROR

    def getCyclicMapping(self):
        rpdos = []
        tpdos = []
        for i in range(9):
            rpdos.append(self.readSDO(ECM_RPDO_MAP_INDEX,i,4))
            tpdos.append(self.readSDO(ECM_TPDO_MAP_INDEX,i,4))
        print([hex(j) for j in rpdos])
        print([hex(j) for j in tpdos])

    def writeOnControlWord(self,bit_number,bit_value):
        control_word = self.readDSPOD("control_word")
        if (bit_value):
            control_word = control_word | (1 << bit_number)
        else:
            control_word = control_word & ~(1 << bit_number)
        return self.writeIO(CTL_WORD_OFFSET,control_word,length=2)
        
    def writeControlWord(self,data):
        return self.writeIO(CTL_WORD_OFFSET,data,length=2)

    def readStatusWord(self):
        return self.readIO(STATUS_WORD_OFFSET,length=2)
    
    def switchOperationMode(self,mode):
        if(mode == ECM_MODE_CST and (isinstance(self.motor,MISMotor))):
            print("CST is not supported by MIS")
            return
        self.writeDSPOD("modes_of_operation",mode)
        self.writeControlWord(6)
        self.readStatusWord()
        self.writeControlWord(7)
        self.readStatusWord()
        self.writeControlWord(15)
        self.readStatusWord()
        return self.readDSPOD("modes_of_operation")
    
    
    def setTargetPosition(self,position):
        if (self.readDSPOD("modes_of_operation") == ECM_MODE_CSP 
            or self.readDSPOD("modes_of_operation") == ECM_MODE_PP):
            self.writeIO(TARGET_POSITION_OFFSET,position)
            return self.readIO(TARGET_POSITION_OFFSET)
        else:
            print("Wrong operating mode: ", self.readDSPOD("modes_of_operation"))
            return

    def setTargetVelocity(self,velocity):
        if (self.readDSPOD("modes_of_operation") == ECM_MODE_CSV
            or self.readDSPOD("modes_of_operation") == ECM_MODE_PV):
            self.writeIO(TARGET_VELOCITY_OFFSET,velocity)
            return self.readIO(TARGET_VELOCITY_OFFSET)
        else:
            print("Wrong operating mode: ", self.readDSPOD("modes_of_operation"))
            return

    def setTargetTorque(self,torque):
        if (self.readDSPOD("modes_of_operation") == ECM_MODE_CST 
            and not (isinstance(self.motor,MISMotor))):
            self.writeIO(TARGET_TORQUE_OFFSET,torque)
            return self.readIO(TARGET_TORQUE_OFFSET)
        elif isinstance(self.motor,MISMotor):
            print("CST is not supported by MIS")
            return
        else:
            print("Wrong operating mode: ", self.readDSPOD("modes_of_operation"))
            return 


    def read(self,reg_num,length=4):
        if reg_num == self.motor.registers["p_ist"][0]:
            return self.readIO(ACTUAL_POSITION_OFFSET)
        elif reg_num == self.motor.registers["v_ist"][0]:
            return self.readIO(ACTUAL_VELOCITY_OFFSET)
        elif reg_num == self.motor.registers["v_soll"][0]:
            return self.readDSPOD("max_motor_speed")
        elif isinstance(self.motor,MISMotor):
            if reg_num == self.motor.registers["actual_torque"][0]:
                return self.readIO(ACTUAL_TORQUE_OFFSET)
            else:
                return self.readMotorSDO(reg_num,length)
        elif isinstance(self.motor,MACMotor):
            if reg_num == self.motor.registers["vf_out"][0]:
                return self.readIO(ACTUAL_TORQUE_OFFSET)
            else:
                return self.readMotorSDO(reg_num,length)
        
    def write(self,reg_num,data,length=4,no_response=False):
        if reg_num == self.motor.registers["p_soll"][0]:
            return self.writeIO(TARGET_POSITION_OFFSET,data)
        elif reg_num == self.motor.registers["v_soll"][0]:
            if (self.readDSPOD("modes_of_operation") == ECM_MODE_CSV
            or self.readDSPOD("modes_of_operation") == ECM_MODE_PV):
                return self.writeIO(TARGET_VELOCITY_OFFSET,data)
            else:
                self.writeDSPOD("max_motor_speed",data)
        elif isinstance(self.motor,MACMotor):
            if reg_num == self.motor.registers["t_soll"][0]:
                return self.writeIO(TARGET_TORQUE_OFFSET,data)
            else:
                return self.writeMotorSDO(reg_num,data,length)
        else:
            return self.writeMotorSDO(reg_num,data,length,no_response=no_response)
        
    def enableDSP(self):
        setup_bits = self.readModule(self.motor.module_registers["setup_bits"])
        self.writeModule(self.motor.module_registers["setup_bits"],setup_bits | (1 << self.motor.module_setup_bits["enable_drive_profile"]))
        self.writeModuleCommand(self.motor.module_cmd_register["save2flash"])
        self.writeModuleCommand(self.motor.module_cmd_register["reset"])
        time.sleep(8)

    def close(self):
        self.driver.closeChannel(self.channel)
        self.driver.closeDriver()