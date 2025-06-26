import psycopg
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Función para conectarse a la base de datos
def conexion_db():
    try:
        conn = psycopg.connect(
            dbname="cled",
            user="postgres",
            password="12638149",
            host="localhost",
            port="5432"
        )
        print("DATABASE CONNECTED!")
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Validar el login
def validar_login(conn, id_ci, nombre):
    try:
        with conn.cursor() as cursor:
            for tabla, id_campo in [
                ("Inscritos", "ci_inscrito"),
                ("Encargados", "id_encargado"),
                ("Docentes", "id_docentes"),
                ("Moderadores", "id_moderador")
            ]:
                query = f"SELECT * FROM {tabla} WHERE {id_campo} = %s AND nombres = %s"
                cursor.execute(query, (id_ci, nombre))
                if cursor.fetchone():
                    return tabla.lower()
        return None
    except Exception as e:
        print("Error al validar el login:", e)
        return None

# Mostrar datos en el Treeview
def mostrar_datos(conn, tree, usuario_tipo, id_ci, nombre):
    try:
        with conn.cursor() as cursor:
            if usuario_tipo == "inscritos":
                query = """
                SELECT I.ci_inscrito, I.nombres, I.apellidos, I.departamento, I.ciudad, C.nombres AS curso
                FROM Inscritos I
                JOIN Cursos C ON I.id_curso = C.id_curso
                WHERE I.ci_inscrito = %s AND I.nombres = %s
                """
                columns = ("CI", "Nombres", "Apellidos", "Departamento", "Ciudad", "Curso")
            elif usuario_tipo == "encargados":
                query = "SELECT * FROM Encargados WHERE id_encargado = %s AND nombres = %s"
                columns = ("ID", "Nombres", "Apellidos", "Telefono", "Area")
            elif usuario_tipo == "docentes":
                query = "SELECT * FROM Docentes WHERE id_docentes = %s AND nombres = %s"
                columns = ("ID", "Nombres", "Apellidos", "Telefono", "Especialidad")
            elif usuario_tipo == "moderadores":
                query = "SELECT * FROM Moderadores WHERE id_moderador = %s AND nombres = %s"
                columns = ("ID", "Nombres", "Apellidos", "Plataforma")
            else:
                return

            cursor.execute(query, (id_ci, nombre))
            registros = cursor.fetchall()

            if not registros:
                messagebox.showinfo("Información", "No hay datos disponibles.")
                return

            tree["columns"] = columns
            tree["show"] = "headings"

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            for row in registros:
                tree.insert("", "end", values=row)
    except Exception as e:
        print("Error al mostrar datos:", e)
        messagebox.showerror("Error", "No se pudieron mostrar los datos.")

# Ventana principal
def ventana_principal(conn, usuario_tipo, id_ci, nombre):
    ventana = tk.Tk()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("800x600")
    ventana.configure(bg="#34495E")

    frame_superior = tk.Frame(ventana, bg="#2C3E50", pady=10)
    frame_superior.pack(fill="x")

    try:
        imagen = Image.open("congreso.jpg")
        imagen = imagen.resize((300, 200))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(ventana, image=imagen_tk, bg="#2C3E50")
        label_imagen.image = imagen_tk
        label_imagen.pack(pady=10)
    except Exception as e:
        print("Error al cargar la imagen:", e)

    tk.Label(
        frame_superior, text="Gestión de Usuarios", font=("Helvetica", 20, "bold"), bg="#2C3E50", fg="white"
    ).pack()

    tree = ttk.Treeview(ventana)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    frame_inferior = tk.Frame(ventana, bg="#2C3E50", pady=10)
    frame_inferior.pack(fill="x")

    tk.Button(
        frame_inferior, text="Cargar Datos",
        command=lambda: mostrar_datos(conn, tree, usuario_tipo, id_ci, nombre),
        bg="#3498DB", fg="white", font=("Helvetica", 12, "bold"), relief="raised"
    ).pack(side="left", padx=10)

    tk.Button(
        frame_inferior, text="Salir",
        command=lambda: (conn.close(), ventana.destroy()),
        bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold"), relief="raised"
    ).pack(side="right", padx=10)

    ventana.mainloop()

# Ventana de login
def ventana_login():
    conn = conexion_db()
    if not conn:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")
    ventana.geometry("400x600")
    ventana.configure(bg="#2C3E50")

    frame = tk.Frame(ventana, bg="#34495E", padx=20, pady=20)
    frame.pack(pady=30)

    try:
        imagen = Image.open("congreso.jpg")
        imagen = imagen.resize((300, 200))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(ventana, image=imagen_tk, bg="#2C3E50")
        label_imagen.image = imagen_tk
        label_imagen.pack(pady=10)
    except Exception as e:
        print("Error al cargar la imagen:", e)

    tk.Label(frame, text="Inicio de Sesión", bg="#34495E", fg="white", font=("Helvetica", 18, "bold")).pack(pady=10)

    id_ci_var = tk.StringVar()
    nombre_var = tk.StringVar()

    tk.Label(frame, text="ID:", bg="#34495E", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    tk.Entry(frame, textvariable=id_ci_var, font=("Helvetica", 12)).pack(fill="x", pady=5)

    tk.Label(frame, text="Nombre:", bg="#34495E", fg="white", font=("Helvetica", 12)).pack(anchor="w")
    tk.Entry(frame, textvariable=nombre_var, font=("Helvetica", 12)).pack(fill="x", pady=5)

    tk.Button(
        frame, text="Iniciar Sesión",
        command=lambda: login(conn, id_ci_var.get(), nombre_var.get(), ventana),
        bg="#3498DB", fg="white", font=("Helvetica", 12, "bold"), relief="raised"
    ).pack(pady=20)

    ventana.mainloop()

# Función de login
def login(conn, id_ci, nombre, ventana):
    if not id_ci or not nombre:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return
    usuario_tipo = validar_login(conn, id_ci, nombre)
    if usuario_tipo:
        ventana.destroy()
        ventana_principal(conn, usuario_tipo, id_ci, nombre)
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")

# Iniciar la aplicación
ventana_login()
