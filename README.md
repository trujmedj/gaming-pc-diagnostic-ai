# Práctica ISSBC: Interfaz MVC para Sistema de Diagnóstico con IA Local (Ollama)

## 1. Dominio elegido y breve descripción

**Dominio:** Diagnóstico de Configuración de Videojuegos (Optimización de FPS)

**Descripción:** Esta aplicación asiste a los usuarios en la identificación de problemas de rendimiento en sus ordenadores al ejecutar videojuegos. A través de la selección de síntomas (stuttering, bajos FPS, crashes) y la introducción de observables técnicos (temperaturas de CPU/GPU, cantidad de RAM, resoluciones), el sistema genera un diagnóstico automatizado.

Como característica adicional de diseño, las vistas se generan de forma dinámica a partir de un archivo de configuración (`config_dominio.json`), permitiendo adaptar el dominio sin modificar el código fuente de la interfaz. El núcleo cognitivo del sistema está impulsado por un modelo de lenguaje grande (LLM) ejecutado localmente mediante **Ollama**, lo que garantiza la privacidad de los datos y un análisis inteligente de las métricas.

## 2. Instrucciones de ejecución y Requisitos

Para ejecutar la aplicación correctamente, el sistema utiliza inteligencia artificial en local, por lo que debes seguir estos pasos:

1. **Instalar Ollama:** Asegúrate de tener [Ollama](https://ollama.com/) instalado en tu sistema.
2. **Descargar el modelo de IA:** Abre tu terminal y descarga el modelo necesario ejecutando:
   `ollama run llama3` (Asegúrate de que el servidor de Ollama esté encendido antes de arrancar la app).
3. **Instalar dependencias de Python:** Asegúrate de tener Python 3.x instalado y ejecuta:
   `pip install PyQt6 ollama`
4. Sitúate en el directorio raíz del proyecto (donde se encuentra `main.py` y `config_dominio.json`).
5. Ejecuta el programa principal con el comando:
   `python main.py`

## 3. Descripción de la arquitectura MVC usada

El proyecto cumple estrictamente con el patrón arquitectónico Modelo-Vista-Controlador (MVC) para separar las responsabilidades, incorporando además concurrencia para una mejor experiencia de usuario:

- **Modelo (`mvc/model.py`):** Mantiene el estado de la aplicación. Lee el archivo JSON para conocer los síntomas y observables disponibles. Almacena las selecciones del usuario, los PDFs aportados y gestiona la **conexión directa con la API de Ollama** para la construcción de _prompts_ y la generación de diagnósticos, todo ello sin interactuar con la interfaz gráfica.
- **Vista (`mvc/view.py`):** Construida con PyQt6. Solo se encarga de dibujar la interfaz (generando componentes dinámicamente y aplicando QSS para el estilo e iconos personalizados) y capturar las interacciones del usuario. Contiene la ventana principal y los diálogos (Hipótesis, Diagnóstico, Justificación, PDFs y Fuentes Web).
- **Controlador (`mvc/controller.py`):** Es el coordinador central. Conecta las señales de la vista con la lógica del modelo. Para evitar que la interfaz se congele durante el tiempo de inferencia de la IA, **implementa un hilo secundario (`QThread` en `TrabajadorIA`)**. Este hilo se comunica de forma asíncrona con la ventana principal para actualizar los estados visuales (como la barra de estado inferior) y lanzar los diálogos de resultados una vez Ollama termina su proceso.

## 4. Explicación del modo Local/Web y su reflejo en la UI

El sistema permite al usuario elegir qué fuentes de conocimiento debe utilizar la IA para generar su diagnóstico y justificación:

- **Modo Local:** Restringe el contexto de búsqueda estrictamente a los documentos PDF proporcionados por el usuario y los síntomas introducidos en la interfaz. Ideal para diagnósticos basados en manuales de hardware específicos.
- **Modo Web:** Permite al sistema simular la búsqueda de información adicional y fiable en internet (foros, guías de hardware) para enriquecer el diagnóstico de la IA, además de los PDFs locales.

**Reflejo en la UI:**
Esta selección se refleja en la interfaz principal mediante un `QGroupBox` con opciones excluyentes (`QRadioButton`) de "Modo Local" y "Modo Web". Cuando se genera un diagnóstico, la ventana de **Justificación** refleja el texto generado por Ollama. Además, la interfaz incluye un botón dedicado a **"Fuentes Web"**; si se hace clic en él estando en Modo Local, el sistema informa mediante una alerta de que no se ha utilizado internet. Si se está en Modo Web, despliega una tabla (`QTableWidget`) con el título, URL y fecha de acceso de las páginas consultadas, garantizando la trazabilidad del proceso.
