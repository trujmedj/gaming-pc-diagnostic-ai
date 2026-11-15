import sys
from PyQt6.QtWidgets import QApplication
from mvc.model import ModeloDiagnostico
from mvc.view import VistaPrincipal
from mvc.controller import ControladorDiagnostico

def aplicar_estilo_moderno(app):
    """Aplica un QSS global con bordes redondeados y corrige fallos visuales de alineación."""
    estilo = """
    /* Fondo general de la aplicación */
    QMainWindow, QDialog {
        background-color: #F3F4F6;
    }

    /* Estilo general para textos */
    QWidget {
        font-family: "Segoe UI", "Roboto", "Helvetica Neue", sans-serif;
        font-size: 14px;
        color: #1F2937;
    }

    /* Paneles de agrupación (Tarjetas blancas) */
    QGroupBox {
        background-color: #FFFFFF;
        border-radius: 16px; 
        border: 1px solid #D1D5DB;
        margin-top: 28px; 
        padding-top: 15px; 
        padding-bottom: 15px;
        padding-left: 10px;
        padding-right: 10px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 6px 16px;
        background-color: #E0E7FF;
        color: #3730A3;
        font-weight: bold;
        border-radius: 14px;
        left: 16px; 
        top: 0px;   
    }

    /* Botones de acción principales */
    QPushButton {
        background-color: #4F46E5; 
        color: #FFFFFF;
        border-radius: 18px; 
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    
    QPushButton:hover {
        background-color: #4338CA; 
    }
    
    QPushButton:pressed {
        background-color: #312E81; 
    }
    
    QPushButton:disabled {
        background-color: #9CA3AF;
        color: #E5E7EB;
    }

    /* Entradas de texto, ComboBox y SpinBox */
    QComboBox, QSpinBox, QTextEdit {
        background-color: #F9FAFB;
        border: 1px solid #D1D5DB;
        border-radius: 10px; 
        padding: 8px 12px;
        color: #111827;
        min-height: 20px; 
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: url(resources/downarrow.png);
        width: 16px;
        height: 16px;
    }

    QSpinBox::up-button {
        border: none;
        width: 25px;
        margin-top: 2px;
    }

    QSpinBox::up-arrow {
        image: url(resources/uparrow.png);
        width: 14px;
        height: 14px;
    }

    QSpinBox::down-button {
        border: none;
        width: 25px;
        margin-bottom: 2px;
    }

    QSpinBox::down-arrow {
        image: url(resources/downarrow.png);
        width: 14px;
        height: 14px;
    }

    /* Checkboxes y RadioButtons */
    QCheckBox, QRadioButton {
        spacing: 12px;
        padding: 6px;
    }
    
    QCheckBox::indicator, QRadioButton::indicator {
        width: 22px;
        height: 22px;
        border-radius: 11px; 
        border: 2px solid #9CA3AF;
        background-color: #FFFFFF;
    }
    
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background-color: #4F46E5;
        border: 2px solid #4F46E5;
    }

    /* Tablas (Ventanas secundarias) */
    QTableWidget {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #D1D5DB;
        gridline-color: #E5E7EB;
    }
    
    QHeaderView::section {
        background-color: #F3F4F6;
        padding: 10px;
        border: none;
        border-bottom: 2px solid #D1D5DB;
        font-weight: bold;
        color: #374151;
    }

    /* ======== NUEVO: BARRA DE PROGRESO ======== */
    QProgressBar {
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        background-color: #E5E7EB;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #4F46E5;
        border-radius: 5px;
    }
    """
    app.setStyleSheet(estilo)

def main():
    app = QApplication(sys.argv)
    
    aplicar_estilo_moderno(app)
    modelo = ModeloDiagnostico("config_dominio.json")
    vista = VistaPrincipal(modelo)
    controlador = ControladorDiagnostico(modelo, vista)
    
    vista.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()