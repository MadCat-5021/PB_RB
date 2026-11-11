class CoilManager:

    def pulse(
        self,
        coil_name,
        duration_ms):
        print(f"COIL PULSE: "f"{coil_name} "f"({duration_ms}ms)")

    def enable(
        self,
        coil_name):
        print(f"COIL ENABLE: "f"{coil_name}")

    def disable(
        self,
        coil_name):
        print(f"COIL DISABLE: "f"{coil_name}")