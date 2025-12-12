from atlib import SIM7600GH, Status
import time

gsm = SIM7600GH("/dev/ttyUSB2", baudrate=115200)

version = gsm.get_version()
bands = gsm.get_allowed_bands()
band = gsm.get_active_band()

quality = gsm.get_signal_quality()
contexts = gsm.get_contexts()
addresses = gsm.get_addresses()

operator = gsm.get_current_operator()
sim_status = gsm.get_sim_status()

gsm.enable_location_reporting()
location = gsm.get_cell_location()

print(version)
print(bands)
print(band)

print(quality)
print(contexts)
print(addresses)

print(operator)
print(sim_status)
print(location)
