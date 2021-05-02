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

def findActivePhases():
    listOfActivePhases=[]
    for phase in range(1,4,1):
        CURRENT_INFLUX_QUERY = 'SELECT * FROM {} ORDER BY time DESC LIMIT 1'.format(Config.CURRENT_INFLUX.format(phase))    
        Lx = 1 if queryDataFromInflux(CURRENT_INFLUX_QUERY,Config.CURRENT_INFLUX.format(phase)) >0 else 0
        listOfActivePhases.append(Lx)
    factor = sum(listOfActivePhases)
    if factor < 1:
        factor = 1
    return int(factor)

