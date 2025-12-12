from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
from pymodbus.exceptions import ModbusIOException

#TODO: Use coils instead of registers

IO_OFFSET = 0
IO_CHANNEL_MAX = 31

POW_OFFSET = 32
POW_MAX = 10

class WagoController():
    def __init__(self,ip="192.168.0.10"):
        self.communication = ModbusTcpClient(host=ip,timeout=5)
        if(self.communication.connect()):
                self.communication.socket.setblocking(True)
        else:
            print("No connection")
            assert False

        self.registers = {
            "watchdog_time": [0x1000, 1, 2],
            "watchdog_coding_mask_1_16": [0x1001, 2, 2],
            "watchdog_coding_mask_17_32": [0x1002, 1, 2],
            "watchdog_trigger": [0x1003, 1, 2],
            "minimum_trigger_time": [0x1004, 1, 0],
            "watchdog_stop": [0x1005, 1, 2],
            "watchdog_status": [0x1006, 1, 0],
            "restart_watchdog": [0x1007, 1, 2],
            "stop_watchdog": [0x1008, 1, 2],
            "modbus_http_close_timeout": [0x1009, 1, 2],
            "watchdog_configuration": [0x100A, 1, 2],
            "save_watchdog_parameter": [0x100B, 1, 2],
            "led_error_code": [0x1020, 1, 0],
            "led_error_argument": [0x1021, 1, 0],
            "num_analog_output_data": [0x1022, 4, 0],
            "num_analog_input_data": [0x1023, 1, 0],
            "num_digital_output_data": [0x1024, 2, 0],
            "num_digital_input_data": [0x1025, 2, 0],
            "modbus_tcp_statistics": [0x1029, 9, 2],
            "num_tcp_connections": [0x102A, 1, 0],
            "kbus_reset": [0x102B, 1, 1],
            "modbus_tcp_timeout": [0x1030, 1, 2],
            "mac_id_readout": [0x1031, 3, 0],
            "modbus_response_delay": [0x1037, 1, 2],
            "modbus_tos": [0x1038, 1, 0],
            "diagnosis_connected_io_modules": [0x1050, 3, 0],
            "constant_0x0000": [0x2000, 9, 0],
            "constant_0xFFFF": [0x2001, 8, 0],
            "constant_0x1234": [0x2002, 7, 0],
            "constant_0xAAAA": [0x2003, 6, 0],
            "constant_0x5555": [0x2004, 5, 0],
            "constant_0x7FFF": [0x2005, 4, 0],
            "constant_0x8000": [0x2006, 3, 0],
            "constant_0x3FFF": [0x2007, 2, 0],
            "constant_0x4000": [0x2008, 1, 0],
            "firmware_version": [0x2010, 1, 0],
            "series_code": [0x2011, 1, 0],
            "coupler_controller_code": [0x2012, 1, 0],
            "firmware_major_version": [0x2013, 1, 0],
            "firmware_minor_version": [0x2014, 1, 0],
            "short_description_controller": [0x2020, 16, 0],
            "compile_time_firmware": [0x2021, 8, 0],
            "compile_date_firmware": [0x2022, 8, 0],
            "firmware_loader_indication": [0x2023, 32, 0],
            "description_connected_io_0_64": [0x2030, 65, 0],
            "description_connected_io_65_128": [0x2031, 64, 0],
            "description_connected_io_129_192": [0x2032, 64, 0],
            "description_connected_io_193_255": [0x2033, 63, 0],
            "process_image_settings": [0x2035, 1, 2],
            "fieldbus_coupler_diagnostics": [0x2036, 1, 0],
            "software_reset": [0x2040, 1, 1],
            "factory_settings": [0x2043, 1, 1]
        }

        self.input_register = 0x0000
        self.output_register = 0x0200

    def __del__(self):
         self.communication.close()

    def read(self,address,length=1):
        result = self.communication.read_holding_registers(address=address)
        if result.isError():
            print("Read ERROR!")
            print(result)
            
        received_values = result.registers
        if isinstance(received_values,list):
            received_bytes = b''.join(value.to_bytes(2, byteorder='little') for value in received_values)
        else:
            received_bytes = received_values
        value = int.from_bytes(received_bytes,byteorder='little',signed=True)
        return value
    
    def write(self,address,data,length=1):
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

        reg = address
        values16 = []

        try:
            if length>4:
                values16 += split_64bit_int(data)
                reg+= 2
            else:
                values16 += split_32bit_int(data)
                reg += 1
            self.communication.write_registers(
                address=address, values=values16
                )
            
            return 0
            
        except ConnectionException as e:
            print("Connection error:", e)
            return
        
    def readBit(self,address,bit):  
        try:
            result = self.communication.read_coils(address + bit, 1)
        except ModbusIOException:
            print(f"{result}")
            return None
        if isinstance(result, ModbusIOException):
             print(f"{result}")
             return None
        else:
            return result.bits[0] if result.bits else None  # Return the first value if available
        
    def writeBit(self,address,bit,bool,max_retries=5):
        for attempt in range(max_retries):
            try:
                return self.communication.write_coil(address+bit,bool)
            except:
                print(f"Error in Wago writeBit on attempt: {attempt+1} -> ReInit of the Wago controller and try again")
                #self.__init__()
                #self.writeBit(address=address,bit=bit,bool=bool)
                self.communication.close()
                if(self.communication.connect()):
                    self.communication.socket.setblocking(True)
        print("Wago writeBit failed after retries.")
        return None

        
    def readRegister(self,register,length=1):
        if self.registers[register][2] != 1:
            return self.read(self.registers[register][0])
        else:
            print("Write only register!")

    def writeRegister(self,register,data,length=1):
        if self.registers[register][2] != 0:
            return self.write(self.registers[register][0],data)
        else:
            print("Read only register")

    def readRegisterBit(self,register,bit,length=1):
        if self.registers[register][2] != 1:
            value = self.readRegister(register)
            return (value >> bit) & 1
        else:
            print("Write only register!")

    def writeRegisterBit(self,register,bit,bool,length=1):
        if self.registers[register][2] == 2:
            value = self.readRegister(register)
            if (bool == 1):
                value |= (1 << bit)
            else:
                value &= ~(1 << bit)
            return self.writeRegister(register,value)
        else:
            print("Write or Read only register - be careful!")

    def setOutputChannel(self,channel):
        return self.writeBit(self.output_register,channel,True)
    
    def cutOutputChannel(self,channel):
        return self.writeBit(self.output_register,channel,False)
    
    def checkOutputChannel(self,channel):
        return self.readBit(self.output_register,channel)
    
    def setInputChannel(self,channel):
        return self.writeBit(self.input_register,channel,True)
    
    def cutInputChannel(self,channel):
        return self.writeBit(self.input_register,channel,False)
    
    def checkInputChannel(self,channel):
        return self.readBit(self.input_register,channel)
    
    def setPowerOutput(self):
        for i in range(POW_OFFSET,POW_OFFSET+POW_MAX):
            self.setOutputChannel(i)
    
    def cutPowerOutput(self):
        for i in range(POW_OFFSET,POW_OFFSET+POW_MAX):
            self.cutOutputChannel(i)
        
    def checkPowerOutput(self):
        is_set = list()
        for i in range(POW_OFFSET,POW_OFFSET+POW_MAX):
            is_set.append(self.checkOutputChannel(i))
        return is_set
    
    def setPowerInput(self):
        for i in range(POW_OFFSET,POW_OFFSET+POW_MAX):
            self.setInputChannel(i)
    
    def cutPowerInput(self):
        for i in range(POW_OFFSET,POW_OFFSET+POW_MAX):
            self.cutInputChannel(i)
    
    def checkPowerInput(self):
        is_set = list()
        for i in range(POW_OFFSET,POW_OFFSET+POW_MAX):
            is_set.append(self.checkInputChannel(i))
        return is_set
    
