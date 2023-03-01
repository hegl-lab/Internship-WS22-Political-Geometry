# Comparing Same - Party and Cross-Party cooperation
# Program creates CSV file with measures indicating high or low cross-party cosponsorship (this is done for every congress overall, for insights into every policy area, use respective program)
# The files used in analysis have to contain data in a particular way (in the way it is obtained by using the respective program in this GitHub repository)
# JSON files that are used for analysis should be named in this way: 'senate_{number}.json'

import json
import numpy as np
import networkx as nx
import csv


RelSen = range(93,118) # Range of Senates to be analyzed

alpha = 0.85 # Quantile used for determining significancy

# Empty list to store data:
data = []

for num in RelSen:
        # Creating empty graph
    G = nx.DiGraph()
    count = 0

    with open(f'senate_{num}.json','r') as file: # Names of data files have to be of this particular form
        obj = json.load(file)

    for x in obj:
        count = count + 1
        ob = json.loads(x)
        sec = ob.get('secondportion')
        cos = ob.get('cosponsors')
        s = sec.get('sponsors')
        sdata = json.dumps(s)
        spon = json.loads(sdata)
        sponID = spon[0]['bioguideId']
        sponParty = spon[0]['party']
        sponName = spon[0]['fullName']
        #print(sponID)
        if G.has_node(sponID) != True: G.add_node(sponID, party = sponParty, name = sponName)
        if cos != None: # Check whether cosponsors exist
            cosp = cos.get('cosponsors')
            for c in cosp:
                cosponState = c.get('state')
                cosponID = c['bioguideId']
                cosponParty = c.get('party')
                cosponName = c.get('fullName')
                #print(cosponID)
                if G.has_node(cosponID) != True: G.add_node(cosponID, party = cosponParty, name = cosponName, state = cosponState)
                if G.has_edge(cosponID, sponID) == True: 
                    G[cosponID][sponID]["weight"] = G[cosponID][sponID]["weight"] + 1
                if G.has_edge(cosponID, sponID) != True: 
                    G.add_edge(cosponID, sponID, weight=1)
                                
        # Creating a list for democrats and republicans:

    dem = []
    rep = []
    ind = []

    for a in G.nodes():
        if G.nodes[a]['party'] == 'D': dem.append(a)
        if G.nodes[a]['party'] == 'R': rep.append(a)
        if G.nodes[a]['party'] == 'I': ind.append(a)
        
        # Numerical analysis: Look, where cross-party cooperation is significant

        # Compute number of cosponsoring for Same party (SP) and Cross Party (CP):

    sp_num = []

    for k in dem:
        for l in dem: 
            if G.has_edge(k,l) == True:
                sp_num.append(G[k][l]["weight"])
                    
    for k in rep:
        for l in rep: 
            if G.has_edge(k,l) == True:
                sp_num.append(G[k][l]["weight"])
                    
    try:
        threshold = np.quantile(sp_num, alpha)  # Determining threshold for evaluating significancy of cosponsorship
    except IndexError:
        threshold = "NaN"
        cross = "NaN"    
        d_rel = "NaN"  
        r_rel = "NaN"
        SP = "NaN"
        print("Same Party", SP)
        print ("Dem: ", d_rel)
        print ("Rep: ", r_rel)
        print ("Cross: ", cross)
        CPSP = "NaN"
        CP_rel = "NaN"
        SP_rel = "NaN"
            
        print("CP / SP: ", CPSP)
        print ("relative CP: ", CP_rel)
        print("relative SP: ", SP_rel)
            
        continue

    d_rel = 0
    r_rel = 0
    cross = 0

    for k in dem:
        for l in dem: 
            if G.has_edge(k,l) == True and G[k][l]["weight"] > threshold:
                d_rel = d_rel + 1
                    
    for k in rep:
        for l in rep: 
            if G.has_edge(k,l) == True and G[k][l]["weight"] > threshold:
                r_rel = r_rel + 1
                     
    for k in rep: 
        for l in dem or ind: 
            if G.has_edge(k,l) == True and G[k][l]["weight"] > threshold:
                cross = cross + 1
    
    for k in dem or ind: 
        for l in rep: 
            if G.has_edge(k,l) == True and G[k][l]["weight"] > threshold:
                cross = cross + 1
    
    # Computing measures
                
    SP = d_rel + r_rel  
    print("Same Party", SP)
    print ("Dem: ", d_rel)
    print ("Rep: ", r_rel)
    print ("Cross: ", cross)
    
    if SP != 0:
        CPSP = cross / SP
    else: 
        CPSP = "NaN"
    CP_rel = cross / count
    SP_rel = SP / count
    every = SP + cross
    if every != 0: 
        SPall = SP / every
        CPall = cross / every
    else: 
        SPall = "NaN"
        CPall = "NaN"
        
    print("CP / SP: ", CPSP)
    print ("relative CP: ", CP_rel)
    print("relative SP: ", SP_rel)
    print("CP by all:", CPall)
    print("SP by all:", SPall)
        
    # Fill data into dict and append list:
    data_dict = {'senate': num, 'SP': SP, 'D': d_rel, 'R': r_rel, 'CP': cross, 'CP/SP': CPSP, 'relative CP': CP_rel, 'relative SP': SP_rel, 'CP by all': CPall, 'SP by all': SPall}
    data.append(data_dict)



# Writing data to CSV

header = ['Senate', 'Same Party', 'Dem Cosponsoring', 'Rep Cosponsoring', 'Cross Party', 'CP/SP', 'relative CP', 'relative SP', 'CP by all', 'SP by all']

with open('all_NEW.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    
    for x in data: 
        wdata = []
        for y in x.keys():
            wdata.append(x[y])
        writer.writerow(wdata)
        
print("CSV created")
