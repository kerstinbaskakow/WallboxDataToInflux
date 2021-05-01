from chargeApp.config import Config
from chargeApp import influxclient,logger

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

def findActivePhases():
    listOfActivePhases=[]
    for phase in range(1,4,1):
        CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(Config.CURRENT_INFLUX.format(phase))
        #Lx = 1 if 5 >0 else 0
        Lx = 1 if queryDataFromInflux(CURRENT_INFLUX_QUERY,Config.CURRENT_INFLUX.format(phase)) >0 else 0
        listOfActivePhases.append(Lx)
    factor = sum(listOfActivePhases)
    print("list of active phases: {}".format(listOfActivePhases))
    return int(factor)

def checkPluggingVehicle():
    rawVal = influxclient.query('SELECT * FROM {} ORDER BY time DESC LIMIT 2'
                                        .format(Config.MEASUREMENT_ITEMS_INPUTREG[5]))
    meas = Config.MEASUREMENT_ITEMS_INPUTREG[5]
    values = list(map(lambda x:x['value'], list(rawVal.get_points(measurement='{}'.format(meas)))))
    logger.debug("chargingState: oldVal: {}, new Val: {}".format(values[1],values[0]))
    if (int(values[1]) in [2,3] and int(values[0]) in [5,7]):
        chargingStateChangeToPlugged = True
    else:
        chargingStateChangeToPlugged = False
    print("chargingstate change: {}".format(chargingStateChangeToPlugged))
    return chargingStateChangeToPlugged
    
