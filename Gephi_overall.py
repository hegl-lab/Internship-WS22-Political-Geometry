# Exporting data to Gephi
# Run this code to create a file that can be read into Gephi
# The program creates a graph for ALL bills listed in the infile. In case you only want a certain policy area to be considered, use seperate program
# (Using Gephi might be useful for visualization and social network analysis)

import json
import networkx as nx

indata = 'senate_117.json' # file which contains information for graph creation
outname = 'something' # insert name for Gephi file here

# Creating empty graph
G = nx.DiGraph()


with open(indata,'r') as file:
    obj = json.load(file)
    
for x in obj:
    ob = json.loads(x)
    sec = ob.get('secondportion')
    cos = ob.get('cosponsors')
    s = sec.get('sponsors')
    sdata = json.dumps(s)
    spon = json.loads(sdata)
    sponID = spon[0]['bioguideId']
    sponParty = spon[0]['party']
    sponName = spon[0]['fullName']
    print(sponID)
    if G.has_node(sponID) != True: G.add_node(sponID, party = sponParty, name = sponName)
    if cos != None: # Check whether cosponsors exist
        cosp = cos.get('cosponsors')
        for c in cosp:
            cosponState = c.get('state')
            cosponID = c['bioguideId']
            cosponParty = c.get('party')
            cosponName = c.get('fullName')
            print(cosponID)
            if G.has_node(cosponID) != True: G.add_node(cosponID, party = cosponParty, name = cosponName, state = cosponState)
            if G.has_edge(cosponID, sponID) == True: 
                G[cosponID][sponID]["weight"] = G[cosponID][sponID]["weight"] + 1
            if G.has_edge(cosponID, sponID) != True: 
                G.add_edge(cosponID, sponID, weight=1)

# Exporting to Gephi
nx.write_gexf(G, f"{outname}.gexf", encoding='utf-8', prettyprint=True)
print("Gephi exported")
