import streamlit as st
from supabase import create_client


# BASE FUNCTION ---
def selectTable(table:str):
    url = st.secrets['url']
    key = st.secrets['key']
    db = create_client(url,key)
    execute = (
        db.table(table)
        .select('*')
        .execute()
    )
    df = execute.data
    return df

def updateTable(
    table:str,
    column:str,
    value:str,
    rowid
):
    url = st.secrets['url']
    key = st.secrets['key']
    db = create_client(url,key)
    execute = (
        db.table(table)
        .update({f'{column}':f'{value}'})
        .eq('id', rowid)
        .execute()
    )


# DATA TABLE
dataProject = selectTable('project')
dataProfile = selectTable('profile')
dataMessage = selectTable('message')


# FUNCTION AND COMPONENT PROFILE
def updateImage(column):
    st.image(dataProfile[0][column])
    update = st.text_input(label=f':red[**{column}**] : {dataProfile[0][column]}',label_visibility='collapsed')
    status = st.progress(0)
    if st.button(f'commit {column}',width='stretch'):
        status.progress(40)
        updateTable(
            table='profile',
            column=column,
            value=update,
            rowid=1
        )
        status.progress(100)
        st.rerun()

def updateProfile(column):
    update = st.text_input(label=f':red[**{column}**] : {dataProfile[0][column]}')
    status = st.progress(0)
    if st.button(f'commit {column}',width='stretch'):
        status.progress(40)
        updateTable(
            table='profile',
            column=column,
            value=update,
            rowid=1
        )
        status.progress(100)
        st.rerun()

def updateAbout(column):
    update = st.text_area(label=f':red[**{column}**] : {dataProfile[0][column]}')
    status = st.progress(0)
    if st.button(f'commit {column}',width='stretch'):
        status.progress(40)
        updateTable(
            table='profile',
            column=column,
            value=update,
            rowid=1
        )
        status.progress(100)
        st.rerun()


# LAYOUT ---
st.set_page_config(
    page_title='rahmadip Panel',
    page_icon=':material/chess_knight:',
    layout='wide'
)

project,profile,messages = st.tabs(['PROJECT','PROFILE','MESSAGES'])
with project:
    tableProjectC, crudPanel = st.columns([4,1])
    with tableProjectC:
        tableProjectPanel = st.dataframe(
            dataProject,
            height=695,
            row_height=50
        )
    with crudPanel:
        updateProject,insertProject,deleteProject = st.tabs(['UPDATE','INSERT','DELETE'])
        with updateProject:
            columnUpdateProject = st.selectbox('Column target',options=dataProject[0].keys())
            rowUpdateProject = st.selectbox('Row target berdasarkan id', options=[row['id'] for row in dataProject])
            valueUpdateProject = st.text_input('Value update')
            statusUpdateProject = st.progress(0)
            if st.button('UPDATE PROJECT',width='stretch'):
                updateTable(
                    table='project',
                    column=columnUpdateProject,
                    value=valueUpdateProject,
                    rowid=rowUpdateProject
                )
                statusUpdateProject.progress(100)
                st.rerun()

with profile:
    profileC2 = st.container()
    with profileC2:
        profileC2a,profileC2b,profileC2c = st.columns(3)
        with profileC2a:
            updateProfile('name')
        with profileC2b:
            updateProfile('occupation')
        with profileC2c:
            updateProfile('domicile')
    st.divider()
    profileC3 = st.container()
    with profileC3:
        profileC3a,profileC3b,profileC3c = st.columns(3)
        with profileC3a:
            updateProfile('email')
        with profileC3b:
            updateProfile('number')
        with profileC3c:
            updateProfile('linkedin')
    st.divider()
    profileC4 = st.container()
    with profileC4:
        profileC4a,profileC4b,profileC4c = st.columns(3)
        with profileC4a:
            updateProfile('behance')
        with profileC4b:
            updateProfile('instagram')
        with profileC4c:
            updateProfile('discord')
    st.divider()
    profileC1 = st.container()
    with profileC1:
        profileC1a,profileC1b,profileC1c = st.columns(3)
        with profileC1a:
            updateImage('banner')
        with profileC1b:
            updateImage('photo')
        with profileC1c:
            updateAbout('about')
with messages:
    st.table(dataMessage,border='horizontal')