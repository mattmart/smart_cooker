def read_temp(slave):
    tfile = open("/sys/bus/w1/devices/"+slave+"/w1_slave") 
    text = tfile.read() 
    tfile.close() 
    secondline = text.split("\n")[1] 
    temperaturedata = secondline.split(" ")[9] 
    temperature = float(temperaturedata[2:]) 
    temperature = temperature / 1000 
    return temperature
    
