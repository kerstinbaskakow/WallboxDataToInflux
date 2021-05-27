from chargeApp.config import Config
from chargeApp import influxclient

def queryDataFromInflux(query,meas,lim):
    import numpy as np
    limit = " LIMIT {}".format(lim)
    rawVal = influxclient.query(query+limit)
    valueList = list(rawVal.get_points(measurement='{}'.format(meas)))#[0]['value']
    values = list(map(lambda x: x['value'],valueList))
    #print(values)
    return int(np.mean(values))



def writeDataToInflux(value,meas):
    body = [{
    "measurement": meas,
    "fields":
        {"value": value}
    }]
    return influxclient.write_points(body, database=Config.DATABASE, time_precision='s', batch_size=10000, protocol='json')

def cloudyDayDetectionBackup(chargingState,detected,listOfActivePhases):
    factor = 0
    if chargingState == 2:
        factor = 1
        detected = 0
    else:
        if detected == 0:
            factor = sum(listOfActivePhases)
            detected = 1   
            if factor < 1:
                detected = 0
    return int(factor),int(detected)

def findActivePhases():
    listOfActivePhases=[]
    for phase in range(1,4,1):
        CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC'.format(Config.CURRENT_INFLUX.format(phase))    
        Lx = 1 if queryDataFromInflux(CURRENT_INFLUX_QUERY,Config.CURRENT_INFLUX.format(phase),1) >0 else 0
        listOfActivePhases.append(Lx)
    #factor = sum(listOfActivePhases)
    #see charging state from influx (not modbus, because than charging connection is safely established)
    chargingState = queryDataFromInflux(Config.CHARGE_STATE_INFLUX_QUERY,Config.CHARGE_STATE_INFLUX,1)
    detected = queryDataFromInflux(Config.ACTIVE_PHASES_DET_INFLUX_QUERY,Config.ACTIVE_PHASES_DET_INFLUX,1) 
    #the phasedetection should only be active a plugging
    # in previous tests the phase detection was calculated each time this function runs
    # at cloudy days this led to toggling charge behaviour and vehicle error state
    factor,detected =  cloudyDayDetectionBackup(chargingState,detected,listOfActivePhases)         
    if factor < 1:
        factor = 1
    writeDataToInflux(int(factor),"phaseDetectionFactor")       
    writeDataToInflux(int(detected),Config.ACTIVE_PHASES_DET_INFLUX)       
    return int(factor)