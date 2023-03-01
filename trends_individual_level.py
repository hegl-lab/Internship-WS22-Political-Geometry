# Comparing Same - Party and Cross-Party cooperation
# Program creates CSV file which lists all significant cosponsoring pairs (including policy area), so it's vital when analyzing cooperation on a personal level
# The files used in analysis have to contain data in a particular way (in the way it is obtained by using the respective program in this GitHub repository)
# JSON files that are used for analysis should be named in this way: 'senate_{number}.json'

import json
import numpy as np
import networkx as nx
import csv

PolArea = ["Agriculture and Food", "Animals", "Armed Forces and National Security", "Arts, Culture, Religion", "Civil Rights and Liberties, Minority Issues", "Commerce", "Congress", "Crime and Law Enforcement", "Economics and Public Finance", "Education", "Emergency Management", "Energy", "Environmental Protection", "Families", "Finance and Financial Sector", "Foreign Trade and International Finance", "Government Operations and Politics", "Health", "Housing and Community Development", "Immigration", "International Affairs", "Labor and Employment", "Law", "Native Americans", "Public Lands and Natural Resources", "Science, Technology, Communications", "Social Sciences and History", "Social Welfare", "Sports and Recreation", "Taxation", "Transportation and Public Works", "Water Resources Development"]
PolDict = {"Agriculture and Food": 0, "Animals": 1, "Armed Forces and National Security": 2, "Arts, Culture, Religion" : 3, "Civil Rights and Liberties, Minority Issues" : 4, "Commerce" : 5, "Congress" : 6, "Crime and Law Enforcement" : 7, "Economics and Public Finance" : 8, "Education" : 9, "Emergency Management" : 10, "Energy" : 11, "Environmental Protection" : 12, "Families" : 13, "Finance and Financial Sector" : 14, "Foreign Trade and International Finance" : 15, "Government Operations and Politics" : 16, "Health" : 17, "Housing and Community Development" : 18, "Immigration" : 19, "International Affairs" : 20, "Labor and Employment" : 21, "Law" : 22, "Native Americans" : 23, "Public Lands and Natural Resources" : 24, "Science, Technology, Communications" : 25, "Social Sciences and History" : 26, "Social Welfare" : 27, "Sports and Recreation" : 28, "Taxation" : 29, "Transportation and Public Works" : 30, "Water Resources Development" : 31}

RelSen = range(93,94) # Senates one wants to analyze

alpha = 0.85 # Quantile used for determining significancy

# Empty list to store data:
data = []

for num in RelSen:
        # Creating empty graph
    K = nx.DiGraph()
    count = 0

    with open(f'senate_{num}.json','r') as file: # File needs to be of particular form and name
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
        if K.has_node(sponID) != True: K.add_node(sponID, party = sponParty, name = sponName)
        if cos != None: # Check whether cosponsors exist
            cosp = cos.get('cosponsors')
            for c in cosp:
                cosponState = c.get('state')
                cosponID = c['bioguideId']
                cosponParty = c.get('party')
                cosponName = c.get('fullName')
                #print(cosponID)
                if K.has_node(cosponID) != True: K.add_node(cosponID, party = cosponParty, name = cosponName, state = cosponState)
                if K.has_edge(cosponID, sponID) == True: 
                    K[cosponID][sponID]["weight"] = K[cosponID][sponID]["weight"] + 1
                if K.has_edge(cosponID, sponID) != True: 
                    K.add_edge(cosponID, sponID, weight=1)
                                
        # Creating a list for democrats and republicans:

    dem = []
    rep = []
    ind = []

    for a in K.nodes():
        if K.nodes[a]['party'] == 'D': dem.append(a)
        if K.nodes[a]['party'] == 'R': rep.append(a)
        if K.nodes[a]['party'] == 'I': ind.append(a)
        
        
        # Analysis - create sets of same party cooperation
        
    sp_num = []

    for k in dem:
        for l in dem: 
            if K.has_edge(k,l) == True:
                    #print(K.nodes[k]["party"])
                    #print(K.nodes[l]["party"])
                mydict = {"spon": k, "cospon": l, "SName": K.nodes[k]["name"], "CName": K.nodes[l]["name"], "sponP": K.nodes[k]["party"], "cosponP": K.nodes[l]["party"], "collabos": K[k][l]["weight"]}
                sp_num.append(mydict)
                        
    for k in rep:
        for l in rep: 
            if K.has_edge(k,l) == True:
                mydict = {"spon": k, "cospon": l, "SName": K.nodes[k]["name"], "CName": K.nodes[l]["name"], "sponP": K.nodes[k]["party"], "cosponP": K.nodes[l]["party"], "collabos": K[k][l]["weight"]}
                sp_num.append(mydict)
         
    same_set = []
        
    for o in sp_num:
        same_set.append(o["collabos"])
                                    
    try:
        threshold = np.quantile(same_set, alpha) # threshold for determining significancy of cosponsorship
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
        
    rel_same = []
    rel_cross = []

    for k in dem:
        for l in dem: 
            if K.has_edge(k,l) == True and K[k][l]["weight"] > threshold:
                mydict = {"spon": k, "cospon": l, "SName": K.nodes[k]["name"], "CName": K.nodes[l]["name"], "sponP": K.nodes[k]["party"], "cosponP": K.nodes[l]["party"], "collabos": K[k][l]["weight"]}
                rel_same.append(mydict)
                d_rel = d_rel + 1
                    
    for k in rep:
        for l in rep: 
            if K.has_edge(k,l) == True and K[k][l]["weight"] > threshold:
                mydict = {"spon": k, "cospon": l, "SName": K.nodes[k]["name"], "CName": K.nodes[l]["name"], "sponP": K.nodes[k]["party"], "cosponP": K.nodes[l]["party"], "collabos": K[k][l]["weight"]}
                rel_same.append(mydict)
                r_rel = r_rel + 1
                         
    for k in rep: 
        for l in dem or ind: 
            if K.has_edge(k,l) == True and K[k][l]["weight"] > threshold:
                mydict = {"spon": k, "cospon": l, "SName": K.nodes[k]["name"], "CName": K.nodes[l]["name"], "sponP": K.nodes[k]["party"], "cosponP": K.nodes[l]["party"], "collabos": K[k][l]["weight"]}
                rel_cross.append(mydict)
                cross = cross + 1
        
    for k in dem or ind: 
        for l in rep: 
            if K.has_edge(k,l) == True and K[k][l]["weight"] > threshold:
                mydict = {"spon": k, "cospon": l, "SName": K.nodes[k]["name"], "CName": K.nodes[l]["name"], "sponP": K.nodes[k]["party"], "cosponP": K.nodes[l]["party"], "collabos": K[k][l]["weight"]}
                rel_cross.append(mydict)
                cross = cross + 1
                    
    print(rel_cross)
                    
        # Plugging in code from creating CSV to get an overview about the situaiton in different political areas
        
    for PA in PolArea: 
            # Creating empty graph
        G = nx.DiGraph()
                  
            # Policy area we are interested in
        PolicyArea = PA
            #print(PA)

        with open(f'senate_{num}.json','r') as file2:  # data for each senate should be stored in a file named 'senate_{num}.json' (when used combine.py, we will have this format)
            obje = json.load(file2)        
            for x in obje:
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
                                    
            # Processing data for CSV creation with cosponsorship data
            
            for k in G.nodes():
                for l in G.nodes(): 
                    g = 0
                    if G.has_edge(k,l) == True:
                        exi = False
                        for h in data: 
                            if h['spon'] == k and h['cospon']==l:
                                exi = True
                                g = h
                        if exi == False:
                            arr = np.zeros((32,), dtype=int)
                            mydata = {'spon': k, 'cospon': l, "SName": G.nodes[k]["name"], "CName": G.nodes[l]["name"], 'sponP': G.nodes[k]["party"], 'cosponP': G.nodes[l]["party"], 'data': arr}
                            piv = PolDict[PA]
                            mydata['data'][piv] = G[k][l]["weight"]
                            data.append(mydata)
                        if exi == True:
                            piv = PolDict[PA]
                            g['data'][piv] = G[k][l]["weight"]
    
    header = ["Sponsor", "Sponsor Name", "Cosponsor", "Cosponsor Name", "Policy Area", "Cosponsorings"]                           
    with open(f'details_{num}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        

        writer.writerow(header)
        for cr in rel_cross: 
            spo = cr["spon"]
            cospo = cr["cospon"]
            for dax in data: 
                if dax["spon"] == spo and dax["cospon"] == cospo: 
                    for ex in PolArea: 
                        piv = PolDict[PA]
                        if dax['data'][piv] != 0:
                            wdata = []
                            wdata.append(spo)
                            wdata.append(dax['SName'])
                            wdata.append(cospo)
                            wdata.append(dax['CName'])
                            wdata.append(ex)
                            wdata.append(dax['data'][piv])
                            writer.writerow(wdata)
                        
    print("CSV created", num)