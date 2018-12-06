import os
import subprocess
import _thread
from time import sleep


class EnergyUtils:

    PG_PATH = None
    PG_EXE = None
    PG_DURATION = None
    LOGS_NAME = "pg_logs.csv"

    PROCESSOR_ENERGY_TXT = "Cumulative Processor Energy_0 (Joules)"
    IA_ENERGY_TXT = "Cumulative IA Energy_0 (Joules)"
    DRAM_ENERGY_TXT = "Cumulative DRAM Energy_0 (Joules)"

    PROCESSOR_ENERGY, IA_ENERGY, DRAM_ENERGY = -1, -1, -1

    def __init__(self, pg_path, pg_exe, duration):
        self.PG_PATH = pg_path
        self.PG_EXE = pg_exe
        self.PG_DURATION = duration
        _thread.start_new_thread(self.set_power_consumption, ("power_thread", ))

    def generate_pg_log(self):
        command = "{0}{1} -resolution 1000 -duration {2} -file {3}".format(
            self.PG_PATH, self.PG_EXE, self.PG_DURATION, self.LOGS_NAME
        )
        pg_proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        pg_output = pg_proc.stdout.read().decode('utf-8')
        return pg_output

    def set_power_consumption(self, thread_name):
        while True:
            self.generate_pg_log()
            try:
                logs = open(self.LOGS_NAME, 'r')
                lines = logs.readlines()
                for line in lines:
                    if line.startswith(self.PROCESSOR_ENERGY_TXT):
                        self.PROCESSOR_ENERGY = float(line.split('=')[1].strip())
                    if line.startswith(self.DRAM_ENERGY_TXT):
                        self.DRAM_ENERGY = float(line.split('=')[1].strip())
                    if line.startswith(self.IA_ENERGY_TXT):
                        self.IA_ENERGY = float(line.split('=')[1].strip())
                logs.close()
            except (IOError, ValueError):
                print("Error reading power files")
            if os.path.exists(self.LOGS_NAME):
                    os.remove(self.LOGS_NAME)

    def get_power_consumption(self):
        return {
            'processor': self.PROCESSOR_ENERGY,
            'ia': self.IA_ENERGY,
            'dram': self.DRAM_ENERGY
        }
