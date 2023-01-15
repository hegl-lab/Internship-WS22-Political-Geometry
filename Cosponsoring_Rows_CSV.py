# Create a certain form of CSV (from the JSON string obtained when downloading data from the API)
# CSV contains (in each row) all the information about one particular pair of (sponsor, cosponsor), such as:
# Party of sponsor, party of cosponsor, cosponsorings for each political area
# Program can only be used for one senate at a time

import json
import numpy as np
import networkx as nx
import csv

# All political areas used to classify bills in the API
PolArea = ["Agriculture and Food", "Animals", "Armed Forces and National Security", "Arts, Culture, Religion", "Civil Rights and Liberties, Minority Issues", "Commerce", "Congress", "Crime and Law Enforcement", "Economics and Public Finance", "Education", "Emergency Management", "Energy", "Environmental Protection", "Families", "Finance and Financial Sector", "Foreign Trade and International Finance", "Government Operations and Politics", "Health", "Housing and Community Development", "Immigration", "International Affairs", "Labor and Employment", "Law", "Native Americans", "Public Lands and Natural Resources", "Science, Technology, Communications", "Social Sciences and History", "Social Welfare", "Sports and Recreation", "Taxation", "Transportation and Public Works", "Water Resources Development"]
PolDict = {"Agriculture and Food": 0, "Animals": 1, "Armed Forces and National Security": 2, "Arts, Culture, Religion" : 3, "Civil Rights and Liberties, Minority Issues" : 4, "Commerce" : 5, "Congress" : 6, "Crime and Law Enforcement" : 7, "Economics and Public Finance" : 8, "Education" : 9, "Emergency Management" : 10, "Energy" : 11, "Environmental Protection" : 12, "Families" : 13, "Finance and Financial Sector" : 14, "Foreign Trade and International Finance" : 15, "Government Operations and Politics" : 16, "Health" : 17, "Housing and Community Development" : 18, "Immigration" : 19, "International Affairs" : 20, "Labor and Employment" : 21, "Law" : 22, "Native Americans" : 23, "Public Lands and Natural Resources" : 24, "Science, Technology, Communications" : 25, "Social Sciences and History" : 26, "Social Welfare" : 27, "Sports and Recreation" : 28, "Taxation" : 29, "Transportation and Public Works" : 30, "Water Resources Development" : 31}

RelSen = ["117"] # Senate we are looking into

# Empty list to store data:
data = []
members = []

for num in RelSen:
    for PA in PolArea: 
        # Creating empty graph
        G = nx.DiGraph()
              
        # Policy area we are interested in
        PolicyArea = PA
        print(PA)

        with open(f'senate_{num}.json','r') as file:  # data for each senate should be stored in a file named 'senate_{num}.json' (when used combine.py, we will have this format)
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
                    if sponID not in members: 
                        members.append(sponID)
                    
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
                        mydata = {'spon': k, 'cospon': l, 'sponP': G.nodes[k]["party"], 'cosponP': G.nodes[l]["party"], 'data': arr}
                        piv = PolDict[PA]
                        mydata['data'][piv] = G[k][l]["weight"]
                        data.append(mydata)
                    if exi == True:
                        piv = PolDict[PA]
                        g['data'][piv] = G[k][l]["weight"]


for m1 in members:
    for m2 in members:
        exi = False
        for d1 in data:
            if d1['spon'] == m1 and d1['cospon']==m2:
                exi = True
        if exi == False:
            arr = np.zeros((32,), dtype=int)
            mydata = {'spon': k, 'cospon': l, 'sponP': G.nodes[k]["party"], 'cosponP': G.nodes[l]["party"], 'data': arr}
            data.append(mydata)
            
# Adding SP / CP information:
for z in data:   
    if z['sponP']== "D" and z['cosponP']=="D":
        z['Prel']="SP"
    elif z['sponP']== "R" and z['cosponP']=="R":
        z['Prel']="SP"
    else: z['Prel']="CP"
        
# Writing data to CSV

header = ["Sponsor", "Cosponsor", "Sponsor Party", "Cosponsor Party", "Party Relation", "Agriculture and Food", "Animals", "Armed Forces and National Security", "Arts, Culture, Religion", "Civil Rights and Liberties, Minority Issues", "Commerce", "Congress", "Crime and Law Enforcement", "Economics and Public Finance", "Education", "Emergency Management", "Energy", "Environmental Protection", "Families", "Finance and Financial Sector", "Foreign Trade and International Finance", "Government Operations and Politics", "Health", "Housing and Community Development", "Immigration", "International Affairs", "Labor and Employment", "Law", "Native Americans", "Public Lands and Natural Resources", "Science, Technology, Communications", "Social Sciences and History", "Social Welfare", "Sports and Recreation", "Taxation", "Transportation and Public Works", "Water Resources Development"]

with open(f'cosponsoring_{num}_row.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    
    counti = 0
    for j in data:
        wdata = []
        wdata.append(j['spon'])
        wdata.append(j['cospon'])
        wdata.append(j['sponP'])
        wdata.append(j['cosponP'])
        wdata.append(j['Prel'])
        for i in range(32):
            wdata.append(j['data'][i])
        writer.writerow(wdata)
        
print("CSV created")