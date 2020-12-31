
import json
string=open("yb.json","r")

jso = json.load(string)

print(jso["databaesconnect"]["sqlserver"])
string.close()