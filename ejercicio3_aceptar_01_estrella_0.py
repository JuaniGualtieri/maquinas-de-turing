import tkinter as tk
from tkinter import messagebox

from mt_core import mt_aceptar_01_estrella_0


def main() -> None:
    tm = mt_aceptar_01_estrella_0()

    root = tk.Tk()
    root.title("MT Ejercicio 3 - Lenguaje 01*0")
    root.geometry("620x280")
    root.resizable(False, False)

    tk.Label(root, text="Entrada binaria (0/1):", font=("Segoe UI", 11)).pack(pady=(16, 4))
    entry = tk.Entry(root, font=("Consolas", 12), width=30)
    entry.insert(0, "01110")
    entry.pack(pady=4)

    out = tk.StringVar(value="Resultado: -")
    info = tk.StringVar(value="Estado final: -")

    def ejecutar() -> None:
        w = entry.get().strip()
        if any(c not in "01" for c in w):
            messagebox.showerror("Error", "Solo se permiten simbolos '0' y '1'.")
            return

        result = tm.run(w)
        if result.accepted is True:
            out.set("Resultado: ACEPTADA")
        else:
            out.set("Resultado: RECHAZADA")
        info.set(f"Estado final: {result.final_state} | Pasos: {result.steps}")

    tk.Button(root, text="Evaluar", command=ejecutar, font=("Segoe UI", 11)).pack(pady=10)

    tk.Label(root, textvariable=out, font=("Consolas", 13, "bold")).pack(pady=4)
    tk.Label(root, textvariable=info, font=("Consolas", 11)).pack(pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()
