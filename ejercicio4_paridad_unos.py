import tkinter as tk
from tkinter import messagebox

from mt_core import mt_paridad_ones


def main() -> None:
    tm = mt_paridad_ones()

    root = tk.Tk()
    root.title("MT Ejercicio 4 - Paridad de 1s")
    root.geometry("620x300")
    root.resizable(False, False)

    tk.Label(root, text="Entrada binaria (0/1):", font=("Segoe UI", 11)).pack(pady=(16, 4))
    entry = tk.Entry(root, font=("Consolas", 12), width=30)
    entry.insert(0, "1011")
    entry.pack(pady=4)

    out = tk.StringVar(value="Salida: -")
    parity = tk.StringVar(value="Paridad: -")
    info = tk.StringVar(value="Pasos: -")

    def ejecutar() -> None:
        w = entry.get().strip()
        if any(c not in "01" for c in w):
            messagebox.showerror("Error", "Solo se permiten simbolos '0' y '1'.")
            return

        result = tm.run(w)
        out.set(f"Salida: {result.tape}")
        if result.tape.endswith("0"):
            parity.set("Paridad: par (se anadio 0)")
        else:
            parity.set("Paridad: impar (se anadio 1)")
        info.set(f"Pasos: {result.steps} | Estado final: {result.final_state}")

    tk.Button(root, text="Ejecutar MT", command=ejecutar, font=("Segoe UI", 11)).pack(pady=10)

    tk.Label(root, textvariable=out, font=("Consolas", 12)).pack(pady=4)
    tk.Label(root, textvariable=parity, font=("Consolas", 11)).pack(pady=4)
    tk.Label(root, textvariable=info, font=("Consolas", 11)).pack(pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()
