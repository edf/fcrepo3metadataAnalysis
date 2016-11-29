import json
import  requests
from collections import Counter

import collections

# skip over collections wyu:55184 wyu:43338 wyu:54075
url = "http://localhost:8080/solr/collection1/select?q=dc.rights%3A*+AND+PID%3Awyu%5C%3A*+AND+-RELS_EXT_isMemberOfCollection_uri_ss%3A+info%5C%3Afedora%2Fwyu%5C%3A55184+AND+-RELS_EXT_isMemberOfCollection_uri_ss%3A+info%5C%3Afedora%2Fwyu%5C%3A43338+AND+-RELS_EXT_isMemberOfCollection_uri_ss%3A+info%5C%3Afedora%2Fwyu%5C%3A54075&rows=999999&fl=PID%2Cdc.rights&wt=json&indent=true"


json_obj = requests.get(url).json()

print "Solr Fields selected: " + json_obj["responseHeader"]["params"]["fl"]
wyu = "http://localhost:8080/solr/collection1/select?q=PID%3Awyu%5C%3A*&rows=9&fl=PID&wt=json"
wyu_obj = requests.get(wyu).json()
wyuPids = wyu_obj["response"]["numFound"]
print "Total wyu PIDs: " + str(wyuPids)
print "Solr Rows count: " + str(json_obj["responseHeader"]["params"]["rows"])
c = collections.Counter()
print "PID,dc_rights"
for i in json_obj["response"]["docs"]:
    dcRights = str(i["dc.rights"])
    #print "PID: " +  i["PID"] + " dc:rights " + dcRights
    #print i["PID"] + "\t" + dcRights
    print i["PID"] + " separatorText " + dcRights
    c.update(i["dc.rights"])

for k, v in sorted(c.items(), key=lambda x: (-x[1],x[0])):
    k.replace("\u2013","-")   # use case wyu:117306
    k.replace('\u2019',"'")   # use case wyu:91994
    k.replace('\u201907',"'07")   # use case wyu:110191 does not replace
    k.replace('\n<br>\n'," ")     # use case wyu:4851
    k.replace('\t'," ")           # need to ID a use case wyu:
    print("{}|{}".format(k, v))
