#first shot at serialization
import os
import io
import json

class CookerState:

    def __init__(self, name, goal_temp, goal_time):
        '''
        WARNING! this method is only meant to be used to
        initialize cooking. it WILL override an existing cooker
        #todo: throw appropriate error
        '''
        self._name = name
        self._goal_temp = goal_temp
        self._goal_time = goal_time
        self.flush()

    def get_name(self):
        return self._name
    
    def get_goal_temp(self):
        return self._goal_temp
    
    def set_goal_temp(self,gtemp):
        self._goal_temp = gtemp
        self.flush()
    
    def get_remaining_time(self):
        return self._goal_time
    
    def set_remaining_time(self, gtime):
        self._goal_time = gtime
        self.flush()
    
    def flush(self):
        filename = "/tmp/"+self._name+".cooker"
        new_filename = "/tmp/"+self._name+".cooker.new"
        with io.open(new_filename,'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(self.__dict__)))
        os.rename(new_filename, filename)
    
    @staticmethod
    def init_from_name(name):
        filename = "/tmp/"+name+".cooker"
        with io.open(filename,'r', encoding='utf-8') as f:
            data = json.load(f)
        name= data['_name']
        gtime= data['_goal_time']
        gtemp= data['_goal_temp']

        return CookerState(name, gtemp, gtime)
        
    
def main():
   cstate = CookerState.init_from_name("Exodus")
   print cstate

if __name__ == "__main__":
    main()
