# Program for combining different JSON strings (we obtained by downloading data from the API)
# When using the program to download data from the API, the program might have crashed and now there are several different JSON strings
# Use program to combine them!

import json

senatenum = 117 # Senate data we want to concatenate
set = {} # Names of the strings that shall be combined, must be in same directory
datalist = []
counter = 0
ac = 0

# Opening JSON files
for dataset in set:
    with open(dataset,'r') as file:
        obj = json.load(file)

# Making sure not to have any duplicates in there
    for x in obj:
        ob = json.loads(x)
        add = True
        for y in datalist:
            a = json.loads(y)
            if a['billtype']==ob['billtype']:
                if a['billnumber']==ob['billnumber']:
                    add = False
        if add == True:
            ac = ac + 1
            print(ac)
            ob_json = json.dumps(ob)
            datalist.append(ob_json)

for z in datalist:
    counter = counter + 1

print("total number:", counter) # total number is printed for verifying that everything worked out
        

# Converting datalist into JSON
data_json = json.dumps(datalist)
        
# Writing to JSON file
with open(f"senate_{senatenum}.json", "w") as outfile:
    outfile.write(data_json)