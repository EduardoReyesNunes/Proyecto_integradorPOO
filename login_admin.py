import tkinter as tk
from tkinter import messagebox
from admin_dashboard import AdminDashboard # <-- IMPORTADO

# --- 🎨 DEFINICIÓN DE ESTILOS Y COLORES ---
COLOR_BG_LOGIN = '#D4C4B8'      # Fondo principal del login
COLOR_INPUT_BG = '#F5ECE5'      # Fondo de campos de entrada
COLOR_TEXT_DARK = '#333333'     # Texto oscuro
COLOR_HIGHLIGHT = '#A37F74'     # Botón de acceder
COLOR_SHADOW = '#B7A294'        # Sombra sutil

class AdminLoginApp(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master_pos = master # Guardamos referencia a la ventana POS
        self.title("Acceso a Administrador")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(bg=COLOR_BG_LOGIN)

        # Centrar la ventana de login
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        # Si la ventana de login se cierra con la X, mostramos el POS de nuevo
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_login_widgets()

        self.valid_username = "admin"
        self.valid_password = "password"

    # ... (Resto del código de create_login_widgets y funciones de placeholder) ...

    def create_login_widgets(self):
        """Crea todos los elementos de la interfaz de login."""
        
        # Fondo con formas curvadas (simulado con canvas y óvalos/rectángulos)
        canvas = tk.Canvas(self, bg=COLOR_BG_LOGIN, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Dibujar las formas curvadas de fondo
        canvas.create_oval(-200, -200, 400, 400, fill=COLOR_SHADOW, outline="")
        canvas.create_oval(600, 400, 1000, 800, fill=COLOR_SHADOW, outline="")
        canvas.create_rectangle(0, 200, 800, 400, fill=COLOR_SHADOW, outline="")
        canvas.create_rectangle(200, 0, 600, 600, fill=COLOR_SHADOW, outline="")

        # Frame principal para el contenido de login (para centrarlo)
        login_content_frame = tk.Frame(canvas, bg=COLOR_BG_LOGIN)
        canvas.create_window(400, 300, window=login_content_frame, anchor="center")

        # --- Logo (texto para simplificar) ---
        logo_frame = tk.Frame(login_content_frame, bg=COLOR_INPUT_BG, relief="solid", bd=0)
        logo_frame.pack(pady=20, padx=50) 
        
        tk.Label(logo_frame, text="Delicias & Coffee", font=("Arial", 20, "bold"), 
                 bg=COLOR_INPUT_BG, fg=COLOR_TEXT_DARK).pack(pady=5, padx=20)
        tk.Label(logo_frame, text="POSTRES Y MÁS", font=("Arial", 12), 
                 bg=COLOR_INPUT_BG, fg=COLOR_TEXT_DARK).pack(pady=(0, 10), padx=20)
        
        # --- Título "Acceso a Administrador" ---
        tk.Label(login_content_frame, text="Acceso a Administrador", font=("Arial", 16, "bold"), 
                 bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK).pack(pady=20)

        # --- Campo de Usuario ---
        user_frame = tk.Frame(login_content_frame, bg=COLOR_BG_LOGIN)
        user_frame.pack(pady=10)
        tk.Label(user_frame, text="Usuario", font=("Arial", 12), bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK).pack(anchor="w")
        self.username_entry = tk.Entry(user_frame, width=40, font=("Arial", 12),
                                       bg=COLOR_INPUT_BG, fg=COLOR_TEXT_DARK,
                                       insertbackground=COLOR_TEXT_DARK, bd=0, relief=tk.FLAT)
        self.username_entry.pack(ipady=8, padx=10)
        self.username_entry.insert(0, "Ingresa nombre de usuario")
        self.username_entry.bind("<FocusIn>", self.clear_placeholder_user)
        self.username_entry.bind("<FocusOut>", self.add_placeholder_user)

        # --- Campo de Contraseña ---
        pass_frame = tk.Frame(login_content_frame, bg=COLOR_BG_LOGIN)
        pass_frame.pack(pady=10)
        tk.Label(pass_frame, text="Contraseña", font=("Arial", 12), bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK).pack(anchor="w")
        self.password_entry = tk.Entry(pass_frame, width=40, font=("Arial", 12), show="*",
                                       bg=COLOR_INPUT_BG, fg=COLOR_TEXT_DARK,
                                       insertbackground=COLOR_TEXT_DARK, bd=0, relief=tk.FLAT)
        self.password_entry.pack(ipady=8, padx=10)
        self.password_entry.insert(0, "Ingresar contraseña") # Placeholder
        self.password_entry.bind("<FocusIn>", self.clear_placeholder_pass)
        self.password_entry.bind("<FocusOut>", self.add_placeholder_pass)
        self.password_entry.bind("<Return>", self.attempt_login) # Intentar login con Enter

        # --- Botón ACCEDER ---
        tk.Button(login_content_frame, text="ACCEDER", font=("Arial", 14, "bold"),
                  bg=COLOR_HIGHLIGHT, fg="white", relief=tk.FLAT, bd=0,
                  padx=30, pady=10, command=self.attempt_login).pack(pady=30)

    # --- Funciones de Placeholder ---
    def clear_placeholder_user(self, event):
        if self.username_entry.get() == "Ingresa nombre de usuario":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg=COLOR_TEXT_DARK)

    def add_placeholder_user(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Ingresa nombre de usuario")
            self.username_entry.config(fg='grey')

    def clear_placeholder_pass(self, event):
        if self.password_entry.get() == "Ingresar contraseña":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show="*", fg=COLOR_TEXT_DARK)

    def add_placeholder_pass(self, event):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Ingresar contraseña")
            self.password_entry.config(show="", fg='grey')

    # --- Función de Cierre ---
    def on_close(self):
        """Muestra el POS y cierra la ventana de login."""
        if self.master_pos:
            self.master_pos.deiconify()
        self.destroy()

    def attempt_login(self, event=None):
        """Intenta iniciar sesión y abre el Dashboard si es exitoso."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.valid_username and password == self.valid_password:
            # 1. Cierra la ventana de login
            self.destroy()
            
            # 2. Oculta la ventana principal del POS (ya hecho en pos_app.py, pero por si acaso)
            if self.master_pos:
                self.master_pos.withdraw() 
            
            # 3. Abre el Panel de Administrador (nueva ventana principal)
            AdminDashboard()
            
            # Nota: Al usar tk.Tk() en AdminDashboard, esta se convierte en 
            # la ventana principal. El mainloop() del POS debe estar activo.

        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, tk.END)
            self.add_placeholder_pass(None)
            self.username_entry.delete(0, tk.END)
            self.add_placeholder_user(None)


if __name__ == "__main__":
    root_test = tk.Tk()
    root_test.withdraw()
    login_window = AdminLoginApp(root_test)
    root_test.mainloop()