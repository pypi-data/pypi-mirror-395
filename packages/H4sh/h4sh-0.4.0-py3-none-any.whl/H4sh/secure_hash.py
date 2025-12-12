import ctypes
import os
from pathlib import Path
import importlib.resources as pkg_resources
import H4sh  # your package

class SecureHash:
    def __init__(self, mode="KeyHash", balance_target=5):
        # Determine DLL filename
        dll_name = 'secure_hash.dll' if os.name == 'nt' else 'secure_hash.so'

        # Load DLL directly from the installed package
        try:
            with pkg_resources.path(PrismCore, f'lib/{dll_name}') as dll_path:
                if not dll_path.exists():
                    raise FileNotFoundError(f"Shared library not found in package: {dll_name}")
                lib_path = dll_path
        except FileNotFoundError:
            raise FileNotFoundError(f"Shared library not found in package: {dll_name}")

        # Load the DLL
        try:
            self.lib = ctypes.CDLL(str(lib_path))
        except OSError as e:
            raise OSError(f"Failed to load shared library {lib_path}: {e}")

        # Set argument types
        self.lib.secure_hash.argtypes = [
            ctypes.c_uint8, ctypes.c_uint8,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8)
        ]
        self.lib.secure_hash_key.argtypes = [
            ctypes.c_uint8, ctypes.c_uint8,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)
        ]
        self.lib.secure_adjust_balance.argtypes = [
            ctypes.c_uint8, ctypes.c_uint8, ctypes.c_float, ctypes.POINTER(ctypes.c_uint8)
        ]

        # Modes
        self.mode_map = {"QuickHash": 0, "KeyHash": 1, "ProofHash": 2}
        self.mode = self.mode_map.get(mode, 1)
        self.balance_target = max(1, min(balance_target, 50))



    def hash(self, data, salt=None):
        data = bytes(data)
        salt = bytes(salt) if salt is not None else b""
        output = (ctypes.c_uint8 * 32)()
        data_array = (ctypes.c_uint8 * len(data))(*data)
        salt_array = (ctypes.c_uint8 * len(salt))(*salt)
        self.lib.secure_hash(self.mode, self.balance_target, data_array, len(data), salt_array, len(salt), output)
        return bytes(output)

    def hash_key(self, key, salt=None):
        key = key.encode('utf-8') if isinstance(key, str) else bytes(key)
        salt = bytes(salt) if salt is not None else b""
        output = (ctypes.c_uint8 * 32)()
        output_salt = (ctypes.c_uint8 * 16)()
        key_array = (ctypes.c_uint8 * len(key))(*key)
        salt_array = (ctypes.c_uint8 * len(salt))(*salt)
        self.lib.secure_hash_key(self.mode, self.balance_target, key_array, len(key), salt_array, len(salt), output, output_salt)
        return bytes(output), bytes(output_salt[:16] if salt else output_salt)

    def adjust_balance(self, target_time):
        output_balance_target = ctypes.c_uint8()
        self.lib.secure_adjust_balance(self.mode, self.balance_target, ctypes.c_float(target_time), ctypes.byref(output_balance_target))
        self.balance_target = output_balance_target.value
        return self.balance_target
