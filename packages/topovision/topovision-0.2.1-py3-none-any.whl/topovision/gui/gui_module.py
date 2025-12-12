"""
This module defines the main window of the TopoVision application,
which orchestrates the GUI and the core application logic.
"""

import json
import logging
import os
import tkinter as tk
from tkinter import Tk, messagebox, ttk
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

import cv2
import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageTk

from topovision.calculus.calculus_module import AnalysisContext
from topovision.capture.preprocessing import ImagePreprocessor
from topovision.core.interfaces import ICamera
from topovision.core.models import (
    AnalysisResult,
    ArcLengthResult,
    GradientResult,
    RegionOfInterest,
    VolumeResult,
)
from topovision.gui.analysis_panel import AnalysisPanel
from topovision.gui.camera_controller import CameraController
from topovision.gui.canvas_panel import CanvasPanel
from topovision.gui.plot3d_window import Plot3DWindow
from topovision.gui.theme import ThemeManager
from topovision.services.task_queue import TaskQueue
from topovision.utils.perspective import PerspectiveCorrector
from topovision.utils.units import UnitConverter
from topovision.visualization.visualizers import HeatmapVisualizer

from .i18n import get_translator

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
USER_SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "user_settings.json"
)


class MainWindow(Tk):
    """The main window of the TopoVision application."""

    def __init__(
        self,
        camera: ICamera,
        calculus_module: AnalysisContext,
        task_queue: TaskQueue,
        preprocessor: ImagePreprocessor,
        lang: str = "en",
    ) -> None:
        super().__init__()

        self.translator = get_translator(lang)
        self._ = self.translator
        self._lang = lang

        self.title(self._("app_title"))
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.calculus_module = calculus_module
        self.visualizer = HeatmapVisualizer()
        self.task_queue = task_queue
        self.preprocessor = preprocessor
        self.unit_converter = UnitConverter(pixels_per_meter=100.0)
        self.perspective_corrector: Optional[PerspectiveCorrector] = None

        self.camera_controller = CameraController(camera, self._update_canvas_image)
        self.photo: Optional[ImageTk.PhotoImage] = None
        self._analysis_result_photo: Optional[ImageTk.PhotoImage] = None
        self.is_showing_analysis: bool = False
        self.selected_region: Optional[Tuple[int, int, int, int]] = None
        self._last_frame: Optional[NDArray[Any]] = None  # Use NDArray[Any]
        self._canvas_image_id: Optional[int] = None
        self.plot3d_window: Optional[Plot3DWindow] = None

        self.user_settings = self._load_user_settings()

        self._setup_styles()
        self._setup_ui()

        self.protocol("WM_DELETE_WINDOW", self._on_exit)
        self.after(100, self._process_results)
        self.after(15, self._update_frame)
        self.after(500, lambda: self._show_tutorial_if_first_time("app_start"))

    def _load_user_settings(self) -> Dict[str, Any]:
        default_settings: Dict[str, Any] = {
            "tutorial_shown": {
                "app_start": False,
                "analysis_panel": False,
                "z_factor": False,
                "scale": False,
                "calibrate_perspective": False,
                "toggle_view": False,
                "clear_selection": False,
                "gradient": False,
                "volume": False,
                "arc_length": False,
                "plot3d": False,
            }
        }
        try:
            if os.path.exists(USER_SETTINGS_FILE):
                with open(USER_SETTINGS_FILE, "r") as f:
                    settings: Dict[str, Any] = json.load(f)
                for key, value in default_settings["tutorial_shown"].items():
                    if key not in settings.get("tutorial_shown", {}):
                        settings.setdefault("tutorial_shown", {})[key] = value
                return settings
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"Could not load user settings: {e}. Using defaults.")
        return default_settings

    def _save_user_settings(self) -> None:
        try:
            with open(USER_SETTINGS_FILE, "w") as f:
                json.dump(self.user_settings, f, indent=4)
        except IOError as e:
            logging.error(f"Could not save user settings: {e}")

    def _show_tutorial_if_first_time(self, tutorial_key: str) -> None:
        if not self.user_settings["tutorial_shown"].get(tutorial_key, False):
            title = self._(f"tutorial_{tutorial_key}_title")
            message = self._(f"tutorial_{tutorial_key}_message")
            messagebox.showinfo(title, message)
            self.user_settings["tutorial_shown"][tutorial_key] = True
            self._save_user_settings()

    def _setup_styles(self) -> None:
        style = ttk.Style(self)
        theme_manager = ThemeManager(style)
        theme_manager.apply("dark")

    def _setup_ui(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        self.canvas = CanvasPanel(
            cast(tk.Widget, self), bg="#0E0F11", highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.canvas.on_selection_made = self._handle_selection
        self.canvas.on_calibration_point_added = self._handle_calibration_point

        available_units = ["meters", "feet", "centimeters", "kilometers", "miles"]
        self.analysis_panel = AnalysisPanel(
            cast(tk.Widget, self),
            self._trigger_analysis,
            self.translator,
            available_units,
            self._update_scale,
            self._start_calibration,
            self._apply_calibration,
            self._show_tutorial_if_first_time,
        )
        self.analysis_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.analysis_panel.toggle_btn.config(command=self.toggle_view)
        self.analysis_panel.clear_btn.config(command=self.clear_selection)

        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_toggle_camera = ttk.Button(
            buttons_frame, text=self._("open_camera_button"), command=self.toggle_camera
        )
        self.btn_toggle_camera.grid(row=0, column=0, sticky="e", padx=10)

        self.btn_open_3d_plot = ttk.Button(
            buttons_frame,
            text=self._("open_3d_plot_button"),
            command=self._open_3d_plot_window,
        )
        self.btn_open_3d_plot.grid(row=0, column=1, sticky="w", padx=10)

        self.btn_exit = ttk.Button(
            buttons_frame, text=self._("exit_button"), command=self._on_exit
        )
        self.btn_exit.grid(row=0, column=2, sticky="e", padx=20)

        self._update_initial_canvas_message()

    def _start_calibration(self) -> None:
        self.canvas.start_calibration()
        self.set_status(self._("calibration_start_prompt"))

    def _handle_calibration_point(self, points: List[Tuple[int, int]]) -> None:
        count = len(points)
        if count < 4:
            self.set_status(self._("calibration_point_added", count=count))
        else:
            self.set_status(self._("calibration_complete_prompt"))
            self.analysis_panel.show_calibration_inputs()

    def _apply_calibration(self, real_width: float, real_height: float) -> None:
        if len(self.canvas.calibration_points) != 4:
            self.set_status(self._("calibration_error"), is_error=True)
            return
        try:
            self.perspective_corrector = PerspectiveCorrector(
                self.canvas.calibration_points, real_width, real_height
            )
            self.unit_converter.update_scale(
                self.perspective_corrector.pixels_per_meter
            )
            self.analysis_panel.scale_entry.delete(0, tk.END)
            self.analysis_panel.scale_entry.insert(
                0, f"{self.perspective_corrector.pixels_per_meter:.2f}"
            )
            self.set_status(self._("calibration_applied"))
        except (ValueError, np.linalg.LinAlgError) as e:
            self.set_status(self._("calibration_error", error=e), is_error=True)
        finally:
            self.canvas.stop_calibration()
            self.analysis_panel.hide_calibration_inputs()

    def _update_scale(self, new_scale: float) -> None:
        try:
            self.unit_converter.update_scale(new_scale)
            self.set_status(f"Scale updated to {new_scale} px/m.")
            if self.selected_region:
                self._handle_selection(self.selected_region, "selection_made")
        except ValueError as e:
            self.set_status(str(e), is_error=True)

    def _open_3d_plot_window(self) -> None:
        if self.plot3d_window is None or not self.plot3d_window.winfo_exists():
            self.plot3d_window = Plot3DWindow(self, lang=self._lang)
            self.plot3d_window.start_live_update()
            self._show_tutorial_if_first_time("plot3d")
        self.plot3d_window.lift()
        self.set_status(self._("3d_plot_window_opened"))

    def set_status(self, message: str, is_error: bool = False) -> None:
        self.analysis_panel.set_status(message, is_error)
        if is_error:
            logging.error(message)
            messagebox.showerror(self._("app_title"), message)

    def _handle_selection(
        self,
        region: Optional[Tuple[int, int, int, int]],
        message_key: str,
        **kwargs: Any,
    ) -> None:
        self.selected_region = region
        if not region:
            self.analysis_panel.set_status(self._(message_key, **kwargs), is_error=True)
            return

        x1, y1, x2, y2 = region
        width_px, height_px = x2 - x1, y2 - y1
        unit = self.analysis_panel.get_selected_unit()

        if self.perspective_corrector:
            tl = self.perspective_corrector.transform_point((x1, y1))
            tr = self.perspective_corrector.transform_point((x2, y1))
            bl = self.perspective_corrector.transform_point((x1, y2))
            br = self.perspective_corrector.transform_point((x2, y2))
            width_corr = (
                np.linalg.norm(np.array(tr) - np.array(tl))
                + np.linalg.norm(np.array(br) - np.array(bl))
            ) / 2
            height_corr = (
                np.linalg.norm(np.array(bl) - np.array(tl))
                + np.linalg.norm(np.array(br) - np.array(tr))
            ) / 2
            width_unit = self.unit_converter.convert_distance(
                cast(float, width_corr), "pixels", unit  # Cast to float
            )
            height_unit = self.unit_converter.convert_distance(
                cast(float, height_corr), "pixels", unit  # Cast to float
            )
        else:
            width_unit = self.unit_converter.convert_distance(width_px, "pixels", unit)
            height_unit = self.unit_converter.convert_distance(
                height_px, "pixels", unit
            )

        self.analysis_panel.set_status(
            self._(
                message_key,
                width_px=width_px,
                height_px=height_px,
                width_unit=width_unit,
                height_unit=height_unit,
                unit=unit,
                **kwargs,
            )
        )

    def _trigger_analysis(self, method: str, unit: str) -> None:
        if not self.selected_region:
            self.set_status(self._("region_error"), is_error=True)
            return
        if self._last_frame is None:
            self.set_status(self._("no_frame_to_analyze"), is_error=True)
            return
        self._show_tutorial_if_first_time(method)
        try:
            z_factor = self.analysis_panel.get_z_factor()
            scale = self.analysis_panel.get_scale()
            self.set_status(self._("calculating", method=method))
            self.task_queue.submit_task(
                self._perform_calculation, method, z_factor, unit, scale
            )
        except ValueError as e:
            self.set_status(str(e), is_error=True)

    def _perform_calculation(
        self, method: str, z_factor: float, unit: str, scale: float
    ) -> Dict[str, Any]:
        if self.selected_region is None or self._last_frame is None:
            raise RuntimeError("Missing data for calculation.")

        x1, y1, x2, y2 = self.selected_region
        h, w, _ = self._last_frame.shape
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()

        rx1, ry1 = int(x1 * w / canvas_w), int(y1 * h / canvas_h)
        rx2, ry2 = int(x2 * w / canvas_w), int(y2 * h / canvas_h)

        calc_result_data: Dict[str, Any] = {}
        data_for_analysis_image: NDArray[Any]  # Use NDArray[Any]

        # Initialize these variables to None
        inverse_local_matrix: Optional[NDArray[np.float32]] = None
        src_quad: Optional[NDArray[np.float32]] = None

        if self.perspective_corrector:
            src_quad = np.array(
                [[rx1, ry1], [rx2, ry1], [rx2, ry2], [rx1, ry2]], dtype=np.float32
            )

            transformed_corners: NDArray[np.float32] = cast(
                NDArray[np.float32],
                cv2.perspectiveTransform(
                    np.array([src_quad]), self.perspective_corrector.matrix
                )[0],
            )

            rect = cv2.boundingRect(transformed_corners)
            dst_w, dst_h = rect[2], rect[3]

            if dst_w < 1 or dst_h < 1:
                raise RuntimeError("Region too small after perspective correction.")

            dst_rect: NDArray[np.float32] = np.array(
                [[0, 0], [dst_w - 1, 0], [dst_w - 1, dst_h - 1], [0, dst_h - 1]],
                dtype=np.float32,
            )

            local_matrix: NDArray[np.float32] = cast(
                NDArray[np.float32], cv2.getPerspectiveTransform(src_quad, dst_rect)
            )
            inverse_local_matrix = cast(
                NDArray[np.float32], cv2.getPerspectiveTransform(dst_rect, src_quad)
            )  # This is where it's defined

            warped_roi: NDArray[Any] = cv2.warpPerspective(
                self._last_frame, local_matrix, (dst_w, dst_h)
            )
            data_for_analysis_image = warped_roi

        else:
            data_for_analysis_image = self._last_frame[ry1:ry2, rx1:rx2]

        # Assign these outside the if block
        calc_result_data["inverse_matrix"] = inverse_local_matrix
        calc_result_data["src_quad"] = src_quad

        data_for_analysis: NDArray[Any]  # Use NDArray[Any]
        if method in ["gradient", "volume"]:
            data_for_analysis = cv2.cvtColor(
                data_for_analysis_image, cv2.COLOR_RGB2GRAY
            )
        elif method == "arc_length":
            gray_region: NDArray[Any] = cv2.cvtColor(
                data_for_analysis_image, cv2.COLOR_RGB2GRAY
            )  # Use NDArray[Any]
            middle_row_idx = gray_region.shape[0] // 2
            points = [
                (i, gray_region[middle_row_idx, i]) for i in range(gray_region.shape[1])
            ]
            data_for_analysis = np.array(points)
        else:
            raise ValueError(f"Unknown analysis method: {method}")

        self.calculus_module.set_strategy(method)
        calc_kwargs: Dict[str, Any] = {"pixels_per_meter": scale, "z_factor": z_factor}
        if method == "volume":
            calc_kwargs["unit"] = f"cubic_{unit}"
        elif method == "arc_length":
            calc_kwargs["unit"] = unit

        result_obj = self.calculus_module.calculate(data_for_analysis, **calc_kwargs)

        calc_result_data.update(
            {"method": method, "result": result_obj, "region": self.selected_region}
        )
        return calc_result_data

    def _process_results(self) -> None:
        result = self.task_queue.get_result()
        if result:
            if isinstance(result, Exception):
                self.set_status(
                    self._("calculation_error", error=result), is_error=True
                )
            else:
                self._handle_calculation_result(result)
        self.after(100, self._process_results)

    def _handle_calculation_result(self, result: Dict[str, Any]) -> None:
        method: str = result["method"]
        calc_result = result["result"]
        region_coords: Optional[Tuple[int, int, int, int]] = result.get("region")
        if not region_coords:
            self.set_status(
                self._("calculation_error", error="Missing region"), is_error=True
            )
            return
        region = RegionOfInterest(*region_coords)

        if method == "gradient" and isinstance(calc_result, GradientResult):
            self.set_status(
                self._(
                    "calculating_gradient",
                    dx=np.mean(calc_result.dz_dx),
                    dy=np.mean(calc_result.dz_dy),
                )
            )
            if self._last_frame is not None:
                original_image_pil = cast(
                    Image.Image, Image.fromarray(self._last_frame)
                )
                analysis_result = AnalysisResult(method, calc_result, region)
                heatmap = self.visualizer.visualize(
                    analysis_result,
                    original_image_pil,
                    inverse_matrix=result.get("inverse_matrix"),
                    src_quad=result.get("src_quad"),
                )
                self.display_result_image(heatmap)
        elif method == "volume" and isinstance(calc_result, VolumeResult):
            self.set_status(
                self._(
                    "calculating_volume",
                    volume=calc_result.volume,
                    units=calc_result.units,
                )
            )
        elif method == "arc_length" and isinstance(calc_result, ArcLengthResult):
            self.set_status(
                self._(
                    "calculating_arc_length",
                    length=calc_result.length,
                    units=calc_result.units,
                )
            )
        else:
            self.set_status(
                self._("calculation_error", error=f"Unknown result type for {method}"),
                is_error=True,
            )

    def clear_selection(self) -> None:
        self._show_tutorial_if_first_time("clear_selection")
        self.canvas.clear_selection()
        self.selected_region = None
        self.set_status(self._("selection_cleared"))
        if self.plot3d_window and self.plot3d_window.winfo_exists():
            self.plot3d_window.clear_plot_data()

    def toggle_view(self) -> None:
        self._show_tutorial_if_first_time("toggle_view")
        if self._analysis_result_photo is None:
            self.set_status(self._("no_analysis_to_show"), is_error=True)
            return
        self.is_showing_analysis = not self.is_showing_analysis
        self.set_status(
            self._(
                f"view_changed_to_{'analysis' if self.is_showing_analysis else 'camera'}"
            )
        )
        self._refresh_gui_display()

    def display_result_image(self, pil_image: Image.Image) -> None:
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1 and h > 1:
            resized_img = pil_image.resize((w, h), Image.Resampling.LANCZOS)
            self._analysis_result_photo = ImageTk.PhotoImage(
                image=resized_img
            )  # Removed redundant cast
            self.is_showing_analysis = True
            self.set_status(self._("analysis_completed"))
            self._refresh_gui_display()

    def toggle_camera(self) -> None:
        try:
            self.camera_controller.toggle()
            self.btn_toggle_camera.config(
                text=self._(
                    f"{'pause' if self.camera_controller.is_running else 'resume'}_camera_button"
                )
            )
            self.set_status(
                self._(
                    f"camera_{'started' if self.camera_controller.is_running else 'paused'}"
                )
            )
            self.is_showing_analysis = False
        except Exception as e:
            self.set_status(self._("camera_error", error=e), is_error=True)

    def _update_frame(self) -> None:
        if self.camera_controller.is_running:
            frame = self.camera_controller.get_frame()
            if frame is not None:
                denoised_frame = self.preprocessor.process(frame)
                self._last_frame = denoised_frame
                self._update_canvas_image(denoised_frame)
                if (
                    self.plot3d_window
                    and self.plot3d_window.winfo_exists()
                    and self.selected_region
                ):
                    self.plot3d_window.set_latest_data(*self._prepare_3d_plot_data())
        self.after(15, self._update_frame)

    def _prepare_3d_plot_data(
        self,
    ) -> Tuple[NDArray[Any], NDArray[Any], NDArray[Any]]:  # Use NDArray[Any]
        if not self.selected_region or self._last_frame is None:
            return np.array([]), np.array([]), np.array([])

        x1, y1, x2, y2 = self.selected_region
        h, w, _ = self._last_frame.shape
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        rx1, ry1 = int(x1 * w / canvas_w), int(y1 * h / canvas_h)
        rx2, ry2 = int(x2 * w / canvas_w), int(y2 * h / canvas_h)

        try:
            z_factor = self.analysis_panel.get_z_factor()
            scale = self.analysis_panel.get_scale()
        except ValueError:
            z_factor = 1.0
            scale = 100.0

        meters_per_pixel = 1.0 / scale

        # Initialize variables before conditional blocks
        real_width: float = 0.0
        real_height: float = 0.0
        gray_region: NDArray[Any] = np.array([])
        x_coords: NDArray[np.float64] = np.array([])
        y_coords: NDArray[np.float64] = np.array([])
        Z: NDArray[np.float64] = np.array([])

        if self.perspective_corrector:
            src_quad: NDArray[np.float32] = np.array(
                [[rx1, ry1], [rx2, ry1], [rx2, ry2], [rx1, ry2]], dtype=np.float32
            )

            transformed_corners: NDArray[np.float32] = cast(
                NDArray[np.float32],
                cv2.perspectiveTransform(
                    np.array([src_quad]), self.perspective_corrector.matrix
                )[0],
            )

            rect = cv2.boundingRect(transformed_corners)
            dst_w, dst_h = rect[2], rect[3]

            if dst_w < 1 or dst_h < 1:
                return np.array([]), np.array([]), np.array([])

            dst_rect: NDArray[np.float32] = np.array(
                [[0, 0], [dst_w - 1, 0], [dst_w - 1, dst_h - 1], [0, dst_h - 1]],
                dtype=np.float32,
            )

            local_matrix: NDArray[np.float32] = cast(
                NDArray[np.float32], cv2.getPerspectiveTransform(src_quad, dst_rect)
            )
            warped_roi: NDArray[Any] = cv2.warpPerspective(
                self._last_frame, local_matrix, (dst_w, dst_h)
            )

            gray_region = cv2.cvtColor(warped_roi, cv2.COLOR_RGB2GRAY)

            real_width = cast(
                float,
                (
                    (
                        np.linalg.norm(transformed_corners[1] - transformed_corners[0])
                        + np.linalg.norm(
                            transformed_corners[2] - transformed_corners[3]
                        )
                    )
                    / 2
                    * meters_per_pixel
                ),
            )
            real_height = cast(
                float,
                (
                    (
                        np.linalg.norm(transformed_corners[3] - transformed_corners[0])
                        + np.linalg.norm(
                            transformed_corners[2] - transformed_corners[1]
                        )
                    )
                    / 2
                    * meters_per_pixel
                ),
            )

            x_coords = np.linspace(0, real_width, dst_w)
            y_coords = np.linspace(0, real_height, dst_h)
            X, Y = np.meshgrid(x_coords, y_coords)
            Z = gray_region * z_factor * meters_per_pixel

        else:
            region_data: NDArray[Any] = self._last_frame[ry1:ry2, rx1:rx2]
            if region_data.size == 0:
                return np.array([]), np.array([]), np.array([])

            gray_region = cv2.cvtColor(region_data, cv2.COLOR_RGB2GRAY)
            rows, cols = gray_region.shape

            real_width = cast(float, cols * meters_per_pixel)
            real_height = cast(float, rows * meters_per_pixel)

            x_coords = np.linspace(0, real_width, cols)
            y_coords = np.linspace(0, real_height, rows)
            X, Y = np.meshgrid(x_coords, y_coords)
            Z = gray_region * z_factor * meters_per_pixel

        return X, Y, Z

    def _update_canvas_image(self, frame: NDArray[Any]) -> None:  # Use NDArray[Any]
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 1 and h > 1:
            resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
            img = cast(
                Image.Image, Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
            )
            self.photo = cast(
                ImageTk.PhotoImage, ImageTk.PhotoImage(image=img)
            )  # Added cast
            self._refresh_gui_display()

    def _refresh_gui_display(self) -> None:
        photo = self._analysis_result_photo if self.is_showing_analysis else self.photo
        if not photo:
            self._update_initial_canvas_message()
            return
        if self._canvas_image_id:
            self.canvas.itemconfig(self._canvas_image_id, image=photo)
        else:
            self._canvas_image_id = self.canvas.create_image(
                0, 0, image=photo, anchor=tk.NW
            )

    def _update_initial_canvas_message(self) -> None:
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 100 and h > 100:
            self.canvas.create_text(
                w / 2,
                h / 2,
                text=self._("click_to_start"),
                fill="#E6E6E6",
                font=("Arial", 16),
                justify="center",
                width=w - 40,
            )

    def _on_exit(self) -> None:
        self.set_status(self._("closing_app"))
        self.camera_controller.stop()
        self.task_queue.stop()
        if self.plot3d_window and self.plot3d_window.winfo_exists():
            self.plot3d_window.stop_live_update()
            self.plot3d_window.destroy()
        self.destroy()

    def run(self) -> None:
        self.mainloop()
