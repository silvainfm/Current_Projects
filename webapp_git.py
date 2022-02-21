import pandas as pd
import streamlit as st
import pdfkit as pdf

st.set_page_config(page_title='WebApp Dashboard', page_icon=':bar_chart:', layout='wide')

# ---- MAINPAGE ----
st.title(':bar_chart: Post-Show Dashboard')
st.markdown('##')

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel(sheet):
    df = pd.read_excel(
        io = 'excel_name.xlsx',
        engine = 'openpyxl',
        sheet_name = sheet)
    df = df.astype(str)
    return df

df = get_data_from_excel('Sheet1')

# ---- SIDEBAR ----
st.sidebar.header('Please Filter Here:')

# filter by unique states contained in the excel
state = st.sidebar.multiselect('Select the State:',
    options=df['State'].unique(),
    default=df['State'].unique() )

# filter by unique rankings contained in the excel
score1 = st.sidebar.multiselect('Select the score 1:',
    options=df['ranking1'].unique(),
    default=df['ranking1'].unique() )

score2 = st.sidebar.multiselect('Select the score 2:',
    options=df['ranking2'].unique(),
    default=df['ranking2'].unique() )

# query the user's selection
df_selection = df.query('(State == @state) & (ranking1 == @score1) & (ranking2 == @score2)')

# show the df with the user's selection
st.dataframe(df_selection)

# CSV Download button 
st.download_button(label = 'Export current selection to CSV', data = df_selection.to_csv(), mime='text/csv')

# To PDF function
def to_pdf(df, variable, pdf_list):
    # loc the row of the variable we want
    pdf1 = df.loc[df['variable'] == variable]
    pdf1 = pdf1.set_index('variable')
    pdf1 = pdf1[pdf_list]

    # transpose df
    pdf1 = pdf1.T

    # convert to html to then convert to pdf
    result = pdf1.to_html(f'{variable}_ht.html', render_links = True) 
    pdf_name = f'{variable}_report.pdf'
    pdf.from_file([f'{variable}_ht.html'], pdf_name)
    return result

# columns wanted in the pdfs

columns_wanted = []
# user selection for one or multiple pdfs
company_bull = st.radio('Do you want to transfer the current selection to pdf or just one variable?', ('Current Selection', '1 variable'))

if company_bull == 'Current Selection':
    button_pdfy = st.button('Export selection to PDF')
    if button_pdfy:
        companies = df_selection['variable'].to_list()
        for c in companies:
            to_pdf(df_selection, c, columns_wanted) 
else: 
    variable = st.text_input('Which variable do you want to export to PDF?')
    button_pdf = st.button('Export to PDF')
    if button_pdf: 
        to_pdf(df_selection, variable, columns_wanted)