import struct
import zipfile
import io
import os
from wasmtime import Engine, Store, Module, Linker, WasiConfig

# ---------------------------------------------------------
# GamePad and GameState Python versions
# ---------------------------------------------------------

class GamePad:
    def __init__(self, button=0, stick_x=0, stick_y=0):
        self.button = button
        self.stick_x = stick_x
        self.stick_y = stick_y

    @staticmethod
    def from_bytes(b):
        button = (b[0] << 8) | b[1]
        stick_x = struct.unpack("b", b[2:3])[0]
        stick_y = struct.unpack("b", b[3:4])[0]
        return GamePad(button, stick_x, stick_y)

class GameState:
    def __init__(self, data):
        # Rust reads 60 bytes: first 24 bytes are pos/vel floats
        b_data = bytes(data)
        floats = [struct.unpack("f", b_data[i:i+4])[0] for i in range(0, 24, 4)]
        self.pos = floats[0:3]
        self.vel = floats[3:6]

# ---------------------------------------------------------
# Utility: unzip and XOR like Rust
# ---------------------------------------------------------

def unzip_bytes(zipped_bytes):
    with zipfile.ZipFile(io.BytesIO(zipped_bytes), 'r') as z:
        return z.read(z.namelist()[0])

import hashlib

ROM_HASH = "9bef1128717f958171a4afac3ed78ee2bb4e86ce"
def check_hash(data: bytes) -> bool:
    sha1 = hashlib.sha1()
    sha1.update(data)
    hash_result = sha1.hexdigest()
    return hash_result == ROM_HASH

# ---------------------------------------------------------
# RngConfig class matching Rust
# ---------------------------------------------------------

class RngConfig:
    def __init__(self, window_length, random_amount, random_burst_length,
                 a_prob, b_prob, z_prob):
        self.window_length = window_length
        self.random_amount = random_amount
        self.random_burst_length = random_burst_length
        self.a_prob = a_prob
        self.b_prob = b_prob
        self.z_prob = z_prob

# ---------------------------------------------------------
# SM64GameGenerator (Python match of Rust version)
# ---------------------------------------------------------

class SM64GameGenerator:
    def __init__(self, wasm_bytes):
        self.wasm_bytes = wasm_bytes

    @staticmethod
    def new(rom_bytes):
        if not check_hash(rom_bytes):
            raise ValueError("Invalid ROM. Should be US z64 (8MB).")

        wasm_bytes = SM64GameGenerator.rom_to_wasm_bytes(rom_bytes)
        return SM64GameGenerator(wasm_bytes)

    @staticmethod
    def from_file(path):
        with open(path, "rb") as f:
            return SM64GameGenerator.new(f.read())

    @staticmethod
    def rom_to_wasm_bytes(rom_bytes):
        rom_len = len(rom_bytes)

        # load XOR bytes exactly like Rust include_bytes!

        base_dir = os.path.dirname(__file__)
        xor_path = os.path.join(base_dir, "..", "..", "pkg", "sm64_headless.us.wasm.zip.xor")

        with open(xor_path, "rb") as f:
            xor_bytes = f.read()

        wasm_zip_bytes = bytes([xor_bytes[i] ^ rom_bytes[i % rom_len]
                                for i in range(len(xor_bytes))])

        return unzip_bytes(wasm_zip_bytes)

    def create_game(self):
        return SM64Game(self.wasm_bytes)

# ---------------------------------------------------------
# SM64Game (Python match of Rust version)
# ---------------------------------------------------------

class SM64Game:
    def __init__(self, wasm_bytes):
        self.engine = Engine()
        self.module = Module(self.engine, wasm_bytes)

        self.store = Store(self.engine)
        self.linker = Linker(self.engine)
        self.linker.define_wasi()

        wasi = WasiConfig()
        wasi.inherit_stdout()
        self.store.set_wasi(wasi)

        self.instance = self.linker.instantiate(self.store, self.module)

        self.using_rng_flag = False

        # call main_func like Rust does
        self.instance.exports(self.store)["main_func"](self.store)

        self.memory = self.instance.exports(self.store)["memory"]

    # -----------------------------------------------------
    # RNG functions
    # -----------------------------------------------------

    def set_rng_config(self, cfg: RngConfig):
        self.using_rng_flag = True
        func = self.instance.exports(self.store)["set_rng_config"]
        func(self.store,
            cfg.window_length,
            cfg.random_amount,
            cfg.random_burst_length,
            cfg.a_prob,
            cfg.b_prob,
            cfg.z_prob
        )

    def set_rng_seed(self, seed):
        self.using_rng_flag = True
        func = self.instance.exports(self.store)["set_rng_seed"]
        func(self.store, seed)

    # -----------------------------------------------------
    # Game stepping + state
    # -----------------------------------------------------

    def step_game(self, pad: GamePad):
        func = self.instance.exports(self.store)["step_game"]
        func(self.store, pad.button, pad.stick_x, pad.stick_y)

    def get_game_state(self):
        func = self.instance.exports(self.store)["get_game_state"]
        ptr = func(self.store)

        raw = self.memory.data_ptr(self.store)[ptr:ptr+60]
        return GameState(raw)

    def rng_pad(self, pad: GamePad):
        func = self.instance.exports(self.store)["rng_pad"]
        ptr = func(self.store, pad.button, pad.stick_x, pad.stick_y)

        raw = self.memory.data_ptr(self.store)[ptr:ptr+4]
        return GamePad.from_bytes(raw)

    def using_rng(self):
        return self.using_rng_flag
