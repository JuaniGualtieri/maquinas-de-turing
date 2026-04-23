from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple


Transition = Dict[Tuple[str, str], Tuple[str, str, str]]


@dataclass
class RunResult:
    raw_tape: str
    tape: str
    halted: bool
    accepted: Optional[bool]
    steps: int
    final_state: str


class TuringMachine:
    def __init__(
        self,
        transitions: Transition,
        start_state: str,
        blank: str = "_",
        accept_states: Optional[Set[str]] = None,
        reject_states: Optional[Set[str]] = None,
        halt_states: Optional[Set[str]] = None,
    ) -> None:
        self.transitions = transitions
        self.start_state = start_state
        self.blank = blank
        self.accept_states = accept_states or set()
        self.reject_states = reject_states or set()
        self.halt_states = halt_states or set()

    def run(self, input_str: str, max_steps: int = 10000) -> RunResult:
        tape: List[str] = list(input_str) if input_str else [self.blank]
        head = 0
        state = self.start_state
        steps = 0

        while steps < max_steps:
            if state in self.halt_states or state in self.accept_states or state in self.reject_states:
                break

            if head < 0:
                tape.insert(0, self.blank)
                head = 0
            elif head >= len(tape):
                tape.append(self.blank)

            symbol = tape[head]
            key = (state, symbol)
            if key not in self.transitions:
                break

            next_state, write_symbol, move = self.transitions[key]
            tape[head] = write_symbol
            state = next_state

            if move == "R":
                head += 1
            elif move == "L":
                head -= 1
            elif move != "S":
                raise ValueError(f"Movimiento invalido: {move}")

            steps += 1

        halted = (
            state in self.halt_states
            or state in self.accept_states
            or state in self.reject_states
            or steps >= max_steps
            or (state, tape[head] if 0 <= head < len(tape) else self.blank) not in self.transitions
        )

        # Recorta blancos laterales para devolver solo el contenido util de cinta.
        raw_content = "".join(tape)
        content = "".join(tape).strip(self.blank)

        accepted: Optional[bool] = None
        if state in self.accept_states:
            accepted = True
        elif state in self.reject_states:
            accepted = False

        return RunResult(
            raw_tape=raw_content,
            tape=content,
            halted=halted,
            accepted=accepted,
            steps=steps,
            final_state=state,
        )


def mt_desplazar_derecha_ab() -> TuringMachine:
    """
    Ejercicio 1: Desplaza una cadena sobre {a,b} una celda a la derecha.
    Ejemplo: aba -> _aba (en contenido util queda aba con un blanco a la izquierda en la cinta).
    """
    transitions: Transition = {
        ("q0", "a"): ("qA", "_", "R"),
        ("q0", "b"): ("qB", "_", "R"),
        ("q0", "_"): ("halt", "_", "S"),

        ("qA", "a"): ("qA", "a", "R"),
        ("qA", "b"): ("qB", "a", "R"),
        ("qA", "_"): ("halt", "a", "S"),

        ("qB", "a"): ("qA", "b", "R"),
        ("qB", "b"): ("qB", "b", "R"),
        ("qB", "_"): ("halt", "b", "S"),
    }
    return TuringMachine(transitions, start_state="q0", halt_states={"halt"})


def mt_duplicar_ceros() -> TuringMachine:
    """
    Ejercicio 2: Duplica una cadena 0^n -> 0^(2n).
    Usa marcas X para originales procesados y Y para copias.
    """
    transitions: Transition = {
        # Buscar un 0 original sin marcar.
        ("q_find", "0"): ("q_seek_end", "X", "R"),
        ("q_find", "X"): ("q_find", "X", "R"),
        ("q_find", "Y"): ("q_find", "Y", "R"),
        ("q_find", "_"): ("q_rewind", "_", "L"),

        # Ir al final para agregar una copia marcada Y.
        ("q_seek_end", "0"): ("q_seek_end", "0", "R"),
        ("q_seek_end", "X"): ("q_seek_end", "X", "R"),
        ("q_seek_end", "Y"): ("q_seek_end", "Y", "R"),
        ("q_seek_end", "_"): ("q_back", "Y", "L"),

        # Volver al inicio.
        ("q_back", "0"): ("q_back", "0", "L"),
        ("q_back", "X"): ("q_back", "X", "L"),
        ("q_back", "Y"): ("q_back", "Y", "L"),
        ("q_back", "_"): ("q_find", "_", "R"),

        # Reposicionarse al inicio para restaurar.
        ("q_rewind", "0"): ("q_rewind", "0", "L"),
        ("q_rewind", "X"): ("q_rewind", "X", "L"),
        ("q_rewind", "Y"): ("q_rewind", "Y", "L"),
        ("q_rewind", "_"): ("q_restore", "_", "R"),

        # Restaurar marcas y terminar.
        ("q_restore", "X"): ("q_restore", "0", "R"),
        ("q_restore", "Y"): ("q_restore", "0", "R"),
        ("q_restore", "0"): ("q_restore", "0", "R"),
        ("q_restore", "_"): ("halt", "_", "S"),
    }
    return TuringMachine(transitions, start_state="q_find", halt_states={"halt"})


def mt_aceptar_01_estrella_0() -> TuringMachine:
    """
    Ejercicio 3: Acepta lenguaje L = { w in {0,1}* | w = 01*0 }.
    """
    transitions: Transition = {
        ("q0", "0"): ("q1", "0", "R"),
        ("q0", "1"): ("reject", "1", "S"),
        ("q0", "_"): ("reject", "_", "S"),

        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "0"): ("q2", "0", "R"),
        ("q1", "_"): ("reject", "_", "S"),

        ("q2", "_"): ("accept", "_", "S"),
        ("q2", "0"): ("reject", "0", "S"),
        ("q2", "1"): ("reject", "1", "S"),
    }
    return TuringMachine(
        transitions,
        start_state="q0",
        accept_states={"accept"},
        reject_states={"reject"},
    )


def mt_paridad_ones() -> TuringMachine:
    """
    Ejercicio 4: Agrega al final 0 si la cantidad de 1 es par, 1 si es impar.
    """
    transitions: Transition = {
        ("q_even", "0"): ("q_even", "0", "R"),
        ("q_even", "1"): ("q_odd", "1", "R"),
        ("q_even", "_"): ("halt", "0", "S"),

        ("q_odd", "0"): ("q_odd", "0", "R"),
        ("q_odd", "1"): ("q_even", "1", "R"),
        ("q_odd", "_"): ("halt", "1", "S"),
    }
    return TuringMachine(transitions, start_state="q_even", halt_states={"halt"})


def mt_copiar_abc() -> TuringMachine:
    """
    Ejercicio 5: Copia una cadena sobre {a,b,c}: w -> ww.
    Usa marcas A/B/C para originales y x/y/z para copias.
    """
    transitions: Transition = {
        # Buscar proximo simbolo original sin marcar.
        ("q_find", "a"): ("q_seek_end_a", "A", "R"),
        ("q_find", "b"): ("q_seek_end_b", "B", "R"),
        ("q_find", "c"): ("q_seek_end_c", "C", "R"),
        ("q_find", "A"): ("q_find", "A", "R"),
        ("q_find", "B"): ("q_find", "B", "R"),
        ("q_find", "C"): ("q_find", "C", "R"),
        ("q_find", "x"): ("q_find", "x", "R"),
        ("q_find", "y"): ("q_find", "y", "R"),
        ("q_find", "z"): ("q_find", "z", "R"),
        ("q_find", "_"): ("q_rewind", "_", "L"),

        # Ir al final y anexar copia marcada.
        ("q_seek_end_a", "a"): ("q_seek_end_a", "a", "R"),
        ("q_seek_end_a", "b"): ("q_seek_end_a", "b", "R"),
        ("q_seek_end_a", "c"): ("q_seek_end_a", "c", "R"),
        ("q_seek_end_a", "A"): ("q_seek_end_a", "A", "R"),
        ("q_seek_end_a", "B"): ("q_seek_end_a", "B", "R"),
        ("q_seek_end_a", "C"): ("q_seek_end_a", "C", "R"),
        ("q_seek_end_a", "x"): ("q_seek_end_a", "x", "R"),
        ("q_seek_end_a", "y"): ("q_seek_end_a", "y", "R"),
        ("q_seek_end_a", "z"): ("q_seek_end_a", "z", "R"),
        ("q_seek_end_a", "_"): ("q_back", "x", "L"),

        ("q_seek_end_b", "a"): ("q_seek_end_b", "a", "R"),
        ("q_seek_end_b", "b"): ("q_seek_end_b", "b", "R"),
        ("q_seek_end_b", "c"): ("q_seek_end_b", "c", "R"),
        ("q_seek_end_b", "A"): ("q_seek_end_b", "A", "R"),
        ("q_seek_end_b", "B"): ("q_seek_end_b", "B", "R"),
        ("q_seek_end_b", "C"): ("q_seek_end_b", "C", "R"),
        ("q_seek_end_b", "x"): ("q_seek_end_b", "x", "R"),
        ("q_seek_end_b", "y"): ("q_seek_end_b", "y", "R"),
        ("q_seek_end_b", "z"): ("q_seek_end_b", "z", "R"),
        ("q_seek_end_b", "_"): ("q_back", "y", "L"),

        ("q_seek_end_c", "a"): ("q_seek_end_c", "a", "R"),
        ("q_seek_end_c", "b"): ("q_seek_end_c", "b", "R"),
        ("q_seek_end_c", "c"): ("q_seek_end_c", "c", "R"),
        ("q_seek_end_c", "A"): ("q_seek_end_c", "A", "R"),
        ("q_seek_end_c", "B"): ("q_seek_end_c", "B", "R"),
        ("q_seek_end_c", "C"): ("q_seek_end_c", "C", "R"),
        ("q_seek_end_c", "x"): ("q_seek_end_c", "x", "R"),
        ("q_seek_end_c", "y"): ("q_seek_end_c", "y", "R"),
        ("q_seek_end_c", "z"): ("q_seek_end_c", "z", "R"),
        ("q_seek_end_c", "_"): ("q_back", "z", "L"),

        # Volver al inicio.
        ("q_back", "a"): ("q_back", "a", "L"),
        ("q_back", "b"): ("q_back", "b", "L"),
        ("q_back", "c"): ("q_back", "c", "L"),
        ("q_back", "A"): ("q_back", "A", "L"),
        ("q_back", "B"): ("q_back", "B", "L"),
        ("q_back", "C"): ("q_back", "C", "L"),
        ("q_back", "x"): ("q_back", "x", "L"),
        ("q_back", "y"): ("q_back", "y", "L"),
        ("q_back", "z"): ("q_back", "z", "L"),
        ("q_back", "_"): ("q_find", "_", "R"),

        # Rewind para restaurar.
        ("q_rewind", "a"): ("q_rewind", "a", "L"),
        ("q_rewind", "b"): ("q_rewind", "b", "L"),
        ("q_rewind", "c"): ("q_rewind", "c", "L"),
        ("q_rewind", "A"): ("q_rewind", "A", "L"),
        ("q_rewind", "B"): ("q_rewind", "B", "L"),
        ("q_rewind", "C"): ("q_rewind", "C", "L"),
        ("q_rewind", "x"): ("q_rewind", "x", "L"),
        ("q_rewind", "y"): ("q_rewind", "y", "L"),
        ("q_rewind", "z"): ("q_rewind", "z", "L"),
        ("q_rewind", "_"): ("q_restore", "_", "R"),

        # Restaurar marcas.
        ("q_restore", "A"): ("q_restore", "a", "R"),
        ("q_restore", "B"): ("q_restore", "b", "R"),
        ("q_restore", "C"): ("q_restore", "c", "R"),
        ("q_restore", "x"): ("q_restore", "a", "R"),
        ("q_restore", "y"): ("q_restore", "b", "R"),
        ("q_restore", "z"): ("q_restore", "c", "R"),
        ("q_restore", "a"): ("q_restore", "a", "R"),
        ("q_restore", "b"): ("q_restore", "b", "R"),
        ("q_restore", "c"): ("q_restore", "c", "R"),
        ("q_restore", "_"): ("halt", "_", "S"),
    }
    return TuringMachine(transitions, start_state="q_find", halt_states={"halt"})


def demo() -> None:
    print("Ejercicio 1: desplazar a la derecha sobre {a,b}")
    mt1 = mt_desplazar_derecha_ab()
    for w in ["", "a", "aba", "bbab"]:
        r = mt1.run(w)
        print(f"  entrada={w!r} -> cinta={r.raw_tape!r}, salida_util={r.tape!r}, pasos={r.steps}")

    print("\nEjercicio 2: duplicar ceros")
    mt2 = mt_duplicar_ceros()
    for w in ["", "0", "0000"]:
        r = mt2.run(w)
        print(f"  entrada={w!r} -> salida={r.tape!r}, pasos={r.steps}")

    print("\nEjercicio 3: aceptar 01*0")
    mt3 = mt_aceptar_01_estrella_0()
    for w in ["00", "010", "01110", "0", "011", "1010"]:
        r = mt3.run(w)
        print(f"  entrada={w!r} -> aceptada={r.accepted}, estado={r.final_state}")

    print("\nEjercicio 4: paridad de 1s (agrega bit al final)")
    mt4 = mt_paridad_ones()
    for w in ["", "0", "1", "1011", "1111", "1010"]:
        r = mt4.run(w)
        print(f"  entrada={w!r} -> salida={r.tape!r}")

    print("\nEjercicio 5: copiar cadena sobre {a,b,c}")
    mt5 = mt_copiar_abc()
    for w in ["", "a", "abc", "aabca"]:
        r = mt5.run(w)
        print(f"  entrada={w!r} -> salida={r.tape!r}")


if __name__ == "__main__":
    demo()
