
from typing import TypeVar
import streamlit as st
StateT = TypeVar('StateT')

def persistent_game_state(initial_state: StateT) -> StateT:
    #session_id = st.session_state.get_report_ctx()#session_id
    session = st.session_state
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', initial_state)
    return session._gamestate
