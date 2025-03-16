# 📊 Clockify Analyzer

### 📌 Descripción
**Clockify Analyzer** es una herramienta diseñada para analizar los datos extraídos desde **Clockify**, brindando una visión detallada del tiempo imputado en diversas tareas. La aplicación permite visualizar y filtrar datos específicos, calcular promedios y obtener equivalencias basadas en tiempos de producción.

Con una interfaz gráfica sencilla y funcionalidades avanzadas de análisis, **Clockify Analyzer** facilita la interpretación de los datos de productividad y proporciona información clave para la toma de decisiones.

---

### 🔥 Características Principales
✅ **Carga de datos** desde archivos Excel extraídos de Clockify.  
✅ **Filtrado inteligente**, excluyendo tareas irrelevantes como reuniones y registros diarios.  
✅ **Cálculo de medias** de duración por cliente y descripción.  
✅ **Visualización de equivalencias**, relacionando tiempos de trabajo con distintas mercancías.  
✅ **Interfaz amigable** basada en `Tkinter`.  
✅ **Conexión con MySQL**, para extraer tiempos de referencia desde una base de datos.

---

### 🚀 Instalación y Uso
#### 1️⃣ **Clonar el repositorio**
```sh
git clone https://github.com/tu-usuario/clockify_analyzer.git
cd clockify_analyzer
```

#### 2️⃣ **Instalar dependencias**
Asegúrate de tener **Python 3.8+** instalado y ejecuta:
```sh
pip install -r requirements.txt
```

#### 3️⃣ **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:
```ini
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=clockify_data
```

#### 4️⃣ **Ejecutar la aplicación**
```sh
python clockify_analyzer.py
```

---

### 📊 ¿Cómo Funciona?
1️⃣ **Carga un archivo Excel** exportado desde Clockify.  
2️⃣ **Filtra automáticamente las descripciones irrelevantes**.  
3️⃣ **Muestra estadísticas clave**, como el tiempo total y promedio imputado.  
4️⃣ **Permite seleccionar tareas específicas** (`[ABS-...]`) para calcular equivalencias con tiempos de producción.  
5️⃣ **Extrae referencias desde MySQL** para generar comparaciones detalladas.  

---

### ⚙️ Tecnologías Utilizadas
🔹 `Python`  
🔹 `Pandas`  
🔹 `Matplotlib`  
🔹 `Tkinter`  
🔹 `MySQL Connector`  
🔹 `dotenv`

---

### 🤝 Contribuciones
¡Este proyecto está abierto a contribuciones! Si deseas mejorar la funcionalidad o corregir errores, siéntete libre de abrir un **Pull Request** o reportar un problema en la sección de **Issues**.

📩 Para consultas, contáctame en [manuelalen@protonmail.com](mailto:manuelalen@protonmail.com)

---

### 📜 Licencia
Este proyecto se distribuye bajo la licencia **GNU GPLv3**. Puedes utilizarlo y modificarlo libremente.

🚀 ¡Gracias por usar Clockify Analyzer! 🎯