import ctypes
import os
from .CifXErrors import *
import time
CIFXHANDLE = ctypes.c_void_p

# DPM memory validation constants
CIFX_DPM_NO_MEMORY_ASSIGNED = 0x0BAD0BAD
CIFX_DPM_INVALID_CONTENT = 0xFFFFFFFF

CIFX_DPMSIGNATURE_BSL_STR = "BOOT"
CIFX_DPMSIGNATURE_BSL_VAL = 0x544F4F42
CIFX_DPMSIGNATURE_FW_STR = "netX"
CIFX_DPMSIGNATURE_FW_VAL = 0x5874656E

# CIFx global timeouts in milliseconds
CIFX_TO_WAIT_HW_RESET_ACTIVE = 2000
CIFX_TO_WAIT_HW = 2000
CIFX_TO_WAIT_COS_CMD = 20
CIFX_TO_WAIT_COS_ACK = 20
CIFX_TO_SEND_PACKET = 5000
CIFX_TO_1ST_PACKET = 1000
CIFX_TO_CONT_PACKET = 1000
CIFX_TO_LAST_PACKET = 1000
CIFX_TO_FIRMWARE_START = 20000
CIFX_TO_FIRMWARE_UPDATE = 30000

# Maximum channel number
CIFX_MAX_NUMBER_OF_CHANNEL_DEFINITION = 8
CIFX_MAX_NUMBER_OF_CHANNELS = 6
CIFX_NO_CHANNEL = 0xFFFFFFFF

# Maximum file name length
CIFX_MAX_FILE_NAME_LENGTH = 260
CIFX_MIN_FILE_NAME_LENGTH = 5

# The system device port number
CIFX_SYSTEM_DEVICE = 0xFFFFFFFF

# Information commands
CIFX_INFO_CMD_SYSTEM_INFORMATION = 1
CIFX_INFO_CMD_SYSTEM_INFO_BLOCK = 2
CIFX_INFO_CMD_SYSTEM_CHANNEL_BLOCK = 3
CIFX_INFO_CMD_SYSTEM_CONTROL_BLOCK = 4
CIFX_INFO_CMD_SYSTEM_STATUS_BLOCK = 5

# General commands
CIFX_CMD_READ_DATA = 1
CIFX_CMD_WRITE_DATA = 2

# HOST mode definition
CIFX_HOST_STATE_NOT_READY = 0
CIFX_HOST_STATE_READY = 1
CIFX_HOST_STATE_READ = 2

# WATCHDOG commands
CIFX_WATCHDOG_STOP = 0
CIFX_WATCHDOG_START = 1

# Configuration Lock commands
CIFX_CONFIGURATION_UNLOCK = 0
CIFX_CONFIGURATION_LOCK = 1
CIFX_CONFIGURATION_GETLOCKSTATE = 2

# BUS state commands
CIFX_BUS_STATE_OFF = 0
CIFX_BUS_STATE_ON = 1
CIFX_BUS_STATE_GETSTATE = 2

# DMA state commands
CIFX_DMA_STATE_OFF = 0
CIFX_DMA_STATE_ON = 1
CIFX_DMA_STATE_GETSTATE = 2

# Memory pointer commands
CIFX_MEM_PTR_OPEN = 1
CIFX_MEM_PTR_OPEN_USR = 2
CIFX_MEM_PTR_CLOSE = 3

# I/O area definition
CIFX_IO_INPUT_AREA = 1
CIFX_IO_OUTPUT_AREA = 2

# xChannelReset definitions
CIFX_SYSTEMSTART = 1
CIFX_CHANNELINIT = 2
CIFX_BOOTSTART = 3  # This definition is not supported by cifXAPI

# xSysdeviceResetEx definitions
CIFX_RESETEX_SYSTEMSTART = 0
CIFX_RESETEX_BOOTSTART = 2
CIFX_RESETEX_UPDATESTART = 3

# Shift value for variant selection of CIFX_RESETEX_UPDATESTART
CIFX_RESETEX_UPDATESTART_VARIANT_SRT = 4

# Sync command definitions
CIFX_SYNC_SIGNAL_CMD = 1
CIFX_SYNC_ACKNOWLEDGE_CMD = 2
CIFX_SYNC_WAIT_CMD = 3

class CIFXNotifyRxMbxFullData(ctypes.Structure):
    _fields_ = [("ulRecvCount", ctypes.c_uint32)]

class CIFXNotifyTxMbxEmptyData(ctypes.Structure):
    _fields_ = [("ulMaxSendCount", ctypes.c_uint32)]

class CIFXNotifyComStateData(ctypes.Structure):
    _fields_ = [("ulComState", ctypes.c_uint32)]

# Notifications
CIFX_NOTIFY_RX_MBX_FULL = 1
CIFX_NOTIFY_TX_MBX_EMPTY = 2
CIFX_NOTIFY_PD0_IN = 3
CIFX_NOTIFY_PD1_IN = 4
CIFX_NOTIFY_PD0_OUT = 5
CIFX_NOTIFY_PD1_OUT = 6
CIFX_NOTIFY_SYNC = 7
CIFX_NOTIFY_COM_STATE = 8

# Extended memory commands
CIFX_GET_EXTENDED_MEMORY_INFO = 1
CIFX_GET_EXTENDED_MEMORY_POINTER = 2
CIFX_FREE_EXTENDED_MEMORY_POINTER = 3

CIFx_MAX_INFO_NAME_LENGTH = 16
CIFX_MAX_PACKET_SIZE = 1596
CIFX_PACKET_HEADER_SIZE = 40
CIFX_MAX_DATA_SIZE = CIFX_MAX_PACKET_SIZE - CIFX_PACKET_HEADER_SIZE

class DRIVER_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("abDriverVersion", ctypes.c_char * 32),  # Driver version
        ("ulBoardCnt", ctypes.c_uint32),           # Number of available Boards
    ]

class CIFX_DIRECTORYENTRY(ctypes.Structure):
    _fields_ = [
        ("hList", ctypes.c_void_p),                   # Handle from Enumeration function
        ("szFilename", ctypes.c_char * CIFx_MAX_INFO_NAME_LENGTH),  # Returned file name
        ("bFiletype", ctypes.c_uint8),                # Returned file type
        ("ulFilesize", ctypes.c_uint32),              # Returned file size
    ]

class CIFX_EXTENDED_MEMORY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("pvMemoryID", ctypes.c_void_p),             # Identification of the memory area
        ("pvMemoryPtr", ctypes.c_void_p),            # Memory pointer
        ("ulMemorySize", ctypes.c_uint32),           # Memory size of the Extended memory area
        ("ulMemoryType", ctypes.c_uint32),           # Memory type information
    ]

class SYSTEM_CHANNEL_SYSTEM_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ulSystemError", ctypes.c_uint32),          # Global system error
        ("ulDpmTotalSize", ctypes.c_uint32),         # Total size dual-port memory in bytes
        ("ulMBXSize", ctypes.c_uint32),              # System mailbox data size [Byte]
        ("ulDeviceNumber", ctypes.c_uint32),         # Global device number
        ("ulSerialNumber", ctypes.c_uint32),         # Global serial number
        ("ulOpenCnt", ctypes.c_uint32),              # Channel open counter
    ]

class SYSTEM_CHANNEL_SYSTEM_INFO_BLOCK(ctypes.Structure):
    _fields_ = [
        ("abCookie", ctypes.c_uint8 * 4),            # 0x00 "netX" cookie
        ("ulDpmTotalSize", ctypes.c_uint32),         # 0x04 Total Size of the whole dual-port memory in bytes
        ("ulDeviceNumber", ctypes.c_uint32),         # 0x08 Device number
        ("ulSerialNumber", ctypes.c_uint32),         # 0x0C Serial number
        ("ausHwOptions", ctypes.c_uint16 * 4),      # 0x10 Hardware options, xC port 0.3
        ("usManufacturer", ctypes.c_uint16),         # 0x18 Manufacturer Location
        ("usProductionDate", ctypes.c_uint16),       # 0x1A Date of production
        ("ulLicenseFlags1", ctypes.c_uint32),        # 0x1C License code flags 1
        ("ulLicenseFlags2", ctypes.c_uint32),        # 0x20 License code flags 2
        ("usNetxLicenseID", ctypes.c_uint16),        # 0x24 netX license identification
        ("usNetxLicenseFlags", ctypes.c_uint16),     # 0x26 netX license flags
        ("usDeviceClass", ctypes.c_uint16),          # 0x28 netX device class
        ("bHwRevision", ctypes.c_uint8),             # 0x2A Hardware revision index
        ("bHwCompatibility", ctypes.c_uint8),        # 0x2B Hardware compatibility index
        ("bDevIdNumber", ctypes.c_uint8),            # 0x2C Device identification number (rotary switch)
        ("bReserved", ctypes.c_uint8),                # 0x2D Reserved byte
        ("usReserved", ctypes.c_uint16),             # 0x2E:0x2F Reserved
    ]

class SYSTEM_CHANNEL_CHANNEL_INFO_BLOCK(ctypes.Structure):
    _fields_ = [
        ("abInfoBlock", ctypes.c_uint8 * (CIFx_MAX_INFO_NAME_LENGTH * 16)),  # Default info block size
    ]

class SYSTEM_CHANNEL_SYSTEM_CONTROL_BLOCK(ctypes.Structure):
    _fields_ = [
        ("ulSystemCommandCOS", ctypes.c_uint32),    # System channel change of state command
        ("ulSystemControl", ctypes.c_uint32),        # System channel control
    ]

class SYSTEM_CHANNEL_SYSTEM_STATUS_BLOCK(ctypes.Structure):
    _fields_ = [
        ("ulSystemCOS", ctypes.c_uint32),            # System channel change of state acknowledge
        ("ulSystemStatus", ctypes.c_uint32),         # Actual system state
        ("ulSystemError", ctypes.c_uint32),          # Actual system error
        ("ulBootError", ctypes.c_uint32),            # Bootup error code (only valid if Cookie="BOOT")
        ("ulTimeSinceStart", ctypes.c_uint32),       # Time since start in seconds
        ("usCpuLoad", ctypes.c_uint16),              # CPU load in 0,01% units (10000 => 100%)
        ("usReserved", ctypes.c_uint16),             # Reserved
        ("ulHWFeatures", ctypes.c_uint32),           # Hardware features
        ("abReserved", ctypes.c_uint8 * 36),         # Reserved
    ]

class BOARD_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("lBoardError", ctypes.c_int32),             # Global Board error
        ("abBoardName", ctypes.c_char * CIFx_MAX_INFO_NAME_LENGTH),  # Global board name
        ("abBoardAlias", ctypes.c_char * CIFx_MAX_INFO_NAME_LENGTH), # Global board alias name
        ("ulBoardID", ctypes.c_uint32),              # Unique board ID, driver created
        ("ulSystemError", ctypes.c_uint32),          # System error
        ("ulPhysicalAddress", ctypes.c_uint32),      # Physical memory address
        ("ulIrqNumber", ctypes.c_uint32),            # Hardware interrupt number
        ("bIrqEnabled", ctypes.c_uint8),             # Hardware interrupt enable flag
        ("ulChannelCnt", ctypes.c_uint32),           # Number of available channels
        ("ulDpmTotalSize", ctypes.c_uint32),         # Dual-Port memory size in bytes
        ("tSystemInfo", SYSTEM_CHANNEL_SYSTEM_INFO_BLOCK),  # System information
    ]

class CHANNEL_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("abBoardName", ctypes.c_char * CIFx_MAX_INFO_NAME_LENGTH),  # Global board name
        ("abBoardAlias", ctypes.c_char * CIFx_MAX_INFO_NAME_LENGTH), # Global board alias name
        ("ulDeviceNumber", ctypes.c_uint32),              # Global board device number
        ("ulSerialNumber", ctypes.c_uint32),              # Global board serial number

        ("usFWMajor", ctypes.c_uint16),                   # Major Version of Channel Firmware
        ("usFWMinor", ctypes.c_uint16),                   # Minor Version of Channel Firmware
        ("usFWBuild", ctypes.c_uint16),                   # Build number of Channel Firmware
        ("usFWRevision", ctypes.c_uint16),                # Revision of Channel Firmware
        ("bFWNameLength", ctypes.c_uint8),               # Length of FW Name
        ("abFWName", ctypes.c_char * 63),               # Firmware Name
        ("usFWYear", ctypes.c_uint16),                    # Build Year of Firmware
        ("bFWMonth", ctypes.c_uint8),                     # Build Month of Firmware (1.12)
        ("bFWDay", ctypes.c_uint8),                       # Build Day of Firmware (1.31)

        ("ulChannelError", ctypes.c_uint32),              # Channel error
        ("ulOpenCnt", ctypes.c_uint32),                   # Channel open counter
        ("ulPutPacketCnt", ctypes.c_uint32),              # Number of put packet commands
        ("ulGetPacketCnt", ctypes.c_uint32),              # Number of get packet commands
        ("ulMailboxSize", ctypes.c_uint32),               # Mailbox packet size in bytes
        ("ulIOInAreaCnt", ctypes.c_uint32),               # Number of IO IN areas
        ("ulIOOutAreaCnt", ctypes.c_uint32),              # Number of IO OUT areas
        ("ulHskSize", ctypes.c_uint32),                   # Size of the handshake cells
        ("ulNetxFlags", ctypes.c_uint32),                 # Actual netX state flags
        ("ulHostFlags", ctypes.c_uint32),                 # Actual Host flags
        ("ulHostCOSFlags", ctypes.c_uint32),              # Actual Host COS flags
        ("ulDeviceCOSFlags", ctypes.c_uint32),            # Actual Device COS flags
    ]

class CHANNEL_IO_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ulTotalSize", ctypes.c_uint32),                # Total IO area size in bytes
        ("ulReserved", ctypes.c_uint32),                 # Reserved for further use
        ("ulIOMode", ctypes.c_uint32),                   # Exchange mode
    ]

class MEMORY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("pvMemoryID", ctypes.c_void_p),                 # Identification of the memory area
        ("ppvMemoryPtr", ctypes.POINTER(ctypes.c_void_p)),  # Memory pointer
        ("ulMemorySize", ctypes.POINTER(ctypes.c_uint32)),               # Memory size of the Extended memory area
        ("ulChannel", ctypes.c_uint32),               # Requested channel number
        ("pulChannelStartOffset", ctypes.POINTER(ctypes.c_uint32)),               # Start offset of the requested channel
        ("pulChannelSize", ctypes.POINTER(ctypes.c_uint32)),               #  Memory size of the requested channel
    ]

class IO_DATA(ctypes.Structure):
    _fields_ = [
        ("ulLength", ctypes.c_uint32),                   # Length of the data
        ("pData", ctypes.POINTER(ctypes.c_uint8)),      # Pointer to the data
    ]

class PLC_MEMORY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("pvMemoryID", ctypes.c_void_p),               # Identification of the memory area
        ("ppvMemoryPtr", ctypes.POINTER(ctypes.c_void_p)),  # Memory pointer
        ("ulAreaDefinition", ctypes.c_uint32),         # Input/output area
        ("ulAreaNumber", ctypes.c_uint32),             # Area number
        ("pulIOAreaStartOffset", ctypes.POINTER(ctypes.c_uint32)),  # Start offset
        ("pulIOAreaSize", ctypes.POINTER(ctypes.c_uint32)),         # Memory size
    ]

class CIFX_PACKET_HEADER(ctypes.Structure):
    _fields_ = [
        ("ulDest", ctypes.c_uint32),                   # Destination of packet, process queue - 0
        ("ulSrc", ctypes.c_uint32),                    # Source of packet, process queue - 0
        ("ulDestId", ctypes.c_uint32),                 # Destination reference of packet - 0
        ("ulSrcId", ctypes.c_uint32),                  # Source reference of packet - 0
        ("ulLen", ctypes.c_uint32),                    # Length of packet data without header
        ("ulId", ctypes.c_uint32),                     # Identification handle of sender - Counter
        ("ulState", ctypes.c_uint32),                  # Status code of operation
        ("ulCmd", ctypes.c_uint32),                    # Packet command defined in TLR_Commands.h
        ("ulExt", ctypes.c_uint32),                    # Extension - 0
        ("ulRout", ctypes.c_uint32),                   # Router - 0
    ]

class CIFX_PACKET(ctypes.Structure):
    _fields_ = [
        ("tHeader", CIFX_PACKET_HEADER),                # Packet header
        ("abData", ctypes.c_uint8 * CIFX_MAX_DATA_SIZE)  # Packet data
    ]

# Constants for callback states
CIFX_CALLBACK_ACTIVE = 0
CIFX_CALLBACK_FINISHED = 1

# Constants for download modes
DOWNLOAD_MODE_FIRMWARE = 1
DOWNLOAD_MODE_CONFIG = 2
DOWNLOAD_MODE_FILE = 3
DOWNLOAD_MODE_BOOTLOADER = 4  # Download bootloader update to target
DOWNLOAD_MODE_LICENSECODE = 5  # License update code
DOWNLOAD_MODE_MODULE = 6

# Define callback types
PFN_PROGRESS_CALLBACK = ctypes.CFUNCTYPE(
    None,  # Return type
    ctypes.c_uint32,  # ulStep
    ctypes.c_uint32,  # ulMaxStep
    ctypes.c_void_p,  # pvUser
    ctypes.c_int8,    # bFinished
    ctypes.c_int32    # lError
)

@PFN_PROGRESS_CALLBACK
def progressCallback(ulStep, ulMaxStep, pvUser, bFinished, lError):
    print(f"Step: {ulStep}/{ulMaxStep}, User:{pvUser} Finished: {bFinished}, Error: {hex(lError)}")

PFN_RECV_PKT_CALLBACK = ctypes.CFUNCTYPE(
    None,  # Return type
    ctypes.POINTER(CIFX_PACKET),  # ptRecvPkt
    ctypes.c_void_p               # pvUser
)

@PFN_RECV_PKT_CALLBACK
def recvPktCallback(ptRecvPkt,pvUser):
    pass

PFN_NOTIFY_CALLBACK = ctypes.CFUNCTYPE(
    None,  # Return type
    ctypes.c_uint32,  # ulNotification
    ctypes.c_uint32,  # ulDataLen
    ctypes.c_void_p,  # pvData
    ctypes.c_void_p   # pvUser
)

PACKET_WAIT_TIMEOUT = 500
IO_WAIT_TIMEOUT  =   10
HOSTSTATE_TIMEOUT =  5000

class CifXDriver:
    def __init__(self):
        self.dll = ctypes.CDLL('cifX32dll.dll')
        self.dll.xDriverOpen.argtypes = [CIFXHANDLE]
        self.dll.xDriverOpen.restype = ctypes.c_int32

        self.dll.xDriverClose.argtypes = [CIFXHANDLE]
        self.dll.xDriverClose.restype = ctypes.c_int32

        self.dll.xDriverGetInformation.argtypes = [CIFXHANDLE,ctypes.c_uint32,ctypes.c_void_p]
        self.dll.xDriverGetInformation.restype = ctypes.c_int32

        self.dll.xDriverGetErrorDescription.argtypes = [ctypes.c_int32, ctypes.c_char_p, ctypes.c_uint32]
        self.dll.xDriverGetErrorDescription.restype = ctypes.c_int32

        self.dll.xDriverEnumBoards.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xDriverEnumBoards.restype = ctypes.c_int32

        self.dll.xDriverEnumChannels.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xDriverEnumChannels.restype = ctypes.c_int32

        self.dll.xDriverMemoryPointer.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xDriverMemoryPointer.restype = ctypes.c_int32

        self.dll.xDriverRestartDevice.argtypes = [CIFXHANDLE, ctypes.c_char_p, ctypes.c_void_p]
        self.dll.xDriverRestartDevice.restype = ctypes.c_int32

        # System device-dependent functions
        self.dll.xSysdeviceOpen.argtypes = [CIFXHANDLE, ctypes.c_char_p, ctypes.POINTER(CIFXHANDLE)]
        self.dll.xSysdeviceOpen.restype = ctypes.c_int32

        self.dll.xSysdeviceClose.argtypes = [CIFXHANDLE]
        self.dll.xSysdeviceClose.restype = ctypes.c_int32

        self.dll.xSysdeviceGetMBXState.argtypes = [CIFXHANDLE, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xSysdeviceGetMBXState.restype = ctypes.c_int32

        self.dll.xSysdevicePutPacket.argtypes = [CIFXHANDLE, ctypes.POINTER(CIFX_PACKET), ctypes.c_uint32]
        self.dll.xSysdevicePutPacket.restype = ctypes.c_int32

        self.dll.xSysdeviceGetPacket.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(CIFX_PACKET), ctypes.c_uint32]
        self.dll.xSysdeviceGetPacket.restype = ctypes.c_int32

        self.dll.xSysdeviceInfo.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xSysdeviceInfo.restype = ctypes.c_int32

        self.dll.xSysdeviceFindFirstFile.argtypes = [
            CIFXHANDLE,
            ctypes.c_uint32,
            ctypes.POINTER(CIFX_DIRECTORYENTRY),
            PFN_RECV_PKT_CALLBACK,
            ctypes.c_void_p
        ]
        self.dll.xSysdeviceFindFirstFile.restype = ctypes.c_int32

        self.dll.xSysdeviceFindNextFile.argtypes = [
            CIFXHANDLE,
            ctypes.c_uint32,
            ctypes.POINTER(CIFX_DIRECTORYENTRY),
            PFN_RECV_PKT_CALLBACK,
            ctypes.c_void_p
        ]
        self.dll.xSysdeviceFindNextFile.restype = ctypes.c_int32

        self.dll.xSysdeviceDownload.argtypes = [
            CIFXHANDLE,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_uint8),  # Pointer to file data
            ctypes.c_uint32,
            PFN_PROGRESS_CALLBACK,
            PFN_RECV_PKT_CALLBACK,
            ctypes.c_void_p
        ]
        self.dll.xSysdeviceDownload.restype = ctypes.c_int32

        self.dll.xSysdeviceUpload.argtypes = [
            CIFXHANDLE,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_uint8),  # Pointer to file data
            ctypes.POINTER(ctypes.c_uint32),  # Pointer to file size
            PFN_PROGRESS_CALLBACK,
            PFN_RECV_PKT_CALLBACK,
            ctypes.c_void_p
        ]
        self.dll.xSysdeviceUpload.restype = ctypes.c_int32

        self.dll.xSysdeviceReset.argtypes = [CIFXHANDLE, ctypes.c_uint32]
        self.dll.xSysdeviceReset.restype = ctypes.c_int32

        self.dll.xSysdeviceResetEx.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32]
        self.dll.xSysdeviceResetEx.restype = ctypes.c_int32

        self.dll.xSysdeviceBootstart.argtypes = [CIFXHANDLE, ctypes.c_uint32]
        self.dll.xSysdeviceBootstart.restype = ctypes.c_int32

        self.dll.xSysdeviceExtendedMemory.argtypes = [
            CIFXHANDLE,
            ctypes.c_uint32,
            ctypes.POINTER(CIFX_EXTENDED_MEMORY_INFORMATION)  # Define this structure appropriately
        ]
        self.dll.xSysdeviceExtendedMemory.restype = ctypes.c_int32
        
        self.dll.xChannelOpen.argtypes = [CIFXHANDLE, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(CIFXHANDLE)]
        self.dll.xChannelOpen.restype = ctypes.c_int32

        self.dll.xChannelClose.argtypes = [CIFXHANDLE]
        self.dll.xChannelClose.restype = ctypes.c_int32

        self.dll.xChannelFindFirstFile.argtypes = [CIFXHANDLE, CIFX_DIRECTORYENTRY, ctypes.c_void_p, ctypes.c_void_p]
        self.dll.xChannelFindFirstFile.restype = ctypes.c_int32

        self.dll.xChannelFindNextFile.argtypes = [CIFXHANDLE, CIFX_DIRECTORYENTRY, ctypes.c_void_p, ctypes.c_void_p]
        self.dll.xChannelFindNextFile.restype = ctypes.c_int32

        self.dll.xChannelDownload.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        self.dll.xChannelDownload.restype = ctypes.c_int32

        self.dll.xChannelUpload.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        self.dll.xChannelUpload.restype = ctypes.c_int32

        self.dll.xChannelGetMBXState.argtypes = [CIFXHANDLE, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xChannelGetMBXState.restype = ctypes.c_int32

        self.dll.xChannelPutPacket.argtypes = [CIFXHANDLE, ctypes.POINTER(CIFX_PACKET), ctypes.c_uint32]
        self.dll.xChannelPutPacket.restype = ctypes.c_int32

        self.dll.xChannelGetPacket.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(CIFX_PACKET), ctypes.c_uint32]
        self.dll.xChannelGetPacket.restype = ctypes.c_int32

        self.dll.xChannelGetSendPacket.argtypes = [CIFXHANDLE, ctypes.c_uint32, CIFX_PACKET]
        self.dll.xChannelGetSendPacket.restype = ctypes.c_int32

        self.dll.xChannelConfigLock.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
        self.dll.xChannelConfigLock.restype = ctypes.c_int32

        self.dll.xChannelReset.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32]
        self.dll.xChannelReset.restype = ctypes.c_int32

        self.dll.xChannelInfo.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelInfo.restype = ctypes.c_int32

        self.dll.xChannelWatchdog.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xChannelWatchdog.restype = ctypes.c_int32

        self.dll.xChannelHostState.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
        self.dll.xChannelHostState.restype = ctypes.c_int32

        self.dll.xChannelBusState.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
        self.dll.xChannelBusState.restype = ctypes.c_int32

        self.dll.xChannelDMAState.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xChannelDMAState.restype = ctypes.c_int32

        self.dll.xChannelIOInfo.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelIOInfo.restype = ctypes.c_int32

        self.dll.xChannelIORead.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint32]
        self.dll.xChannelIORead.restype = ctypes.c_int32

        self.dll.xChannelIOWrite.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint32]
        self.dll.xChannelIOWrite.restype = ctypes.c_int32

        self.dll.xChannelIOReadSendData.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelIOReadSendData.restype = ctypes.c_int32

        self.dll.xChannelControlBlock.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelControlBlock.restype = ctypes.c_int32

        self.dll.xChannelCommonStatusBlock.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelCommonStatusBlock.restype = ctypes.c_int32

        self.dll.xChannelExtendedStatusBlock.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelExtendedStatusBlock.restype = ctypes.c_int32

        #self.dll.xChannelUserBlock.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
        #self.dll.xChannelUserBlock.restype = ctypes.c_int32

        self.dll.xChannelPLCMemoryPtr.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_void_p]
        self.dll.xChannelPLCMemoryPtr.restype = ctypes.c_int32

        self.dll.xChannelPLCIsReadReady.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xChannelPLCIsReadReady.restype = ctypes.c_int32

        self.dll.xChannelPLCIsWriteReady.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xChannelPLCIsWriteReady.restype = ctypes.c_int32

        self.dll.xChannelPLCActivateWrite.argtypes = [CIFXHANDLE, ctypes.c_uint32]
        self.dll.xChannelPLCActivateWrite.restype = ctypes.c_int32

        self.dll.xChannelPLCActivateRead.argtypes = [CIFXHANDLE, ctypes.c_uint32]
        self.dll.xChannelPLCActivateRead.restype = ctypes.c_int32

        self.dll.xChannelRegisterNotification.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p]
        self.dll.xChannelRegisterNotification.restype = ctypes.c_int32

        self.dll.xChannelUnregisterNotification.argtypes = [CIFXHANDLE, ctypes.c_uint32]
        self.dll.xChannelUnregisterNotification.restype = ctypes.c_int32

        self.dll.xChannelSyncState.argtypes = [CIFXHANDLE, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32)]
        self.dll.xChannelSyncState.restype = ctypes.c_int32

        self.driver =  CIFXHANDLE()
        self.driver_info = DRIVER_INFORMATION()
        self.board_info = []
        self.board_name = []
        self.channel_info = [[]]
        self.device = CIFXHANDLE()

        self.openDriver()
        self.enumBoardsDriver()
        self.enumChannelsDriver()

    # ========================================= DRIVER FUNCTIONS ================================
    def openDriver(self):
        return self.dll.xDriverOpen(ctypes.byref(self.driver))
    
    def closeDriver(self):
        return self.dll.xDriverClose(self.driver)
    
    def getInfoDriver(self):
        self.driver_info = DRIVER_INFORMATION()
        error_code = self.dll.xDriverGetInformation(self.driver,
                                              ctypes.sizeof(self.driver_info),
                                              ctypes.byref(self.driver_info))
        return self.driver_info,error_code
    
    def getErrorDescriptionDriver(self,error):
        error_description = (ctypes.c_char*1024)()
        error_code = self.dll.xDriverGetErrorDescription(ctypes.c_int32(error),error_description,
                                                   ctypes.sizeof(error_description))
        return error_description.value.decode('utf-8').rstrip('\x00')
    
    def enumBoardsDriver(self):
        board_error = CIFX_NO_ERROR
        index = 0
        while board_error == CIFX_NO_ERROR:
            board_info = BOARD_INFORMATION()
            board_error = self.dll.xDriverEnumBoards(self.driver, index,
                                            ctypes.sizeof(board_info),
                                            ctypes.byref(board_info))
            if board_error == CIFX_NO_ERROR:
                self.board_info.append(board_info)
                self.board_name.append(board_info.abBoardName.decode('utf-8'))
                if index > 0:
                    self.channel_info.append([])
            index+=1

    def enumChannelsDriver(self):
        for i in range(len(self.board_info)):
            channel_error = CIFX_NO_ERROR
            index = 0
            while channel_error == CIFX_NO_ERROR:
                channel_info = CHANNEL_INFORMATION()
                channel_error = self.dll.xDriverEnumChannels(self.driver,i,
                                                              index, ctypes.sizeof(channel_info),
                                                                ctypes.byref(channel_info))
                if channel_error == CIFX_NO_ERROR:
                    self.channel_info[i].append(channel_info)
                index+=1

    def memoryPointerDriver(self,board_index):
        buffer = (ctypes.c_char*100)()
        memory_id = ctypes.c_uint32(0)
        dpm_memory =  ctypes.c_char_p()
        memory_size = ctypes.c_uint32(0)
        channel_start_offset = ctypes.c_uint32(0)
        channel_size =  ctypes.c_uint32(0)

        self.memory = MEMORY_INFORMATION()
        self.memory.pvMemoryID = ctypes.byref(memory_id)
        self.memory.ppvMemoryPtr = ctypes.byref(dpm_memory)
        self.memory.pulMemorySize = ctypes.byref(memory_size)
        self.memory.ulChannel = CIFX_NO_CHANNEL
        self.memory.pulChannelStartOffset = ctypes.byref(channel_start_offset)
        self.memory.pulChannelSize = ctypes.byref(channel_size)

        return self.dll.xDriverMemoryPointer(self.driver,board_index,
                                             CIFX_MEM_PTR_OPEN,ctypes.byref(self.memory))
    
    def restartDeviceDriver(self,board_number):
        name = ctypes.c_char_p(self.board_name[board_number].encode('utf-8'))
        return self.dll.xDriverRestartDevice(self.driver,name,None)

    # ========================================= SYSTEM DEVICE FUNCTIONS ================================
    def openSysDevice(self,board_number):
        name = ctypes.c_char_p(self.board_name[board_number].encode('utf-8'))
        return self.dll.xSysdeviceOpen(self.driver,name,ctypes.byref(self.device))
    
    def closeSysDevice(self):
        return self.dll.xSysdeviceClose(self.device)
    
    def getMBXStateSysDevice(self):
        recv_count = ctypes.c_uint32()
        sent_count = ctypes.c_uint32()
        error_code = self.dll.xSysdeviceGetMBXState(self.device,
                                                    ctypes.byref(recv_count),
                                                    ctypes.byref(sent_count))
        return recv_count,sent_count,error_code,
    
    def putPacketSysDevice(self,packet,timeout):
        return self.dll.xSysdevicePutPacket(self.device,ctypes.byref(packet),timeout)
    
    def getPacketSysDevice(self,timeout):
        rcv_packet = CIFX_PACKET()
        error_code = self.dll.xSysdeviceGetPacket(self.device,ctypes.sizeof(rcv_packet),
                                                  ctypes.byref(rcv_packet),timeout)
        return rcv_packet.abData,error_code
        
    def infoSysDevice(self,cmd):
        if cmd == CIFX_INFO_CMD_SYSTEM_INFORMATION:
            info = SYSTEM_CHANNEL_SYSTEM_INFORMATION()
            size = ctypes.sizeof(info)
        elif cmd == CIFX_INFO_CMD_SYSTEM_INFO_BLOCK:
            info = SYSTEM_CHANNEL_SYSTEM_INFO_BLOCK()
            size = ctypes.sizeof(info)
        elif cmd == CIFX_INFO_CMD_SYSTEM_CHANNEL_BLOCK:
            info = SYSTEM_CHANNEL_CHANNEL_INFO_BLOCK()
            size = ctypes.sizeof(info)
        elif cmd == CIFX_INFO_CMD_SYSTEM_CONTROL_BLOCK:
            info = SYSTEM_CHANNEL_SYSTEM_CONTROL_BLOCK()
            size = ctypes.sizeof(info)
        elif cmd == CIFX_INFO_CMD_SYSTEM_STATUS_BLOCK:
            info = SYSTEM_CHANNEL_SYSTEM_STATUS_BLOCK()
            size = ctypes.sizeof(info)

        error_code = self.dll.xSysdeviceInfo(self.device,cmd, size,ctypes.byref(info))
        return info,error_code
    
    def findFirstFileSysDevice(self,ch_num):
        directory_info = CIFX_DIRECTORYENTRY()
        error_code = self.dll.xSysdeviceFindFirstFile(self.device,ch_num,
                                                      ctypes.byref(directory_info),
                                                      None,None)
        return directory_info,error_code
    
    def findNextFileSysDevice(self,ch_num,directory):
        error_code = self.dll.xSysdeviceFindNextFile(self.device,ch_num,
                                                     ctypes.byref(directory),None,None)
        return directory,error_code
    
    def osFileOpen(self,file_path):
        try:
            with open(file_path, "rb") as file:
                # Seek to the end of the file to determine the size
                file.seek(0, os.SEEK_END)
                file_size = file.tell()  # Get the current position which is the file size
                file.seek(0, os.SEEK_SET)  # Seek back to the start of the file
                file_data = file.read()
                file_data_uint8 = (ctypes.c_uint8 * file_size).from_buffer_copy(file_data)
                return file_data_uint8, file_size  # Return the file handle and its size
        except (OSError, IOError) as e:
            print(f"Error opening file: {file_path}, {e}")
            return None, 0  # Return None if there's any error
    
    def downloadSysDevice(self,ch_num,dwnld_mode,filename,file_path):
        file_data,file_size = self.osFileOpen(file_path)
        filename = ctypes.c_char_p(filename.encode('utf-8'))
        pvUser = ctypes.c_void_p()
        err = self.dll.xSysdeviceDownload(self.device,ch_num,dwnld_mode,
                                           filename,file_data,file_size,progressCallback,recvPktCallback,pvUser) 
        if (err != CIFX_NO_ERROR):
            print("Error with progress callback downloading:", err)
        return err
        
    def downloadFirmwareSysDevice(self,board_number,file_path):
        err = self.openSysDevice(board_number)
        if (err != CIFX_NO_ERROR):
            print("Error device not open:", hex(err))
        filename = "firmware.nxf"
        err = self.downloadSysDevice(0,DOWNLOAD_MODE_FIRMWARE,filename,file_path)
        self.closeSysDevice()
        return err

    def resetSysDevice(self,board_number):
        err = self.openSysDevice(board_number)
        if (err != CIFX_NO_ERROR):
            print("Error device not open:", hex(err))
        err = self.dll.xSysdeviceReset(self.device,3000)
        time.sleep(3)
        self.closeSysDevice()
        return err
    
    def openChannel(self,board_number,ch_num):
        channel = CIFXHANDLE()
        name = ctypes.c_char_p(self.board_name[board_number].encode('utf-8'))
        error_code = self.dll.xChannelOpen(self.driver,name,ctypes.c_uint32(ch_num),ctypes.byref(channel))
        return channel,error_code
    
    def closeChannel(self,channel):
        return self.dll.xChannelClose(channel)

    def findFirstFileChannel(self,channel):
        directory = CIFX_DIRECTORYENTRY()
        error_code = self.dll.xChannelFindFirstFile(channel,ctypes.byref(directory),None,None)
        return directory, error_code
    
    def findNextFileChannel(self,channel,directory):
        error_code = self.dll.xChannelFindNextFile(channel,ctypes.byref(directory),None,None)
        return directory, error_code
    
    def downloadChannel(self,channel,dwnld_mode,filename,file_path):
        file_data,file_size = self.osFileOpen(file_path)
        filename = ctypes.c_char_p(filename.encode('utf-8'))
        pvUser = ctypes.c_void_p()
        err = self.dll.xChannelDownload(channel,dwnld_mode,filename,file_data,file_size,
                                         progressCallback,recvPktCallback,pvUser)
        if (err != CIFX_NO_ERROR):
                print("Error with progress callback downloading:", hex(err))
        return err
    
    def downloadFirmwareChannel(self,board_number,file_path):
        channel, err = self.openChannel(board_number,0)
        self.unlockConfigChannel(channel)
        filename="firmware.nxf"
        err = self.downloadChannel(channel,DOWNLOAD_MODE_FIRMWARE,filename,file_path)
        self.lockConfigChannel(channel)
        return err
    
    def downloadConfigurationChannel(self,board_number,file_path):
        channel, err = self.openChannel(board_number,0)
        self.unlockConfigChannel(channel)
        filename="config.nxd"
        err = self.downloadChannel(channel,DOWNLOAD_MODE_CONFIG,filename,file_path)
        self.lockConfigChannel(channel)
        return err

    def getMBXStateChannel(self,channel):
        recv_count = ctypes.c_uint32(0)
        sent_count = ctypes.c_uint32(0)
        error_code = self.dll.xChannelGetMBXState(channel,
                                                  ctypes.byref(recv_count),
                                                  ctypes.byref(sent_count))
        return recv_count,sent_count,error_code
    
    def putPacketChannel(self,channel,packet,timeout):
        return self.dll.xChannelPutPacket(channel,ctypes.byref(packet),timeout)
    
    def getPacketChannel(self,channel,timeout):
        rcv_packet = CIFX_PACKET()
        error_code = self.dll.xChannelGetPacket(channel,
                                                ctypes.sizeof(rcv_packet),
                                                ctypes.byref(rcv_packet),timeout)
        return rcv_packet, error_code
    
    def getSendPacketChannel(self,channel):
        packet = CIFX_PACKET()
        error_code = self.dll.xChannelGetSendPacket(channel,
                                                    ctypes.sizeof(packet),
                                                    ctypes.byref(packet))
        return packet, error_code
    
    def configLockChannel(self,channel,cmd,timeout):
        state = ctypes.c_uint32(0)
        error_code = self.dll.xChannelConfigLock(channel,cmd,ctypes.byref(state),timeout)
        return state, error_code
    
    def getLockStateChannel(self,channel):
        return self.configLockChannel(channel,CIFX_CONFIGURATION_GETLOCKSTATE,
                                      ctypes.c_uint32(0))
    
    def unlockConfigChannel(self,channel):
        return self.configLockChannel(channel,CIFX_CONFIGURATION_UNLOCK,
                                      ctypes.c_uint32(100))
    
    def lockConfigChannel(self,channel):
        return self.configLockChannel(channel,CIFX_CONFIGURATION_LOCK,
                                      ctypes.c_uint32(100))
    
    def resetChannel(self,channel,reset_mode,timeout):
        return self.dll.xChannelReset(channel,reset_mode,timeout)
    
    def infoChannel(self,channel):
        info = CHANNEL_INFORMATION()
        error_code = self.dll.xChannelInfo(channel,
                                           ctypes.sizeof(info),
                                           ctypes.byref(info))
        return info, error_code
    
    def watchdogChannel(self,channel,cmd):
        old_trigger = ctypes.c_uint32(0)
        error_code = self.dll.xChannelWatchdog(channel,cmd,ctypes.byref(old_trigger))
        return old_trigger, error_code

    def startWatchdogChannel(self,channel):
        return self.watchdogChannel(channel,CIFX_WATCHDOG_START)
    
    def stopWatchdogChannel(self,channel):
        return self.watchdogChannel(channel,CIFX_WATCHDOG_STOP)
    
    def hostStateChannel(self,channel,cmd,timeout):
        state = ctypes.c_uint32(0)
        error_code = self.dll.xChannelHostState(channel,cmd,ctypes.byref(state),timeout)
        return state, error_code
    
    def getHostStateChannel(self,channel):
        return self.hostStateChannel(channel,CIFX_HOST_STATE_READ,ctypes.c_uint32(0))
    
    def clearHostStateChannel(self,channel):
        return self.hostStateChannel(channel,CIFX_HOST_STATE_NOT_READY,ctypes.c_uint32(HOSTSTATE_TIMEOUT))
    
    def setHostStateChannel(self,channel):
        return self.hostStateChannel(channel,CIFX_HOST_STATE_READY,ctypes.c_uint32(HOSTSTATE_TIMEOUT))
    
    def busStateChannel(self,channel,cmd,timeout):
        state = ctypes.c_uint32(0)
        error_code = self.dll.xChannelBusState(channel,cmd,ctypes.byref(state),timeout)
        return state, error_code
    
    def getBusStateChannel(self,channel):
        return self.busStateChannel(channel,CIFX_BUS_STATE_GETSTATE,ctypes.c_uint32(1000))
    
    def onBusStateChannel(self,channel):
        return self.busStateChannel(channel,CIFX_BUS_STATE_ON,ctypes.c_uint32(0))
    
    def offBusStateChannel(self,channel):
        return self.busStateChannel(channel,CIFX_BUS_STATE_OFF,ctypes.c_uint32(0))
    
    def dmaStateChannel(self,channel,cmd):
        state = ctypes.c_uint32(0)
        error_code = self.dll.xChannelDMAState(channel,cmd,ctypes.byref(state))
        return state, error_code

    def getDMAStateChannel(self,channel):
        return self.dmaStateChannel(channel,CIFX_DMA_STATE_GETSTATE)
    
    def onDMAStateChannel(self,channel):
        return self.dmaStateChannel(channel,CIFX_DMA_STATE_ON)
    
    def offDMAStateChannel(self,channel):
        return self.dmaStateChannel(channel,CIFX_DMA_STATE_OFF)
    
    def infoIOChannel(self,channel,cmd,area):
        info = CHANNEL_IO_INFORMATION()
        error_code = self.dll.xChannelIOInfo(channel,cmd,area,
                                             ctypes.sizeof(info),
                                             ctypes.byref(info))
        return info,error_code
    
    def readIOChannel(self,channel,area,offset,size):
        data = (ctypes.c_uint8*size)()
        size = ctypes.sizeof(data)
        error_code = self.dll.xChannelIORead(channel,area,offset,size,data,ctypes.c_uint32(IO_WAIT_TIMEOUT))
        return data, error_code
    
    def writeIOChannel(self,channel,area,offset,data,size):
        write_data = (ctypes.c_uint8*size)()
        for i in range(size):
            write_data[i] = data[i]
        error_code = self.dll.xChannelIOWrite(channel,area,offset,size,write_data,ctypes.c_uint32(IO_WAIT_TIMEOUT))
        return error_code

    def readSendDataIOChannel(self,channel,area,size,offset):
        data = (ctypes.c_uint8*size)()
        error_code = self.dll.xChannelIOReadSendData(channel,area,offset,size,data)
        return data, error_code

    def controlBlockChannel(self,channel,cmd,offset,size,data):
        uint8_t_data = (ctypes.c_uint8*size)(*data)
        error_code = self.dll.xChannelControlBlock(channel,cmd,offset,size,uint8_t_data)
        return uint8_t_data, error_code

    def readControlBlockChannel(self,channel,offset,size):
        data = ctypes.c_uint8*size
        return self.controlBlockChannel(channel,CIFX_CMD_READ_DATA,offset,
                                        size,data) 
    
    def writeControlBlockChannel(self,channel,offset,size,data):
        return self.controlBlockChannel(channel,CIFX_CMD_WRITE_DATA,offset,
                                        size, data)
    
    def commonStatusBlockChannel(self,channel,cmd,offset,size,data):
        uint8_t_data = (ctypes.c_uint8*size)(*data)
        error_code = self.dll.xChannelCommonStatusBlock(channel,cmd,offset,size,uint8_t_data)
        return uint8_t_data, error_code
    
    def readCommonStatusBlockChannel(self,channel,offset,size):
        data = ctypes.c_uint8*size
        return self.controlBlockChannel(channel,CIFX_CMD_READ_DATA,offset,
                                        size,data) 
    
    def writeCommonStatusBlockChannel(self,channel,offset,size,data):
        return self.controlBlockChannel(channel,CIFX_CMD_WRITE_DATA,offset,
                                        size, data)
    
    def extendedCommonStatusBlockChannel(self,channel,cmd,offset,size,data):
        uint8_t_data = (ctypes.c_uint8*size)(*data)
        error_code = self.dll.xChannelExtendedStatusBlock(channel,cmd,offset,size,uint8_t_data)
        return uint8_t_data, error_code
    
    def readExtendedCommonStatusBlockChannel(self,channel,offset,size):
        data = ctypes.c_uint8*size
        return self.extendedCommonStatusBlockChannel(channel,CIFX_CMD_READ_DATA,offset,
                                        size,data) 
    
    def writeExtenedCommonStatusBlockChannel(self,channel,offset,size,data):
        return self.extendedCommonStatusBlockChannel(channel,CIFX_CMD_WRITE_DATA,offset,
                                        size, data)
    
    def userBlockChannel(self,channel,cmd,area,offset,size,data):
        uint8_t_data = (ctypes.c_uint8*size)(*data)
        error_code = self.dll.xChannelUserBlock(channel,area,cmd,offset,size,uint8_t_data)
        return uint8_t_data, error_code
    
    def readUserBlockChannel(self,channel,area,offset,size):
        data = ctypes.c_uint8*size
        return self.useBlockChannel(channel,CIFX_CMD_READ_DATA,area,offset,
                                        size,data) 
    
    def writeUserBlockChannel(self,channel,area,offset,size,data):
        return self.useBlockChannel(channel,CIFX_CMD_WRITE_DATA,area,offset,
                                        size, data)
    
    def plcMemoryPtrChannel(self,channel,cmd):
        memory = PLC_MEMORY_INFORMATION()
        error_code = self.dll.xChannelPLCMemoryPtr(channel,cmd,ctypes.byref(memory))
        return memory, error_code
    
    def plcIsReadReadyChannel(self,channel,area):
        state = ctypes.c_uint32(0)
        error_code = self.dll.xChannelPLCIsReadReady(channel,area,ctypes.byref(state))
        return state, error_code
    
    def plcIsWriteReadyChannel(self,channel,area):
        state = ctypes.c_uint32(0)
        error_code = self.dll.xChannelPLCIsWriteReady(channel,area,ctypes.byref(state))
        return state, error_code
    
    def plcActivateReadChannel(self,channel,area):
        return self.dll.xChannelPLCActivateRead(channel,area)
    
    def plcActivateWriteChannel(self,channel,area):
        return self.dll.xChannelPLCActivateWrite(channel,area)
    
    def syncStateChannel(self,channel,cmd,timeout):
        counter = ctypes.c_uint32(0)
        error_code = self.dll.xChannelSyncState(channel,cmd,timeout,ctypes.byref(counter))
        return counter, error_code