import pykoppu as pk
from pykoppu.opu.device import OPU
from pykoppu.electrophysiology import connect
from pykoppu.oos.process import Process
from pykoppu.biocompiler.isa import OpCode
import numpy as np

def test_hello_opu():
    print("Testing OPU...")
    # 1. Instantiate OPU
    opu = OPU(capacity=100, neuron_model={})

    # 2. Connect Driver
    driver = connect("brian2", opu)
    print(f"Driver connected: {driver}")

    # 3. Create Manual Instructions
    program = [
        {"op": OpCode.ALC, "size": 100},
        {"op": OpCode.SIG, "val": 2.0},
        {"op": OpCode.RUN, "duration": 500},
        {"op": OpCode.REA}
    ]

    # 4. Execute Process
    process = Process(pid=1, code=program, hardware=driver)
    result = process.start()
    print("Execution result shape:", result.shape if result is not None else "None")

    if result is not None:
        print("Success! OPU is alive.")
        print("Mean voltage:", np.mean(result))
    else:
        print("Failed to get result.")

if __name__ == "__main__":
    test_hello_opu()
