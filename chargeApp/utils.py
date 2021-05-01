from chargeApp.config import Config
from chargeApp import influxclient,logger

def queryDataFromInflux(query,meas):
    try:
        rawVal = influxclient.query(query)
        value = list(rawVal.get_points(measurement='{}'.format(meas)))[0]['value']
    except Exception as e:
        logger.error(e)
        #if value for power is zero this will prevent from charging
        value = 0
    finally:
        return value

def writeDataToInflux(value,meas):
    body = [{
    "measurement": meas,
    "fields":
        {"value": value}
    }]
    try: 
        influxclient.write_points(body, database=Config.DATABASE, time_precision='s'
                                     , batch_size=10000, protocol='json')
    except Exception as e:
        logger.error(e)


def findActivePhases():
    listOfActivePhases=[]
    try:
        for phase in range(1,4,1):
            CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(Config.CURRENT_INFLUX.format(phase))
            Lx = 1 if queryDataFromInflux(CURRENT_INFLUX_QUERY,Config.CURRENT_INFLUX.format(phase)) >0 else 0
            listOfActivePhases.append(Lx)
        factor = sum(listOfActivePhases)
        #set mininmum value for phases to 1
        #if this is zero no current will be available at plugging a vehicle
        if factor == 0:
            factor = 1
        logger.debug("list of active phases: {}".format(listOfActivePhases))
    except Exception as e:
        logger.error(e)
        #0 prevents from charging
        #1 allows current corresponding to one phase active
        factor=0
    finally:
        return int(factor)

#def checkPluggingVehicle():
#    rawVal = influxclient.query('SELECT * FROM {} ORDER BY time DESC LIMIT 2'
#                                        .format(Config.MEASUREMENT_ITEMS_INPUTREG[5]))
#    meas = Config.MEASUREMENT_ITEMS_INPUTREG[5]
#    values = list(map(lambda x:x['value'], list(rawVal.get_points(measurement='{}'.format(meas)))))
#    logger.debug("chargingState: oldVal: {}, new Val: {}".format(values[1],values[0]))
#    if (int(values[1]) in [2,3] and int(values[0]) in [4,5,7]):
#        chargingStateChangeToPlugged = True
#    else:
#        chargingStateChangeToPlugged = False
#    logger.debug("chargingstate change: {}".format(chargingStateChangeToPlugged))
#    return chargingStateChangeToPlugged
    
