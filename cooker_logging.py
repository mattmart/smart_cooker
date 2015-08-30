import logging
import psycopg2
import uuid
import logging.handlers

from cooker_plotting import CookerPlotter

def getLogger(name, probe_id, enable_logging):
    return CookingLogger(name, probe_id, enable_logging)

#maybe should be composition, but w/e
class CookingLogger (logging.Logger):
    def __init__(self, name, probe_id, enable_logging):    
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._enable_logging = enable_logging
        if enable_logging:
            cooker_handler = CookerDBHandler(probe_id)
            self._db_handler = cooker_handler
            cooker_handler.setLevel(logging.INFO)
            self._logger.addHandler(cooker_handler)
    
    def debug(self, msg, extra = {}):
        self._logger.debug(msg, extra)

    def info(self, msg, extra = {}):
        self._logger.info(msg, extra)
    
    def finish_logging(self):
        if self._enable_logging:
            plotter = CookerPlotter()
            print plotter.upload_to_plotly(self._db_handler._uuid)


class CookerDBHandler(logging.Handler):
    def __init__(self, name):
        logging.Handler.__init__(self)
        self._uuid = str(uuid.uuid4())
        self._conn=psycopg2.connect("dbname=cooker user=cooker")
        self._curr = self._conn.cursor()
        self._curr.execute("select sc_id from t_slowcookers where cooker_name = '%s'" % name)
        self._probe_id = self._curr.fetchone()
    
    def emit(self, record):
        curr_temp = record.args.get('curr_temp')
        goal_temp = record.args.get('goal_temp')
        self._curr.execute("insert into t_sc_timing (sc_id, curr_temp, target_temp, uuid) values (%s, %s, %s, %s)",(self._probe_id,curr_temp,goal_temp, self._uuid))
        self._conn.commit()