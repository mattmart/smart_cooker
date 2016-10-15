import threading
import time
import os
import signal

import cooker_thermometer as therm
import cooker_logging
import cooker_state
from cooker_x10 import CookerX10

running_cookers = []   

class CookerManager:
    def __init__(self, name, description,  enable_logging = True):
        '''
        initializes cooker manager - can be instantiated multiple times
        with the same cooker name(id), should probably be locked somehow
        '''
        self._name = name
        self._enable_logging = enable_logging
        self._description = description
        self._started_cooking = False
        self._finished_cooking = False
        self._probe_id = "28-00000545b919"
        self._probe_id = "28-0000054823e9"
        self._plotly_link = ""
        use_x10 = True
        if use_x10:
            #testing for now
            self._icooker = CookerX10()
        else:
            self._icooker = CookerStrogonanoff()

    def _is_finished_controlling(self):
        '''
        cheap method to check if we're done yet
        '''
        if not self._started_cooking:
            raise ValueError('have not started cooking yet!')
        return self._cstate.get_remaining_time() <= 0

    def is_finished_cooking(self):
        '''
        cheap method to check if we're done yet
        '''
        return self._finished_cooking

    def get_description(self):
        '''
        '''
        return self._description
    
    def set_description(self, descript):
        '''
        '''
        self._description = descript
        if self._enable_logging:
            self._logger.set_description(descript)

    def get_name(self):
        '''
        '''
        return self._name

    def get_plotly_link(self):
        '''
        '''
        return self._plotly_link

    def _set_plotly_link(self, link):
        '''
        '''
        self._plotly_link = link
 
    def get_current_temp(self):
        '''
        fetches the current temperature associated with this
        cooker - uses the probe id
        '''
        return therm.read_temp(self._probe_id)
    
    def _set_slowcooker_state(self):
        '''
        one time only tries to read the temperature from the probe
        and weigh it against the goal temperature, then turn off or 
        on the cooker. hardcoded button, gpio, and channel vals
        '''

        curr_temp = self.get_current_temp()
        extra = { 'curr_temp': curr_temp, 'goal_temp' : self._cstate.get_goal_temp() }

        if self._cstate.get_goal_temp() >= curr_temp:
            #wtf
            for i in range(5):
                self._icooker.turn_on()
            self._logger.info("turning on slow cooker", extra)
        else:
            #wtf
            for i in range(5):
                self._icooker.turn_off()
            self._logger.info("turning off slow cooker", extra)
    
    def _start_logging(self):
        '''
        sets up database logging for this cooker. if logging is not enabled, noop
        '''
        self._logger = cooker_logging.getLogger(__name__,self._name, self._description, self._enable_logging)
    
    def _log(self):
        '''
        '''
        return self._logger.log()

    def _finish_logging(self):
        '''
        '''
        return self._logger.finish_logging()

    def set_goal_temp(self, gtemp):
        '''
        '''
        self._cstate.set_goal_temp(gtemp)

    def get_goal_temp(self):
        '''
        '''
        return self._cstate.get_goal_temp()
    
    
    def _turn_off_perm(self):
        '''
        meant to be used  to turn off the cooker permanently
        '''
        #turn the cooker off
        self._cstate = cooker_state.CookerState.init_from_name(self._name)
        self._cstate.set_goal_temp(0.1)
        for i in range(1, 5):
            self._set_slowcooker_state()
        running_cookers.remove(self)

    def get_remaining_time(self):
        return self._cstate.get_remaining_time()

    def set_remaining_time(self, time_in_seconds):
        return self._cstate.set_remaining_time(time_in_seconds)
    
    def _cook(self,gtemp, gtime):
        '''
        decrements the number of seconds until we're done when we said we 
        would be, then sets the state of the cooker to whatever is necessary
        '''
        self._start_logging()
        self._cstate = cooker_state.CookerState(self._name,gtemp,gtime)
        while not self._is_finished_controlling():
            time.sleep(1)
            if self._cstate.get_remaining_time()% 10 == 1 or self._cstate.get_remaining_time()% 10 == 0:
                self._set_plotly_link(self._log())
            self._set_slowcooker_state()
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
                self._finish_logging()
                signal.signal(signum, signal.SIG_DFL)
                os.kill(os.getpid(), signum) # Rethrow signal, this time without catching it
            return _handler

        signal.signal(signal.SIGINT, _handler_helper(self))
        signal.signal(signal.SIGTERM, _handler_helper(self))
        
    def _start_cooking_helper(self, gtemp, gtime, set_daemon=False):
        '''
        the main method to start off cooking - hidden because
        it's not meant to be called by people outside this module. 
        We should start the cooking either by start_async_cooking or
        start_sync_cooking, as those methods "do the right thing"
        depending on what you want to do
        '''
        #self._setup_kill_signals()

        self._started_cooking = True
        thr = threading.Thread(target=self._cook, args=(gtemp,gtime))
        thr.setDaemon(set_daemon)
        thr.start()
        return thr

    def start_async_cooking(self, gtime, gtemp):
        '''
        meant to call the start cooking method and return
        immediately. makes sure started thread is a daemon
        '''
        thread = self._start_cooking_helper(gtime, gtemp, True)
