import streamlit as st
from streamlit_app import fetch, commit, logout

PAGE_NAME = 'Space'
TABLE_NAME = 'svg' 
PRIMARY_KEY = 'id'  
EDITOR_KEY = 'panel_svg'
DF_DATA = 'df_svg'

if 'needs_reload' not in st.session_state:
    st.session_state.needs_reload = False

if 'authenticated' in st.session_state and st.session_state.authenticated:
    if DF_DATA not in st.session_state:
        st.session_state[DF_DATA] = fetch(TABLE_NAME, PRIMARY_KEY)

if DF_DATA in st.session_state:
    original_df = st.session_state[DF_DATA].copy()
else:
    st.stop()

def handle_commit():
    if EDITOR_KEY in st.session_state and (
        st.session_state[EDITOR_KEY]['edited_rows'] or
        st.session_state[EDITOR_KEY]['added_rows'] or
        st.session_state[EDITOR_KEY]['deleted_rows']
    ):
        data_changes = st.session_state[EDITOR_KEY]
        if commit(
            TABLE_NAME,
            PRIMARY_KEY,
            data_changes,
            original_df
        ):
            st.session_state.needs_reload = True
    else:
        st.toast(
            'No changes detected to commit.',
            icon='🚨',
            duration='infinite'
        )

def logoutAndClear():
    if DF_DATA in st.session_state:
        del st.session_state[DF_DATA]
    if EDITOR_KEY in st.session_state:
        del st.session_state[EDITOR_KEY]
    logout()
    st.session_state.needs_reload = True

st.set_page_config(
    layout='wide',
    page_title=f'DIP Panel | {PAGE_NAME}',
    page_icon='📙'
)

if st.session_state.needs_reload:
    st.session_state.needs_reload = False
    st.rerun()

with st.sidebar:
    st.button(
        'Logout',
        on_click=logoutAndClear,
        type='secondary',
        width='stretch'
    )
       
c1, c2 = st.columns([3,1])
with c1:
    header = st.container(border=True)
    with header:
        st.header(
            f'ADMIN PANEL PAGE: {PAGE_NAME}',
            divider='orange'
        )
        st.markdown(f'''
            :orange-badge[:material/link: https://rahmadip.github.io/profile/]
            :blue-badge[:material/table: {TABLE_NAME}]
            :green-badge[:material/key: {PRIMARY_KEY}]
        ''')
    edited_df = st.data_editor(
        original_df,
        key=EDITOR_KEY,                   
        num_rows='dynamic',
        height=650,
        hide_index=False
    )
with c2:
    log = st.container(
        border=True,
        height='stretch'
    )
    with log:
        st.header(
            'Changes Log',
            divider='orange'
        )
        st.markdown("Changes detected by `st.data_editor`:")
        if EDITOR_KEY in st.session_state:
            st.json(
                st.session_state[EDITOR_KEY],
                expanded=True
            )
        else:
            st.toast(
                'No interaction with the data editor',
                icon='🚨',
                duration='infinite'
            )
    st.button(
        'Commit Changes',
        on_click=handle_commit,
        width='stretch'
    )