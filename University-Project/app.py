from typing import TypeVar

import dataclasses
from PIL import Image

import streamlit as st
from src import home, guess_word, madlibs, hangchicken, guess_number, tic_tac_toe, mastermind, gamestate

def init():
    st.session_state["page"] = 'Dom'
    st.session_state["project"] = False
    st.session_state["game"] = False

    st.session_state["pages"] = {
        'Dom': home.main,
        'Zgadnij Słowo': guess_word.main,
        'Madlibs': madlibs.main,
        'PowieśKuraka': hangchicken.main,
        'Zgadnij numer': guess_number.main,
        '🥶VS😎': tic_tac_toe.main,
        '!MISTRZ UMYSLU!': mastermind.main,
        }


def draw_style():
    st.set_page_config(page_title='MASNA STRONA\'s Project', page_icon='https://bi.im-g.pl/im/7b/aa/1a/z27960187Q,Boxdel.jpg',initial_sidebar_state="auto", menu_items={'About': "giga op stona w skrucie es"})


    style = """
        <style>
            header {visibility: visible;}
            footer {visibility: hidden;}
        </style>

    """

    st.markdown(style, unsafe_allow_html=True)


def load_page():
    st.session_state["pages"][st.session_state["page"]]()


def set_page(loc=None, reset=False):
    if not st.session_state["page"] == 'Dom ':
        for key in list(st.session_state.keys()):
            if key not in ('page', 'project', 'game', 'pages', 'set'):
                st.session_state.pop(key)

    if loc:
        st.session_state["page"] = loc
    else:
        st.session_state["page"] = st.session_state.set

    if reset:
        st.session_state["project"] = False
    elif st.session_state["page"] in ('Message me', 'About me'):
        st.session_state["project"] = True
        st.session_state["game"] = False
    else:
        pass


def change_button():
    set_page('Zgadnij Słowo')
    st.session_state["game"] = True
    st.session_state["project"] = True


def main():
    if 'page' not in st.session_state:
        init()

    with st.sidebar:
        project, about, source = st.columns([1.2, 1, 1])
        contact = st.columns([0.2, 1])

        if not st.session_state["project"]:
            project.button('😍😍😍MASNE GRY!@!@!😍😍', on_click=change_button)
        else:
            project.button('🏠 Dom', on_click=set_page, args=('Dom', True))

        if st.session_state["project"] and st.session_state["game"]:
            st.selectbox(
                'List of projects',
                [ 'Zgadnij Słowo','Madlibs','PowieśKuraka','Zgadnij numer', '🥶VS😎','!MISTRZ UMYSLU!' ],
                key='set',
                on_change=set_page,
            )
    if st.session_state.page == 'Dom':
        st.image('https://c.tenor.com/fduJnRpzsvoAAAAd/masny-ben.gif')
    if st.session_state.page == 'PowieśKuraka':
            st.image('https://c.tenor.com/KalHR7-z7MsAAAAi/masno-masnoni.gif')
    if st.session_state.page == '!MISTRZ UMYSLU!':
            st.image('https://c.tenor.com/-JWN77jPOS0AAAAi/hamood-hamood-habibi.gif')

    load_page()


if __name__ == '__main__':
    main()
