import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# =================================================================
# NUEVO: HILO SECUNDARIO PARA LA IA
# =================================================================
class TrabajadorIA(QThread):
    terminado = pyqtSignal(bool, str)

    def __init__(self, modelo):
        super().__init__()
        self.modelo = modelo

    def run(self):
        exito, mensaje = self.modelo.ejecutar_diagnostico_ia()
        self.terminado.emit(exito, mensaje)


class ControladorDiagnostico:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.trabajador_ia = None 

        self.vista.btn_evaluar.clicked.connect(self.evaluar_hipotesis)
        self.vista.btn_diagnosticar.clicked.connect(self.iniciar_diagnostico_ia)
        self.vista.btn_justificacion.clicked.connect(self.mostrar_justificacion)
        self.vista.btn_pdfs.clicked.connect(self.gestionar_pdfs)
        self.vista.btn_web_sources.clicked.connect(self.mostrar_fuentes_web)
        self.vista.dialogo_diagnostico.btn_ver_justificacion.clicked.connect(self.mostrar_justificacion)

        self.vista.dialogo_pdfs.btn_anadir.clicked.connect(self.anadir_pdf)
        self.vista.dialogo_pdfs.btn_eliminar.clicked.connect(self.eliminar_pdf)
        self.vista.dialogo_pdfs.btn_vaciar.clicked.connect(self.vaciar_pdfs)

    # =================================================================
    # INTEGRACIÓN CON OLLAMA (CONCURRENTE)
    # =================================================================
    def iniciar_diagnostico_ia(self):
        sintomas, observables, modo = self.vista.obtener_datos_interfaz()
        self.modelo.actualizar_entrada_usuario(sintomas, observables, modo)

        if not sintomas:
            QMessageBox.warning(self.vista, "Aviso", "Por favor, selecciona al menos un síntoma antes de consultar a la IA.")
            return

        if modo == "Local" and not self.modelo.pdfs_locales:
            QMessageBox.information(
                self.vista, 
                "Diagnóstico sin PDFs", 
                "No se han detectado PDFs aportados. El diagnóstico se realizará utilizando el conocimiento general de la IA sobre hardware y videojuegos."
            )

        # --- NUEVO FEEDBACK VISUAL ---
        self.vista.lbl_estado.setText("Estado: Analizando datos con Ollama. Por favor, espera...")
        self.vista.btn_diagnosticar.setEnabled(False)
        self.vista.btn_evaluar.setEnabled(False)
        
        # 1. Mostrar la barra de progreso animada
        self.vista.barra_progreso.setVisible(True)
        # 2. Cambiar el cursor del ratón a "Cargando"
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.trabajador_ia = TrabajadorIA(self.modelo)
        self.trabajador_ia.terminado.connect(self.finalizar_diagnostico_ia)
        self.trabajador_ia.start()

    def finalizar_diagnostico_ia(self, exito, mensaje):
        # --- RESTAURAR FEEDBACK VISUAL ---
        self.vista.lbl_estado.setText("Estado: Motor IA (Ollama) conectado y listo.")
        self.vista.btn_diagnosticar.setEnabled(True)
        self.vista.btn_evaluar.setEnabled(True)
        
        # 1. Ocultar la barra de progreso
        self.vista.barra_progreso.setVisible(False)
        # 2. Restaurar el cursor normal del ratón
        QApplication.restoreOverrideCursor()

        if exito:
            self.vista.dialogo_diagnostico.actualizar_datos(self.modelo.diagnostico_final, self.modelo.confianza_diagnostico)
            self.vista.dialogo_diagnostico.exec()
        else:
            QMessageBox.critical(self.vista, "Error de IA", mensaje)

    # =================================================================
    # RESTO DE FUNCIONES
    # =================================================================
    def evaluar_hipotesis(self):
        self.modelo.hipotesis = [
            {"nombre": "Análisis inteligente centralizado", "probabilidad": "Gestionado por Ollama", "estado": "En proceso"},
            {"nombre": "Evaluación de métricas de Hardware", "probabilidad": "Alta", "estado": "Delegado a la IA"}
        ]
        self.vista.dialogo_hipotesis.actualizar_datos(self.modelo.hipotesis)
        self.vista.dialogo_hipotesis.exec()

    def mostrar_justificacion(self):
        if not self.modelo.justificacion:
            QMessageBox.information(self.vista, "Info", "Primero debes generar un diagnóstico con la IA para ver su justificación.")
            return
        self.vista.dialogo_justificacion.actualizar_datos(self.modelo.justificacion)
        self.vista.dialogo_justificacion.exec()

    def mostrar_fuentes_web(self):
        _, _, modo = self.vista.obtener_datos_interfaz()
        if modo == "Local":
            QMessageBox.information(self.vista, "Modo Local", "Estás en Modo Local. No se han usado fuentes web.")
            return
            
        self.vista.dialogo_web.actualizar_datos(self.modelo.fuentes_web)
        self.vista.dialogo_web.exec()

    def gestionar_pdfs(self):
        self.vista.dialogo_pdfs.actualizar_datos(self.modelo.pdfs_locales)
        self.vista.dialogo_pdfs.exec()

    def anadir_pdf(self):
        rutas, _ = QFileDialog.getOpenFileNames(self.vista, "Seleccionar PDFs", "", "Archivos PDF (*.pdf)")
        for ruta in rutas:
            nombre = os.path.basename(ruta)
            tamano = os.path.getsize(ruta)
            self.modelo.anadir_pdf(ruta, nombre, tamano)
        self.vista.dialogo_pdfs.actualizar_datos(self.modelo.pdfs_locales)

    def eliminar_pdf(self):
        filas_seleccionadas = set(item.row() for item in self.vista.dialogo_pdfs.tabla.selectedItems())
        for fila in sorted(filas_seleccionadas, reverse=True):
            del self.modelo.pdfs_locales[fila]
        self.vista.dialogo_pdfs.actualizar_datos(self.modelo.pdfs_locales)

    def vaciar_pdfs(self):
        self.modelo.vaciar_pdfs()
        self.vista.dialogo_pdfs.actualizar_datos(self.modelo.pdfs_locales)