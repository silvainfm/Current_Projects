# import libraries (pyforest includes pandas and numpy...)
import pyforest
import pdfkit as pdf

# import the excel file or csv file
#chase_df = pd.read_csv('.csv', parse_dates=True))
chase_df = pd.read_excel('sales_data', parse_dates=True)

# getting a list of the columns of the df and rearrange
col_list = chase_df.columns.tolist()

# fill the NAs with 0 for easier manipulation
chase_df = chase_df.fillna(0)

# getting only the columns wanted
chase_df = chase_df[col_list]

# rename columns 
chase_df.columns = []

# get columns that need to be analyzed in list
newcols = []

# list of states to find in the excel: 
states = [] 
'''
'Alabama’, ‘Alaska’, ‘American Samoa’, ‘Arizona’, ‘Arkansas’, ‘California’, ‘Colorado’, ‘Connecticut’, ‘Delaware’, ‘District of Columbia’, ‘Florida’, ‘Georgia’, 
‘Guam’, ‘Hawaii’, ‘Idaho’, ‘Illinois’, ‘Indiana’, ‘Iowa’, ‘Kansas’, ‘Kentucky’, ‘Louisiana’, ‘Maine’, ‘Maryland’, ‘Massachusetts’, ‘Michigan’, ‘Minnesota’, 
‘Minor Outlying Islands’, ‘Mississippi’, ‘Missouri’, ‘Montana’, ‘Nebraska’, ‘Nevada’, ‘New Hampshire’, ‘New Jersey’, ‘New Mexico’, ‘New York’, ‘North Carolina’, 
‘North Dakota’, ‘Northern Mariana Islands’, ‘Ohio’, ‘Oklahoma’, ‘Oregon’, ‘Pennsylvania’, ‘Puerto Rico’, ‘Rhode Island’, ‘South Carolina’, ‘South Dakota’, ‘Tennessee’, 
‘Texas’, ‘U.S. Virgin Islands’, ‘Utah’, ‘Vermont’, ‘Virginia’, ‘Washington’, ‘West Virginia’, ‘Wisconsin’, ‘Wyoming’
‘AK’, ‘AL’, ‘AR’, ‘AS’, ‘AZ’, ‘CA’, ‘CO’, ‘CT’, ‘DC’, ‘DE’, ‘FL’, ‘GA’, ‘GU’, ‘HI’, ‘IA’, ‘ID’, ‘IL’, ‘IN’, ‘KS’, ‘KY’, ‘LA’, ‘MA’, ‘MD’, ‘ME’, ‘MI’, ‘MN’, 
‘MO’, ‘MP’, ‘MS’, ‘MT’, ‘NC’, ‘ND’, ‘NE’, ‘NH’, ‘NJ’, ‘NM’, ‘NV’, ‘NY’, ‘OH’, ‘OK’, ‘OR’, ‘PA’, ‘PR’, ‘RI’, ‘SC’, ‘SD’, ‘TN’, ‘TX’, ‘UM’, ‘UT’, ‘VA’, ‘VI’, 
‘VT’, ‘WA’, ‘WI’, ‘WV’, ‘WY’
'''
# create dictionary to hold keywords for each category
keyword_dic = {}

# get all row containing list of keywords
def get_allrows(df, keylist):
    new_df = df[df.stack().str.contains('|'.join(keylist)).any(level=0)]
    return new_df 

# sort a df by column
def sort_df(df, column):
    df.sort_values(by = column, inplace = True, ascending = True)
    return df
    
# lowercase all the words in columns in list
def strlow(df, newcol): 
    for c in newcol:
        df[c] = df[c].str.lower()

# getting the keyword count per category
def getkcount(df, category, listcol):
    for col in listcol:
        df[col+'_'+category+'_kcount'] = sum([df[col].str.contains(keyword) for keyword in keyword_dic[category]]).astype(float)
    df = df.fillna(0)
    # getting total kcount 
    df[category+'_total_kcount'] = (df['col1_'+category+'_kcount'] + df['col2_'+category+'_kcount'] + 
    df['col3_'+category+'_kcount'] + df['col4_'+category+'_kcount'] + df['col5_'+category+'_kcount'] +
    df['col6_'+category+'_kcount'] + df['col7_'+category+'_kcount'] + 
    df['col8_'+category+'_kcount'] + df['col9_'+category+'_kcount'])
    return df

# get rows based on multiple kcount columns and a count parameter
def loc_any_kcount(df, k, count): #k= category
    df = df.loc[(df['col1_'+k+'_kcount'] > count) | (df['col2_'+k+'_kcount'] > count) | (df['col3_'+k+'_kcount'] > count) | 
    (df['col4_'+k+'_kcount'] > count) | (df['col5_'+k+'_kcount'] > count) | (df['col6_'+k+'_kcount'] > count) | 
    (df['col7_'+k+'_kcount'] > count) | (df['col8_'+k+'_kcount'] > count) | (df['col9_'+k+'_kcount'] > count)]
    df = df.sort_values(by = [k+'_total_kcount'], inplace = True, ascending = False)
    return df

# get the total kcount based on a count parameter
def loc_total_kcount(df, category, count): 
    df = df.loc[(df[category + '_total_kcount'] > count)]
    return df

# create word count columns for wanted columns
for col in newcols: 
    chase_df[col+'_wcount'] = chase_df[col].apply(lambda x: len(str(x).split(' ')))

# function to set index before exporting
def setindex(df, columnI):
    df = df.set_index(columnI)
    return df


writer = pd.ExcelWriter('excel_name.xlsx', engine='xlsxwriter')

#move the different dfs to excel 
chase_df1.to_excel(writer, sheet_name = 'category1')

chase_df2.to_excel(writer, sheet_name = 'category2')

chase_df3.to_excel(writer, sheet_name = 'category3')

chase_df.to_excel(writer, sheet_name = 'Full_data')

writer.save(
