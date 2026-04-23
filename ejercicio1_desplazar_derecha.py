import tkinter as tk
from tkinter import messagebox

from mt_core import mt_desplazar_derecha_ab


def main() -> None:
    tm = mt_desplazar_derecha_ab()

    root = tk.Tk()
    root.title("MT Ejercicio 1 - Desplazar a la derecha")
    root.geometry("620x280")
    root.resizable(False, False)

    tk.Label(root, text="Entrada (alfabeto {a,b}):", font=("Segoe UI", 11)).pack(pady=(16, 4))
    entry = tk.Entry(root, font=("Consolas", 12), width=30)
    entry.insert(0, "aba")
    entry.pack(pady=4)

    out_raw = tk.StringVar(value="Cinta: -")
    out_trim = tk.StringVar(value="Salida util: -")
    out_steps = tk.StringVar(value="Pasos: -")

    def ejecutar() -> None:
        w = entry.get().strip()
        if any(c not in "ab" for c in w):
            messagebox.showerror("Error", "Solo se permiten simbolos 'a' y 'b'.")
            return

        result = tm.run(w)
        out_raw.set(f"Cinta: {result.raw_tape}")
        out_trim.set(f"Salida util: {result.tape}")
        out_steps.set(f"Pasos: {result.steps} | Estado final: {result.final_state}")

    tk.Button(root, text="Ejecutar MT", command=ejecutar, font=("Segoe UI", 11)).pack(pady=10)

    tk.Label(root, textvariable=out_raw, font=("Consolas", 11)).pack(pady=4)
    tk.Label(root, textvariable=out_trim, font=("Consolas", 11)).pack(pady=4)
    tk.Label(root, textvariable=out_steps, font=("Consolas", 11)).pack(pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()
