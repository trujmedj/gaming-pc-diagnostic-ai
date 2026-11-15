import json
import os
import ollama # Importación del motor local de IA

class ModeloDiagnostico:
    def __init__(self, config_path="config_dominio.json"):
        # --- Datos Estáticos (Cargados desde el archivo de parametrización) ---
        self.config_path = config_path
        self.dominio = ""
        self.entidad = ""
        self.sintomas_disponibles = []
        self.obs_categoricos_disponibles = []
        self.obs_cuantitativos_disponibles = []
        
        self.cargar_configuracion()

        # --- Estado Dinámico (Entrada del usuario) ---
        self.sintomas_seleccionados = []  # Lista de IDs de síntomas
        self.observables_valores = {}     # Diccionario {id_observable: valor}
        
        # --- Estado de Gestión de Conocimiento ---
        self.modo_conocimiento = "Local"  # Puede ser "Local" o "Web" 
        self.modelo_llm = "llama3"        # Nombre exacto del modelo en Ollama
        self.pdfs_locales = []            # Lista de dicts con metadatos de PDFs 
        self.fuentes_web = []             # Lista de fuentes consultadas 

        # --- Estado de Resultados (Salida del LLM) ---
        self.hipotesis = []               # Lista de dicts {nombre, probabilidad, estado} 
        self.diagnostico_final = ""       # Texto del diagnóstico final 
        self.confianza_diagnostico = ""   # Nivel de confianza 
        self.justificacion = ""           # Razón del diagnóstico 

    def cargar_configuracion(self):
        """Lee el archivo JSON y parametriza las opciones disponibles para la vista."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dominio = data.get("dominio", "Diagnóstico General")
                self.entidad = data.get("entidad_diagnostico", "Sistema")
                self.sintomas_disponibles = data.get("sintomas", [])
                self.obs_categoricos_disponibles = data.get("observables_categoricos", [])
                self.obs_cuantitativos_disponibles = data.get("observables_cuantitativos", [])
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.config_path}. Se usarán listas vacías.")
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.config_path} no es un JSON válido.")

    # --- Métodos para actualizar el estado desde el Controlador ---
    def actualizar_entrada_usuario(self, sintomas, observables, modo="Local"):
        self.sintomas_seleccionados = sintomas
        self.observables_valores = observables
        self.modo_conocimiento = modo

    def anadir_pdf(self, ruta, nombre, tamano):
        self.pdfs_locales.append({"ruta": ruta, "nombre": nombre, "tamano": tamano})

    def vaciar_pdfs(self):
        self.pdfs_locales = []

    def set_resultados_llm(self, hipotesis, diagnostico, confianza, justificacion):
        self.hipotesis = hipotesis
        self.diagnostico_final = diagnostico
        self.confianza_diagnostico = confianza
        self.justificacion = justificacion

# --- NUEVO MÉTODO: Integración con Ollama ---
    def ejecutar_diagnostico_ia(self):
        """Construye el prompt con los datos actuales y consulta a Ollama."""
        
        # 1. Crear diccionarios de traducción (ID -> Texto legible)
        desc_sintomas = {s["id"]: s["descripcion"] for s in self.sintomas_disponibles}
        
        etiquetas_obs = {}
        for obs in self.obs_categoricos_disponibles:
            etiquetas_obs[obs["id"]] = obs["etiqueta"]
        for obs in self.obs_cuantitativos_disponibles:
            etiquetas_obs[obs["id"]] = obs["etiqueta"]

        # 2. Traducir las selecciones del usuario a texto real
        sintomas_traducidos = [desc_sintomas.get(sid, sid) for sid in self.sintomas_seleccionados]
        texto_sintomas = ", ".join(sintomas_traducidos) if sintomas_traducidos else "Ninguno reportado"
        
        # Formateamos los observables uno por línea para mayor claridad
        obs_traducidos = [f"{etiquetas_obs.get(k, k)}: {v}" for k, v in self.observables_valores.items()]
        texto_observables = "\n        - ".join(obs_traducidos) if obs_traducidos else "Ninguno reportado"
        
        # 3. Diseñamos el Prompt para el LLM
        prompt = f"""
        Actúa como un experto en diagnóstico para el dominio: {self.dominio}.
        La entidad a diagnosticar es: {self.entidad}.
        
        A continuación te presento los datos recogidos:
        - Síntomas presentados: {texto_sintomas}
        - Observables medidos: 
        - {texto_observables}
        """

        # --- NUEVO: CONDICIÓN DE CONTEXTO PARA LA IA ---
        if self.modo_conocimiento == "Local" and not self.pdfs_locales:
            prompt += "\n        Nota para la IA: El usuario no ha proporcionado manuales técnicos en PDF. Basa tu diagnóstico EXCLUSIVAMENTE en tu conocimiento general sobre hardware y videojuegos."
        elif self.modo_conocimiento == "Local" and self.pdfs_locales:
             prompt += f"\n        Nota para la IA: El usuario ha proporcionado {len(self.pdfs_locales)} documento(s) PDF. Prioriza la información de estos documentos para emitir tu diagnóstico."
        elif self.modo_conocimiento == "Web":
             prompt += "\n        Nota para la IA: El usuario ha activado el Modo Web. Ten en cuenta las últimas novedades, foros y guías de hardware de internet para enriquecer tu diagnóstico."

        prompt += "\n\n        Por favor, analiza estos datos y devuelve un diagnóstico final, el nivel de confianza (Alto/Medio/Bajo) y una breve justificación de tu razonamiento."
        
        try:
            # Llamada al motor local de Ollama
            respuesta_bruta = ollama.generate(model=self.modelo_llm, prompt=prompt)
            texto_respuesta = respuesta_bruta['response']
            
            # Guardamos TODO lo que ha dicho la IA en la justificación
            self.justificacion = texto_respuesta
            
            # En el diagnóstico final ponemos un resumen para la ventanita pequeña
            self.diagnostico_final = "Análisis completado. Por favor, abre la justificación para leer el informe detallado de la IA."
            self.confianza_diagnostico = "Alta (Generada por LLM)"
            
            return True, "Diagnóstico generado correctamente."
        except Exception as e:
            error_msg = f"Fallo al conectar con Ollama. Asegúrate de tener el servidor encendido. Detalle: {str(e)}"
            self.diagnostico_final = "Error de conexión."
            self.justificacion = error_msg
            return False, error_msg