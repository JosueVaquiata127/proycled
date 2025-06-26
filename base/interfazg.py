import psycopg
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Conexión a la base de datos
def conexion_db():
    conn = psycopg.connect(
        dbname="cled",
        user="postgres",
        password="12638149"
    )
    print("DATABASE CONNECTED!")
    return conn

# Mostrar datos de una tabla
def mostrar_tabla(conn, tabla):
    cursor = conn.cursor()

    # Obtener columnas y registros de la tabla
    query = f"SELECT * FROM {tabla} LIMIT 1"
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]

    query = f"SELECT * FROM {tabla}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Crear una ventana para los datos
    window = tk.Toplevel()
    window.title(f"Datos de {tabla}")
    window.geometry("800x600")
    window.configure(bg="#dff9fb")  # Fondo blanco-azul

    # Etiqueta de encabezado
    header_label = tk.Label(window, text=f"Tabla: {tabla}", font=("Helvetica", 16, "bold"), bg="#3498db", fg="white")
    header_label.pack(fill=tk.X, pady=10)

    # Crear Treeview para mostrar datos
    tree = ttk.Treeview(window, columns=columns, show="headings", selectmode="browse")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=150, anchor="center")

    for row in rows:
        tree.insert("", "end", values=row)

    # Scrollbar para el Treeview
    tree_scroll = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    tree_scroll.pack(side="right", fill="y")

    # Botón para cerrar la ventana
    close_button = tk.Button(window, text="Cerrar", command=window.destroy, bg="#e74c3c", fg="white", font=("Helvetica", 12, "bold"))
    close_button.pack(pady=10)

# Crear la ventana principal
def crear_menu():
    conn = conexion_db()

    root = tk.Tk()
    root.title("Base de Datos Congreso Latinoamericano de Especializacion")
    root.geometry("800x600")
    root.configure(bg="#dff9fb")  # Fondo blanco-azul

    # Título principal
    title_label = tk.Label(root, text="Congreso Latinoamericano de Especializacion", font=("Helvetica", 20, "bold"), bg="#2980b9", fg="white")
    title_label.pack(fill=tk.X, pady=10)

    # Cargar y mostrar imagen
    try:
        imagen = Image.open("congreso.jpg")  # Cambia la ruta si es necesario
        imagen = imagen.resize((200, 150))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(root, image=imagen_tk, bg="#dff9fb")
        label_imagen.image = imagen_tk  # Evitar que la referencia a la imagen se elimine
        label_imagen.pack(pady=10)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    # Marco para los botones
    button_frame = tk.Frame(root, bg="#dff9fb")
    button_frame.pack(pady=20)

    tablas = ["Encargados", "Docentes", "Moderadores", "Cursos", 
              "Inscritos", "Certificados", "Concluyentes", "Obtencion"]

    # Botones de tablas
    for tabla in tablas:
        button = tk.Button(
            button_frame, text=f"Mostrar {tabla}", 
            command=lambda t=tabla: mostrar_tabla(conn, t),
            bg="#3498db", fg="white", font=("Helvetica", 12, "bold"),
            width=25, height=2
        )
        button.pack(pady=5)

    # Botón para salir
    exit_button = tk.Button(root, text="Salir", command=lambda: [root.quit(), conn.close()],
                            bg="#e74c3c", fg="white", font=("Helvetica", 14, "bold"), width=15)
    exit_button.pack(pady=20)

    root.mainloop()

# Iniciar la aplicación
def main():
    crear_menu()

if __name__ == "__main__":
    main()
