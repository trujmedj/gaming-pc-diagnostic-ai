from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QCheckBox, QLabel, QComboBox, QSpinBox, 
                             QPushButton, QGroupBox, QRadioButton, QDialog, 
                             QTableWidget, QTableWidgetItem, QTextEdit, 
                             QHeaderView, QFileDialog, QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

# =====================================================================
# VENTANAS SECUNDARIAS (QDialogs)
# =====================================================================

class VentanaHipotesis(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hipótesis Posibles")
        self.resize(500, 300)
        layout = QVBoxLayout(self)

        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Hipótesis", "Probabilidad", "Estado"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

    def actualizar_datos(self, hipotesis_lista):
        self.tabla.setRowCount(0)
        for row, hip in enumerate(hipotesis_lista):
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(hip.get("nombre", ""))))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(hip.get("probabilidad", ""))))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(hip.get("estado", ""))))

class VentanaDiagnostico(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Diagnóstico Final (Generado por Ollama)") 
        self.resize(450, 200) # Lo he hecho un pelín más ancho para que quepan los dos botones
        layout = QVBoxLayout(self)

        self.lbl_diagnostico = QLabel("<b>Diagnóstico:</b> ")
        self.lbl_diagnostico.setWordWrap(True)
        self.lbl_confianza = QLabel("<b>Nivel de confianza:</b> ")
        
        layout.addWidget(self.lbl_diagnostico)
        layout.addWidget(self.lbl_confianza)

        # --- NUEVOS BOTONES DE ACCIÓN ---
        btn_layout = QHBoxLayout()
        
        # Botón para ir directo a la justificación
        self.btn_ver_justificacion = QPushButton("Leer Justificación Detallada")
        self.btn_ver_justificacion.setStyleSheet("""
            QPushButton {
                background-color: #10B981; /* Color verde esmeralda para destacar */
                color: white;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        # Al hacer clic, cerramos esta ventanita pequeña (el controlador abrirá la grande)
        self.btn_ver_justificacion.clicked.connect(self.accept) 
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_ver_justificacion)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)

    def actualizar_datos(self, diagnostico, confianza):
        self.lbl_diagnostico.setText(f"<b>Diagnóstico:</b> {diagnostico}")
        self.lbl_confianza.setText(f"<b>Nivel de confianza:</b> {confianza}")
        
class VentanaJustificacion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Justificación de la IA (Ollama)") 
        self.resize(600, 400)
        layout = QVBoxLayout(self)

        self.texto_justificacion = QTextEdit()
        self.texto_justificacion.setReadOnly(True) 
        layout.addWidget(self.texto_justificacion)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

    def actualizar_datos(self, justificacion_texto):
                self.texto_justificacion.setMarkdown(justificacion_texto)

class VentanaPDFs(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de PDFs")
        self.resize(500, 300)
        layout = QVBoxLayout(self)

        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Ruta", "Tamaño"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        btn_layout = QHBoxLayout()
        self.btn_anadir = QPushButton("Añadir PDFs")
        self.btn_eliminar = QPushButton("Eliminar Seleccionados")
        self.btn_vaciar = QPushButton("Vaciar Lista")
        
        btn_layout.addWidget(self.btn_anadir)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_vaciar)
        layout.addLayout(btn_layout)

    def actualizar_datos(self, lista_pdfs):
        self.tabla.setRowCount(0)
        for row, pdf in enumerate(lista_pdfs):
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(pdf.get("nombre", ""))))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(pdf.get("ruta", ""))))
            self.tabla.setItem(row, 2, QTableWidgetItem(f"{pdf.get('tamano', 0)} bytes"))

class VentanaWeb(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fuentes Web Utilizadas")
        self.resize(600, 300)
        layout = QVBoxLayout(self)

        self.tabla = QTableWidget(0, 3)
        self.tabla.setHorizontalHeaderLabels(["Título", "URL", "Fecha"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

    def actualizar_datos(self, lista_fuentes):
        self.tabla.setRowCount(0)
        for row, fuente in enumerate(lista_fuentes):
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(fuente.get("titulo", ""))))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(fuente.get("url", ""))))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(fuente.get("fecha", ""))))


# =====================================================================
# VENTANA PRINCIPAL (QMainWindow)
# =====================================================================

class VistaPrincipal(QMainWindow):
    def __init__(self, modelo):
        super().__init__()
        self.modelo = modelo
        self.initUI()

        self.dialogo_hipotesis = VentanaHipotesis(self)
        self.dialogo_diagnostico = VentanaDiagnostico(self)
        self.dialogo_justificacion = VentanaJustificacion(self)
        self.dialogo_pdfs = VentanaPDFs(self)
        self.dialogo_web = VentanaWeb(self)

    def initUI(self):
        self.setWindowTitle("Herramienta de diagnóstico de rendimiento")
        self.setGeometry(100, 100, 750, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- HEADER CON LOGO ---
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        
        logo_label = QLabel()
        try:
            pixmap = QPixmap("resources/ollama-icon.png")
            scaled_pixmap = pixmap.scaledToHeight(50, Qt.TransformationMode.SmoothTransformation) 
            logo_label.setPixmap(scaled_pixmap)
        except:
            pass # Si falla al cargar la imagen, simplemente no se muestra
            
        header_layout.addWidget(logo_label)
        
        title_decorativo = QLabel("¿Por dónde empezamos?")
        title_decorativo.setStyleSheet("font-size: 20px; font-weight: bold; color: #3730A3; margin-left: 10px;")
        header_layout.addWidget(title_decorativo)
        
        main_layout.addLayout(header_layout)

        # --- 1. SECCIÓN DE SÍNTOMAS --- 
        sintomas_group = QGroupBox("Entrada de Síntomas")
        sintomas_layout = QVBoxLayout()
        self.checkboxes_sintomas = {}
        
        for sintoma in self.modelo.sintomas_disponibles:
            cb = QCheckBox(sintoma["descripcion"])
            self.checkboxes_sintomas[sintoma["id"]] = cb
            sintomas_layout.addWidget(cb)
            
        sintomas_group.setLayout(sintomas_layout)
        main_layout.addWidget(sintomas_group)

        # --- 2. SECCIÓN DE OBSERVABLES --- 
        obs_group = QGroupBox("Observables")
        obs_layout = QVBoxLayout()
        self.inputs_observables = {}
        
        for obs in self.modelo.obs_categoricos_disponibles:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(obs["etiqueta"] + ":"))
            combo = QComboBox()
            combo.addItems(obs["valores"])
            self.inputs_observables[obs["id"]] = combo
            h_layout.addWidget(combo)
            obs_layout.addLayout(h_layout)
            
        for obs in self.modelo.obs_cuantitativos_disponibles:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(obs["etiqueta"] + ":"))
            spin = QSpinBox()
            spin.setRange(obs["rango"][0], obs["rango"][1])
            self.inputs_observables[obs["id"]] = spin
            h_layout.addWidget(spin)
            obs_layout.addLayout(h_layout)
            
        obs_group.setLayout(obs_layout)
        main_layout.addWidget(obs_group)

        # --- 3. SELECTOR DE MODO --- 
        modo_group = QGroupBox("Selector de Modo de Conocimiento")
        modo_layout = QHBoxLayout()
        self.btn_local = QRadioButton("Modo Local (Sólo PDFs)") 
        self.btn_web = QRadioButton("Modo Web (Internet + PDFs)")
        self.btn_local.setChecked(True) 
        
        modo_layout.addWidget(self.btn_local)
        modo_layout.addWidget(self.btn_web)
        modo_group.setLayout(modo_layout)
        main_layout.addWidget(modo_group)

        # --- 4. CONTROLES DE ACCIÓN --- 
        btn_layout = QHBoxLayout()
        self.btn_evaluar = QPushButton("Evaluar Hipótesis") 
        self.btn_diagnosticar = QPushButton("Diagnosticar con IA (Ollama)") 
        self.btn_justificacion = QPushButton("Ver Justificación")
        self.btn_pdfs = QPushButton("Gestión de PDFs") 
        self.btn_web_sources = QPushButton("Fuentes Web")
        
        btn_layout.addWidget(self.btn_evaluar)
        btn_layout.addWidget(self.btn_diagnosticar)
        btn_layout.addWidget(self.btn_justificacion)
        btn_layout.addWidget(self.btn_pdfs)
        btn_layout.addWidget(self.btn_web_sources)
        
        main_layout.addLayout(btn_layout)

        # --- 5. BARRA DE ESTADO Y PROGRESO ---
        status_layout = QVBoxLayout() # Usamos vertical para apilar el texto y la barra
        
        self.lbl_estado = QLabel("Estado: Motor IA (Ollama) conectado y listo.")
        self.lbl_estado.setStyleSheet("color: gray; font-style: italic;")
        self.lbl_estado.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Nueva barra de progreso (indeterminada)
        self.barra_progreso = QProgressBar()
        self.barra_progreso.setRange(0, 0) # Rango 0,0 la hace indeterminada (animación contínua)
        self.barra_progreso.setTextVisible(False)
        self.barra_progreso.setFixedHeight(12) # Fina y elegante
        self.barra_progreso.setVisible(False) # Oculta por defecto
        
        status_layout.addWidget(self.lbl_estado)
        status_layout.addWidget(self.barra_progreso)
        main_layout.addLayout(status_layout)

    def obtener_datos_interfaz(self):
        sintomas_seleccionados = [sid for sid, cb in self.checkboxes_sintomas.items() if cb.isChecked()]
        
        observables = {}
        for oid, widget in self.inputs_observables.items():
            if isinstance(widget, QComboBox):
                observables[oid] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                observables[oid] = widget.value()
                
        modo = "Local" if self.btn_local.isChecked() else "Web"
        
        return sintomas_seleccionados, observables, modo
