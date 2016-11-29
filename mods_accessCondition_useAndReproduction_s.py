import json
import  requests
from collections import Counter

import collections


## skip over collections wyu:55184 wyu:43338 wyu:54075
url = "http://localhost:8080/solr/collection1/select?q=mods_accessCondition_useAndReproduction_s%3A*+AND+PID%3Awyu%5C%3A*+AND+-RELS_EXT_isMemberOfCollection_uri_ss%3A+info%5C%3Afedora%2Fwyu%5C%3A55184+AND+-RELS_EXT_isMemberOfCollection_uri_ss%3A+info%5C%3Afedora%2Fwyu%5C%3A43338+AND+-RELS_EXT_isMemberOfCollection_uri_ss%3A+info%5C%3Afedora%2Fwyu%5C%3A54075&rows=999999&fl=PID%2Cmods_accessCondition_useAndReproduction_s&wt=json&indent=true"

json_obj = requests.get(url).json()

print "Solr Fields selected: " + json_obj["responseHeader"]["params"]["fl"]
wyu = "http://localhost:8080/solr/collection1/select?q=PID%3Awyu%5C%3A*&rows=9&fl=PID&wt=json"
wyu_obj = requests.get(wyu).json()
wyuPids = wyu_obj["response"]["numFound"]
print "Total wyu PIDs: " + str(wyuPids)
print "Solr Rows count: " + str(json_obj["responseHeader"]["params"]["rows"])

c = collections.Counter()

for i in json_obj["response"]["docs"]:
    #print i
    mods = str(i["mods_accessCondition_useAndReproduction_s"])
    #print "PID: " +  i["PID"] + " dc:rights " + mods
    #print i["PID"] + "\t" + mods
    print i["PID"] + " separatorText " + mods
    c[mods] += 1

for k, v in sorted(c.items(), key=lambda x: (-x[1],x[0])):
    print("{}|{}".format(k, v))

