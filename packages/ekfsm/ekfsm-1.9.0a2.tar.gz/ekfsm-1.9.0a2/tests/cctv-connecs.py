import threading
import pprint
import logging

# from time import sleep
from pathlib import Path
from ekfsm.system import System


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Initialize system first (without profiling the setup)
config = Path(__file__).parent / "cctv.yaml"
system = System(config, abort=True)

pprint.pprint(f"System slots {system.slots}")

system.print()

cpu = system["CPU"]
cpuB = system.cpu
cpuC = system[0]

assert cpu == cpuB == cpuC

# To check why below is failing
# cpu_slot = system.slots["SYSTEM_SLOT"]
# cpu_slotB = system.slots.SYSTEM_SLOT
# cpu_slotC = system.slots[0]

# assert cpu_slot == cpu_slotB == cpu_slotC

cpu.print()
print(f"probing CPU: {cpu.probe()}")
print(
    f"inventory: {cpu.inventory.vendor()} {cpu.inventory.model()} {cpu.inventory.serial()}"
)

smc = system.smc

smc.print()

# Test 4 connection in parallels to io4edge
i4e = smc.i4e

# Test watchdog client connection
i4e.watchdog.client.open()

# open led client connection
i4e.leds.client.open()

# open power and redriver client connections
pw_toggle = i4e.gpios.power
redriver_toggle = i4e.gpios.redriver

i4e.gpios.client.open()

# open button client connection
button_array = i4e.gpios.buttons

eject = button_array.eject

eject.handler = lambda: print("Eject pressed")

stop_event = threading.Event()
button_thread = threading.Thread(target=button_array.read, args=(stop_event,))


# operate
button_thread.start()

for i in range(5):
    print("Main thread running...")
    i4e.watchdog.kick()

    # Test LED operations
    i4e.leds.led2.set(0, True)
    led2 = i4e.leds.led2.get()
    assert led2 == (0, True)
    i4e.leds.led5.set(3, True)
    led5 = i4e.leds.led5.get()
    assert led5 == (3, True)
    i4e.leds.led3.set(5, False)
    led3 = i4e.leds.led3.get()
    assert led3 == (5, False)

    pw_toggle.on()
    # sleep(0.5)
    pw_toggle.off()
    # sleep(0.5)
    redriver_toggle.on()
    # sleep(0.5)
    redriver_toggle.off()
    # sleep(0.5)

i4e.leds.client.close()
i4e.gpios.client.close()
i4e.watchdog.client.close()

# To stop the thread:
stop_event.set()
button_thread.join()
