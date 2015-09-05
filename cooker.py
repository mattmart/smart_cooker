import argparse
import time
import cooker_manager
import pdb 


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--goal-temp", help="the goal temperature that we want to reach (in celsius)", type=float, required=True)
    parser.add_argument("--skip-logging", help="use this if the postgres database is down",action='store_true')
    parser.add_argument("--cooker-name", help="the cooker name that we are currently using",type=str, required=True)
    parser.add_argument("-t","--time", help="amount of time in minutes to run for before turning cooker off, then exiting. Defaults to 60 minutes", type=int)
    parser.add_argument("-d","--description", help="the description of whatever it is we're cooking - this will show up in the graph if we're generating one", type=str, required=True)

    _myargs = parser.parse_args()

    if _myargs.time > 0:
        _time_in_seconds = _myargs.time * 60
    else:
        _time_in_seconds = 3600

    cooker = cooker_manager.CookerManager(_myargs.cooker_name,_myargs.description, not _myargs.skip_logging)

    cooker.start_async_cooking(_myargs.goal_temp,_time_in_seconds)
    
    while not cooker.is_finished_cooking():
        time.sleep(5)
        print "cooker not finished! remaining time is:" + str(cooker.get_remaining_time()) + " at temperature: " + str(cooker.get_current_temp())

if __name__ == "__main__":
    main()
