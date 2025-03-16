import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime, timedelta
import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def conectar_bd():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def validar_encabezados(df):
    required_headers = {"Project", "Client", "Description", "Task", "User", "Group", "Email", "Tags", "Type", "Invoiced", "Invoice ID", "Start Date", "Start Time", "End Date", "End Time", "Duration (h)", "Duration (decimal)", "ITOps Area", "Technology DSSIT", "Type DSSIT", "Servicenow Ticket", "Danone_Maintenance_Apps"}
    return required_headers.issubset(set(df.columns))

def calcular_medias(file_path):
    df = pd.read_excel(file_path)
    
    if not validar_encabezados(df):
        messagebox.showerror("Error", "El archivo subido no tiene los encabezados correctos. Suba un archivo válido.")
        return None, None, None, None
    
    df["Start Date"] = pd.to_datetime(df["Start Date"], errors='coerce')
    
    three_months_ago = datetime.today() - timedelta(days=90)
    df = df[df["Start Date"] >= three_months_ago]
    
    sum_duration_by_client = df.groupby("Client")["Duration (decimal)"].sum()
    mean_duration_by_client = sum_duration_by_client.sum() / len(sum_duration_by_client)
    
    filtered_df = df[
        (~df["Description"].str.lower().str.contains("daily", na=False)) &
        (df["Task"].str.lower() != "meeting")
    ]
    
    global sum_duration_by_description
    sum_duration_by_description = filtered_df.groupby("Description")["Duration (decimal)"].sum().reset_index()
    mean_duration_by_description = sum_duration_by_description["Duration (decimal)"].sum() / len(sum_duration_by_description)
    
    global abs_descriptions
    abs_descriptions = filtered_df[filtered_df["Description"].str.match(r"\[ABS-.*\]", na=False)]
    
    return mean_duration_by_client, mean_duration_by_description, sum_duration_by_description, abs_descriptions

def consultar_equivalencias(selected_description):
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tiempos_produccion")
    tiempos = cursor.fetchall()
    conn.close()
    
    equivalencias = []
    sum_duration = sum_duration_by_description.loc[sum_duration_by_description["Description"] == selected_description, "Duration (decimal)"].values[0]
    
    for tiempo in tiempos:
        equivalencia = sum_duration / tiempo["ttasn_minutes"]
        equivalencias.append([tiempo["mercancia"], equivalencia])
    
    return pd.DataFrame(equivalencias, columns=["Mercancía", "Equivalencia"])

def seleccionar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        global abs_descriptions
        mean_client, mean_description, sum_duration_by_description, abs_descriptions = calcular_medias(file_path)
        if mean_client is not None:
            messagebox.showinfo("Resultados", f"Media de duración por cliente: {mean_client:.2f} horas\nMedia de duración por descripción: {mean_description:.2f} horas")
            actualizar_desplegable()

def actualizar_desplegable():
    description_combobox['values'] = abs_descriptions["Description"].tolist()
    if abs_descriptions.empty:
        messagebox.showinfo("Información", "No se encontraron descripciones ABS disponibles.")

def mostrar_equivalencias():
    selected_description = description_combobox.get()
    if selected_description:
        df_equivalencias = consultar_equivalencias(selected_description)
        messagebox.showinfo("Equivalencias", df_equivalencias.to_string(index=False))
    else:
        messagebox.showwarning("Advertencia", "Seleccione una descripción válida.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Analizador de Duración de Tareas")
root.geometry("500x400")
root.configure(bg="#f5f5f5")

frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=20)

btn_cargar = tk.Button(frame, text="Cargar Archivo Excel", command=seleccionar_archivo, bg="#007BFF", fg="white", padx=10, pady=5)
btn_cargar.pack(pady=10)

description_combobox = ttk.Combobox(frame, width=50)
description_combobox.pack(pady=10)

description_button = tk.Button(frame, text="Mostrar Equivalencias", command=mostrar_equivalencias, bg="#28a745", fg="white", padx=10, pady=5)
description_button.pack(pady=10)

root.mainloop()