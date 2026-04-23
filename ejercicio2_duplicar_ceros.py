import tkinter as tk
from tkinter import messagebox

from mt_core import mt_duplicar_ceros


def main() -> None:
    tm = mt_duplicar_ceros()

    root = tk.Tk()
    root.title("MT Ejercicio 2 - Duplicar ceros")
    root.geometry("600x260")
    root.resizable(False, False)

    tk.Label(root, text="Entrada (solo 0):", font=("Segoe UI", 11)).pack(pady=(16, 4))
    entry = tk.Entry(root, font=("Consolas", 12), width=30)
    entry.insert(0, "000")
    entry.pack(pady=4)

    out = tk.StringVar(value="Salida: -")
    info = tk.StringVar(value="Pasos: -")

    def ejecutar() -> None:
        w = entry.get().strip()
        if any(c != "0" for c in w):
            messagebox.showerror("Error", "La entrada debe ser una cadena de '0'.")
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
