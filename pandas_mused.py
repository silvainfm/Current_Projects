# Most used code bits: 

# import most used 
import pyforest
import pdfkit as pdf

# import the excel file or csv file
df = pd.read_csv('df.csv', parse_dates=True)
df = pd.read_excel('df.xlsx', parse_dates=True)

# changing the columns order by getting the list of cols and modifying it 
col_list = df.columns.tolist() # can also apply list(df.columns)
df = df[col_list]
# getting rows from df that are in a list
df = df[df['col'].isin(list)]
# getting the value counts for a comparison before comparing and storing the data
df['colA'].isin(df2['colB']).value_counts()
# getting one column in list form
colA_list = df['colA'].tolist()
# then comparing that list with another df's column (add ~ for NOT in)
new_df = df2[df2['colB'].isin(colA_list)]


# making string values lowercase for keyword match
df['col'] = df['col'].str.lower()

# renaming a df column
df.rename(columns={'old_col': 'new_col'}, inplace=True)
# renaming a list of columns
newcolumns1 = {}
for key in old_columns:
    for value in new_columns:
        newcolumns1[key] = value
        new_columns.remove(value)
        break
df.rename(columns=newcolumns1,inplace=True)

# getting all rows containing any value in a list of keywords
list_keywords ={}
key_df = df[df.stack().str.contains('|'.join(list_keywords)).any(level=0)]

# locating rows based on condition 
newdf = df.loc[df['col'] == 'condition']
# multiple conditions
df.loc[(df["B"] > 50) & (df["C"] == 900)]
# using loc as a way to assign values in a new column based on condition
df.loc[(df['column'] > 'condition'), 'new_column'] = 'value'

# return wanted result based on condition
df['newcol'] = np.where(df['column'] == 'condition', 'result if yes', 'result if no')

# transpose a df making the rows columns or vice versa
df2 = df.T

# converting to datetime format
df['col'] = pd.to_datetime(df['col'], format='YYYY-MM-DD').date()

# getting columns in df and df2 
df.columns.intersection(df2.columns)
# columns in df and not in df2 
df.columns.difference(df2.columns)

# getting only certain columns from a df 
df_some = df[['colA', 'colB']]
# dropping duplicates in a df
df.drop_duplicates(keep='first', inplace=True) 

# merging 2 dfs based on 1 column or appending a df to another
merged_df = pd.merge(df, df2, on=['same_col'], how='inner')
appended_df = df.append(df1)

# sorting a df by a certain column and setting a column as the index 
df = df.sort_values(by=['col']) 
df = df.set_index('col')

# select cols by dtypes
# select just object columns
df.select_dtypes(include='object')
# select multiple data types
df.select_dtypes(include=['int', 'datetime', 'object'])
# exclude certain data types
df.select_dtypes(exclude='int')

# drop duplicates
df.drop_duplicates('col', keep = 'first') #can be 'last'
# dropping rows if NaN are present
df.dropna(axis = 0)
# dropping cols if NaN are present
df.dropna(axis = 1)
#dropping col in which more than 10% of values are NaN
df.dropna(thresh=len(df)*0.9, axis=1)
# replaing NaN with previous rows' value
df.fillna(axis=0, method='ffill') #or bfill for next row
# replaing NaN with previous cols' value
df.fillna(axis=1, method='ffill')

# to excel or csv for a df
df.to_excel('df_name.xlsx') or df.to_csv('df_name.csv')

# to html to then convert to a pdf
result = df.to_html()
# write html to file
text_file = open("index.html", "w")
text_file.write(result)
text_file.close()