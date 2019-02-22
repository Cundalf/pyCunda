import os,sys

try:
    import requests
    import json
except:
    print("Falta lib: requests. Probar: pip install requests")
    exit()

#array((server,port),(server,port),...)
arrWS=[["localhost","8085"]]

for ws in arrWS:
    server=ws[0]
    port=ws[1]

    arr=[("P0",server),("P1",port),("P2","NAGIOS"),("P3",""),("P4",""),
         ("P5","") ,("P6",""),("P7",""),("P8",""),("P9",""),
         ("code","D TESTWS^CUNDA(P0,P1,P2,.P9)"),("global",""),
         ("mserver","localhost"),
         ("namespace","TEST"),("global_index","")]
    try:
        r = requests.post("http://" + server + ":" + port + "/Ejecutar", data=arr,timeout=15)
        if (r.status_code == 200):
            res=r.json()
            if (res["params"]["P9"] == "OK"):
                print("OK " + server + ":" + port)
                #sys.exit(0)
            else:
                print("WARNING " + server + ":" + port)
                #sys.exit(1)
        else:
            r = requests.post("http://" + server + ":" + port + "/Ejecutar", data=arr,timeout=15)
        if (r.status_code == 200):
            res=r.json()
            if (res["params"]["P9"] == "OK"):
                print("OK " + server + ":" + port)
                #sys.exit(0)
            else:
                print("WARNING " + server + ":" + port)
                #sys.exit(1)
        else:
            print("CRITICAL " + server + ":" + port)
           # sys.exit(2)
    except:
        print("UNKNOW " + server + ":" + port)
        #sys.exit(3)