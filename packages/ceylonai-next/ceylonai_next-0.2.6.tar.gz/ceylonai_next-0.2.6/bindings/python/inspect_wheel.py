import zipfile
import glob
import os

wheels = glob.glob("target/wheels/*.whl")
if not wheels:
    print("No wheels found")
else:
    wheel_path = wheels[0]
    print(f"Inspecting wheel: {wheel_path}")
    with zipfile.ZipFile(wheel_path, 'r') as z:
        for name in z.namelist():
            print(name)
