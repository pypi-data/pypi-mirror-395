import pprint
import threading
import logging
from pathlib import Path
from ekfsm.system import System


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ekfsm.log"),
        logging.StreamHandler(),  # Console output
    ],
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

i4e = smc.i4e
# i4e.watchdog.kick()
# i4e.leds.led2.set(0, True)
# led2 = i4e.leds.led2.get()
# assert led2 == (0, True)
# i4e.leds.led5.set(3, True)
# led5 = i4e.leds.led5.get()
# assert led5 == (3, True)
# i4e.leds.led3.set(5, False)
# led3 = i4e.leds.led3.get()
# assert led3 == (5, False)

button_array = i4e.gpios.buttons
pw_toggle = i4e.gpios.power
redriver_toggle = i4e.gpios.redriver

eject = button_array.eject

eject.handler = lambda: print("Eject pressed")

stop_event = threading.Event()
button_thread = threading.Thread(target=button_array.read, args=(stop_event,))
button_thread.start()

for i in range(200):
    print(f"Main thread running... {i}")
    # i4e.watchdog.kick()
    i4e.leds.led1.set(1, True)
    led1 = i4e.leds.led1.get()
    assert led1 == (1, True)
    i4e.leds.led4.set(2, True)
    led4 = i4e.leds.led4.get()
    assert led4 == (2, True)
    i4e.leds.led6.set(4, False)
    led6 = i4e.leds.led6.get()
    assert led6 == (4, False)
    pw_toggle.off()
    pw_toggle.on()
    redriver_toggle.off()
    redriver_toggle.on()

# To stop the thread:
stop_event.set()
button_thread.join()
