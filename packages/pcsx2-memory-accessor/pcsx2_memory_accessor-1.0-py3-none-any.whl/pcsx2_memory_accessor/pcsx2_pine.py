"""
Provides convenient access to PCSX2 memory via the Pine IPC protocol.
"""
import ctypes
import os
import platform
import struct
from typing import Optional
from importlib import resources

libipc = None
ipc_handle = None

PCSX2Ipc = ctypes.c_void_p
uint32_t = ctypes.c_uint32
uint64_t = ctypes.c_uint64
bool_t = ctypes.c_bool
size_t = ctypes.c_uint32

MSG_READ_8 = 0
MSG_READ_16 = 1
MSG_READ_32 = 2
MSG_READ_64 = 3
MSG_WRITE_8 = 4
MSG_WRITE_16 = 5
MSG_WRITE_32 = 6
MSG_WRITE_64 = 7


def _define_signatures():
    if libipc is None:
        return

    # Core functions
    libipc.pcsx2ipc_new.argtypes = []
    libipc.pcsx2ipc_new.restype = PCSX2Ipc

    libipc.pcsx2ipc_delete.argtypes = [PCSX2Ipc]
    libipc.pcsx2ipc_delete.restype = None

    libipc.pcsx2ipc_get_error.argtypes = [PCSX2Ipc]
    libipc.pcsx2ipc_get_error.restype = ctypes.c_int

    # Single value operations
    libipc.pcsx2ipc_read.argtypes = [PCSX2Ipc, uint32_t, ctypes.c_int, bool_t]
    libipc.pcsx2ipc_read.restype = uint64_t

    libipc.pcsx2ipc_write.argtypes = [PCSX2Ipc, uint32_t, uint64_t, ctypes.c_int, bool_t]
    libipc.pcsx2ipc_write.restype = None

    # Bulk operations
    libipc.pcsx2ipc_read_buffer.argtypes = [PCSX2Ipc, uint32_t, ctypes.POINTER(ctypes.c_char), size_t]
    libipc.pcsx2ipc_read_buffer.restype = bool_t

    libipc.pcsx2ipc_write_buffer.argtypes = [PCSX2Ipc, uint32_t, ctypes.POINTER(ctypes.c_char), size_t]
    libipc.pcsx2ipc_write_buffer.restype = None


def init() -> bool:
    """
    Initialize the PCSX2 IPC connection
    """
    global libipc, ipc_handle
    
    if ipc_handle is not None:
        print("Warning: PCSX2 IPC already initialized.")
        return True

    # Determine library extension based on OS
    cur_os = platform.system()
    if cur_os == "Windows":
        lib_ext = ".dll"
    elif cur_os == "Linux": # Linux .so not included
        lib_ext = ".so"

    dll_resource = resources.files('pcsx2_memory_accessor').joinpath(f'dll/libpcsx2_ipc_bulk_c{lib_ext}')
    
    lib_path_str = ""
    
    try:
        with resources.as_file(dll_resource) as lib_path:
            lib_path_str = str(lib_path)
            #print(f"Attempting to load library from: {lib_path_str}")
            
            libipc = ctypes.CDLL(lib_path_str)
            
            _define_signatures()
            ipc_handle = libipc.pcsx2ipc_new()

        # Check for initialization errors
        error = get_last_error()
        if error != 0:
            print(f"Error during IPC initialization: Error code {error}")
            shutdown()
            return False
            
        print("PCSX2 IPC initialized successfully.")
        return True
        
    except OSError as e:
        print(f"ERROR: Could not load library '{lib_path_str}'")
        print(f"Details: {e}")
        return False


def shutdown():
    global ipc_handle, libipc
    
    if ipc_handle is not None and libipc is not None:
        libipc.pcsx2ipc_delete(ipc_handle)
        ipc_handle = None
        libipc = None
        print("PCSX2 IPC shut down.")


def get_last_error() -> int:
    if ipc_handle is None or libipc is None:
        return -1
    
    return libipc.pcsx2ipc_get_error(ipc_handle)


# ============================================================================
# Single Value Operations (Returns python integers)
# ============================================================================
def read_u8(address: int) -> int:
    """
    Read an 8-bit unsigned integer from PS2 memory.
    
    Args:
        address: PS2 memory address
        
    Returns:
        Value read (0-255)
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return 0
    
    value = libipc.pcsx2ipc_read(ipc_handle, uint32_t(address), MSG_READ_8, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error reading u8 at {hex(address)}: Error code {error}")
    
    return value & 0xFF


def read_u16(address: int) -> int:
    """
    Read a 16-bit unsigned integer from PS2 memory.
    
    Args:
        address: PS2 memory address
        
    Returns:
        Value read (0-65535)
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return 0
    
    value = libipc.pcsx2ipc_read(ipc_handle, uint32_t(address), MSG_READ_16, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error reading u16 at {hex(address)}: Error code {error}")
    
    return value & 0xFFFF


def read_u32(address: int) -> int:
    """
    Read a 32-bit unsigned integer from PS2 memory.
    
    Args:
        address: PS2 memory address
        
    Returns:
        Value read (0-4294967295)
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return 0
    
    value = libipc.pcsx2ipc_read(ipc_handle, uint32_t(address), MSG_READ_32, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error reading u32 at {hex(address)}: Error code {error}")
    
    return value & 0xFFFFFFFF


def read_u64(address: int) -> int:
    """
    Read a 64-bit unsigned integer from PS2 memory.
    
    Args:
        address: PS2 memory address
        
    Returns:
        Value read
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return 0
    
    value = libipc.pcsx2ipc_read(ipc_handle, uint32_t(address), MSG_READ_64, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error reading u64 at {hex(address)}: Error code {error}")
    
    return value


def write_u8(address: int, value: int):
    """
    Write an 8-bit unsigned integer to PS2 memory.
    
    Args:
        address: PS2 memory address
        value: Value to write (0-255)
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return
    
    libipc.pcsx2ipc_write(ipc_handle, uint32_t(address), uint64_t(value & 0xFF), MSG_WRITE_8, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error writing u8 at {hex(address)}: Error code {error}")


def write_u16(address: int, value: int):
    """
    Write a 16-bit unsigned integer to PS2 memory.
    
    Args:
        address: PS2 memory address
        value: Value to write (0-65535)
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return
    
    libipc.pcsx2ipc_write(ipc_handle, uint32_t(address), uint64_t(value & 0xFFFF), MSG_WRITE_16, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error writing u16 at {hex(address)}: Error code {error}")


def write_u32(address: int, value: int):
    """
    Write a 32-bit unsigned integer to PS2 memory.
    
    Args:
        address: PS2 memory address
        value: Value to write (0-4294967295)
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return
    
    libipc.pcsx2ipc_write(ipc_handle, uint32_t(address), uint64_t(value & 0xFFFFFFFF), MSG_WRITE_32, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error writing u32 at {hex(address)}: Error code {error}")


def write_u64(address: int, value: int):
    """
    Write a 64-bit unsigned integer to PS2 memory.
    
    Args:
        address: PS2 memory address
        value: Value to write
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return
    
    libipc.pcsx2ipc_write(ipc_handle, uint32_t(address), uint64_t(value), MSG_WRITE_64, False)
    
    error = get_last_error()
    if error != 0:
        print(f"Error writing u64 at {hex(address)}: Error code {error}")


# ============================================================================
# Multi-byte Operations (N IPC calls for N bytes)
# ============================================================================
def read_pcsx2_memory(address: int, size: int) -> Optional[bytes]:
    """
    Read a block of memory from PS2 Memory.
    
    Args:
        address: Memory Address
        size: Number of bytes to read
        
    Returns:
        bytes object containing the data, or None on failure
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return None

    if size <= 0:
        print("Error: Size must be greater than 0")
        return None
    
    read_buffer = (ctypes.c_char * size)()
    
    success = libipc.pcsx2ipc_read_buffer(
        ipc_handle,
        uint32_t(address),
        read_buffer,
        size_t(size)
    )
    
    if success:
        return bytes(read_buffer)
    else:
        error = get_last_error()
        print(f"Error reading memory at {hex(address)} (size: {size}): Error code {error}")
        return None


def write_pcsx2_memory(address: int, data: bytes) -> bool:
    """
    Write a block of bytes to PS2 Memory.
    
    Args:
        address: Memory Address
        data: bytes or bytearray to write
        
    Returns:
        True if successful, False otherwise
    """
    if ipc_handle is None or libipc is None:
        print("Error: IPC not initialized")
        return False
    
    if not isinstance(data, (bytes, bytearray)):
        print("Error: data must be bytes or bytearray")
        return False
    
    size = len(data)
    if size <= 0:
        print("Error: data cannot be empty")
        return False
    
    write_buffer = ctypes.create_string_buffer(data)
    
    libipc.pcsx2ipc_write_buffer(
        ipc_handle,
        uint32_t(address),
        write_buffer,
        size_t(size)
    )
    
    error = get_last_error()
    if error != 0:
        print(f"Error writing memory at {hex(address)} (size: {size}): Error code {error}")
        return False
    
    return True


# Aliases
read_bytes = read_pcsx2_memory
write_bytes = write_pcsx2_memory