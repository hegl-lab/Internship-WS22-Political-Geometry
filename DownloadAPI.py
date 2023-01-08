# Downloading all data from the API and saving it

# Remark: Sometimes, the program might crash (due to loss of Wifi, too many requests, ...). If that happens, do the follwing:
# Adapt the categories listed in "types1"
# Adapt the offset "off" (these two things can be adapted perfectly by considering information from recovery URL)
# Use the first URL below, not the second (first includes "offset" parameter)
# Run program again
# You might have to concetenate several JSON files --> See program on Github for this purpose

import requests
import math
import pandas as pd
import json
import numpy as np
import time

congress = 117 #Congress we are interested in

key = None # Insert your API key here


types1 = ["s", "sres", "sjres", "sconres"] # Senate data is stored in these 4 subcategories

# We have to consider everything in types to get all bills connected to the Senate

datalist = []
rec_num = 0
rec_url = None
off = 0 # In case program crashed

for c in types1:
    
    # Initialization
    types = c
    print("begin: ", types)
    #url = f'https://api.congress.gov/v3/bill/{congress}/{types}?format=json&limit=70&offset={off}&api_key{key}'
    url = f'https://api.congress.gov/v3/bill/{congress}/{types}?format=json&limit=70&api_key{key}'
    m = requests.get(url, headers={"X-API-Key":key})
    rdata = m.json()
    rawdata = rdata.get('bills')
    pag = rdata.get('pagination') 

    counter = 0
    iter = pag.get('count')
    it = math.ceil(iter/70) # Divide by 70, since we request 70 bills at once
    print("it for this type:", it)
    
    # Looping over entries

    while it > 0:
        for x in rawdata:
            counter = counter + 1
            print(counter)
            bill_number = x.get('number')
            bill_type = x.get('type')
            newurl = x.get('url')
            newurl = f'{newurl}&limit=250&api_key{key}'
            d = requests.get(newurl, headers={"X-API-Key":key})
            da = d.json()
            da=da.get('bill')
            policy = da.get('policyArea')
            cos = da.get('cosponsors')
            if cos != None: # Check whether cosponsors exist
                curl = cos.get('url')
                curl2 = f'{curl}&limit=250&api_key{key}'

                # Requesting Cosponsorship
                
                e = requests.get(curl2, headers={"X-API-Key":key})
                co = e.json()
                entry = {'billnumber': bill_number, 'billtype': bill_type, 'policy': policy, 'firstportion': x, 'secondportion': da, 'cosponsors': co}
            else:
                entry = {'billnumber': bill_number, 'billtype': bill_type, 'policy': policy, 'firstportion': x, 'secondportion': da}
            
            # Looking for data for recovery file:
            if bill_number != None:
                rec_num = bill_number
                with open("recovery117.txt", "w") as outfile:
                    outfile.write(c)
                    outfile.write(rec_num)
                
            # Converting entry (dict) to JSON
            entry_json = json.dumps(entry)
        
            # Appending datalist with the JSON string
            datalist.append(entry_json)
            
            # Sleeping sufficiently long
            time.sleep(10.2)  # Ran quite good with 10.2
            

        # Converting datalist into JSON
        data_json = json.dumps(datalist)
        
        # Writing to JSON file
        with open("API_data_117.json", "w") as outfile:
            outfile.write(data_json)
         
        pag = rdata.get('pagination')
        nurl = pag.get('next')
        if nurl != None:
            m = requests.get(nurl, headers={"X-API-Key":key})
            rdata = m.json()
            rawdata = rdata.get('bills')
            with open("recovery_url.txt", "w") as outfile:
                outfile.write(nurl)
        it = it-1

    print("end: ", c)