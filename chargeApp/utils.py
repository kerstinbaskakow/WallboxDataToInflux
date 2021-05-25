from chargeApp.config import Config
from chargeApp import influxclient

def queryDataFromInflux(query,meas):
    rawVal = influxclient.query(query)
    value = list(rawVal.get_points(measurement='{}'.format(meas)))[0]['value']
    return value



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
    return int(factor)

def findActivePhases():
    listOfActivePhases=[]
    for phase in range(1,4,1):
        CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(Config.CURRENT_INFLUX.format(phase))    
        Lx = 1 if queryDataFromInflux(CURRENT_INFLUX_QUERY,Config.CURRENT_INFLUX.format(phase)) >0 else 0
        listOfActivePhases.append(Lx)
    #factor = sum(listOfActivePhases)
    #see charging state from influx (not modbus, because than charging connection is safely established)
    chargingState = queryDataFromInflux(Config.CHARGE_STATE_INFLUX_QUERY,Config.CHARGE_STATE_INFLUX)
    detected = queryDataFromInflux(Config.ACTIVE_PHASES_DET_INFLUX_QUERY,Config.ACTIVE_PHASES_DET_INFLUX) 
    #the phasedetection should only be active a plugging
    # in previous tests the phase detection was calculated each time this function runs
    # at cloudy days this led to toggling charge behaviour and vehicle error state
    factor =  cloudyDayDetectionBackup(chargingState,detected,listOfActivePhases)         
    if factor < 1:
        factor = 1
    writeDataToInflux(factor,"phaseDetectionFactor")       
    writeDataToInflux(detected,Config.ACTIVE_PHASES_DET_INFLUX)       
    return int(factor)

