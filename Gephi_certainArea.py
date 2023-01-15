# Exporting data to Gephi
# Remark: This code exports data for one policy area specified below and is ideal to analyze one specific policy area.
# To get all data from the file as Gephi data set, use Gephi_overall.py

import json
import networkx as nx

PolicyArea = "Health" # Policy area we are interested in (has to be one of the pre-defined policy areas by the US Senate)
indata = 'senate_117.json' # file which contains information for graph creation
outname = 'something' # insert name for Gephi file here

# Creating empty graph
G = nx.DiGraph()

with open(indata,'r') as file:
    obj = json.load(file)
    
for x in obj:
    ob = json.loads(x)
    area = ob.get('policy')
    if area != None:
        pol = area.get('name')
        if pol == PolicyArea:
            sec = ob.get('secondportion')
            cos = ob.get('cosponsors')
            s = sec.get('sponsors')
            sdata = json.dumps(s)
            spon = json.loads(sdata)
            sponID = spon[0]['bioguideId']
            sponParty = spon[0]['party']
            sponName = spon[0]['fullName']
            if G.has_node(sponID) != True: G.add_node(sponID, party = sponParty, name = sponName)
            if cos != None: # Check whether cosponsors exist
                cosp = cos.get('cosponsors')
                for c in cosp:
                    cosponState = c.get('state')
                    cosponID = c['bioguideId']
                    cosponParty = c.get('party')
                    cosponName = c.get('fullName')
                    if G.has_node(cosponID) != True: G.add_node(cosponID, party = cosponParty, name = cosponName, state = cosponState)
                    if G.has_edge(cosponID, sponID) == True: 
                        G[cosponID][sponID]["weight"] = G[cosponID][sponID]["weight"] + 1
                    if G.has_edge(cosponID, sponID) != True: 
                        G.add_edge(cosponID, sponID, weight=1)


# Exporting to Gephi

nx.write_gexf(G, f"{outname}.gexf", encoding='utf-8', prettyprint=True)
print("Gephi exported")
