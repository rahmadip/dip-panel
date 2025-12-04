import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection
import bcrypt


def check_password(
    password: str,
    hashed_password: str
) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

if not st.session_state.authenticated:
    with st.sidebar:
        input_password = st.text_input(
            'Password',
            type='password',
            key='input_password',
            label_visibility='collapsed',
            placeholder='Key'
        )
        if st.button(
            'Login',
            width='stretch'
        ):
            try:
                hp = st.secrets['hp']
            except Exception:
                st.toast(
                    'Key not found',
                    icon='🚨',
                    duration='infinite'
                )
                st.stop()
            if check_password(input_password, hp):
                st.session_state.authenticated = True
                st.session_state.failed_attempts = 0
                st.toast(
                    'Login successful',
                    icon='🔓',
                    duration='infinite'
                )
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.toast(
                    'Login failed',
                    icon='🔐',
                    duration='infinite'
                )
                if st.session_state.failed_attempts >= 10:
                    st.toast(
                        'Possible unauthorized attempt',
                        icon='🔐',
                        duration='infinite'
                    )
    st.stop() 

def logout():
    st.session_state.authenticated = False
    st.session_state.failed_attempts = 0
    st.toast(
        'Logged out successfully',
        icon='🔒',
        duration='infinite'
    )

@st.cache_resource
def connection():
    try:
        return st.connection(
            'supabase',
            type=SupabaseConnection
        )
    except Exception as error:
        st.toast(
            error,
            icon='🚨',
            duration='infinite'
        )
        st.stop()

@st.cache_data(ttl=600)
def fetch(
    table: str,
    primary: str
):
    try:
        select = (
            connection()
            .table(table)
            .select('*')
            .order(primary, desc=False)
            .execute()
        )
        df = select.data
        return pd.DataFrame(df)
    except Exception as error:
        st.toast(
            error,
            icon='🚨',
            duration='infinite'
        )
        return pd.DataFrame()

def commit(
    table: str,
    primary: str,
    data_changes: dict,
    original_data: pd.DataFrame
):
    st.toast(
        'Executing Commit',
        icon='🔨',
        duration='infinite'
    )
    changes_committed = False
    if data_changes['deleted_rows']:
        for row_idx in data_changes['deleted_rows']:
            pk_value = original_data.iloc[row_idx][primary]
            try:
                delete = (
                    connection()
                    .table(table)
                    .delete()
                    .eq(primary, pk_value)
                    .execute()
                )
                st.toast(
                    'Successfully delete data',
                    icon='🗑️',
                    duration='infinite'
                )
                changes_committed = True
            except Exception as error:
                st.toast(
                    f'Failed to delete data | {error}',
                    icon='🚨',
                    duration='infinite'
                )
    if data_changes['edited_rows']:
        for row_idx, updates in data_changes['edited_rows'].items():
            pk_value = original_data.iloc[row_idx][primary]
            updateData = {
                key: value for key,
                value in updates.items() if key != primary
            }
            if updateData:
                try:
                    update = (
                        connection()
                        .table(table)
                        .update(updateData)
                        .eq(primary, pk_value)
                        .execute()
                    )
                    st.toast(
                        'Successfully update data',
                        icon='📝',
                        duration='infinite'
                    )
                    changes_committed = True
                except Exception as error:
                    st.toast(
                        f'Failed to update data | {error}',
                        icon='🚨',
                        duration='infinite'
                    )  
    if data_changes['added_rows']:
        for new_row in data_changes['added_rows']:
            insertData = {
                key: value for key,
                value in new_row.items() if key != primary
            }
            try:
                insert = (
                    connection()
                    .table(table)
                    .insert(insertData)
                    .execute()
                )
                st.toast(
                    'Successfully insert data',
                    icon='📑',
                    duration='infinite'
                )
                changes_committed = True
            except Exception as error:
                st.toast(
                    f'Failed to insert data | {error}',
                    icon='🚨',
                    duration='infinite'
                )
    if changes_committed:
        st.cache_data.clear()
        return True
    return False