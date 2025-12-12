"""
Internationalization (i18n) support for TopoVision.

This module provides a simple framework for translating UI strings.
"""

from typing import Any, Callable, Dict, Protocol

# Default language
DEFAULT_LANG = "en"

# English translations
en = {
    "app_title": "TopoVision - 3D Topographic Analysis",
    "analysis_controls_title": "Analysis Controls",
    "calculation_parameters_title": "Calculation Parameters",
    "z_factor_label": "Z-Factor:",
    "z_factor_info": "Height values scale\n1.0 = normal, >1.0 = more sensitive",
    "scale_label": "Scale (px/m):",
    "scale_info": "Pixels per meter\nDefines the real-world scale",
    "unit_label": "Unit:",
    "analysis_actions_title": "Analysis Actions",
    "gradient_button": "Calculate Gradient",
    "volume_button": "Calculate Volume",
    "arc_length_button": "Calculate Arc Length",
    "visualization_title": "Visualization",
    "toggle_view_button": "Toggle View",
    "clear_selection_button": "Clear Selection",
    "status_ready": "System ready. Select a region or calibrate.",
    "open_camera_button": "Open Camera",
    "pause_camera_button": "Pause Camera",
    "resume_camera_button": "Resume Camera",
    "exit_button": "Exit",
    "open_3d_plot_button": "Open 3D Plot Window",
    "camera_error": "Could not connect to the camera. Error: {error}",
    "region_error": "Please select a rectangular region first.",
    "z_factor_error": "The Z-Factor must be a positive number.",
    "scale_error": "The Scale must be a positive number.",
    "analysis_completed": "Calculation completed. Showing results.",
    "camera_started": "Camera started successfully.",
    "camera_paused": "Camera paused.",
    "calculating_gradient": "Calculated gradient: dx={dx:.2f}, dy={dy:.2f}",
    "calculating_volume": "Calculated volume: {volume:.2f} {units}",
    "calculating_arc_length": "Calculated arc length: {length:.2f} {units}",
    "selection_cleared": "Selection cleared.",
    "view_changed_to_analysis": "View changed to: Analysis",
    "view_changed_to_camera": "View changed to: Live Camera",
    "no_analysis_to_show": "No analysis results to show.",
    "click_to_start": "Click 'Open Camera' to begin",
    "closing_app": "Closing application...",
    "selection_made": "Region: {width_px}x{height_px} px ({width_unit:.2f}x{height_unit:.2f} {unit})",
    "selection_too_small": "Selection too small. Minimum {min_size}x{min_size} pixels.",
    "no_frame_to_analyze": "No frame available to analyze.",
    "calculating": "Calculating {method}...",
    "calculation_error": "Error during calculation: {error}",
    "3d_plot_window_title": "3D Topographic Analysis - Live Surface Viewer",
    "no_3d_plot_yet": "No 3D plot generated yet.",
    "3d_plot_window_opened": "3D Live Surface window opened.",
    "3d_surface_plot_title": "Live 3D Surface Plot of Selected Region",
    "3d_surface_plot_generated": "Live 3D Surface Plot initialized.",
    # Calibration
    "calibration_title": "Perspective Calibration",
    "calibrate_button": "Calibrate Perspective",
    "calibration_start_prompt": "Calibration started. Click the 4 corners of a real-world rectangle.",
    "calibration_point_added": "Point {count}/4 added. Click the next corner.",
    "calibration_complete_prompt": "All 4 points selected. Enter the real-world dimensions.",
    "real_width_label": "Real Width (m):",
    "real_height_label": "Real Height (m):",
    "apply_calibration_button": "Apply Calibration",
    "calibration_applied": "Perspective calibration applied successfully.",
    "calibration_error": "Calibration failed. Please try again.",
    "calibration_invalid_dimensions": "Real-world dimensions must be positive numbers.",
    # --- Tutorials ---
    # Startup
    "tutorial_app_start_title": "Welcome to TopoVision!",
    "tutorial_app_start_message": "To get started, please press the 'Open Camera' button at the bottom of the screen.",
    "tutorial_analysis_panel_title": "The Analysis Panel",
    "tutorial_analysis_panel_message": (
        "This panel on the right is your control center. Here you can set calculation parameters, "
        "run analyses, and manage the display."
    ),
    # Features
    "tutorial_z_factor_title": "What is the Z-Factor?",
    "tutorial_z_factor_message": (
        "The Z-Factor is a multiplier that scales the height (or intensity) of the data. A value greater than 1.0 "
        "exaggerates the peaks and valleys, making subtle topographic features more visible in 3D plots and "
        "calculations."
    ),
    "tutorial_scale_title": "What is Scale?",
    "tutorial_scale_message": (
        "The Scale defines how many pixels in the image correspond to one meter in the real world. If you have not "
        "performed a perspective calibration, you must set this value manually to get accurate measurements. "
        "For example, if an object you know is 2 meters wide appears as 200 pixels wide in the image, "
        "the scale is 100."
    ),
    "tutorial_calibrate_perspective_title": "Perspective Calibration",
    "tutorial_calibrate_perspective_message": (
        "To get accurate real-world measurements, you must calibrate the perspective. First, click the four "
        "corners of a known rectangle in the camera view (e.g., a piece of paper). Then, enter its actual "
        "width and height in meters in the fields that appear."
    ),
    "tutorial_toggle_view_title": "Toggle View",
    "tutorial_toggle_view_message": (
        "This button switches the main view between the live camera feed and the last analysis result "
        "(like a gradient heatmap)."
    ),
    "tutorial_clear_selection_title": "Clear Selection",
    "tutorial_clear_selection_message": (
        "This button removes any selection rectangle from the canvas, allowing you to draw a new one."
    ),
    "tutorial_gradient_title": "Gradient Analysis Tutorial",
    "tutorial_gradient_message": (
        "The Gradient Analysis calculates the rate of change of height in both X and Y directions within the "
        "selected region. This helps visualize slopes and steepness. A heatmap will be overlaid on your image."
    ),
    "tutorial_volume_title": "Volume Calculation Tutorial",
    "tutorial_volume_message": (
        "The Volume Calculation estimates the volume under the surface defined by the selected region. "
        "The 'Z-Factor' scales the height values, allowing you to adjust the perceived depth."
    ),
    "tutorial_arc_length_title": "Arc Length Calculation Tutorial",
    "tutorial_arc_length_message": (
        "Arc Length estimates the length of a curve. For image analysis, it typically calculates the length of a "
        "cross-section (e.g., a middle row) within your selected region."
    ),
    "tutorial_plot3d_title": "3D Live Surface Plot Tutorial",
    "tutorial_plot3d_message": (
        "The 3D Live Surface Plot visualizes the selected region as a dynamic 3D topographic map. Brighter areas "
        "in the original image correspond to higher elevations. You can adjust colormap, shading, and resolution "
        "using the controls on the left. Select a region in the main window to see it in 3D."
    ),
}

# Spanish translations
es = {
    "app_title": "TopoVision - Análisis Topográfico 3D",
    "analysis_controls_title": "Controles de Análisis",
    "calculation_parameters_title": "Parámetros de Cálculo",
    "z_factor_label": "Factor Z:",
    "z_factor_info": "Escala de valores de altura\n1.0 = normal, >1.0 = más sensible",
    "scale_label": "Escala (px/m):",
    "scale_info": "Píxeles por metro\nDefine la escala del mundo real",
    "unit_label": "Unidad:",
    "analysis_actions_title": "Acciones de Análisis",
    "gradient_button": "Calcular Gradiente",
    "volume_button": "Calcular Volumen",
    "arc_length_button": "Calcular Longitud de Arco",
    "visualization_title": "Visualización",
    "toggle_view_button": "Alternar Vista",
    "clear_selection_button": "Borrar Selección",
    "status_ready": "Sistema listo. Selecciona una región o calibra.",
    "open_camera_button": "Abrir Cámara",
    "pause_camera_button": "Pausar Cámara",
    "resume_camera_button": "Reanudar Cámara",
    "exit_button": "Salir",
    "open_3d_plot_button": "Abrir Ventana de Gráficos 3D",
    "camera_error": "No se pudo conectar con la cámara. Error: {error}",
    "region_error": "Por favor, selecciona una región rectangular primero.",
    "z_factor_error": "El Factor Z debe ser un número positivo.",
    "scale_error": "La Escala debe ser un número positivo.",
    "analysis_completed": "Cálculo completado. Mostrando resultados.",
    "camera_started": "Cámara iniciada correctamente.",
    "camera_paused": "Cámara pausada.",
    "calculating_gradient": "Gradiente calculado: dx={dx:.2f}, dy={dy:.2f}",
    "calculating_volume": "Volumen calculado: {volume:.2f} {units}",
    "calculating_arc_length": "Longitud de arco calculada: {length:.2f} {units}",
    "selection_cleared": "Selección borrada.",
    "view_changed_to_analysis": "Vista cambiada a: Análisis",
    "view_changed_to_camera": "Vista cambiada a: Cámara en Vivo",
    "no_analysis_to_show": "No hay resultados de análisis para mostrar.",
    "click_to_start": "Haz clic en 'Abrir Cámara' para comenzar",
    "closing_app": "Cerrando aplicación...",
    "selection_made": "Región: {width_px}x{height_px} px ({width_unit:.2f}x{height_unit:.2f} {unit})",
    "selection_too_small": "Selección muy pequeña. Mínimo {min_size}x{min_size} píxeles.",
    "no_frame_to_analyze": "No hay fotograma para analizar.",
    "calculating": "Calculando {method}...",
    "calculation_error": "Error durante el cálculo: {error}",
    "3d_plot_window_title": "Visor de Superficie 3D en Vivo",
    "no_3d_plot_yet": "Aún no se ha generado ningún gráfico 3D.",
    "3d_plot_window_opened": "Ventana de Superficie 3D en Vivo abierta.",
    "3d_surface_plot_title": "Gráfico de Superficie 3D de la Región Seleccionada",
    "3d_surface_plot_generated": "Gráfico de Superficie 3D inicializado.",
    # Calibration
    "calibration_title": "Calibración de Perspectiva",
    "calibrate_button": "Calibrar Perspectiva",
    "calibration_start_prompt": "Calibración iniciada. Haz clic en las 4 esquinas de un rectángulo del mundo real.",
    "calibration_point_added": "Punto {count}/4 añadido. Haz clic en la siguiente esquina.",
    "calibration_complete_prompt": "4 puntos seleccionados. Introduce las dimensiones reales.",
    "real_width_label": "Ancho Real (m):",
    "real_height_label": "Alto Real (m):",
    "apply_calibration_button": "Aplicar Calibración",
    "calibration_applied": "Calibración de perspectiva aplicada con éxito.",
    "calibration_error": "La calibración ha fallado. Por favor, inténtalo de nuevo.",
    "calibration_invalid_dimensions": "Las dimensiones reales deben ser números positivos.",
    # --- Tutoriales ---
    # Inicio
    "tutorial_app_start_title": "¡Bienvenido a TopoVision!",
    "tutorial_app_start_message": (
        "Para comenzar, por favor presiona el botón 'Abrir Cámara' en la parte inferior de la pantalla."
    ),
    "tutorial_analysis_panel_title": "El Panel de Análisis",
    "tutorial_analysis_panel_message": (
        "Este panel a la derecha es tu centro de control. Aquí puedes establecer parámetros de cálculo, "
        "ejecutar análisis y gestionar la visualización."
    ),
    # Funcionalidades
    "tutorial_z_factor_title": "¿Qué es el Factor Z?",
    "tutorial_z_factor_message": (
        "El Factor Z es un multiplicador que escala la altura (o intensidad) de los datos. Un valor mayor que 1.0 "
        "exagera los picos y valles, haciendo que las características topográficas sutiles sean más visibles "
        "en los gráficos 3D y los cálculos."
    ),
    "tutorial_scale_title": "¿Qué es la Escala?",
    "tutorial_scale_message": (
        "La Escala define cuántos píxeles en la imagen corresponden a un metro en el mundo real. Si no has "
        "realizado una calibración de perspectiva, debes establecer este valor manualmente para obtener "
        "mediciones precisas. Por ejemplo, si un objeto que sabes que mide 2 metros de ancho aparece como "
        "200 píxeles de ancho en la imagen, la escala es 100."
    ),
    "tutorial_calibrate_perspective_title": "Calibración de Perspectiva",
    "tutorial_calibrate_perspective_message": (
        "Para obtener mediciones precisas del mundo real, debes calibrar la perspectiva. Primero, haz clic en "
        "las cuatro esquinas de un rectángulo conocido en la vista de la cámara (por ejemplo, una hoja de papel). "
        "Luego, introduce su ancho y alto reales en metros en los campos que aparecerán."
    ),
    "tutorial_toggle_view_title": "Alternar Vista",
    "tutorial_toggle_view_message": (
        "Este botón cambia la vista principal entre la transmisión en vivo de la cámara y el último resultado "
        "del análisis (como un mapa de calor de gradiente)."
    ),
    "tutorial_clear_selection_title": "Borrar Selección",
    "tutorial_clear_selection_message": (
        "Este botón elimina cualquier rectángulo de selección del lienzo, permitiéndote dibujar uno nuevo."
    ),
    "tutorial_gradient_title": "Tutorial de Análisis de Gradiente",
    "tutorial_gradient_message": (
        "El Análisis de Gradiente calcula la tasa de cambio de altura en las direcciones X e Y dentro de la "
        "región seleccionada. Esto ayuda a visualizar pendientes e inclinaciones. Se superpondrá un mapa de "
        "calor en tu imagen."
    ),
    "tutorial_volume_title": "Tutorial de Cálculo de Volumen",
    "tutorial_volume_message": (
        "El Cálculo de Volumen estima el volumen bajo la superficie definida por la región seleccionada. "
        "El 'Factor Z' escala los valores de altura, permitiéndote ajustar la profundidad percibida."
    ),
    "tutorial_arc_length_title": "Tutorial de Cálculo de Longitud de Arco",
    "tutorial_arc_length_message": (
        "La Longitud de Arco estima la longitud de una curva. Para el análisis de imágenes, típicamente "
        "calcula la longitud de una sección transversal (por ejemplo, una fila central) dentro de tu región "
        "seleccionada."
    ),
    "tutorial_plot3d_title": "Tutorial de Gráfico de Superficie 3D en Vivo",
    "tutorial_plot3d_message": (
        "El Gráfico de Superficie 3D en Vivo visualiza la región seleccionada como un mapa topográfico 3D "
        "dinámico. Las áreas más brillantes en la imagen original corresponden a elevaciones más altas. "
        "Puedes ajustar el mapa de colores, el sombreado y la resolución usando los controles de la "
        "izquierda. Selecciona una región en la ventana principal para verla en 3D."
    ),
}


# Add all languages to a central dictionary
LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": en,
    "es": es,
}


class Translator(Protocol):
    def __call__(self, key: str, **kwargs: Any) -> str: ...


def get_translator(lang: str) -> Translator:
    """
    Returns a translation function for the given language.
    """
    translations = LANGUAGES.get(lang, LANGUAGES[DEFAULT_LANG])
    default_translations = LANGUAGES[DEFAULT_LANG]

    def translate(key: str, **kwargs: Any) -> str:
        """
        Translates the given key.
        """
        message = translations.get(key, default_translations.get(key, key))
        if kwargs:
            return message.format(**kwargs)
        return message

    return translate
