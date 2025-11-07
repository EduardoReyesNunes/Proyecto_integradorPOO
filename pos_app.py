import tkinter as tk
from tkinter import ttk, messagebox
from login_admin import AdminLoginApp
from database import db # <-- Importamos el gestor de base de datos

# --- 🎨 DEFINICIÓN DE ESTILOS Y COLORES ---
COLOR_BG_POS = '#D4C4B8'        
COLOR_BUTTON_PRIMARY = '#A37F74' 
COLOR_BUTTON_TEXT = '#333333'    
COLOR_GRID_ITEM_BG = '#F5ECE5'   
COLOR_BORDER = '#333333'        
COLOR_HIGHLIGHT_PRODUCT = '#94786A' # Nuevo color para el producto seleccionado

# --- CLASE PRINCIPAL DEL PUNTO DE VENTA (POS) ---
class PosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Punto de Venta - Delicias & Coffee")
        self.geometry("1024x768")
        self.config(bg=COLOR_BG_POS)

        self.admin_password = "admin" 
        self.current_category = "WAFFLES" 
        self.selected_product_button = None 
        
        # 1. Inicializar variables AQUI para evitar errores de Attribute.
        self.all_products = [] 
        self.available_toppings = []
        
        # 2. Cargar datos de la DB AQUI.
        self.load_products() 
        self.load_ingredients()
        
        # 3. Crear la interfaz AQUI (que ahora puede usar los datos cargados).
        self.create_widgets()
        

    def create_widgets(self):
        """Crea todos los elementos de la interfaz del POS."""

        # --- Barra Superior ---
        top_bar = tk.Frame(self, bg=COLOR_BG_POS)
        top_bar.pack(fill="x", pady=10, padx=20)
        self.settings_frame = tk.Frame(top_bar, bg=COLOR_BG_POS)
        self.settings_frame.pack(side="left")
        
        self.settings_button = tk.Button(self.settings_frame, text="⚙️", font=("Arial", 24), 
                                         bg=COLOR_BG_POS, fg=COLOR_BORDER,
                                         relief=tk.FLAT, bd=0, command=self.toggle_admin_panel_options)
        self.settings_button.pack(side="left")
        
        self.admin_options_frame = tk.Frame(self.settings_frame, bg=COLOR_BG_POS, bd=1, relief=tk.SOLID)
        tk.Label(self.admin_options_frame, text="Abrir panel admin.", 
                 font=("Arial", 10), bg=COLOR_BG_POS, fg=COLOR_BORDER).pack(padx=5, pady=2, anchor="w")
        
        self.admin_password_entry = tk.Entry(self.admin_options_frame, width=15, show="*",
                                              bg=COLOR_GRID_ITEM_BG, fg=COLOR_BUTTON_TEXT,
                                              insertbackground=COLOR_BUTTON_TEXT, bd=0, relief=tk.FLAT)
        self.admin_password_entry.pack(padx=5, pady=2)
        self.admin_password_entry.bind("<Return>", self.open_admin_login_window)

        exit_button = tk.Button(top_bar, text="🚪", font=("Arial", 24), 
                                bg=COLOR_BG_POS, fg=COLOR_BORDER,
                                relief=tk.FLAT, bd=0, command=self.quit)
        exit_button.pack(side="right")

        # --- Categorías de Productos ---
        categories_frame = tk.Frame(self, bg=COLOR_BG_POS)
        categories_frame.pack(pady=10)

        categories = ["COMBOS", "SALADO", "WAFFLES", "CREPAS", "MINI DONUTS",
                      "MINI HOTCAKES", "FRAPPES", "MALTEADAS", "POSTRES"]
        
        row_num = 0
        col_num = 0
        self.category_buttons = {}
        
        for i, category in enumerate(categories):
            btn = tk.Button(categories_frame, text=category, font=("Arial", 10, "bold"),
                            bg=COLOR_GRID_ITEM_BG, fg=COLOR_BUTTON_TEXT,
                            relief=tk.SOLID, bd=1, padx=15, pady=8,
                            activebackground=COLOR_BUTTON_PRIMARY, 
                            activeforeground="white",
                            command=lambda c=category: self.filter_products_by_category(c))
            btn.grid(row=row_num, column=col_num, padx=5, pady=5, sticky="nsew")
            self.category_buttons[category] = btn
            
            col_num += 1
            if col_num >= 5: 
                col_num = 0
                row_num += 1

        # --- Contenedor Principal: Grid de Productos y Toppings ---
        main_content_frame = tk.Frame(self, bg=COLOR_BG_POS)
        main_content_frame.pack(pady=20, padx=20, expand=True, fill="both")

        main_content_frame.grid_columnconfigure(0, weight=3) # Cuadrícula de Productos
        main_content_frame.grid_columnconfigure(1, weight=1) # Toppings
        main_content_frame.grid_rowconfigure(0, weight=1)

        # 1. Cuadrícula de Productos
        self.products_grid_frame = tk.Frame(main_content_frame, bg=COLOR_BG_POS)
        self.products_grid_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 2. Toppings/Modificadores
        self.toppings_frame = tk.LabelFrame(main_content_frame, text="Toppings / Modificadores", 
                                            font=("Arial", 12, "bold"), bg=COLOR_GRID_ITEM_BG, 
                                            fg=COLOR_BUTTON_TEXT, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.toppings_frame.grid(row=0, column=1, sticky="nsew")

        # Inicializar la vista de productos (ya tiene self.all_products disponible)
        self.filter_products_by_category(self.current_category)

    def load_products(self):
        """Carga todos los productos de la DB en un diccionario."""
        query = "SELECT id, nombre, categoria, precio, habilitado FROM productos"
        self.all_products = db.execute_query(query)
        
    def load_ingredients(self):
        """Carga todos los ingredientes habilitados de la DB."""
        # Nota: Cargamos todos los ingredientes para poder recargarlos fácilmente en el admin, 
        # pero en el POS solo usaremos los habilitados.
        query = "SELECT id, nombre, estado FROM ingredientes" 
        self.all_ingredients = db.execute_query(query)
        
    def filter_products_by_category(self, category):
        """Muestra los productos de la categoría seleccionada."""
        self.current_category = category

        # Resaltar el botón de categoría activo
        for name, btn in self.category_buttons.items():
            bg_color = COLOR_BUTTON_PRIMARY if name == category else COLOR_GRID_ITEM_BG
            fg_color = "white" if name == category else COLOR_BUTTON_TEXT
            btn.config(bg=bg_color, fg=fg_color)
            
        # Limpiar la cuadrícula de productos
        for widget in self.products_grid_frame.winfo_children():
            widget.destroy()
            
        # Si había un producto seleccionado, deseleccionarlo
        if self.selected_product_button:
            self.selected_product_button = None
            self.display_toppings(None) # Limpiar el panel de toppings

        # Filtrar y mostrar los productos habilitados de la categoría
        filtered_products = [p for p in self.all_products if p[2] == category and p[4] == 1]
        
        for r in range(4): 
            self.products_grid_frame.grid_rowconfigure(r, weight=1)
            for c in range(5): 
                self.products_grid_frame.grid_columnconfigure(c, weight=1)
                
                index = r * 5 + c
                if index < len(filtered_products):
                    product_id, name, _, price, _ = filtered_products[index]
                    
                    # Usamos un Frame con un Button para un diseño de tarjeta
                    item_box = tk.Frame(self.products_grid_frame, bg=COLOR_GRID_ITEM_BG, 
                                        relief=tk.SOLID, bd=1)
                    item_box.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                    
                    btn = tk.Button(item_box, 
                                    text=f"{name}\n${price:.2f}", 
                                    font=("Arial", 12, "bold"),
                                    bg=COLOR_GRID_ITEM_BG, fg=COLOR_BUTTON_TEXT,
                                    relief=tk.FLAT, bd=0, 
                                    command=lambda p_id=product_id, p_name=name, box=item_box: self.select_product(p_id, p_name, box))
                    btn.pack(expand=True, fill="both")
                    item_box.product_button = btn # Almacenar la referencia al botón
                else:
                    # Crear cuadros vacíos para completar la cuadrícula
                    item_box = tk.Frame(self.products_grid_frame, bg=COLOR_BG_POS, bd=0)
                    item_box.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

    def select_product(self, product_id, product_name, product_frame):
        """Resalta el producto seleccionado y carga los toppings disponibles."""
        # Restablecer el color del botón previamente seleccionado
        if self.selected_product_button:
            # Buscamos el Frame contenedor del botón para cambiar su color
            if isinstance(self.selected_product_button.master, tk.Frame):
                self.selected_product_button.master.config(bg=COLOR_GRID_ITEM_BG) 
            self.selected_product_button.config(bg=COLOR_GRID_ITEM_BG, fg=COLOR_BUTTON_TEXT)

        # Resaltar el nuevo botón seleccionado
        product_frame.config(bg=COLOR_HIGHLIGHT_PRODUCT) # Resalta el frame
        product_frame.product_button.config(bg=COLOR_HIGHLIGHT_PRODUCT, fg="white") # Resalta el botón
        self.selected_product_button = product_frame.product_button

        # Actualizar la vista de toppings
        self.display_toppings(product_name)

    def display_toppings(self, product_name):
        """Muestra los toppings disponibles, excluyendo los deshabilitados."""
        
        # Limpiar el frame de toppings
        for widget in self.toppings_frame.winfo_children():
            widget.destroy()
            
        if product_name is None:
            tk.Label(self.toppings_frame, text="Selecciona un producto", 
                     font=("Arial", 11, "italic"), bg=COLOR_GRID_ITEM_BG, 
                     fg=COLOR_BUTTON_TEXT).pack(pady=20)
            return

        tk.Label(self.toppings_frame, text=f"Modificadores para:\n{product_name}", 
                 font=("Arial", 11, "italic"), bg=COLOR_GRID_ITEM_BG, 
                 fg=COLOR_BUTTON_TEXT).pack(pady=(0, 10))

        # Recargar solo los ingredientes habilitados
        self.load_ingredients()
        available_toppings = [i for i in self.all_ingredients if i[2] == 1]

        for _, name, _ in available_toppings:
            btn = tk.Button(self.toppings_frame, text=name, 
                            font=("Arial", 10),
                            bg=COLOR_BUTTON_PRIMARY, fg="white",
                            relief=tk.FLAT, bd=0, padx=10, pady=5,
                            command=lambda n=name: print(f"Añadir topping: {n}")) 
            btn.pack(fill="x", pady=2)
            
        if not available_toppings:
             tk.Label(self.toppings_frame, text="No hay toppings disponibles.", 
                     font=("Arial", 10), bg=COLOR_GRID_ITEM_BG, 
                     fg=COLOR_BUTTON_TEXT).pack(pady=20)


    # ... (Funciones de Admin Login y Logout son las mismas) ...
    def toggle_admin_panel_options(self):
        """Muestra u oculta las opciones del panel de administrador."""
        if self.admin_options_frame.winfo_ismapped():
            self.admin_options_frame.pack_forget()
        else:
            self.admin_options_frame.pack(side="left", padx=(10, 0), pady=0)
            self.admin_password_entry.focus_set()

    def open_admin_login_window(self, event=None):
        """Verifica la contraseña del POS para acceder al Login Admin."""
        entered_password = self.admin_password_entry.get()
        if entered_password == self.admin_password:
            self.admin_password_entry.delete(0, tk.END)
            self.toggle_admin_panel_options() 

            admin_login_window = AdminLoginApp(self) 
            admin_login_window.focus_set() 
            self.withdraw() 
            
            admin_login_window.protocol("WM_DELETE_WINDOW", lambda: self.show_pos_and_destroy_login(admin_login_window))
            
            self.wait_window(admin_login_window)
            # Después de cerrar la ventana de admin, recargamos los datos por si hubo cambios
            self.load_products()
            self.load_ingredients()
            self.filter_products_by_category(self.current_category)
            self.deiconify() 

        else:
            messagebox.showerror("Error de Acceso", "Contraseña POS incorrecta.")
            self.admin_password_entry.delete(0, tk.END)

    def show_pos_and_destroy_login(self, login_window):
        """Función para mostrar el POS y destruir la ventana de login."""
        self.deiconify()
        login_window.destroy()


if __name__ == "__main__":
    app = PosApp()
    app.mainloop()