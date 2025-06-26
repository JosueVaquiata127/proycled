import psycopg
from tkinter import Tk, Button, Label, Entry, StringVar, ttk, Frame, messagebox
from PIL import Image, ImageTk

# Función para conectarse a la base de datos
def conexion_db():
    try:
        conn = psycopg.connect(
            dbname="cled",
            user="postgres",
            password="12638149",
            host="localhost",  # Asegúrate de usar el host correcto
            port="5432"        # Cambia el puerto si es necesario
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
            # Consultar en cada tabla
            for tabla, id_campo in [("Inscritos", "ci_inscrito"), 
                                    ("Encargados", "id_encargado"),
                                    ("Docentes", "id_docentes"), 
                                    ("Moderadores", "id_moderador")]:
                query = f"SELECT * FROM {tabla} WHERE {id_campo} = %s AND nombres = %s"
                cursor.execute(query, (id_ci, nombre))
                if cursor.fetchone():  # Si se encuentra un resultado
                    return tabla.lower()
        return None
    except Exception as e:
        print("Error al validar el login:", e)
        return None

# Mostrar datos en el Treeview
def mostrar_datos(conn, tree, usuario_tipo, id_ci, nombre):
    try:
        with conn.cursor() as cursor:
            # Determinar la consulta y las columnas según el tipo de usuario
            if usuario_tipo == "inscritos":
                query = """
                SELECT I.ci_inscrito, I.nombres, I.apellidos, I.departamento, I.ciudad, C.nombre AS curso
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

            # Ejecutar la consulta
            cursor.execute(query, (id_ci, nombre))
            registros = cursor.fetchall()

            if not registros:
                messagebox.showinfo("Información", "No hay datos disponibles.")
                return

            # Configurar columnas del Treeview
            tree["columns"] = columns
            tree["show"] = "headings"

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            # Insertar los registros en el Treeview
            for row in registros:
                tree.insert("", "end", values=row)
    except Exception as e:
        print("Error al mostrar datos:", e)
        messagebox.showerror("Error", "No se pudieron mostrar los datos.")

# Ventana principal
def ventana_principal(conn, usuario_tipo, id_ci, nombre):
    ventana = Tk()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("800x600")
    ventana.configure(bg="#2C3E50")

    # Mostrar imagen
    try:
        imagen = Image.open("congreso.jpg")  # Asegúrate de que la ruta sea válida
        imagen = imagen.resize((300, 200))
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = Label(ventana, image=imagen_tk, bg="#2C3E50")
        label_imagen.image = imagen_tk  # Mantener referencia
        label_imagen.pack(pady=10)
    except Exception as e:
        print("Error al cargar la imagen:", e)

    # Crear un Treeview para mostrar datos
    tree = ttk.Treeview(ventana)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Botones
    Button(
        ventana, text="Cargar Datos",
        command=lambda: mostrar_datos(conn, tree, usuario_tipo, id_ci, nombre),
        bg="#3498DB", fg="white", font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    Button(
        ventana, text="Salir",
        command=lambda: (conn.close(), ventana.destroy()),
        bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    ventana.mainloop()

# Ventana de login
def ventana_login():
    conn = conexion_db()
    if not conn:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    ventana = Tk()
    ventana.title("Inicio de Sesión")
    ventana.geometry("400x300")
    ventana.configure(bg="#2C3E50")

    id_ci_var = StringVar()
    nombre_var = StringVar()

    Label(ventana, text="ID:", bg="#2C3E50", fg="white", font=("Helvetica", 12)).pack(pady=5)
    Entry(ventana, textvariable=id_ci_var).pack(pady=5)

    Label(ventana, text="Nombre:", bg="#2C3E50", fg="white", font=("Helvetica", 12)).pack(pady=5)
    Entry(ventana, textvariable=nombre_var).pack(pady=5)

    Button(
        ventana, text="Iniciar Sesión",
        command=lambda: login(conn, id_ci_var.get(), nombre_var.get(), ventana),
        bg="#3498DB", fg="white", font=("Helvetica", 12, "bold")
    ).pack(pady=10)

    ventana.mainloop()

# Función de login
def login(conn, id_ci, nombre, ventana):
    usuario_tipo = validar_login(conn, id_ci, nombre)
    if usuario_tipo:
        ventana.destroy()
        ventana_principal(conn, usuario_tipo, id_ci, nombre)
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")

# Iniciar aplicación
ventana_login()