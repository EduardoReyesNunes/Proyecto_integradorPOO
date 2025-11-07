# admin_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import db
import sqlite3 # <-- Importamos el gestor de base de datos
# ... (Resto de las definiciones de estilos y colores) ...
COLOR_BG_LIGHT = '#F5ECE5'
COLOR_BG_DARK = '#D4C4B8'
COLOR_TEXT_DARK = '#333333'
COLOR_ACCENT = '#94786A'
COLOR_BUTTON_PRIMARY = '#A37F74'
COLOR_CARD_BG = '#F5ECE5'
COLOR_TABLE_ROW_EVEN = '#E5E5E5'
COLOR_BUTTON_ENABLE = '#4CAF50'
COLOR_BUTTON_DISABLE = '#F44336'


class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Administrador - Delicias & Coffee")
        self.geometry("1024x768")
        self.config(bg=COLOR_BG_DARK)
        self.state('zoomed') 

        self.create_widgets()
        
    # ... (create_widgets, create_sidebar, handle_menu_click, clear_content_frame, quit_and_open_pos son iguales) ...
    def create_widgets(self):
        """Crea la estructura principal (Sidebar y Contenido)"""
        
        main_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        main_frame.pack(fill="both", expand=True)

        main_frame.grid_columnconfigure(0, weight=0) 
        main_frame.grid_columnconfigure(1, weight=1) 
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Columna 0) ---
        sidebar = tk.Frame(main_frame, width=250, bg=COLOR_BG_LIGHT)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.pack_propagate(False) 

        self.create_sidebar(sidebar)

        # --- Contenido Principal (Columna 1) ---
        self.content_frame = tk.Frame(main_frame, bg=COLOR_BG_DARK, padx=40, pady=30)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.handle_menu_click("Ventas", self.show_ventas_view) 

    def create_sidebar(self, sidebar):
        """Crea los elementos dentro del menú lateral."""
        
        # 1. Logo (Simulado con texto)
        tk.Label(sidebar, text="Delicias & Coffee", font=("Arial", 16, "bold"), 
                 bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_DARK).pack(pady=(40, 0))
        tk.Label(sidebar, text="POSTRES Y MÁS", font=("Arial", 10), 
                 bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_DARK).pack(pady=(0, 40))

        # 2. Navegación del Menú
        menu_items = [
            ("Ventas", self.show_ventas_view),
            ("C. Inventario", self.show_inventario_view),
            ("Productos", self.show_productos_view), 
            ("Reportes", self.show_reportes_view),
        ]
        
        menu_frame = tk.Frame(sidebar, bg=COLOR_BG_LIGHT)
        menu_frame.pack(fill="x", padx=10)
        
        self.menu_buttons = {} 
        
        for name, command in menu_items:
            btn_frame = tk.Frame(menu_frame, bg=COLOR_BG_LIGHT)
            btn_frame.pack(fill="x", pady=5)
            
            btn = tk.Button(btn_frame, text=f"   {name}", anchor="w", 
                            font=("Arial", 12), bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_DARK,
                            relief=tk.FLAT, bd=0, padx=10, 
                            command=lambda n=name, cmd=command: self.handle_menu_click(n, cmd))
            btn.pack(side="left", fill="x", expand=True)
            self.menu_buttons[name] = btn
            
            tk.Label(btn_frame, text=">", font=("Arial", 12), 
                     bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_DARK).pack(side="right", padx=10)

        # 3. Footer (Administrador y Salir)
        footer_frame = tk.Frame(sidebar, bg=COLOR_BG_LIGHT)
        footer_frame.pack(side="bottom", fill="x", pady=20)
        
        tk.Label(footer_frame, text="Administrador", font=("Arial", 10), 
                 bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_DARK).pack(pady=(10, 5))
        
        tk.Button(footer_frame, text="Salir", font=("Arial", 12, "bold"), 
                  bg=COLOR_BUTTON_PRIMARY, fg="white", 
                  relief=tk.FLAT, bd=0, padx=40, pady=10, 
                  command=self.quit_and_open_pos).pack(pady=5)
        
    def handle_menu_click(self, name, command):
        """Maneja el clic en el menú: resalta el botón y ejecuta el comando."""
        for btn_name, btn in self.menu_buttons.items():
            if btn.master:
                btn.master.config(bg=COLOR_BG_LIGHT)
            btn.config(bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_DARK, font=("Arial", 12))
            
        self.menu_buttons[name].master.config(bg=COLOR_ACCENT)
        self.menu_buttons[name].config(bg=COLOR_ACCENT, fg="white", font=("Arial", 12, "bold"))

        command()
        
    def clear_content_frame(self):
        """Limpia el frame principal para cargar una nueva vista."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_view_placeholder(self):
        """Vista de marcador de posición para otras secciones."""
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Vista en Construcción", 
                 font=("Arial", 24), bg=COLOR_BG_DARK, fg=COLOR_TEXT_DARK).pack(pady=100)

    def quit_and_open_pos(self):
        """Cierra el dashboard y vuelve a abrir la ventana del POS (simulado)."""
        self.destroy() 
        # Aquí es donde se debería llamar a la ventana del POS.
        print("Cerrando Dashboard y volviendo al POS (Simulado).")


    # --- VISTA: C. INVENTARIO (CONECTADA A DB) ---
    def show_inventario_view(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Panel de Administrador", 
                 font=("Arial", 20, "bold"), bg=COLOR_BG_DARK, 
                 fg=COLOR_TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 20))

        # Encabezados de la tabla de inventario
        headers = ["Topping/Ingrediente", "Estado/Acciones"]
        header_frame = tk.Frame(self.content_frame, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(header_frame, text=headers[0], font=("Arial", 14), 
                 bg=COLOR_BG_DARK, fg=COLOR_TEXT_DARK, anchor="w").pack(side="left", expand=True)
        tk.Label(header_frame, text=headers[1], font=("Arial", 14), 
                 bg=COLOR_BG_DARK, fg=COLOR_TEXT_DARK, anchor="e").pack(side="right", padx=10)

        # Contenedor para la lista de ingredientes con scrollbar
        scroll_canvas = tk.Canvas(self.content_frame, bg=COLOR_BG_DARK, highlightthickness=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        ingredientes_container = tk.Frame(scroll_canvas, bg=COLOR_BG_DARK)
        scroll_canvas.create_window((0, 0), window=ingredientes_container, anchor="nw", width=self.content_frame.winfo_width())
        ingredientes_container.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        self.content_frame.bind("<Configure>", lambda e: ingredientes_container.config(width=e.width))

        self.load_ingredientes(ingredientes_container)

        # Botón AGREGAR INGREDIENTE
        tk.Button(self.content_frame, text="Agregar Ingredientes/Toppings", 
                  font=("Arial", 12, "bold"), 
                  bg=COLOR_BUTTON_PRIMARY, fg="white", 
                  relief=tk.FLAT, bd=0, padx=20, pady=10,
                  command=self.open_add_ingrediente_window).pack(pady=20, anchor="e")

    def load_ingredientes(self, container):
        """Carga la lista de ingredientes desde la DB y los muestra en el contenedor."""
        # Limpiar el contenedor antes de recargar
        for widget in container.winfo_children():
            widget.destroy()
            
        ingredientes = db.execute_query("SELECT id, nombre, estado FROM ingredientes ORDER BY nombre")
        
        for i, (id, nombre, estado) in enumerate(ingredientes):
            row_bg_color = COLOR_BG_LIGHT if i % 2 == 0 else COLOR_TABLE_ROW_EVEN
            row_frame = tk.Frame(container, bg=row_bg_color, padx=15, pady=10)
            row_frame.pack(fill="x", pady=2)
            
            # Nombre del ingrediente
            tk.Label(row_frame, text=nombre, font=("Arial", 12), 
                     bg=row_bg_color, fg=COLOR_TEXT_DARK, anchor="w").pack(side="left", fill="x", expand=True)
            
            # Botones de Acción
            action_frame = tk.Frame(row_frame, bg=row_bg_color)
            action_frame.pack(side="right")
            
            # Habilitar
            tk.Button(action_frame, text="Habilitar", font=("Arial", 10, "bold"), 
                      bg=COLOR_BUTTON_ENABLE, fg="white", relief=tk.FLAT, bd=0, 
                      padx=10, pady=5, 
                      command=lambda i=id: self.update_ingrediente_status(i, 1)).pack(side="left", padx=5)
            
            # Deshabilitar
            tk.Button(action_frame, text="Deshabilitar", font=("Arial", 10, "bold"), 
                      bg=COLOR_BUTTON_DISABLE, fg="white", relief=tk.FLAT, bd=0, 
                      padx=10, pady=5,
                      command=lambda i=id: self.update_ingrediente_status(i, 0)).pack(side="left", padx=5)
                      
            # Etiqueta de estado (Opcional, para indicar el estado actual)
            estado_texto = "HABILITADO" if estado == 1 else "DESHABILITADO"
            estado_color = COLOR_BUTTON_ENABLE if estado == 1 else COLOR_BUTTON_DISABLE
            tk.Label(action_frame, text=f"({estado_texto})", font=("Arial", 8), 
                     bg=row_bg_color, fg=estado_color).pack(side="left", padx=10)


    def update_ingrediente_status(self, ingrediente_id, status):
        """Actualiza el estado de habilitado/deshabilitado en la DB y recarga la vista."""
        try:
            db.execute_commit("UPDATE ingredientes SET estado = ? WHERE id = ?", (status, ingrediente_id))
            messagebox.showinfo("Éxito", f"Ingrediente ID {ingrediente_id} actualizado.")
            self.show_inventario_view() # Recargar la vista para reflejar el cambio
        except Exception as e:
            messagebox.showerror("Error de DB", f"No se pudo actualizar el ingrediente: {e}")

    def open_add_ingrediente_window(self):
        """Abre una ventana para añadir un nuevo ingrediente."""
        # Crea una Toplevel window para el formulario
        add_win = tk.Toplevel(self)
        add_win.title("Añadir Ingrediente")
        add_win.geometry("300x150")
        add_win.config(bg=COLOR_BG_LIGHT)

        tk.Label(add_win, text="Nombre:", bg=COLOR_BG_LIGHT).pack(pady=5)
        name_entry = tk.Entry(add_win)
        name_entry.pack(pady=5)

        def save_ingrediente():
            name = name_entry.get().strip()
            if name:
                try:
                    db.execute_commit("INSERT INTO ingredientes (nombre, estado) VALUES (?, 1)", (name,))
                    messagebox.showinfo("Éxito", f"Ingrediente '{name}' añadido.")
                    add_win.destroy()
                    self.show_inventario_view()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Este ingrediente ya existe.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar: {e}")
            else:
                messagebox.showwarning("Advertencia", "El nombre no puede estar vacío.")

        tk.Button(add_win, text="Guardar", command=save_ingrediente, bg=COLOR_BUTTON_PRIMARY, fg="white").pack(pady=10)


    # --- VISTA: PRODUCTOS (CONECTADA A DB) ---
    def show_productos_view(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Panel de Administrador", 
                 font=("Arial", 20, "bold"), bg=COLOR_BG_DARK, 
                 fg=COLOR_TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 20))

        # Contenedor para la tabla Treeview (más simple que el scrollbar manual)
        table_frame = tk.Frame(self.content_frame, bg=COLOR_BG_DARK)
        table_frame.pack(fill="both", expand=False)
        
        # ... (Configuración de estilos Treeview) ...
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), 
                        background=COLOR_ACCENT, foreground="white")
        style.configure("Treeview", font=('Arial', 11), rowheight=30,
                        background=COLOR_BG_LIGHT, foreground=COLOR_TEXT_DARK, 
                        fieldbackground=COLOR_BG_LIGHT) 

        tree = ttk.Treeview(table_frame, columns=("ID", "Producto", "Categoría", "Precio", "Estado"), 
                            show="headings", height=5)
        
        # Encabezados
        tree.heading("ID", text="ID", anchor="w")
        tree.heading("Producto", text="Producto", anchor="w")
        tree.heading("Categoría", text="Categoría", anchor="w")
        tree.heading("Precio", text="Precio", anchor="w")
        tree.heading("Estado", text="Estado", anchor="center")

        # Ancho de columnas
        tree.column("ID", width=50, anchor="w")
        tree.column("Producto", width=200, anchor="w")
        tree.column("Categoría", width=150, anchor="w")
        tree.column("Precio", width=100, anchor="w")
        tree.column("Estado", width=100, anchor="center")

        # Cargar datos desde la DB
        productos = db.execute_query("SELECT id, nombre, categoria, precio, habilitado FROM productos ORDER BY categoria, nombre")

        for i, (id, name, category, price, enabled) in enumerate(productos):
            tag_color = 'oddrow' if i % 2 != 0 else 'evenrow'
            estado = "Habilitado" if enabled == 1 else "Deshabilitado"
            tree.insert("", "end", values=(id, name, category, f"${price:.2f}", estado), tags=(tag_color,))
        
        tree.tag_configure('evenrow', background=COLOR_BG_LIGHT) 
        tree.tag_configure('oddrow', background=COLOR_TABLE_ROW_EVEN) 

        tree.pack(fill="x", expand=False)
        
        # ... (Botón Agregar Producto y otras vistas) ...
        tk.Button(self.content_frame, text="Agregar Producto", 
                  font=("Arial", 12, "bold"), 
                  bg=COLOR_BUTTON_PRIMARY, fg="white", 
                  relief=tk.FLAT, bd=0, padx=20, pady=10).pack(pady=20, anchor="e")

    # ... (show_ventas_view y show_reportes_view son iguales a la versión anterior, 
    #       excepto que show_ventas_view ahora usa datos simulados, ya que la tabla de ventas
    #       se poblará desde el POS más adelante.) ...
    def show_ventas_view(self):
        # ... (código show_ventas_view anterior) ...
        pass
        
    def show_reportes_view(self):
        # ... (código show_reportes_view anterior) ...
        pass
        
    # --- VISTA: REPORTES (Similar a image_0c1d82.png) ---
    def show_reportes_view(self):
        """Muestra el panel de métricas y reportes semanales."""
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Panel de Administrador", 
                 font=("Arial", 20, "bold"), bg=COLOR_BG_DARK, 
                 fg=COLOR_TEXT_DARK, anchor="w").pack(fill="x", pady=(0, 20))
        
        tk.Label(self.content_frame, text="Esta semana:", font=("Arial", 14), 
                 bg=COLOR_BG_DARK, fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(10, 10))
        
        # Frame de Métricas (Cards)
        cards_frame = tk.Frame(self.content_frame, bg=COLOR_BG_DARK)
        cards_frame.pack(fill="x", pady=10)
        
        metric_data = [
            ("Ventas Totales", "$6,500.00"),
            ("Total de pagos", "300 pedidos"),
            ("Producto mas vendido", "Frappe Oreo")
        ]
        
        for title, value in metric_data:
            card = tk.Frame(cards_frame, bg=COLOR_CARD_BG, padx=20, pady=15, relief=tk.FLAT, bd=0)
            card.pack(side="left", expand=True, fill="x", padx=10)
            
            tk.Label(card, text=title, font=("Arial", 10), bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack()
            tk.Label(card, text=value, font=("Arial", 20, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT_DARK).pack()

        # Historial de Reportes Semanales (Tabla)
        tk.Label(self.content_frame, text="Historial de reportes semanales:", font=("Arial", 14), 
                 bg=COLOR_BG_DARK, fg=COLOR_TEXT_DARK).pack(anchor="w", pady=(30, 10))

        table_frame = tk.Frame(self.content_frame, bg=COLOR_BG_DARK)
        table_frame.pack(fill="x", pady=10)
        
        report_data = [
            ("27 Oct - 2 Nov", "$6,500", "Frappe Oreo"),
            ("20 Oct - 26 Oct", "$6,800", "Creppa Especial Crepizzza"),
            ("13 Oct - 19 Oct", "$6,285", "Chocolate")
        ]
        
        headers = ["Semana", "Ventas Totales", "Producto mas vendido"]
        header_color = COLOR_ACCENT
        
        for col, header_text in enumerate(headers):
            tk.Label(table_frame, text=header_text, font=("Arial", 11, "bold"), bg=header_color, fg="white", padx=10, pady=10).grid(row=0, column=col, sticky="nsew")
            table_frame.grid_columnconfigure(col, weight=1) 
            
        for row, data in enumerate(report_data):
            current_color = COLOR_BG_LIGHT if row % 2 == 0 else COLOR_TABLE_ROW_EVEN
            
            for col, cell_data in enumerate(data):
                font_style = ("Arial", 10, "bold") if col == 1 else ("Arial", 10) 
                
                tk.Label(table_frame, text=cell_data, font=font_style, bg=current_color, fg=COLOR_TEXT_DARK, padx=10, pady=10, anchor="w").grid(row=row + 1, column=col, sticky="nsew")


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()