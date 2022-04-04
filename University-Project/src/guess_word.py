import streamlit as st
import random
import json
import os


def get_word(language: str, length: int) -> str:
    with open(os.path.join('University-Project','src', 'assets', 'languagepl.json')) as raw:
        data = json.load(raw)[language]

    word = random.choice(data)

    while not 3 <= len(word) <= length or any(c in word for c in (' ', '-')):
        word = random.choice(data)

    return word


def set_space(only_len=False) -> int:
    word_len = len(st.session_state.word)
    if only_len:
        return word_len
    if word_len <= 5:
        return 5 - (word_len / 5)
    elif word_len <= 10:
        return 5 - (word_len / 5 + 0.5)
    else:
        return 5 - (word_len / 5 + 1)


def load_box():
    word = [c if c in st.session_state.guessed else '_' for c in st.session_state.word]
    for i in range(set_space(True)):
        guess_box[i + 1].button(word[i], key=i)


def init(language: str = 'Polski', length: int = 6, heart: int = 5, post_init=False):
    if not post_init:
        st.session_state.input = 0
        st.session_state.win = 0
    st.session_state.word = get_word(language, length)
    st.session_state.lives = heart
    st.session_state.guessed = []


def restart():
    init(
        st.session_state.language,
        st.session_state.length,
        st.session_state.heart,
        post_init=True,
    )
    st.session_state.input += 1


def main():
    global guess_box

    st.write(
        '''
        # 🔠 ZGAAAAAAAAAAAADNIJ SLOWO🤯🤯🤯🤯 🥵 🥵 🥵
        '''
    )

    if 'word' not in st.session_state:
        init()

    reset, win, lives, settings = st.columns([0.45, 0.3, 1, 1])
    guess_box = st.columns([set_space()] + [1] * set_space(True) + [set_space()])

    reset.button('Nowa gra', on_click=restart)

    with settings.expander('Opcje'):
        st.write('ZMIANA TYCH USTAWIEŃ ZRESETUJE TWOJĄ ROZGRYWKĘ:(')
        st.selectbox(
            'Wybierz język xD', ['Polski', 'Indonezyjski'], key='language', on_change=restart
        )
        st.select_slider(
            'Ile serduszek', list(range(1, 11)), 5, key='heart', on_change=restart
        )
        st.slider('Wybierz długość słowa', 3, 16, 6, key='length', on_change=restart)

    placeholder, debug = st.empty(), st.empty()
    guess = placeholder.text_input(
        'Zgadnij Literę', key=st.session_state.input, max_chars=1
    ).lower()

    if not guess or not guess.isalpha():
        debug.write('Proszę wpisz literę')
    elif guess in st.session_state.guessed:
        debug.warning(f"Już zgadywałeś **{guess}** 🛐🛐🛐")
    elif guess not in st.session_state.word:
        debug.warning(f"To słowo nie ma **{guess}** 🛐🛐🛐")
        st.session_state.lives -= 1
        st.session_state.guessed.append(guess)
    else:
        debug.info('DOBRA ODPOWIEDZ 😍 🥰😍 🥰😍 🥰')
        st.session_state.guessed.append(guess)

    if st.session_state.lives == 0:
        debug.error(f"**PRZEGRALES NOBIE🤣🤣🤣😂😂😂, słowo to: **{st.session_state.word}** 😓")
        placeholder.empty()
    elif all(c in st.session_state.guessed for c in st.session_state.word):
        debug.success(f"**ZWYCIĘŻYLES BOŻE JESTEŚ BOSKI!!!!!!🤩 🥳🤩 🥳 {st.session_state.word} 🎈")
        st.session_state.win += 1
        placeholder.empty()

    load_box()

    lives.button(
        f'{("❤️" * st.session_state.lives) if st.session_state.lives else "💀 porażka93023913"}'
    )
    win.button(f'🏆 {st.session_state.win}')

    st.button(
        f'{" ".join(st.session_state.guessed) if st.session_state.guessed else "Użyta litera412914"}'
    )


if __name__ == '__main__':
    main()
