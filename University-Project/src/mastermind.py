from typing import Tuple, NamedTuple, Union, List
import random
import dataclasses

import streamlit as st

from src.gamestate import persistent_game_state

DIGITS = ['0', '1', '2', '3', '4', '5']
K = 4


class Guess(NamedTuple):
    guess: str
    red: int
    white: int

    def show(self):
        st.write(f"{self.guess}, Białe {self.white}, Czerwone {self.red}")


@dataclasses.dataclass
class GameState:
    secret_code: str
    game_number: int = 0
    previous_guesses: Tuple[Guess, ...] = ()
    game_over: bool = False


state = GameState(''.join(random.choices(DIGITS, k=4)))


if st.button("NEW GAME"):
    state.secret_code = ''.join(random.choices(DIGITS, k=4))
    state.game_number += 1
    state.previous_guesses = ()
    state.game_over = False


# Don't use Union types!
def main():
    def parse_guess(guess: str) -> Union[str, List[str]]:
        if not all('0' <= c <= '5' for c in guess):
            return "POWIEDZIALEM **NUMERY POMIĘDZY 0 a 5!**"
        if len(guess) != K:
            return f"POWIEDZIALEM **{K}** KOD!"
        return list(guess)


    if not state.game_over:
        raw_guess = st.text_input(f"PROSZĘ ZGADNIJ {K} NUMERY KODU INACZAEJ ZGINĘ OKRUTNIE, NUMERY SĄ W ZAKRESIE OD 0 DO 5: ", key=state.game_number)
        guess = parse_guess(raw_guess) if raw_guess else ''

        if not guess and not state.previous_guesses:
            pass
        elif isinstance(guess, str):
            st.markdown(guess)
        else:
            white = 0  # correct color + correct location
            red = 0  # correct color + wrong location

            for i in range(K):
                if guess[i] == state.secret_code[i]:
                    white += 1
                    guess[i] = -1  # sentinel for "already counted as white"

            for i in range(K):
                if guess[i] == -1:
                    continue
                try:
                    idx = guess.index(state.secret_code[i])
                    red += 1
                    guess[idx] = -2  # sentinel for "already counted as red"
                except ValueError:
                    continue

            state.previous_guesses += (Guess(raw_guess, red, white),)

            if white == K:
                state.game_over = True
                st.markdown("MASZ TO WOOOOOO!!@!😻 😻 😻 🤩 🥳🤩 🥳!")
                st.markdown(f"ZAJĘLO CI TO TYLKO: {len(state.previous_guesses)} PRÓB")

            for previous_guess in reversed(state.previous_guesses):
                previous_guess.show()