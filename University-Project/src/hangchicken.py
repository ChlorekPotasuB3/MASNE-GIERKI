from typing import List, Tuple
from string import ascii_lowercase
import types
import random
import dataclasses

import streamlit as st
# import app

# from app import state
from src.gamestate import persistent_game_state

# from app import session

PROTOTYPE = """
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╣
 ┃ ╨ ╨
 ┻━━━━
"""

STEPS = [
    """
     ┏━━┑
     ┃
     ┃
     ┃
     ┃
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O
     ┃
     ┃
     ┃
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O>
     ┃
     ┃
     ┃
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O>
     ┃ ╔╧╗
     ┃ ╚═╝
     ┃
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O>
     ┃>╦╧╗
     ┃ ╚═╝
     ┃
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O>
     ┃>╦╧╦<
     ┃ ╚═╝
     ┃
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O>
     ┃>╦╧╦<
     ┃ ╠═╝
     ┃ ╨
     ┻━━━━
    """,
    """
     ┏━━┑
     ┃  O>
     ┃>╦╧╦<
     ┃ ╠═╣
     ┃ ╨ ╨
     ┻━━━━
    """
]

MIN_LENGTH = 3
MAX_LENGTH = 8


@st.cache
def get_words() -> List[str]:
    with open('1000words.txt') as f:
        words = [line.strip() for line in f]

    words = [w for w in words if MIN_LENGTH <= len(w) <= MAX_LENGTH]
    words = [w for w in words if all('a' <= c <= 'z' for c in w)]

    return words


@dataclasses.dataclass
class GameState:
    game_number: int
    word: str
    guessed: Tuple[str, ...] = ()
    step: int = 0
    game_over: bool = False


def main():
    state = persistent_game_state(initial_state=GameState(0, random.choice(get_words())))
    if st.button("Nowa gra"):
        state.guessed = ()
        state.step = 0
        state.game_number += 1
        state.word = random.choice(get_words())
        state.game_over = False

    if not state.game_over:
        guess = st.text_input("zgadnij literę", max_chars=1, key=state.game_number)

        if not guess:
            st.write("ładnie proszę zgadnij")
        elif guess < 'a' or guess > 'z':
            st.write("please guess a lowercase letter!")
        elif guess in state.guessed:
            st.write(f"już zgadłeś **{guess}**")
        elif guess not in state.word:
            st.write(f"słowo nie ma **{guess}**")
            state.step += 1
            state.guessed += (guess,)
        else:
            st.write("dobry strzał😎")
            state.guessed += (guess,)

    if state.step == len(STEPS) - 1:
        st.markdown(f"PRZEGRALES NOBIE🤣🤣🤣😂😂😂, słowo to: **{state.word}**")
        state.game_over = True
    elif all(c in state.guessed for c in state.word):
        st.markdown(f"**ZWYCIĘŻYLES BOŻE JESTEŚ BOSKI!!!!!!🤩 🥳🤩 🥳**")
        state.game_over = True

    # Show the chicken
    st.text(STEPS[state.step])

    # Show the word
    chars = [c if c in state.guessed else "_" for c in state.word]
    st.text(" ".join(chars))

    # Show the guessed letters
    st.text(f'wpisane litery: {" ".join(state.guessed)}')


if __name__ == '__main__':
    main()
