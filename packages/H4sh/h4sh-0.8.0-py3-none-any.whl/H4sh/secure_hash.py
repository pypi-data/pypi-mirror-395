import ctypes
import os
from pathlib import Path
import importlib.resources as pkg_resources
import H4sh  # your package

class SecureHash:
    def __init__(self, mode="KeyHash", balance_target=5):
        self.mode_map = {"QuickHash": 0, "KeyHash": 1, "ProofHash": 2, "GpuHash": 3}
        self.mode = self.mode_map.get(mode, 1)
        self.balance_target = max(1, min(balance_target, 50))

        # ---------------- Load CPU DLL ----------------
        cpu_dll_name = 'secure_hash.dll' if os.name == 'nt' else 'secure_hash.so'
        try:
            with pkg_resources.path(H4sh, f'lib/{cpu_dll_name}') as dll_path:
                if not dll_path.exists():
                    raise FileNotFoundError(f"CPU DLL not found: {cpu_dll_name}")
                self.cpu_lib = ctypes.CDLL(str(dll_path))
        except FileNotFoundError:
            raise FileNotFoundError(f"CPU DLL not found in package: {cpu_dll_name}")

        # CPU function argtypes
        self.cpu_lib.secure_hash.argtypes = [
            ctypes.c_uint8, ctypes.c_uint8,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8)
        ]
        self.cpu_lib.secure_hash.restype = None

        self.cpu_lib.secure_hash_key.argtypes = [
            ctypes.c_uint8, ctypes.c_uint8,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8)
        ]
        self.cpu_lib.secure_hash_key.restype = None

        self.cpu_lib.secure_adjust_balance.argtypes = [
            ctypes.c_uint8, ctypes.c_uint8, ctypes.c_float, ctypes.POINTER(ctypes.c_uint8)
        ]
        self.cpu_lib.secure_adjust_balance.restype = None

        # ---------------- Load GPU DLL ----------------
        gpu_dll_name = 'gpu_hash.dll' if os.name == 'nt' else 'gpu_hash.so'
        try:
            with pkg_resources.path(H4sh, f'lib/{gpu_dll_name}') as dll_path:
                if not dll_path.exists():
                    raise FileNotFoundError(f"GPU DLL not found: {gpu_dll_name}")
                self.gpu_lib = ctypes.CDLL(str(dll_path))
        except FileNotFoundError:
            raise FileNotFoundError(f"GPU DLL not found in package: {gpu_dll_name}")

        # GPU function argtypes
        self.gpu_lib.secure_hash_gpu.argtypes = [
          ctypes.POINTER(ctypes.c_uint8),   # inputs (flattened)
          ctypes.c_int,                     # input_len
          ctypes.POINTER(ctypes.c_uint64),  # nonces
          ctypes.POINTER(ctypes.c_uint8),   # outputs (flattened)
          ctypes.c_int                      # batch_size
        ]
        self.gpu_lib.secure_hash_gpu.restype = None

    # ---------------- Hash function ----------------
    def hash(self, data, salt=None, nonce=0):
        data_bytes = bytes(data)

        # GPU mode: always batch, even for single call
        if self.mode == 3:
            batch_result = self.hash_gpu_batch([data_bytes], [nonce])
            return batch_result[0]

        # CPU fallback
        output = (ctypes.c_uint8 * 32)()
        data_array = (ctypes.c_uint8 * len(data_bytes))(*data_bytes)

        salt_bytes = bytes(salt) if salt else b""
        salt_array = (ctypes.c_uint8 * len(salt_bytes))(*salt_bytes) if salt_bytes else (ctypes.c_uint8 * 1)()

        self.cpu_lib.secure_hash(
            ctypes.c_uint8(self.mode),
            ctypes.c_uint8(self.balance_target),
            data_array,
            ctypes.c_uint32(len(data_bytes)),
            salt_array,
            ctypes.c_uint32(len(salt_bytes)),
            output
        )
        return bytes(output)

    def hash_gpu_batch(self, data_list, nonces=None):
        batch_size = len(data_list)
        input_len = len(data_list[0])

        # Flatten input data
        flat_inputs = b"".join(data_list)
        inputs_array = (ctypes.c_uint8 * len(flat_inputs))(*flat_inputs)

        # Nonces
        if nonces is None:
            nonces = [0] * batch_size
        nonces_array = (ctypes.c_uint64 * batch_size)(*nonces)

        # Output buffer
        outputs_array = (ctypes.c_uint8 * (32 * batch_size))()

        # Call batch GPU function
        self.gpu_lib.secure_hash_gpu(
            inputs_array,
            ctypes.c_int(input_len),
            nonces_array,
            outputs_array,
            ctypes.c_int(batch_size)
        )

        # Split output
        return [bytes(outputs_array[i*32:(i+1)*32]) for i in range(batch_size)]



    # ---------------- Hash key function ----------------
    def hash_key(self, key, salt=None):
        key_bytes = key.encode('utf-8') if isinstance(key, str) else bytes(key)
        salt_bytes = bytes(salt) if salt else b""
        key_array = (ctypes.c_uint8 * len(key_bytes))(*key_bytes)
        salt_array = (ctypes.c_uint8 * len(salt_bytes))(*salt_bytes) if salt_bytes else (ctypes.c_uint8 * 1)()
        output = (ctypes.c_uint8 * 32)()
        output_salt = (ctypes.c_uint8 * 16)()
        self.cpu_lib.secure_hash_key(
            ctypes.c_uint8(self.mode),
            ctypes.c_uint8(self.balance_target),
            key_array, ctypes.c_uint32(len(key_bytes)),
            salt_array, ctypes.c_uint32(len(salt_bytes)),
            output, ctypes.byref(output_salt)
        )
        return bytes(output), bytes(output_salt[:16] if salt else output_salt)

    # ---------------- Adjust balance ----------------
    def adjust_balance(self, target_time):
        output_balance = ctypes.c_uint8()
        self.cpu_lib.secure_adjust_balance(
            ctypes.c_uint8(self.mode),
            ctypes.c_uint8(self.balance_target),
            ctypes.c_float(target_time),
            ctypes.byref(output_balance)
        )
        self.balance_target = output_balance.value
        return self.balance_target
