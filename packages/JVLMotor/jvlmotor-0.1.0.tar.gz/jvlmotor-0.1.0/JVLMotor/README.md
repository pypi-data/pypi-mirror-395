# JVLMotor

## Overview
The MotorCom class is designed to manage communication with various motor types (such as MAC and MIS motors) through different communication protocols (like MacTalk, ModBus, EthernetIP, Profinet, and EtherCAT). It provides a unified interface to interact with the motors, read and write data, and manage motor settings across different communication protocols.

It also provides drivers for EA PSU (based on `ea-psu-controller`) and for Matrix APS AC PSU.

### Initialization and Motor Selection
The class constructor allows selection of various parameters:

- **Motor type**: Users can choose between "MAC" or "MIS" motors.
- **Communication type**: It supports different types like serial communication, Ethernet, and more.
- **Protocol selection**: Supports multiple protocols such as MacTalk, ModBus, EthernetIP, Profinet, and EtherCAT, each of which is instantiated accordingly

### Read/Write Operations
 The class provides multiple methods to interact with motor registers:

- **Write/Read operations**: The class allows writing to and reading from motor registers, with optional scaling and error handling.
- **WriteModule/ReadModule**: These methods are designed to handle specific module register operations, further extending communication possibilities.

The class simplifies reading and writing to specific motor registers and module registers by providing helper functions like `writeRegister`, `readRegister`, `writeModuleRegister`, and `readModuleRegister` where the registers can be read and written using their name (these names are specified in the Motors files).

## Requirements
- **Git**: Ensure that Git is installed on your machine. You can download it from [here](https://git-scm.com/downloads).
- **Python**: Make sure you have Python 3.x installed. You can download it from [here](https://www.python.org/downloads/).
- **Cifx Driver**: Install the **Cifx Driver** from the [Hilscher website](https://www.hilscher.com) as it's required for ethernet communication.
- **CIFX 50-RE PCI**: A CIFX 50-RE PCI card is required if the real-time Ethernet protocol are used.

## Usage
Simple example to run the motor at a 1000 RPM for 2 seconds.
```python
from JVLMotor.MotorCom import *

mc = MotorCom(port="COM6",motor="MAC")
print(mc.readRegister("p_ist"))
print(mc.readRegister("v_ist"))
mc.setVelocity(1000)
print(mc.readRegister("v_soll",mc.motor.registers["v_soll"][1]))
print(mc.readRegister("a_soll",mc.motor.registers["a_soll"][1]))

mc.setControlMode("velocity")
time.sleep(2)
print(mc.readRegister("p_ist"))
print(mc.readRegister("v_ist"))
mc.setControlMode("passive")
```

For the name of the registers or the commands, refer to the corresponding user manual [here](https://www.jvl.dk/416/user-manuals).

### Details
- **Creating a MotorCom object**: To create a MotorCom object, you can initialize it by specifying the motor type, communication type, protocol, and various other configuration parameters.
```python
motor_com = MotorCom(
    motor="MAC",               # Motor type: "MAC" or "MIS"
    com_type="Serial",         # Communication type: "Serial" or "Ethernet"
    protocol="MacTalk",        # Communication protocol: "MacTalk", "ModBus", "EthernetIP", "Profinet", "EtherCAT".
    port=None,                 # Serial port (optional)
    ip=None,                   # IP address (for Ethernet-based communication - Only ModBus TCP, the others are fixed inside a configuration file)
    baudrate=19200,            # Baudrate (for Serial communication)
    motor_address=254,         # Motor address (default: 254)
    netX=50,                   # Network settings (for ModBus communication)
    io_mode=None,              # IO mode (for EtherCAT communication, e.g., "Registers", "Driver")
    motor_version="0",         # Motor version (optional, used for certain protocols like EtherCAT)
    update=False               # Flag to determine if a CifX firmware update is needed (optional)
)
```

- **Main Functions**:
    - `write(self,reg,data,scaling=1,length=4,no_response=False)`: Writes to a register by its number
    - `read(self,reg,scaling=1,length=4)`: Reads a register by its number
    - `writeModule(self,reg,data,scaling=1,length=4,no_response=False)`: Write to a module register by its number
    - `readModule(self,reg,scaling=1,length=4)`: Read a module register by its name
    - `writeBit(self,reg,bit,data)`: Writes a specific bit (0 or 1) in the register specified by its name
    - `readBit(self,reg,bit)`: Reads a specific bit in the register specified by its name
    - `writeRegister(self,name, value, scaling=1, length=4, no_response=False)`: Writes to a register by its name.
    - `readRegister(self,name, scaling=1, length=4)`: Reads a register by its name.
    - `writeModuleRegister(self,name, value, scaling=1, length=4, no_response=False)`: Writes to a module register by its name.
    - `readModuleRegister(self,name, scaling=1, length=4)`: Reads a module register by its name.
    - `setControlMode(self,mode):`: Set the motor control mode according to: 
        ```python
        {
            "passive": 0,
            "velocity": 1,
            "position": 2,
            "gear": 3,
            "analog_trq": 4,
            "analog_vel": 5,
            "analog_vel_gear": 6,
            "manual_current": 7,
            "test_u": 8,
            "test_a": 9,
            "brake": 10,
            "stop": 11,
            "torque": 12,
            "forward": 13,
            "forward_backward": 14,
            "safe": 15,
            "analog_vel_deadband": 16,
            "analog_trq_vel_limited": 17,
            "analog_gear": 18,
            "coil": 19,
            "analog_bi_pos": 20,
            "analog_to_pos": 21,
            "test_ki": 22,
            "test_trq": 23,
            "gear_follow": 24,
            "index_slow": 25,
            "index_fast": 26,
            "highest": 27
        }
        ``` 
    - `setPosition(self,counts,length=4)`: Set the target position `p_soll` in counts.
    - `readPosition(self,length=4)`: Reads the current position `p_ist` in counts.
    - `setVelocity(self,vel_rpm):`: Set the target/maximum velocity `v_soll` in rpm.
    - `readVelocity(self)`: Reads the current velocity `v_ist` in rpm (according to the scaling - can be modified according to the motor parametrization).
    - `setAcceleration(self,acc_rpm_s)`: Set the maximum acceleration `a_soll` in rpm/s.
    - `clearErrors(self)`: Clear the error register.
    - `command(self,command,no_response=False)`: Write a command by its name.
    - `writeModuleCommand(self,command,no_response=False)`: Write a command in the module by its name.
    - `resetModule(self)`: Reset the module
    - `resetSynchronous(self)`: Reset the module and the motor synchronously.
    - `saveToFlashReset(self)`: Save to flash and reset.
    - `saveToFlashResetModule(self)`: Save to module's flash and reset.
    - `scopeVelocity(self,threshold = 10,size="small")`: Set the trigger and arm to scope the velocity when it's above the threshold in rpm.

Each of these methods allows you to interact with the motor, configuring it for data collection, triggering events, or reading and writing motor parameters via different protocols. Every register has a also a scaling value which can be accessed by :
```python
scaling = mc.motor.registers["my_register"][1]
```
- **Switching protocol**
If `update=True` the CifX firmware and configuration will be updated (only for real-time protocols). During this process, it is important to refrain from using the keyboard and mouse, as the update requires keyboard inputs to complete successfully.

- **Scope function**
The `MotorCom` also provide the scope function (not available with real-time protocol). To do so here is a simple example where the scope is triggered when the velocity is above 100 RPM:
```python
    mc.setScopeTrigger("compareValue", mc.motor.registers["v_ist"][0],
                        100*(1/mc.motor.registers["v_ist"][1],
                        condition = ">",trig_on_change=True))
    mc.arm([mc.motor.registers["v_soll"][0],mc.motor.registers["v_ist"][0],
            mc.motor.registers["p_ist"][0],mc.motor.registers["a_soll"][0]],
            size="small",rec_inner=False)

    mc.setVelocity(1000)
    mc.setControlMode("velocity")
    time.sleep(2)
    mc.setControlMode("passive")
    
    mc.downloadSBuf()
    mc.rescaleData([mc.motor.registers["v_soll"][1],mc.motor.registers["v_ist"][1],
            mc.motor.registers["p_ist"][1],mc.motor.registers["a_soll"][1]])

    mc.save("my_csv.csv")
```

- **Functions detailled**
    - `setScopeTrigger(self, mode, L=0, R=0, H=0, condition="",trigger_pos=0, trig_on_change=False, divisor=0)`: Set the trigger of the scope. Different mode: `Never,Always,compareValue,compareRegister,bitcondition,withinThreshold,outsideThreshold`. Different conditions: `==,!=,>,>=,<,<=,<<,!<<,||`.
    - ` arm(self,registers,size="normal",rec_inner=False)`: Arm the scope, with a list of registers (sepcified by their number).
    - `downloadSBuf(self)`: Download the scope buffer and put it into `self.channels`
    - `rescale(self,index,scaling)`: Rescale a specific channel.
    - ` rescaleData(self,scalings)`: Rescale the channels according to the scalings list provided.
    - `save(self,file_name)`: Save the data into a csv file.

## PSU Usage
# Elektro-Automatik PSU
The `EaPsuController` is designed to be used with EA PSU with 2 outputs but can also be used for single or more outputs. For more functionnalities please refer to: `https://pypi.org/project/ea-psu-controller/`
- **Initialization**: 
```python
# If with source code in the directory: 
from JVLMotor.MotorCom import *
# Else 

from JVLMotorLibrary.
psu = EaPsuController(comport="COM3",v_1=24, i_1=1, v_2=12, i_2=0.5,
                        ovp_1=30,ocp_1=2,ovp_2=20,ocp_2=1)
# Only if the PSU has 2 outputs:
psu.setupPsu()                        
```
- **Minimal Example**:
```python
psu.setupOutput(0,voltage=30,current=1,ovp=50,ocp=2)

psu.set_ovp(10,1)
psu.set_ocp(1,1)
psu.set_voltage(5,1)
psu.set_current(0.2,1)
psu.output_on(1)

psu.remote_off(0)
psu.remote_off(1)
```

# Matrix APS AC PSU
- **Initialization**
```python
from JVLMotor.MotorCom import *
psu = APSController(port="COM7",baudrate=19200,timeout=1,device_id=1)
psu.setup(voltage=220,frequency=50,max_current=5)
```
- **Minimal Example**
```python
psu.writeAutoTargetVoltage(150)
psu.writeControlOutput(True)
voltage = psu.readAutoTargetVoltage()
print(voltage)
```
## Project Structure
- **MotorCom.py**: The main class for communication with different motors
- **Motors/**: Directory containing the different class for the motors. 
    - **Motor.py**: Contains dictionnaries common to both motors.
    - **MACMotor.py**: Contains dictionnaries specific for MAC.
    - **MISMotor.py**: Contains dictionnaries specific for Mis.
- **Protocols/**: Directory containing the different class for the protocols and the communications
    - **TemplateProtocol.py**: A template that every protocol should inherit from
    - **MacTalkProtocol.py**: The class for the MacTalk protocol (Serial and UDP)
    - **ModBusProtocol.py**: The class for the Modbus protocol (Serial and TCP)
    - **EthernetIPProtocol.py**: The class for the EthernetIP protocol
    - **ProfinetIOProtocol.py**: The class for the ProfiNet protocol
    - **EtherCATRegistersProtocol.py**: The class for the EtherCAT protocol configured to use 8 fixed registers in the IO
    - **EtherCATDSPProtocol.py**: The class for the EtherCAT protocol configured to use a driver profile (fixed by the configuration of the CifX board)
    - **Communications/**: Directory containing the different class for the communications and lower level classes
        - **TemplateCommunication.py**: A template that every communication should inherit from
        - **SerialCommunication**: The class for a serial communication
        - **Drivers/**: Directory containing the different drivers and configuration for the CifX board
            - **EaPsuController.py**: The class for the EA PSU driver and control
            - **APSController.py**: The class for the APS PSu driver, communication and control
            - **CifxDriver.py**: The class to wrap up the CifX driver .dll and defining user-friendly functions
            - **CifXErrors.py**: A definition of every error code provided by Hilscher related to the driver
            - **Firmwares/**: The directory containing the different firmwares and configuration for the CifX board
                - **EIM**: The directory containing the files related to the EthernetIP protocol:
                    - **cifxeim.nxf**: The CifX firmare for the EthernetIP protocol
                    - **config.nxd**: The CifX configuration file for the EthernetIP protocol
                    - **nwid.nxd**: The network datbase for the EthernetIP protocol
                    - **updateEIMFirmware.py**: A subprocess called as an admin to use `CifX Driver Setup` and configure the board
                - **PNM**: The directory containing the files related to the ProfiNet protocol:
                    - **cifxeim.nxf**: The CifX firmare for the ProfiNet protocol
                    - **config.nxd**: The CifX configuration file for the ProfiNet protocol
                    - **updatePNMFirmware.py**: A subprocess called as an admin to use `CifX Driver Setup` and configure the board
                - **ECM**: The directory containing the files related to the EtherCAT protocol:
                    - **cifxeim.nxf**: The CifX firmare for the EtherCAT protocol
                    - **updateECMFirmware.py**: A subprocess called as an admin to use `CifX Driver Setup` and configure the board
                    - **DSP_MAC_50**: A directory containing the configuration file for a MAC 50-141 and configured to use a drive profile
                    - **DSP_MAC_400**: A directory containing the configuration file for a MAC 400+ and configured to use a drive profile
                    - **DSP_MIS**: A directory containing the configuration file for a MIS and configured to use a drive profile
                    - **JVL_MAC_50**: A directory containing the configuration file for a MAC 50-141 and configured to use fixed registers in the I/O
                    - **JVL_MAC_400**: A directory containing the configuration file for a MAC 400+ and configured to use fixed registers in the I/O
                    - **JVL_MIS**: A directory containing the configuration file for a MIS and configured to use fixed registers in the I/O