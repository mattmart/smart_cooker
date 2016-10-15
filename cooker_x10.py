from subprocess import call

class CookerX10:
    def __init__(self):
        self._test = "TTY /dev/ttyUSB0"
        self._address = "a1"
        self._heyu_bin = "heyu"
    
    def turn_off(self):
        call([self._heyu_bin,"fon",self._address])

    def turn_on(self):
        call([self._heyu_bin,"foff",self._address])

