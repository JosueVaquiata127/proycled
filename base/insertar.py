import psycopg
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

# Conectar a la base de datos
def conexion_db():
    try:
        conn = psycopg.connect(
            dbname="cled",
            user="postgres",
            password="12638149",  # Asegúrate de cambiar la contraseña si es diferente
            host="localhost",  # O el host de tu servidor
            port="5432"  # El puerto de tu base de datos (default es 5432)
        )
        print("Conexión exitosa a la base de datos.")
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para agregar un inscrito a la base de datos
def agregar_inscrito():
    ci_inscrito = ci_inscrito_var.get()
    nombres = nombres_var.get()
    apellidos = apellidos_var.get()
    departamento = departamento_var.get()
    ciudad = ciudad_var.get()
    telefono = telefono_var.get()
    medio_inscripcion = medio_inscripcion_var.get()
    id_encargado = id_encargado_var.get()
    id_curso = id_curso_var.get()

    if not ci_inscrito or not nombres or not apellidos or not departamento or not ciudad or not telefono or not medio_inscripcion or not id_encargado or not id_curso:
        messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")
        return

    conn = conexion_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            INSERT INTO Inscritos (ci_inscrito, nombres, apellidos, departamento, ciudad, telefono, medio_inscripcion, id_encargado, id_curso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ci_inscrito, nombres, apellidos, departamento, ciudad, telefono, medio_inscripcion, id_encargado, id_curso))
            conn.commit()
            messagebox.showinfo("Éxito", "Inscrito agregado exitosamente.")
        except Exception as e:
            print("Error al agregar inscrito:", e)
            messagebox.showerror("Error", "No se pudo agregar al inscrito.")
        finally:
            cursor.close()
            conn.close()

# Función para borrar un inscrito de la base de datos
def borrar_inscrito():
    ci_inscrito = ci_inscrito_borrar_var.get()

    if not ci_inscrito:
        messagebox.showwarning("Advertencia", "Debe ingresar el CI del inscrito a eliminar.")
        return

    conn = conexion_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            DELETE FROM Inscritos WHERE ci_inscrito = %s
            """
            cursor.execute(query, (ci_inscrito,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Inscrito eliminado exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "No se encontró un inscrito con ese CI.")
        except Exception as e:
            print("Error al borrar inscrito:", e)
            messagebox.showerror("Error", "No se pudo borrar al inscrito.")
        finally:
            cursor.close()
            conn.close()

# Función para actualizar todos los datos de un inscrito
def actualizar_todos_los_datos():
    ci_inscrito = ci_inscrito_actualizar_var.get()
    nombres = nombres_actualizar_var.get()
    apellidos = apellidos_actualizar_var.get()
    departamento = departamento_actualizar_var.get()
    ciudad = ciudad_actualizar_var.get()
    telefono = telefono_actualizar_var.get()
    medio_inscripcion = medio_inscripcion_actualizar_var.get()
    id_encargado = id_encargado_actualizar_var.get()
    id_curso = id_curso_actualizar_var.get()

    if not ci_inscrito:
        messagebox.showwarning("Advertencia", "Debe ingresar el CI del inscrito a actualizar.")
        return

    conn = conexion_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
            UPDATE Inscritos SET
                nombres = %s,
                apellidos = %s,
                departamento = %s,
                ciudad = %s,
                telefono = %s,
                medio_inscripcion = %s,
                id_encargado = %s,
                id_curso = %s
            WHERE ci_inscrito = %s
            """
            cursor.execute(query, (nombres, apellidos, departamento, ciudad, telefono, medio_inscripcion, id_encargado, id_curso, ci_inscrito))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Datos del inscrito actualizados exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "No se encontró un inscrito con ese CI.")
        except Exception as e:
            print("Error al actualizar inscrito:", e)
            messagebox.showerror("Error", "No se pudo actualizar al inscrito.")
        finally:
            cursor.close()
            conn.close()

# Crear la ventana de la interfaz gráfica
def ventana_principal():
    ventana = Tk()
    ventana.title("Gestión de Inscritos")
    ventana.geometry("2560x1440")
    ventana.config(bg="#f0f0f0")  # Fondo suave y claro

    # Frame para organizar los campos
    frame = Frame(ventana, bg="#595c5e", bd=2, relief="solid", padx=10, pady=10)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Imagen
    try:
        imagen = Image.open("congreso.jpg")  # Asegúrate de que la imagen esté en la misma carpeta
        imagen = imagen.resize((300, 300))  # Redimensionar la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = Label(frame, image=imagen_tk, bg="#ffffff")
        label_imagen.image = imagen_tk  # Mantener una referencia a la imagen
        label_imagen.grid(row=0, column=1, columnspan=1, pady=2)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        Label(frame, text="Imagen no encontrada", font=("Arial", 12), bg="#ffffff", fg="#ff0000").grid(row=1, column=0, columnspan=3, pady=10)

    # Inicialización de las variables StringVar
    global ci_inscrito_var, nombres_var, apellidos_var, departamento_var, ciudad_var, telefono_var, medio_inscripcion_var, id_encargado_var, id_curso_var
    global ci_inscrito_borrar_var, ci_inscrito_actualizar_var, nombres_actualizar_var, apellidos_actualizar_var, departamento_actualizar_var
    global ciudad_actualizar_var, telefono_actualizar_var, medio_inscripcion_actualizar_var, id_encargado_actualizar_var, id_curso_actualizar_var

    ci_inscrito_var = StringVar()
    nombres_var = StringVar()
    apellidos_var = StringVar()
    departamento_var = StringVar()
    ciudad_var = StringVar()
    telefono_var = StringVar()
    medio_inscripcion_var = StringVar()
    id_encargado_var = StringVar()
    id_curso_var = StringVar()

    ci_inscrito_borrar_var = StringVar()

    ci_inscrito_actualizar_var = StringVar()
    nombres_actualizar_var = StringVar()
    apellidos_actualizar_var = StringVar()
    departamento_actualizar_var = StringVar()
    ciudad_actualizar_var = StringVar()
    telefono_actualizar_var = StringVar()
    medio_inscripcion_actualizar_var = StringVar()
    id_encargado_actualizar_var = StringVar()
    id_curso_actualizar_var = StringVar()

    # Sección para agregar un inscrito
    frame_add = Frame(frame, bg="#4676a3")
    frame_add.grid(row=0, column=0, padx=10, pady=10)

    Label(frame_add, text="Agregar Inscrito", font=("Arial", 16, "bold"), bg="#ffffff", fg="#1E90FF").grid(row=0, column=0  , columnspan=2, pady=10)
    campos = [
        ("CI Inscrito", ci_inscrito_var),
        ("Nombres", nombres_var),
        ("Apellidos", apellidos_var),
        ("Departamento", departamento_var),
        ("Ciudad", ciudad_var),
        ("Teléfono", telefono_var),
        ("Medio Inscripción", medio_inscripcion_var),
        ("ID Encargado", id_encargado_var),
        ("ID Curso", id_curso_var),
    ]
    for i, (label_text, entry_var) in enumerate(campos):
        Label(frame_add, text=label_text, font=("Arial", 12), bg="#ffffff", fg="#0008ff").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
        entry_widget = Entry(frame_add, font=("Arial", 12), bd=2, relief="solid", textvariable=entry_var)  # Asociando la variable StringVar
        entry_widget.grid(row=i+1, column=1, padx=10, pady=5)

    agregar_btn = Button(frame_add, text="Agregar Inscrito", font=("Arial", 14), bg="#32CD32", fg="#ffffff", command=agregar_inscrito)
    agregar_btn.grid(row=len(campos)+1, column=0, columnspan=2, pady=10)

    # Sección para borrar un inscrito
    frame_delete = Frame(frame, bg="#4676a3")
    frame_delete.grid(row=1, column=1, padx=10, pady=10)

    Label(frame_delete, text="Borrar Inscrito", font=("Arial", 16, "bold"), bg="#ffffff", fg="#FF6347").grid(row=0, column=0, columnspan=2, pady=10)
    Label(frame_delete, text="CI Inscrito", font=("Arial", 12), bg="#ffffff", fg="#FF6347").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ci_inscrito_borrar_var = Entry(frame_delete, font=("Arial", 12), bd=2, relief="solid")
    ci_inscrito_borrar_var.grid(row=1, column=1, padx=10, pady=10)
    borrar_btn = Button(frame_delete, text="Borrar Inscrito", font=("Arial", 14), bg="#FF6347", fg="#ffffff", command=borrar_inscrito)
    borrar_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Sección para actualizar datos de un inscrito
    frame_update = Frame(frame, bg="#4676a3")
    frame_update.grid(row=0, column=2, padx=10, pady=10)

    Label(frame_update, text="Actualizar Datos Inscrito", font=("Arial", 16, "bold"), bg="#ffffff", fg="#ff0077").grid(row=0, column=0, columnspan=2, pady=10)
    campos_update = [
        ("CI Inscrito", ci_inscrito_actualizar_var),
        ("Nombres", nombres_actualizar_var),
        ("Apellidos", apellidos_actualizar_var),
        ("Departamento", departamento_actualizar_var),
        ("Ciudad", ciudad_actualizar_var),
        ("Teléfono", telefono_actualizar_var),
        ("Medio Inscripción", medio_inscripcion_actualizar_var),
        ("ID Encargado", id_encargado_actualizar_var),
        ("ID Curso", id_curso_actualizar_var),
    ]
    for i, (label_text, entry_var) in enumerate(campos_update):
        Label(frame_update, text=label_text, font=("Arial", 12), bg="#ffffff", fg="#0008ff").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
        entry_widget = Entry(frame_update, font=("Arial", 12), bd=2, relief="solid", textvariable=entry_var)  # Asociando la variable StringVar
        entry_widget.grid(row=i+1, column=1, padx=10, pady=5)

    actualizar_btn = Button(frame_update, text="Actualizar Datos", font=("Arial", 14), bg="#FFD700", fg="#ffffff", command=actualizar_todos_los_datos)
    actualizar_btn.grid(row=len(campos_update)+1, column=0, columnspan=2, pady=10)

    ventana.mainloop()

# Inicializar la ventana principal
ventana_principal()