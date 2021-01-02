import speedtest
import json
from influxdb import InfluxDBClient

serverip = "192.168.100.20"  ## your Influx Docker/Server IP
serverport = 8086  ## Influx port
serverdatabase = "telegraf" ## you can use new one, i am using existing one
teststation = 'sr-net.ddns.net' ## in case multiple testpoints

def speed():    
    servers = [] for closest server, unless you want otherwise
    threads = 1
    test = speedtest.Speedtest()
    test.get_servers(servers)
    test.get_best_server()
    test.download(threads=threads)
    test.upload(threads=threads)
    test.results.share()
    results = test.results.dict()
    result = {}
    result["UploadSpeed"] = results["upload"]
    result["DownloadSpeed"] = results["download"]
    result["Ping"] = results["ping"]
    return(result)

def uploadInfluxdata(host='192.168.100.20', port=8086):
    query = 'select Float_value from cpu_load_short;'
    query_where = 'select Int_value from cpu_load_short where host=$host;'
    bind_params = {'host': teststation}
    testdata = speed()
    json_body = [
        {
            "measurement": "PythonSpeedTest",
            "tags": {
                "host": servernickname,
            },

            "fields": {
                "Upload": testdata["UploadSpeed"],
                "Download": testdata["DownloadSpeed"],
                "Ping": testdata["Ping"]
            }
        }
    ]

    client = InfluxDBClient(host, port, database = serverdatabase)  # Init connection to Influx Server
    client.write_points(json_body)  # Write Speedtest results

uploadInfluxdata()
