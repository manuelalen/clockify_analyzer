import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def calcular_medias(file_path):
    # Cargar el archivo Excel
    df = pd.read_excel(file_path)
    
    # Convertir Start Date a formato datetime
    df["Start Date"] = pd.to_datetime(df["Start Date"], errors='coerce')
    
    # Filtrar los datos de los últimos 3 meses
    three_months_ago = datetime.today() - timedelta(days=90)
    df = df[df["Start Date"] >= three_months_ago]
    
    # Sumar la duración por cliente
    sum_duration_by_client = df.groupby("Client")["Duration (decimal)"].sum()
    
    # Calcular la media de duración por cliente
    mean_duration_by_client = sum_duration_by_client.sum() / len(sum_duration_by_client)
    
    # Filtrar las descripciones que NO contengan "daily" y tareas que NO sean "Meeting"
    filtered_df = df[
        (~df["Description"].str.lower().str.contains("daily", na=False)) &
        (df["Task"].str.lower() != "meeting")
    ]
    
    # Sumar la duración por descripción
    sum_duration_by_description = filtered_df.groupby("Description")["Duration (decimal)"].sum()
    
    # Calcular la media de duración por descripción
    mean_duration_by_description = sum_duration_by_description.sum() / len(sum_duration_by_description)
    
    return mean_duration_by_client, mean_duration_by_description, sum_duration_by_description

def graficar_duracion_por_descripcion(sum_duration_by_description):
    plt.figure(figsize=(12, 6))
    sum_duration_by_description.sort_values(ascending=False).plot(kind='bar')
    plt.xlabel("Descripción")
    plt.ylabel("Media de Duración (decimal)")
    plt.title("Media de duración por descripción (últimos 3 meses, filtrada)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Ejemplo de uso
file_path = "files/clockify.xlsx"  # Reemplazar con la ruta real del archivo
mean_client, mean_description, sum_duration_by_description = calcular_medias(file_path)
print(f"Media de duración por cliente: {mean_client:.2f} horas")
print(f"Media de duración por descripción (filtrada): {mean_description:.2f} horas")

graficar_duracion_por_descripcion(sum_duration_by_description)
