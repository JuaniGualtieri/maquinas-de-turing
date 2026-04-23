import tkinter as tk
from tkinter import messagebox

from mt_core import mt_copiar_abc


def main() -> None:
    tm = mt_copiar_abc()

    root = tk.Tk()
    root.title("MT Ejercicio 5 - Copiar cadena {a,b,c}")
    root.geometry("660x310")
    root.resizable(False, False)

    tk.Label(root, text="Entrada (alfabeto {a,b,c}):", font=("Segoe UI", 11)).pack(pady=(16, 4))
    entry = tk.Entry(root, font=("Consolas", 12), width=34)
    entry.insert(0, "aabca")
    entry.pack(pady=4)

    out = tk.StringVar(value="Salida: -")
    info = tk.StringVar(value="Pasos: -")

    def ejecutar() -> None:
        w = entry.get().strip()
        if any(c not in "abc" for c in w):
            messagebox.showerror("Error", "Solo se permiten simbolos 'a', 'b' y 'c'.")
            return

        result = tm.run(w)
        out.set(f"Salida: {result.tape}")
        info.set(f"Pasos: {result.steps} | Estado final: {result.final_state}")

    tk.Button(root, text="Ejecutar MT", command=ejecutar, font=("Segoe UI", 11)).pack(pady=10)

    tk.Label(root, textvariable=out, font=("Consolas", 12)).pack(pady=4)
    tk.Label(root, textvariable=info, font=("Consolas", 11)).pack(pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()
