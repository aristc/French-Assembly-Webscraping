import urllib2
import pandas as pd
from bs4 import BeautifulSoup


## STEP 1 - EXTRACT LIST OF DEPUTES BY AGE RANGE (INCLUDING CIRCONSCRIPTION, REGION, ID)

url_age = "http://www2.assemblee-nationale.fr/deputes/liste/ages/(vue)/tableau"
page_age = urllib2.urlopen(url_age)

# The full list of depute names is displayed in table format and can be easily extracted with pandas.read.html
# This page contains relevant information on each depute such as their circonscription, will be kept in the df

df_age = pd.read_html(url_age) # Extracts a list of dataframes from the webpage (as many dataframes as there are age groups)
df_age= pd.concat(df_age,ignore_index=True) #concatenates all the dataframes so we have just one and ignores the indexes to recreate a new index (necessary for the later concatenation)
df_age= df_age.drop('Lien fiche',1) # Removes an empty column

# However the age is not displayed in the tables but in a title before each table
# also the depute id is hidden in the link to each depute's profile page
# (the unique depute ID is needed in order to perform a join with other dataframes later on)
# Hence the missing information will be added by scraping the data with BeautifulSoup

soup_age = BeautifulSoup(page_age,'html.parser')
table_age = soup_age.find('div', {'id': 'deputes-list'})

agetmp=[]
age=[]
dep_id = []

# The loop below is going to go through each row of the 'a' section with "deputes-list"
# each time a "name" is found then it's an age range and it's stored in a temporary list
# this value is assigned to each following depute ID until a new age range is found

for row in table_age.findAll('a'):
	if not (row.get("name")=='' or row.get("name")==None): 			# Only the rows with a "name" tag contain an age range
		agetmp = row.get("name") 				# Stores the latest age range found in a temporary list
	elif not (row.get("href")==None): 			# The rows with a "href" tag correspond to the list of depute names
		dep_id.append(row.get("href").replace("/deputes/fiche/OMC_PA","")) 		# Extracts the depute ID from each link to the depute profile page
		age.append(agetmp) 		# Appends the latest age range found to each depute ID
	else:
		continue 		# If the row does not have "name" or a "href" tag then it's not relevant and it's skipped

df_age_add = pd.DataFrame(
    {'Dep_ID': dep_id,
    'Age': age
    }) 	# Creates a dataframe with the two lists

# The two datasets are merged into one
df_age = pd.concat([df_age,df_age_add],axis=1)

print df_age.head(n=15)

## STEP 2 - EXTRACT LIST OF DEPUTES BY OCCUPATION (INCLUDING ID) - NOTE: NON-EXHAUSTIVE LIST

url_occ = "http://www2.assemblee-nationale.fr/deputes/liste/cat-sociopro"
page_occ = urllib2.urlopen(url_occ)

soup_occ = BeautifulSoup(page_occ,'html.parser')
table_occ = soup_occ.find('div', {'id': 'deputes-list'})

occupationtmp=[]
occupation=[]
dep_id=[]

# As with the age range (see STEP 1) each depute's occupation is not displayed in a table but in a title before each table
# The process of extracting the information will be the same as for age range

for row in table_occ.findAll('a'):
   if not (row.get("name")=='' or row.get("name")==None):
      occupationtmp=row.get("name")
   elif not (row.text=='' or row.text==None):
      dep_id.append(row.get("href").replace("/deputes/fiche/OMC_PA",""))
      occupation.append(occupationtmp)
   else:
      continue

df_occ = pd.DataFrame(
    {'Dep_ID': dep_id,
    'Cat SocioPro': occupation
    })

print df_occ.head(n=15)

## STEP 3 - EXTRACT LIST OF DEPUTES BY SEAT (INCLUDING ID) - NOTE: NON-EXHAUSTIVE LIST

url_seat = "http://www2.assemblee-nationale.fr/deputes/hemicycle"
page_seat = urllib2.urlopen(url_seat)
soup_seat = BeautifulSoup(page_seat,'html.parser')

table_seat = soup_seat.find('div', {'id': 'data'})

seat=[]
dep_id=[]

for row in table_seat.findAll("dl"):
   seat.append(row.get("data-place").replace("s","")) #seat is displayed as "s1", "s2"... so this value is cleaned up to keep only the seat number
   dep_id.append(row.get ("data-id"))

df_seat = pd.DataFrame(
    {'Siege': seat,
     'Dep_ID':dep_id
    })

print df_seat.head(n=15)

## STEP 4 - JOIN ALL DATAFRAMES TOGETHER USING DEPUTE ID AND EXPORT TO CSV

df = pd.merge(df_age, df_seat, on='Dep_ID', how='left')
df = pd.merge(df, df_occ, on='Dep_ID', how='left')

output_file = "deputes-info.csv"

df.to_csv(output_file,encoding='utf-8',index=False)

print df.head(n=15)

## DISPLAY RESULTS

print "df_age: [" + str(df_age.shape[0]) + " rows x " + str(df_age.shape[1]) + " columns]"
print "df_occ: [" + str(df_occ.shape[0]) + " rows x " + str(df_occ.shape[1]) + " columns]"
print "df_seat: ["  + str(df_seat.shape[0]) + " rows x " + str(df_seat.shape[1]) + " columns]"
print "df: ["  + str(df.shape[0]) + " rows x " + str(df.shape[1]) + " columns]"

print "df exported to csv as "  + output_file

