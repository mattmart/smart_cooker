import argparse
import time
import cooker_manager
from flask import Flask, render_template, request, abort, redirect, url_for
app = Flask(__name__)

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

def get_cooker_name_from_request():
    if not request.form.has_key('cooker_name') or request.form['cooker_name'] == "":
        raise ValueError("no cooker name given")
    else:
        return request.form['cooker_name']

def get_description_from_request():
     if not request.form.has_key('description') or request.form['description'] == "":
        raise ValueError("no description given")
     else:
        return request.form['description']

def get_goal_temp_from_request():
    if request.form.has_key('goal_temp'):
        goal_temp = float(request.form['goal_temp'])
        if goal_temp <=0 or goal_temp >= 100:
            raise ValueError("goal temp wasn't inside acceptable bounds")
        return goal_temp
    else:
        raise ValueError("no goal temperature given")

def get_time_from_request():
    if not request.form.has_key('time_in_seconds') or request.form['time_in_seconds']=="":
        time_in_seconds = 3600
    else:
        if request.form['time_in_seconds'].isdigit():
            return int(request.form['time_in_seconds'])
        else:
            raise ValueError("time_in_seconds wasn't a number")

@app.route('/')
@app.route('/index.html')
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')


@app.route('/modify_cooker', methods=['POST'])
def modify_cooker():
    
    goal_temp = None
    remaining_time = None
    description = None
    
    try:
        goal_temp = get_goal_temp_from_request()
    except ValueError:
        pass
    
    try:
        remaining_time = get_time_from_request()
    except ValueError:
        pass
    
    try:
        description = get_description_from_request()
    except ValueError:
        pass


    cooker_name = get_cooker_name_from_request()
    cur_cookers = cooker_manager.CookerManager.running_cookers
    cooker = None
    for c in cur_cookers:
        if cooker_name == c.get_name():
            cooker = c
    
    if remaining_time or goal_temp or description:
        #gotta actually modify it - doing so now...
        if remaining_time:
            cooker.set_remaining_time(remaining_time)
        if description:
            cooker.set_description(description)
        if goal_temp:
            cooker.set_goal_temp(goal_temp)
        return redirect(url_for('status'))
    
    return render_template('modify_cooker.html',cooker=cooker)

@app.route('/status_ajax')
def status_ajax():
    cur_cookers = cooker_manager.CookerManager.running_cookers
    return render_template('show_status_ajax.html',entries=cur_cookers)

@app.route('/status')
@app.route('/status.html')
def status():
    cur_cookers = cooker_manager.CookerManager.running_cookers
    return render_template('show_status.html',entries=cur_cookers)

@app.route('/add_new_cooker', methods=['POST'])
def add_new_cooker():
    cooker_name = get_cooker_name_from_request()
    description = get_description_from_request()
    goal_temp = get_goal_temp_from_request()
    time_in_seconds = get_time_from_request()
    
    #sanity check on the cooker
    for cooker in cooker_manager.CookerManager.running_cookers:
        if cooker.get_name() == cooker_name:
            errors.append("Cooker given is already in use!")
    
    skip_logging = False
    if request.form.has_key('skip_logging') and request.form['skip_logging'] == True:
        skip_logging = True
    
    cooker = cooker_manager.CookerManager(cooker_name, description, not skip_logging)
    cooker.start_async_cooking(goal_temp,time_in_seconds)
    
    cooker_manager.CookerManager.running_cookers.append(cooker)
    
    return redirect(url_for('status'))

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
    #main()
