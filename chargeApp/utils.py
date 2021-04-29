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
