import time
import csv
import platform
from typing import Optional, Literal, Union, Any
from .Protocols.MacTalkProtocol import *
from .Protocols.ModBusProtocol import *
if platform.system() == "Windows":
    from .Protocols.EthernetIPProtocol import EthernetIPProtocol
    from .Protocols.ProfinetIOProtocol import ProfinetIOProtocol
    from .Protocols.EtherCATRegistersProtocol import EtherCATRegistersProtocol
    from .Protocols.EtherCATDSPProtocol import EtherCATDSPProtocol
else:
    # Define stubs for unsupported protocols
    class EthernetIPProtocol:
        def __init__(*args, **kwargs):
            raise NotImplementedError("EthernetIP is not supported on this platform.")

    class ProfinetIOProtocol:
        def __init__(*args, **kwargs):
            raise NotImplementedError("ProfinetIO is not supported on this platform.")

    class EtherCATRegistersProtocol:
        def __init__(*args, **kwargs):
            raise NotImplementedError("EtherCATRegisters is not supported on this platform.")

    class EtherCATDSPProtocol:
        def __init__(*args, **kwargs):
            raise NotImplementedError("EtherCATDSP is not supported on this platform.")

from .Motors.MACMotor import *
from .Motors.MISMotor import *

REG_LENGTH = 4
# Define a maximum retry for read and write - can be changed for more strict testing
MAX_RETRIES = 5
class MotorCom:
    def __init__(
        self,
        motor:str ="MAC",
        com_type: Literal["Serial","Ethernet"]="Serial",
        protocol: Literal["MacTalk","ModBus","EIP","EP","EC"]="MacTalk",
        port: Optional[str]=None,
        ip:Optional[str]=None,
        station_address:Optional[int]=0x100,
        baudrate:Optional[int]=19200,
        motor_address:int=254,
        netX:Optional[int]=50,
        io_mode:Optional[Literal["JVL","DSP"]]=None,
        motor_version:str="0",
        update:bool=False, 
        enc_type:Optional[Literal["relative","absolute"]] = None):
        
        self.port:str = port
        self.baudrate:int = baudrate
        self.motor_address:int = motor_address
        self.com_type:str
        self.motor:Union[MACMotor,MISMotor]
        self.motor_type:str = motor
        self.protocol: Union[
            MacTalkProtocol,
            ModBusProtocol,
            EthernetIPProtocol,
            ProfinetIOProtocol,
            EtherCATRegistersProtocol,
            EtherCATDSPProtocol
        ]
        self.enc_type:Literal["relative","absolute"]
        self.register_flag:bool=True
        self.real_time:bool
        

        if platform.system() == "Windows":
            self.com_type = com_type
        else:
            self.com_type = "Serial"

        self.motor_version = motor_version
        if motor == "MAC":
                self.motor = MACMotor()
        elif motor == "MIS":
                self.motor = MISMotor()

        if (enc_type == None):
            self.enc_type = "relative"
        else:
            self.enc_type = enc_type
        
        if protocol == "MacTalk":
            self.protocol = MacTalkProtocol(com_type=com_type,
                                            port=port,
                                            ip=ip,
                                            baudrate=baudrate,
                                            motor_address=motor_address,
                                            motor=motor)
            self.real_time = False
            self.disableCyclicWrite()

        elif (protocol == "ModBus" or protocol == "Modbus" 
              or protocol == "ModbusTCP" or protocol == "EM"):
            # ModBus protocol needs to know the motor type for the command register
            self.protocol = ModBusProtocol(com_type=com_type,
                                           port=port,
                                           ip = ip,
                                           baudrate=baudrate,
                                           parity="E",
                                           motor_address=motor_address,
                                           motor=motor,
                                           motor_version = motor_version,
                                           netX=netX,
                                           update=update)
            self.real_time = False
            self.disableCyclicWrite()

        elif protocol == "EIP" or protocol == "EthernetIP" or protocol == "EI":
            self.protocol = EthernetIPProtocol(motor=motor,port=port,
                                               product=motor_version,
                                               update=update)
            self.real_time = True
            self.enableCyclicWrite()

        elif protocol == "ProfinetIO" or protocol == "Profinet" or protocol == "EP":
            self.protocol = ProfinetIOProtocol(motor=motor,port=port,
                                               update=update)
            self.real_time = True
            self.enableCyclicWrite()

        elif protocol == "EtherCAT" or protocol == "Ethercat" or protocol == "EC":
            if io_mode == "Registers" or io_mode == "Reg" or io_mode == "JVL":
                self.protocol = EtherCATRegistersProtocol(motor=motor,motor_version=motor_version,
                                                          station_address=station_address,update=update)
                self.real_time = True
                self.enableCyclicWrite()

            elif io_mode == "Driver" or io_mode == "DSP" or io_mode == "CiA" or io_mode == "402":
                self.protocol = EtherCATDSPProtocol(motor=motor,motor_version=motor_version,
                                                    station_address=station_address,update=update)
                self.real_time = True
                self.register_flag = False
                self.enableCyclicWrite()
            else:
                raise NotImplementedError("Other IO modes are not implemented")
        #TODO: Other protocols

    def getProtocol(self):
        if isinstance(self.protocol,MacTalkProtocol):
            return "MacTalk"
        elif isinstance(self.protocol,ModBusProtocol):
            return "ModBus"
        elif isinstance(self.protocol,EthernetIPProtocol):
            return "EthernetIP"
        elif isinstance(self.protocol,ProfinetIOProtocol):
            return "Profinet"
        elif isinstance(self.protocol,EtherCATRegistersProtocol):
            return "EtherCAT JVL"
        elif isinstance(self.protocol,EtherCATDSPProtocol):
            return "EtherCAT DSP"

    def write(self,reg:int,data:float,scaling:float=NO_SCALING,
              length:Literal[4,8]=REG_LENGTH,no_response:bool=False,
              max_retries:int=MAX_RETRIES):
        #TODO: Handle errors
        data = data/scaling
        if data < 0:
            data = (1 << 8*length) + int(data)
        
        for attempt in range(max_retries):
            result = self.protocol.write(reg,int(data),length,no_response)
            if result is not None:
                return result
            else:
                print(f"[Write Attempt {attempt + 1}] failed for register {reg}")
                # if (isinstance(self.protocol, EthernetIPProtocol)):
                    # time.sleep(0.1)
        raise RuntimeError(f"Write failed after {max_retries} attempts for register {reg}")

    def read(self,reg:int,scaling:float=NO_SCALING,
             length:Literal[4,8]=REG_LENGTH,max_retries:int=MAX_RETRIES):
        #TODO: Handle Errors
        for attempt in range(max_retries):
            result = self.protocol.read(reg,length=length)
            if result is not None:
                return result*scaling
            else:
                print(f"[Read Attempt {attempt + 1}] failed for register {reg}")
                # if (isinstance(self.protocol, EthernetIPProtocol)):
                    # time.sleep(0.1)
        raise RuntimeError(f"Read failed after {max_retries} attempts for register {reg}")
    
    def writeModule(self,reg:int,data:float,scaling:float=NO_SCALING,
                    length:Literal[4,8]=REG_LENGTH,no_response:bool=False,
                    max_retries:int=MAX_RETRIES):
        data = data/scaling
        if data < 0:
            data = (1 << 8*length) + int(data)
        
        for attempt in range(max_retries):
            result = self.protocol.writeModule(reg,int(data),length,no_response)
            if result is not None:
                return result
            else:
                print(f"Write attempt {attempt + 1} failed for register {reg}")
        raise RuntimeError(f"Write failed after {max_retries} attempts for register {reg}")
    
    def readModule(self,reg:int,scaling:float=NO_SCALING,
                   length:Literal[4,8]=REG_LENGTH,max_retries:int=MAX_RETRIES):
        #TODO: Handle Errors
        for attempt in range(max_retries):
            result = self.protocol.readModule(reg,length=length)
            if result is not None:
                return result*scaling
            else:
                print(f"Read attempt {attempt + 1} failed for register {reg}")
        raise RuntimeError(f"Read failed after {max_retries} attempts for register {reg}")
    
    def writeBit(self,reg:Union[MACRegisterName,MISRegisterName],bit:int,data:bool,max_retries:int=MAX_RETRIES):
        addr = self.motor.registers[reg][0]
        for attempt in range(max_retries):
            value = self.protocol.read(addr)
            if value is not None:
                if data == 1:
                    value |= (1 << bit)
                else:
                    value &= ~(1 << bit)
                result = self.protocol.write(addr, value)
                if result is not None:
                    return result
            print(f"writeBit attempt {attempt + 1} failed for register {reg}")
        raise RuntimeError(f"writeBit failed after {max_retries} attempts for register {reg}")    

    def readBit(self,reg:Union[MACRegisterName,MISRegisterName],bit:int,max_retries:int=MAX_RETRIES):
        addr = self.motor.registers[reg][0]
        for attempt in range(max_retries):
            value = self.protocol.read(addr)
            if value is not None:
                return (value >> bit) & 1
            print(f"readBit attempt {attempt + 1} failed for register {reg}")
        raise RuntimeError(f"readBit failed after {max_retries} attempts for register {reg}")
    
    def writeField(self,reg:Union[MACRegisterName,MISRegisterName],data:int,start_bit:int,bit_length:int):
        if data >= (1 << bit_length):
            raise ValueError(
                f"Value {data} too large for a {bit_length}-bit field"
            )
        mask = ((1 << bit_length) - 1) << start_bit   # e.g. 0b1111 for 4 bits
        current = int(self.readRegister(reg))         # get the 32-bit register value
        new_value = (current & ~mask) | ((data << start_bit) & mask)
        self.writeRegister(reg, new_value)
        
    def readField(self,reg:Union[MACRegisterName,MISRegisterName],start_bit:int,bit_length:int):
        value = int(self.readRegister(reg))  # Read full 32-bit register
        mask = (1 << bit_length) - 1    # e.g., 0b1111 for 4 bits
        return (value >> start_bit) & mask
    
    def implicitRead(self,reg:int,scaling:float=NO_SCALING,
                     length:Literal[4,8]=REG_LENGTH):
        if (isinstance(self.protocol, EthernetIPProtocol)):
            data = self.protocol.readClass3(reg,length)
            return data*scaling
        elif (isinstance(self.protocol, ProfinetIOProtocol)):
            data = self.protocol.readAcyclic(reg,length)
            return data*scaling
        elif (isinstance(self.protocol, EtherCATRegistersProtocol) or 
              isinstance(self.protocol, EtherCATDSPProtocol)):
            data = self.protocol.readMotorSDO(reg,length)
            return data*scaling
        else:
            return self.read(reg,scaling,length)
    
    def setScopeTrigger(self, mode:str, L:int=0, R:int=0, H:int=0, condition:str="",
                         trigger_pos:int=0, trig_on_change:bool=False, divisor:int=0):       
        self.divisor = divisor
        capcom_1 = 0
        capcom_2 = L
        capcom_3 = R
        capcom_4 = H
        compare = False
        if mode == "Never":
            capcom_1 = 0
        elif mode == "Always":
            capcom_1 = 1
        elif mode == "compareValue":
            capcom_1 = 0
            compare = True
        elif mode == "compareRegister":
            capcom_1 = 1 << 7
            compare = True
        elif mode == "bitcondition":
            if "<<" == condition: 
                capcom_1 = 8
            elif "!<<" == condition: 
                capcom_1 = 9
            elif "||" == condition: 
                capcom_1 = 10
        elif mode == "withinThreshold":
            capcom_1 = 11
        elif mode == "outsideThreshold":
            capcom_1 = 12

        if compare:
            if condition == "==":
                capcom_1 |= 2
            elif condition == "!=":
                capcom_1 |= 3
            elif condition == ">":
                capcom_1 |= 4
            elif condition == ">=":
                capcom_1 |= 5
            elif condition == "<":
                capcom_1 |= 6
            elif condition == "<=":
                capcom_1 |= 7

        capcom_1 |= trigger_pos << 8
        capcom_1 |= divisor << 12
        capcom_1 |= int(trig_on_change) << 17

        self.write(self.motor.registers["capcom1"][0],capcom_1)
        self.write(self.motor.registers["capcom2"][0],capcom_2)
        self.write(self.motor.registers["capcom3"][0],capcom_3)
        self.write(self.motor.registers["capcom4"][0],capcom_4)

    def IsTriggered(self):
        ctrl_bits = self.read(self.motor.registers["cntrl_bits"][0])
        return (ctrl_bits & (1 << 15)) > 0
    
    def arm(self,registers: list[int],size:str="normal",rec_inner:bool=False):
        self.scope_registers = registers
        self.scope_size = size
        self.rec_inner = rec_inner

        if (self.scope_size == "small"):
            self.s_buf_size = 8 * 1024
            hw_setup = 0
        elif (self.scope_size == "normal"):
            self.s_buf_size = 16 * 1024
            hw_setup = (1<<23)
        elif (self.scope_size == "large"):
            self.s_buf_size = 32 * 1024
            hw_setup = (1<<23)
        elif (self.scope_size == "xlarge"):
            self.s_buf_size = 64 * 1024
            hw_setup = (1<<23)
        elif (self.scope_size == "xxlarge"):
            self.s_buf_size = 128 * 1024
            hw_setup = (1<<23)

        if len(self.scope_registers) > 4:
            hw_setup |= 1 << 28

        for channel in range(len(self.scope_registers)):
            self.write(self.motor.registers["sample1"][0]+channel,self.scope_registers[channel])

        self.write(self.motor.registers["hw_setup"][0],hw_setup)

        cntrl_bits = 0
        cntrl_bits |= (int(self.rec_inner) << 2)
        cntrl_bits |= (1 << 10) | 0x3400 
        cntrl_bits |= (1 << 13)

        self.write(self.motor.registers["cntrl_bits"][0], cntrl_bits)

    def downloadSBuf(self):
        buffer = bytearray()
        while (len(buffer) < self.s_buf_size):
            buffer += self.protocol.readSBUF()
            print(f"{len(buffer)} bytes of {self.s_buf_size} bytes total")
 
        rec_cnt = self.read(self.motor.registers["rec_cnt"][0])
        self.scope_bufffer = buffer

        print("Download complete")
        if self.scope_size == "small":
            self.n_samples = 512
        elif self.scope_size == "normal":
            self.n_samples = 1024
        elif self.scope_size == "large":
            self.n_samples = 2048
        elif self.scope_size == "xlarge":
            self.n_samples = 4096
        elif self.scope_size == "xxlarge":
            self.n_samples = 8192
        total_samples = (self.divisor+1)*self.n_samples

        if self.rec_inner:
            t_s = 100e-6
        else:
            #t_s_bit = self.readBit(self.motor.registers["setup_bits"][0],
            #                       self.motor.setup_bits["ms1_0"])
            t_s_bit = 0
            if t_s_bit == 1:
                t_s = 1e-3
            else:
                t_s = 1.3e-3
        interval = (self.divisor+1)*t_s
        # TODO: Use n_samples

        self.t = [t*interval for t in range(self.n_samples)]
        self.channels = list()
        self.channels_name = list()
        for channel in range(len(self.scope_registers)):
            self.channels_name.append(f"Reg{self.scope_registers[channel]}")
            ch = [int.from_bytes(self.scope_bufffer[i:i+4], "little", signed = "True") for i in range(channel*4, self.s_buf_size, 4*4)]
            self.channels.append(ch)

    def rescale(self,index:int,scaling:float=NO_SCALING):
        self.channels[index] = [v *scaling for v in self.channels[index]]

    def rescaleData(self,scalings:list[float]):
        for i in range(len(scalings)):
            self.rescale(i,scalings[i])
    
    def save(self,file_name:str):
        with open(file_name, 'w', newline = "") as csvfile:
            fieldnames = ['t'] + self.channels_name
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow(fieldnames)
            for s in range(self.n_samples):
                writer.writerow([self.t[s]]+ [self.channels[i][s] for i in range(len(self.scope_registers))])

    
    #HELP FUNCTIONS (to be extended according to the needs)
    # TODO: List of the helpers
    def writeRegister(self,name:Union[MACRegisterName,MISRegisterName],value:float,scaling:float=NO_SCALING,
                      length:Literal[4,8]=REG_LENGTH,no_response:bool=False):
        return self.write(self.motor.registers[name][0],value,
                   scaling=scaling,length=length,no_response=no_response)

    def readRegister(self,name:Union[MACRegisterName,MISRegisterName],scaling:float=NO_SCALING,length:Literal[4,8]=REG_LENGTH):
        return self.read(self.motor.registers[name][0],scaling=scaling,length=length)

    def writeModuleRegister(self,name:ModuleRegisterName,value:float,scaling:float=NO_SCALING,
                            length:Literal[4,8]=REG_LENGTH,no_response:bool=False):
        return self.writeModule(self.motor.module_registers[name],value,
                   scaling=scaling,length=length,no_response=no_response)

    def readModuleRegister(self,name:ModuleRegisterName,scaling:float=NO_SCALING,length:Literal[4,8]=REG_LENGTH):
        return self.readModule(self.motor.module_registers[name],scaling=scaling,length=length)

    def setControlMode(self,mode:str):
        self.writeRegister("mode_reg",self.motor.ctl_mode[mode])

    def setPosition(self,counts:int,length:Literal[4,8]=REG_LENGTH):
        self.writeRegister("p_soll",counts,length=length)

    def setVelocity(self,vel_rpm:float):
        self.writeRegister("v_soll",vel_rpm,
                scaling=self.motor.registers["v_soll"][1])
        
    def setAcceleration(self,acc_rpm_s:float):
        self.writeRegister("a_soll",acc_rpm_s,
                   scaling=self.motor.registers["a_soll"][1])
        
    def clearErrors(self):
        self.writeRegister("error_bits",0)

    def command(self,command:str,no_response:bool=False):
        self.writeRegister("command",self.motor.cmd_reg[command],
                   no_response=no_response)
        
    def writeModuleCommand(self,command:str,no_response:bool=False):
        value = self.motor.module_cmd_register[command]
        self.protocol.writeModuleCommand(value,no_response=no_response)

    def resetModule(self):
        self.writeModuleCommand("reset",no_response=True)
        self.closeCom()
        time.sleep(8)
        self.openCom()

    def closeCom(self):
        if isinstance(self.protocol, ModBusProtocol):
            if self.protocol.communication.connected:
                self.protocol.communication.close()
        if self.com_type == "Serial" and isinstance(self.protocol, MacTalkProtocol):
            if self.protocol.communication.serial_connection.is_open:
                self.protocol.communication.close()
        elif self.com_type == "Ethernet" and isinstance(self.protocol, MacTalkProtocol):
            self.protocol.communication.close()

    def openCom(self):
        # if(isinstance(self.protocol,MacTalkProtocol) or isinstance(self.protocol,ModBusProtocol)):
        #     if (self.com_type == "Serial" and isinstance(self.protocol,MacTalkProtocol)):
        #         self.protocol.communication.open()
        #     else: 
        #         self.protocol.communication.connect()

        if isinstance(self.protocol, ModBusProtocol):
            if not self.protocol.communication.connected:
                self.protocol.communication.connect()
        
        if self.com_type == "Serial" and isinstance(self.protocol, MacTalkProtocol):
            if not self.protocol.communication.serial_connection.is_open:
                self.protocol.communication.open()

        elif self.com_type == "Ethernet" and isinstance(self.protocol, MacTalkProtocol):
            if not self.protocol.communication.connected:
                self.protocol.communication.connect()

        if (isinstance(self.protocol,EthernetIPProtocol)):
            self.protocol.openClass3Connection()
            # Ensuring motor is ready
            # timeout = 30
            # start_time = time.time()
            # while self.readRegister("prog_version") == None:
            #     if time.time() - start_time >= timeout:
            #         raise TimeoutError("Class 3 did not become ready within timeout.")
            
    def resetSynchronous(self):
        self.writeModuleCommand("reset_motor_module",no_response=True)
        self.closeCom()
        time.sleep(8)
        self.openCom()

    def saveToFlashReset(self):
        time.sleep(0.2) #Ensuring last changes have been processed by the motor
        if(isinstance(self.protocol,MacTalkProtocol) or isinstance(self.protocol,ModBusProtocol)):
            self.command("save2flash_reset",no_response=True)
            self.closeCom()
            time.sleep(6)
            self.openCom()
        else:
            self.writeModuleCommand("save2flash_motor_resync",no_response=True)
            time.sleep(8)
            self.openCom()
            self.writeModuleCommand("reset_motor_module",no_response=True)
            time.sleep(8)
            self.openCom()

    def saveToFlashResetModule(self):
        if(isinstance(self.protocol,MacTalkProtocol) or isinstance(self.protocol,ModBusProtocol)):
            self.writeModuleCommand("save2flash",no_response=True)
            self.writeModuleCommand("reset",no_response=True)
            self.closeCom()
            time.sleep(6)
            self.openCom()
        else:
            self.writeModuleCommand("save2flash",no_response=True)
            self.writeModuleCommand("reset",no_response=True)
            time.sleep(8)
            self.openCom()
        
    def readVelocity(self):
        return self.readRegister("v_ist",
                  scaling=self.motor.registers["v_ist"][1])
    
    def readPosition(self,length=4):
        return self.readRegister("p_ist",length=length)
    
    def scopeVelocity(self,threshold = 10,size="small"):
        self.setScopeTrigger("compareValue",self.motor.registers["v_ist"][0],
                   threshold*(1/self.motor.registers["v_ist"][1]),condition = ">", trig_on_change=True)

        self.arm([self.motor.registers["v_soll"][0],self.motor.registers["v_ist"][0],
            self.motor.registers["p_ist"][0],self.motor.registers["a_soll"][0]],
            size=size,rec_inner=False)
    
    
    # ePLC - Only with ModBus so far
    def uploadPLC(self,file_path:str=None,file:Any=None):
        if isinstance(self.protocol,ModBusProtocol):
            return self.protocol.setFile(self.protocol.file_id["ePLC_program"][0],
                                        file_path,file)
        else:
            print("Uploading ePLC is not supported by this protocol")
            return
        
    def writePLCCommand(self,command:str):
        if isinstance(self.motor,MACMotor):
            command = command & 0xFF
            ePLC_command = self.readRegister("ePLC_command") & 0xFFFFFF00
            ePLC_command |= command
            return self.writeRegister("ePLC_command",ePLC_command)
        else:
            print("MIS Motors are not supported yet")

    def startPLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["start"])
    
    def stopPLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["stop"])
    
    def pausePLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["pause"])
    
    def stepPLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["step"])
    
    def setOutputPLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["set_output"])
    
    def setPassPLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["set_pass"])
    
    def prepareWritePLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["prepare_write"])
    
    def applyPassPLC(self):
        return self.writePLCCommand(self.motor.ePLC_cmd["apply_pass"])
    
    def isPLCRunning(self):
        ePLC_status = self.readRegister("ePLC_status_a")
        ePLC_status = (ePLC_status >> 24) & 0xFF
        return ePLC_status == self.motor.ePLC_status["running"]
    
    def isPLCPassive(self):
        ePLC_status = self.readRegister("ePLC_status_a") & 0XFF
        ePLC_status = (ePLC_status >> 24) & 0xFF
        return ePLC_status == self.motor.ePLC_status["passive"]
    
    def isPLCPaused(self):
        ePLC_status = self.readRegister("ePLC_status_a")
        ePLC_status = (ePLC_status >> 24) & 0xFF
        return ePLC_status == self.motor.ePLC_status["paused"]
    
    def isPLCStopped(self):
        ePLC_status = self.readRegister("ePLC_status_a")
        ePLC_status = (ePLC_status >> 24) & 0xFF
        return ePLC_status == self.motor.ePLC_status["stopped"]

    def isInvertDirection(self):
        if isinstance(self.motor, MACMotor):
            return self.readBit("hw_setup",self.motor.hw_setup_bits["invrotdir"])
        if isinstance(self.motor, MISMotor):
            return self.readBit("setup_bits",self.motor.setup_bits["invert_dir"])
    
    def invertDirection(self):
        #Invert direction
        self.setControlMode("passive")
        if isinstance(self.motor, MACMotor):
            self.writeBit("hw_setup",self.motor.hw_setup_bits["invrotdir"],1)
            self.saveToFlashReset()

        if isinstance(self.motor, MISMotor):
            self.writeBit("setup_bits",self.motor.setup_bits["invert_dir"],1)
            self.command("encoder_preset")
            self.saveToFlashReset()

    def normalDirection(self):
        self.setControlMode("passive")
        if isinstance(self.motor, MACMotor):
            self.writeBit("hw_setup",self.motor.hw_setup_bits["invrotdir"],0)
            self.saveToFlashReset()

        if isinstance(self.motor, MISMotor):
            self.writeBit("setup_bits",self.motor.setup_bits["invert_dir"],0)
            self.command("encoder_preset")
            self.saveToFlashReset()

    def resetPosition(self):
        if isinstance(self.motor,MACMotor):
            if(self.enc_type == "relative" or 
               (self.motor_version == "404" and self.motor_version == "1004")):
    
                self.writeRegister("p_ist",0)

            elif(self.enc_type == "absolute"):

                abs_enc_pos = self.readRegister("abs_enc_pos")
                self.writeRegister("enc_offset", -abs_enc_pos)
                self.saveToFlashReset()

            else:
                print("No encoder type provided - writing on p_ist")
                self.writeRegister("p_ist",0)

        if isinstance(self.motor, MISMotor):
            self.command("encoder_preset")
            self.command("reset_encoder")

    def setLoadFactor(self, load:int):
        if isinstance(self.motor,MACMotor):
            return self.writeRegister("kvout",load,
                                      scaling=self.motor.registers["kvout"][1])
        
    def setTorque(self,torque:float):
        if isinstance(self.motor,MACMotor):
            return self.writeRegister("t_soll",torque,
                                      scaling=self.motor.registers["t_soll"][1])
        
    def mechanicalPositionReset(self,timeout:float,counts_window:int,log:bool=False):
        if (self.enc_type == "absolute"):
            self.setControlMode("passive")
            self.resetPosition()
            if not self.isInvertDirection():
                p_soll_reset = -self.readRegister("abs_enc_pos")
            else: 
                p_soll_reset = self.readRegister("abs_enc_pos")
            self.setPosition(p_soll_reset)
            self.setControlMode("position")

            self.waitUntilInPos(p_soll=p_soll_reset,timeout=timeout,
                                counts_window=counts_window,log=log)
            
            self.setControlMode("passive")
            self.resetPosition()
            return self.readRegister("abs_enc_pos")
        
        else:
            self.resetPosition()
            return self.readPosition()
        
    def waitUntilInPos(self,p_soll:int,timeout:float,counts_window:int,log:bool=False):
        try:
            time_out = timeout + time.time()
            p_ist = self.readPosition()
            while(p_ist < p_soll - counts_window or p_ist > p_soll + counts_window):
                p_ist = self.readPosition()
                
                if time.time() > time_out:
                    raise TimeoutError
                
                if log:
                    print(f"p_ist: {p_ist}, p_soll: {p_soll}")
                    time.sleep(0.1)
                
            time.sleep(0.1)    
            return self.readPosition()
            
        except TimeoutError:
            return None
        
    def waitUntilInVelocity(self,v_soll:float,timeout:int,counts_window:int,log:bool=False):
        try:
            time_out = timeout + time.time()
            v_ist = self.readRegister("v_ist")
            while (v_ist <= v_soll - counts_window or v_ist >= v_soll + counts_window):
                if isinstance(self.motor, MISMotor):
                    v_ist = self.readRegister("v_ist")
                if isinstance(self.motor, MACMotor):
                    v_ist = self.readRegister('v_ist_16')
                
                if time.time() > time_out:
                    raise TimeoutError
                
                if log:
                    print(f"v_ist: {v_ist}, v_soll: {v_soll}")
                    time.sleep(0.1)

            time.sleep(0.1)
            return self.readRegister("v_ist")

        except TimeoutError:
            return None

    def stopMotor(self,timeout:float=10.):
        self.setVelocity(0)
        return self.waitUntilStopped(timeout=timeout)
        
    def waitUntilStopped(self,timeout:float=10.):
        try: 
            time_out = timeout + time.time()
            while self.readVelocity() != 0:
                if time.time() > time_out:
                    raise TimeoutError
            return self.readVelocity()
        
        except TimeoutError:
            return None
        
    def isInPos(self):
        if isinstance(self.motor,MACMotor):
            return self.readBit("error_bits","in_pos")
        if isinstance(self,MISMotor):
            return self.readBit("status_bit", "in_position")

    def disableCyclicWrite(self):
        self.writeModuleCommand("disable_cyclic_write")
        time.sleep(0.5)
        #self.saveToFlashReset()

    def enableCyclicWrite(self):
        self.writeModuleCommand("reenable_cyclic_write")
        time.sleep(0.5)
        #self.saveToFlashReset()

    def setReadIO(self,read_number:int,register:str):
        if not self.real_time:
            print("Setting IO for a non real-time protocol is not supported")
            return
        cyclic_register = "cyclic_read_" + str(read_number)
        self.writeModuleRegister(cyclic_register,self.motor.registers[register][0])
        self.saveToFlashResetModule()
        if read_number <= len(self.motor.io_read_words) - 1:
            self.motor.io_read_words[read_number] = self.motor.registers[register][0]
        else:
            self.motor.io_read_words.append(self.motor.registers[register][0])

    def setWriteIO(self,write_number:int,register:str):
        if not self.real_time:
            print("Setting IO for a non real-time protocol is not supported")
            return
        cyclic_register = "cyclic_write_" + str(write_number)
        self.writeModuleRegister(cyclic_register, self.motor.registers[register][0])
        self.saveToFlashResetModule()
        if write_number <= len(self.motor.io_write_words) - 1:
            self.motor.io_write_words[write_number] = self.motor.registers[register][0]
        else:
            self.motor.io_write_words.append(self.motor.registers[register][0])

    def changeBaudrate(self,baudrate:Literal[9600,19200,38400,57600,115200,230400],
                       channel:Literal["UART0","UART1"]="UART0",save_in_flash:bool=False):
        baud_rates = [9600, 19200, 38400, 57600, 115200, 230400]
        
        if isinstance(self.motor,MISMotor):
            self.writeRegister("baud_rate",baud_rates.index(baudrate),no_response=True)
            if self.com_type == "Serial":
                if isinstance(self.protocol,MacTalkProtocol):
                    self.closeCom()
                    self.protocol.communication.baudrate = baudrate
                if isinstance(self.protocol,ModBusProtocol):
                    self.protocol.communication.comm_params.baudrate = baudrate
                self.baudrate = baudrate
                time.sleep(1)
                self.openCom()  
                  
        if isinstance(self.motor,MACMotor):
            if channel == "UART0":
                uart_reg_name = "uart0_setup"
            if channel == "UART1":
                uart_reg_name = "uart1_setup"
            self.writeField(reg=uart_reg_name,data=baud_rates.index(baudrate),
                            start_bit=self.motor.uart_setup["baudrate"][0],
                            bit_length=self.motor.uart_setup["baudrate"][1])
            if save_in_flash:
                self.saveToFlashReset()
                if self.com_type == "Serial":
                    if isinstance(self.protocol,MacTalkProtocol):
                        self.closeCom()
                        self.protocol.communication.baudrate = baudrate
                    if isinstance(self.protocol,ModBusProtocol):
                        self.protocol.communication.socket.baudrate = baudrate
                    self.baudrate = baudrate
                    time.sleep(1)
                    self.openCom()    
                
    def setupModBusRTU(self,parity:Literal["N","O","E"],n_stop_bits:Literal[1,2]=1,
                       channel:Literal["UART0","UART1"]="UART0",save_in_flash:bool=False):
        if isinstance(self.motor, MISMotor):
            if not isinstance(self.protocol,ModBusProtocol):
                if parity == "N":
                    self.writeBit("modbus_setup",bit=2,data=False)
                    self.writeBit("modbus_setup",bit=3,data=False)
                if parity == "O":
                    self.writeBit("modbus_setup",bit=2,data=True)
                    self.writeBit("modbus_setup",bit=3,data=False)
                if parity == "E":
                    self.writeBit("modbus_setup",bit=2,data=False)
                    self.writeBit("modbus_setup",bit=3,data=True)
                self.writeBit("modbus_setup",bit=0,data=True)
                if n_stop_bits == 1:
                    self.writeBit("modbus_setup",bit=5,data=False)
                else:
                    self.writeBit("modbus_setup",bit=5,data=True)
            else:
                print("Unable to reconfigure ModBus using ModBus")
                
        if isinstance(self.motor,MACMotor):
            if channel == "UART0":
                uart_reg_name = "uart0_setup"
            if channel == "UART1":
                uart_reg_name = "uart1_setup"
            if not isinstance(self.protocol,ModBusProtocol):
                if parity == "N":
                    self.writeField(uart_reg_name,4,
                                    self.motor.uart_setup["parity"][0],
                                    self.motor.uart_setup["parity"][1])
                if parity == "O":
                    self.writeField(uart_reg_name,1,
                                    self.motor.uart_setup["parity"][0],
                                    self.motor.uart_setup["parity"][1]) 
                if parity == "E":
                    self.writeField(uart_reg_name,0,
                                    self.motor.uart_setup["parity"][0],
                                    self.motor.uart_setup["parity"][1])
                    
                if n_stop_bits == 1:
                    self.writeField(uart_reg_name,0,
                                    self.motor.uart_setup["stopbits"][0],
                                    self.motor.uart_setup["stopbits"][1])
                else:
                    self.writeField(uart_reg_name,2,
                                    self.motor.uart_setup["stopbits"][0],
                                    self.motor.uart_setup["stopbits"][1])
                # 8 data bits
                self.writeField(uart_reg_name,3,
                                self.motor.uart_setup["bitsno"][0],
                                self.motor.uart_setup["bitsno"][1])
                self.writeField(uart_reg_name,1,
                                start_bit=self.motor.uart_setup["protocol"][0],
                                bit_length=self.motor.uart_setup["protocol"][1])
                
                if save_in_flash:
                    self.saveToFlashReset()
            else:
                print("Unable to reconfigure ModBus using ModBus")
                
    def disableModBusRTU(self,channel:Literal["UART0","UART1"]="UART0",default=False):
        if isinstance(self.motor, MISMotor):
            self.writeRegister("modbus_setup",0)
        if isinstance(self.motor,MACMotor):
            if channel == "UART0":
                uart_reg_name = "uart0_setup"
            if channel == "UART1":
                uart_reg_name = "uart1_setup"
            # self.writeField(uart_reg_name,0,
            #                     start_bit=self.motor.uart_setup["protocol"][0],
            #                     bit_length=self.motor.uart_setup["protocol"][1])
            if default:
                self.writeRegister(uart_reg_name,0x01)
                self.baudrate = 19200
            else:
                self.writeField(uart_reg_name,0,
                                start_bit=self.motor.uart_setup["protocol"][0],
                                bit_length=self.motor.uart_setup["protocol"][1])
            self.saveToFlashReset()
        
    def switchMacTalkModBusRTU(self,parity:Literal["N","O","E"]="N"):
        if self.com_type == "Serial":
            if isinstance(self.protocol, MacTalkProtocol):
                self.closeCom()
                self.protocol = ModBusProtocol(com_type=self.com_type,
                                               port=self.port,
                                               baudrate=self.baudrate,
                                               parity=parity,
                                               motor_address=self.motor_address,
                                               motor=self.motor_type,
                                               motor_version=self.motor_version)
                
            elif isinstance(self.protocol, ModBusProtocol):
                self.closeCom()
                self.protocol = MacTalkProtocol(com_type=self.com_type,
                                               port=self.port,
                                               baudrate=self.baudrate,
                                               motor_address=self.motor_address,
                                               motor=self.motor_type)
        