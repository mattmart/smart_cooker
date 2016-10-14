from rpi_strogonanoff import strogonanoff_sender
from rpi_strogonanoff import WiringPin as WPin

class CookerStrogonanoff:
    def __init__(self):
        pin=WPin.WiringPin(0).export()

    def turn_off(self):
        strogonanoff_sender.send_command(pin,1,1,False)
    

    def turn_on(self):
        strogonanoff_sender.send_command(pin,1,1,True)

