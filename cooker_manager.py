import threading
import time
import os
import signal

from rpi_strogonanoff import strogonanoff_sender
from rpi_strogonanoff import WiringPin as WPin
import cooker_thermometer as therm
import cooker_logging

class CookerManager:
    
    def __init__(self, name, gtemp, gtime, enable_logging = True):
        '''
        initializes cooker manager - can be instantiated multiple times
        with the same cooker name(id), should probably be locked somehow
        '''
        self._cooker_name = name
        self._goal_temp = gtemp
        self._remaining_time = gtime
        self._enable_logging = enable_logging
        self._started_cooking = False
        self._finished_cooking = False
        self._probe_id = "28-00000545b919"

    def _is_finished_controlling(self):
        '''
        cheap method to check if we're done yet
        '''
        if not self._started_cooking:
            raise ValueError('have not started cooking yet!')
        return self._remaining_time <= 0

    def is_finished_cooking(self):
        '''
        cheap method to check if we're done yet
        '''
        return self._finished_cooking

    def get_current_temp(self):
        '''
        fetches the current temperature associated with this
        cooker - uses the probe id
        '''
        return therm.read_temp(self._probe_id)
    
    def _set_cooker_state(self):
        '''
        one time only tries to read the temperature from the probe
        and weigh it against the goal temperature, then turn off or 
        on the cooker. hardcoded button, gpio, and channel vals
        '''
        pin=WPin.WiringPin(0).export()

        curr_temp = self.get_current_temp()
        extra = { 'curr_temp': curr_temp, 'goal_temp' : self._goal_temp }

        if self._goal_temp >= curr_temp:
            #wtf
            for i in range(1, 6):
                strogonanoff_sender.send_command(pin,1,1,True)
            self._logger.info("turning on slow cooker", extra)
        else:
            #wtf
            for i in range(1, 6):
                strogonanoff_sender.send_command(pin,1,1,False)
            self._logger.info("turning off slow cooker", extra)
    
    def _start_logging(self):
        '''
        sets up database logging for this cooker. if logging is not enabled, noop
        '''
        self._logger = cooker_logging.getLogger(__name__,self._cooker_name, self._enable_logging)
    
    def _finish_logging(self):
        '''
        '''
        self._logger.finish_logging()
    
    def _turn_off_perm(self):
        '''
        meant to be used  to turn off the cooker permanently
        '''
        #turn the cooker off
        self._goal_temp = 0.1
        for i in range(1, 5):
            self._set_cooker_state()

    def _cook(self):
        '''
        decrements the number of seconds until we're done when we said we 
        would be, then sets the state of the cooker to whatever is necessary
        '''
        self._start_logging()
        while not self._is_finished_controlling():
            time.sleep(1)
            self._remaining_time = self._remaining_time - 1
            self._set_cooker_state()
        self._turn_off_perm()
        self._finish_logging()
        self._finished_cooking = True

    def _setup_kill_signals(self):
        '''
        Sets up kill signals appropriately (sigint and sigterm)
        to allow us to clean up after ourselves and not leave the
        cooker on - that would be bad!
        '''
        def _handler_helper(cooker):
            def _handler(signum, frame):
                print "received graceful kill signal! Turning off cooker permanently..."
                cooker._turn_off_perm()
                signal.signal(signum, signal.SIG_DFL)
                os.kill(os.getpid(), signum) # Rethrow signal, this time without catching it
            return _handler

        signal.signal(signal.SIGINT, _handler_helper(self))
        signal.signal(signal.SIGTERM, _handler_helper(self))
        
    def _start_cooking_helper(self, set_daemon=False):
        '''
        the main method to start off cooking - hidden because
        it's not meant to be called by people outside this module. 
        We should start the cooking either by start_async_cooking or
        start_sync_cooking, as those methods "do the right thing"
        depending on what you want to do
        '''
        self._setup_kill_signals()

        self._started_cooking = True
        thr = threading.Thread(target=self._cook, kwargs={})
        thr.setDaemon(set_daemon)
        thr.start()
        return thr

    def start_async_cooking(self):
        '''
        meant to call the start cooking method and return
        immediately. makes sure started thread is a daemon
        '''
        thread = self._start_cooking_helper(True)
