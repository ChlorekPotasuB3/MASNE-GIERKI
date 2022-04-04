import streamlit as st
import random


def get_number(length: int) -> int:
    return random.randint(1, length)


def init(length: int = 100, post_init=False):
    if not post_init:
        st.session_state.input = 0
        st.session_state.win = 0
    st.session_state.number = get_number(length)
    st.session_state.tries = 0
    st.session_state.over = False


def restart():
    init(st.session_state.length, post_init=True)
    st.session_state.input += 1


def main():
    st.write(
        """
        4️⃣2️⃣0️⃣ZGAAAADNIJ LICZBĘ6️⃣9️⃣
        """
    )

    if 'number' not in st.session_state:
        init()

    reset, win, set_range = st.columns([0.39, 1, 1])
    reset.button('Nowa Gra', on_click=restart)

    with set_range.expander('Opcje'):
        st.select_slider(
            'ustaw maksymalną długość',
            [10**i for i in range(1, 6)],
            value=100,
            key='length',
            on_change=restart,
        )

    placeholder, debug = st.empty(), st.empty()
    guess = placeholder.number_input(
        f'wpisz swoje odpowiedzi od 1 - {st.session_state.length}',
        key=st.session_state.input,
        min_value=0,
        max_value=st.session_state.length,
    )

    if guess:
        st.session_state.tries += 1
        if guess < st.session_state.number:
            debug.warning(f'{guess} jest za małe!!!')
        elif guess > st.session_state.number:
            debug.warning(f'{guess} jest za duże mordo!!!')
        else:
            debug.success(
                f'DOBRA ROBOTA MORDZIATY😎😎😎😎 {st.session_state.tries} prób 🎈'
            )
            st.session_state.over = True
            st.session_state.win += 1
            placeholder.empty()

    win.button(f'🏆 {st.session_state.win}')


if __name__ == '__main__':
    main()