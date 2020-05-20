import pandas as pd

# load data
mobility = pd.read_csv("C:/Users/lamps/Documents/COVID/data/applemobilitytrends-2020-05-18.csv")
cases = pd.read_csv("C:/Users/lamps/Documents/COVID/data/daily-by-state.csv")

# state list used to keep only US states ("region" in original data)
states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

# dictionary used to map state name to two-letter abbreviation
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

###########################
### Apple mobility data ###
###########################

# keep just US states
data = mobility[mobility.region.isin(states)]

# change 
data = data.replace({"region": us_state_abbrev})

# restrict data to only state and mobility data by date
data.drop(data.columns[[0, 2, 3, 4, 5]], axis=1, inplace=True)

# rename columns to remove dash
data.columns = data.columns.str.replace("-", "")

# pivot the data from wide to long
data = pd.wide_to_long(data, stubnames='2020', i='region', j='date')
data = data.reset_index() # turns index into two columns

# create days from 1/13 variables
data.date = data.date.astype(str)
data.days_from_jan13 = 0

data.loc[data.date.str.startswith("1"), 'days_from_jan13'] = data.date.astype(int) - 113
data.loc[data.date.str.startswith("2"), 'days_from_jan13'] = data.date.astype(int) - 213 + 31
data.loc[data.date.str.startswith("3"), 'days_from_jan13'] = data.date.astype(int) - 313 + 31 + 29
data.loc[data.date.str.startswith("4"), 'days_from_jan13'] = data.date.astype(int) - 413 + 31 + 29 + 31
data.loc[data.date.str.startswith("5"), 'days_from_jan13'] = data.date.astype(int) - 513 + 31 + 29 + 31 + 30
data.loc[data.date.str.startswith("6"), 'days_from_jan13'] = data.date.astype(int) - 613 + 31 + 29 + 31 + 30 + 31

data = data.rename(columns={"2020": "driving_mobility"})


#####################
### Daily US Data ###
#####################

# remove leading 5 digits from date
cases.date = cases.date.astype(str)
cases['date'] = cases['date'].str[5:8]

#############
### Merge ###
#############

merged = data.merge(cases, left_on=['region', 'date'], right_on=['state', 'date'])
merged = merged.fillna(0)
