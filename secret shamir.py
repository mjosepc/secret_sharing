import random
import tkinter as tk
from tkinter import messagebox

def gen_polinomio(secreto, k):
    coeficientes = [secreto] + [random.randint(0, 100) for _ in range(k - 1)]
    polinomio_str = ' + '.join(f'{coef}*x^{i}' for i, coef in enumerate(coeficientes))
    return coeficientes, polinomio_str

def dividir_secreto(secreto, k, n):
    coeficientes, _ = gen_polinomio(secreto, k)
    shares = []
    for i in range(1, n + 1):
        x = i
        y = sum(coef * (x ** j) for j, coef in enumerate(coeficientes))
        shares.append((x, y))
    return shares

def lagrange_interpolacion(shares, k):
    if len(shares) < k:
        raise ValueError(f"Se necesitan al menos {k} partes para reconstruir el secreto")

    def L(i, x):
        numerador = 1
        denominador = 1
        xi, yi = shares[i]

        for j in range(len(shares)):
            if i != j:
                xj, _ = shares[j]
                numerador *= (x - xj)
                denominador *= (xi - xj)

        return numerador / denominador

    secreto = 0
    for i in range(len(shares)):
        xi, yi = shares[i]
        secreto += yi * L(i, 0)

    return int(round(secreto))

def construir_partes():
    secreto = int(secreto_entry.get())
    n = int(n_entry.get())
    k = int(k_entry.get())

    shares = dividir_secreto(secreto, k, n)
    shares_text.delete(1.0, tk.END)
    shares_text.insert(tk.END, f"Partes generadas: {shares}")

def reconstruir_secreto():
    k = int(k_reconstruct_entry.get())
    shares = []

    for i in range(k):
        x = int(x_entries[i].get())
        y = int(y_entries[i].get())
        shares.append((x, y))

    try:
        secreto_reconstruido = lagrange_interpolacion(shares, k)
        messagebox.showinfo("Secreto Reconstruido", f"Secreto reconstruido: {secreto_reconstruido}")

        # Limpiar los campos después de reconstruir el secreto
        limpiar_entradas_reconstruccion()

        # Volver a mostrar la pantalla de crear entradas
        mostrar_reconstruir_secreto()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def limpiar_entradas_reconstruccion():
    # Limpia el contenido de todas las entradas de x y y
    for entry in x_entries + y_entries:
        entry.delete(0, tk.END)

    # Limpia la entrada de 'k'
    k_reconstruct_entry.delete(0, tk.END)

    # Limpiar las entradas dinámicas
    for widget in reconstruir_secreto_frame.winfo_children():
        if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label):
            if widget not in [k_reconstruct_label, k_reconstruct_entry, crear_entradas_button]:
                widget.destroy()

    # Eliminar el botón de reconstruir secreto si existe
    for widget in reconstruir_secreto_frame.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == "Reconstruir Secreto":
            widget.destroy()

    # Volver a mostrar el botón de crear entradas
    crear_entradas_button.pack()

def mostrar_construir_partes():
    construir_partes_frame.pack(fill=tk.BOTH, expand=True)
    reconstruir_secreto_frame.pack_forget()

def mostrar_reconstruir_secreto():
    reconstruir_secreto_frame.pack(fill=tk.BOTH, expand=True)
    construir_partes_frame.pack_forget()

# Crear la ventana principal
root = tk.Tk()
root.title("Esquema de Shamir")

# Crear el menú
menu = tk.Menu(root)
root.config(menu=menu)

menu.add_command(label="Construir Partes", command=mostrar_construir_partes)
menu.add_command(label="Reconstruir Secreto", command=mostrar_reconstruir_secreto)
menu.add_command(label="Salir", command=root.quit)

# Crear el frame para construir partes
construir_partes_frame = tk.Frame(root)

secreto_label = tk.Label(construir_partes_frame, text="Secreto:")
secreto_label.pack()
secreto_entry = tk.Entry(construir_partes_frame)
secreto_entry.pack()

n_label = tk.Label(construir_partes_frame, text="Número de partes a dividir (n):")
n_label.pack()
n_entry = tk.Entry(construir_partes_frame)
n_entry.pack()

k_label = tk.Label(construir_partes_frame, text="Número mínimo para reconstruir el secreto (k):")
k_label.pack()
k_entry = tk.Entry(construir_partes_frame)
k_entry.pack()

construir_button = tk.Button(construir_partes_frame, text="Construir Partes", command=construir_partes)
construir_button.pack()

shares_text = tk.Text(construir_partes_frame, height=3, width=40)
shares_text.pack()

# Crear el frame para reconstruir el secreto
reconstruir_secreto_frame = tk.Frame(root)

k_reconstruct_label = tk.Label(reconstruir_secreto_frame, text="Número mínimo de partes necesarias para reconstruir el secreto (k):")
k_reconstruct_label.pack()
k_reconstruct_entry = tk.Entry(reconstruir_secreto_frame)
k_reconstruct_entry.pack()

x_entries = []
y_entries = []

def crear_entradas_partes():
    # Primero limpia las entradas dinámicas anteriores si existen
    for entry in x_entries + y_entries:
        entry.destroy()

    x_entries.clear()
    y_entries.clear()

    # Obtenemos el valor de k
    k = int(k_reconstruct_entry.get())

    # Creamos las entradas dinámicas
    for i in range(k):
        x_label = tk.Label(reconstruir_secreto_frame, text=f"Parte {i+1} (valor de x):")
        x_label.pack()
        x_entry = tk.Entry(reconstruir_secreto_frame)
        x_entry.pack()
        x_entries.append(x_entry)

        y_label = tk.Label(reconstruir_secreto_frame, text=f"Valor correspondiente de y para la parte {i+1}:")
        y_label.pack()
        y_entry = tk.Entry(reconstruir_secreto_frame)
        y_entry.pack()
        y_entries.append(y_entry)

    reconstruir_button = tk.Button(reconstruir_secreto_frame, text="Reconstruir Secreto", command=reconstruir_secreto)
    reconstruir_button.pack()

# Crear el botón para generar las entradas dinámicas
crear_entradas_button = tk.Button(reconstruir_secreto_frame, text="Crear Entradas", command=crear_entradas_partes)
crear_entradas_button.pack()

# Mostrar el frame de construir partes por defecto
mostrar_construir_partes()

# Iniciar el bucle principal de la aplicación
root.mainloop()
