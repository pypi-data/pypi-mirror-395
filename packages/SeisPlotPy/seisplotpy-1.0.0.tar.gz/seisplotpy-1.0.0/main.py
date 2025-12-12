import sys
import os
import traceback
from PyQt6.QtWidgets import (QApplication, QFileDialog, QMessageBox, QInputDialog,
                             QMenuBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QDoubleSpinBox, QDialog, QDialogButtonBox,
                             QComboBox, QRadioButton, QButtonGroup)
from PyQt6.QtGui import QAction, QCursor, QIcon
from PyQt6.QtCore import Qt
import pyqtgraph as pg

# Local Imports
from ui.seismic_view import SeismicView
from ui.header_tools import TextHeaderDialog, HeaderQCPlot, SpectrumPlot, HeaderExportDialog
from ui.horizon_manager import HorizonManager
from ui.dialogs import GeometryDialog, BandpassDialog
from core.data_handler import SeismicDataManager
from core.processing import SeismicProcessing

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def apply_light_style(app: QApplication):
    """
    Use Qt's Fusion style and a simple light stylesheet so the UI
    stays readable even when the OS is in dark mode.
    """
    # Use a platform-independent style
    app.setStyle("Fusion")

    # Apply a basic light stylesheet
    app.setStyleSheet("""
        QWidget {
            color: #000000;
            background-color: #f0f0f0;
        }

        QMenuBar, QMenu {
            background-color: #f0f0f0;
            color: #000000;
        }

        QToolTip {
            color: #000000;
            background-color: #ffffff;
            border: 1px solid #aaaaaa;
        }

        QPushButton {
            background-color: #e0e0e0;
            border: 1px solid #888888;
            padding: 4px;
        }

        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
            background-color: #ffffff;
            color: #000000;
        }

        QStatusBar {
            background-color: #e0e0e0;
        }
    """)

def resource_path(relative_path):
    try: 
        base_path = sys._MEIPASS
    except Exception: 
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainController:
    def __init__(self):
        self.view = SeismicView()
        self.data_manager = None
        self.current_data = None
        self.active_header_map = None
        self.full_cum_dist = None
        self.dist_unit = "m"

        self.is_programmatic_update = False
        self.is_picking_mode = False

        self.horizon_manager = HorizonManager(None)
        self.horizon_items = []

        self.setup_menu()

        # Connections
        self.view.btn_load.clicked.connect(self.load_file)
        self.view.btn_apply.clicked.connect(self.apply_changes)
        self.view.btn_reset.clicked.connect(self.reset_view)

        self.view.chk_manual_step.stateChanged.connect(self.toggle_manual_step)
        self.view.combo_cmap.currentTextChanged.connect(self.change_colormap)
        self.view.spin_contrast.valueChanged.connect(self.update_contrast)
        self.view.combo_domain.currentTextChanged.connect(self.update_labels)
        self.view.btn_export.clicked.connect(self.export_figure)
        self.view.chk_flip_x.stateChanged.connect(self.toggle_flip_x)
        self.view.chk_grid.stateChanged.connect(self.toggle_grid)
        self.view.btn_preview_ratio.clicked.connect(self.match_aspect_ratio)
        self.view.plot_widget.sigRangeChanged.connect(self.sync_view_to_controls)
        self.view.combo_header.activated.connect(self.on_header_changed)

        self.horizon_manager.picking_toggled.connect(self.set_picking_mode)
        self.horizon_manager.horizon_visibility_changed.connect(self.draw_horizons)
        self.horizon_manager.horizon_color_changed.connect(self.draw_horizons)
        self.horizon_manager.horizon_removed.connect(self.draw_horizons)
        self.horizon_manager.export_requested.connect(self.handle_horizon_export)
        self.view.plot_widget.scene().sigMouseClicked.connect(self.on_plot_clicked)

        self.view.show()

    # --- Loading Logic ---
    def load_file(self):
        # If something is already loaded, ask whether to clear & reload
        if self.data_manager is not None:
            reply = QMessageBox.question(
                self.view,
                "Load New SEG-Y?",
                (
                    "A SEG-Y line is already loaded in this window.\n\n"
                    "Do you want to load a NEW file?\n"
                    "This will clear the current view and any interpreted horizons."
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

            # Clear existing state so we can load a fresh line
            self.reset_for_new_file()

        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Open SEG-Y File",
            "",
            "SEG-Y Files (*.sgy *.segy)"
        )
        if not file_path:
            return
        
        self.view.update_status("Loading. Please wait")
        QApplication.processEvents()
        try:
            self.data_manager = SeismicDataManager(file_path)
            self.full_cum_dist = None
            self.dist_unit = "m"
            
            # Enable Controls
            self.action_text_header.setEnabled(True)
            self.action_header_qc.setEnabled(True)
            self.action_agc.setEnabled(True)
            self.action_filter.setEnabled(True)
            self.action_reset.setEnabled(True)
            self.action_spectrum.setEnabled(True)
            self.action_dist.setEnabled(True)
            self.act_env.setEnabled(True)
            self.act_phase.setEnabled(True)
            self.act_cos.setEnabled(True)
            self.act_freq.setEnabled(True)
            self.act_rms.setEnabled(True)
            self.action_histogram.setEnabled(True)
            
            # Header combo
            self.view.chk_manual_step.setChecked(False)
            self.view.spin_step.setEnabled(False)
            self.view.combo_header.clear()
            self.view.combo_header.addItem("Trace Index")
            self.view.combo_header.addItems(self.data_manager.available_headers)
            
            if "CDP" in self.data_manager.available_headers:
                self.view.combo_header.setCurrentText("CDP")
                self.active_header_map = self.data_manager.get_header_slice(
                    "CDP", 0, self.data_manager.n_traces, 1
                )
            else:
                self.view.combo_header.setCurrentText("Trace Index")
                self.active_header_map = None
            
            total_traces = self.data_manager.n_traces
            smart_step = max(1, int(total_traces / 2000))
            self.load_data_internal(0, total_traces, smart_step, auto_fit=True)

            # Status text only (no lock)
            self.view.update_status(
                f"Loaded: {os.path.basename(file_path)}\nTraces: {total_traces}"
            )

        except Exception as e:
            traceback.print_exc()
            self.view.update_status("Load failed.")
            QMessageBox.critical(self.view, "Error", f"Failed to load file:\n{str(e)}")


    def load_data_internal(self, start, end, step, auto_fit=False):
        try:
            self.loaded_start_trace = max(0, start)
            self.loaded_end_trace = min(self.data_manager.n_traces, end)
            
            if self.loaded_start_trace >= self.loaded_end_trace:
                return
            
            self.view.update_status("Reading Data...")
            QApplication.processEvents()
            
            self.current_data = self.data_manager.get_data_slice(self.loaded_start_trace, self.loaded_end_trace, step)
            
            header = self.view.combo_header.currentText()
            if header == "Trace Index": 
                self.x_vals = np.arange(self.loaded_start_trace, self.loaded_end_trace, step)
            else: 
                self.x_vals = self.get_scaled_header(header, self.loaded_start_trace, self.loaded_end_trace, step)
            
            self.t_vals = self.data_manager.time_axis
            x_min = self.x_vals[0] if self.x_vals.size > 0 else 0
            x_max = self.x_vals[-1] if self.x_vals.size > 0 else 1
            t_min = self.t_vals[0]
            t_max = self.t_vals[-1]
            
            self.is_programmatic_update = True
            self.view.display_seismic(self.current_data.T, x_range=(x_min, x_max), y_range=(t_min, t_max))
            
            if not self.view.chk_manual_step.isChecked(): 
                self.view.spin_step.setValue(step)
            
            if auto_fit:
                self.view.plot_widget.autoRange()
                self.view.spin_x_min.setValue(x_min)
                self.view.spin_x_max.setValue(x_max)
                self.view.spin_y_min.setValue(t_min)
                self.view.spin_y_max.setValue(t_max)
            
            self.update_contrast()
            self.update_labels()
            self.draw_horizons()
            
            self.is_programmatic_update = False
            self.view.update_status("Ready")
            
        except Exception as e: 
            traceback.print_exc()
            print(f"Load error: {e}")
            self.is_programmatic_update = False

    # --- Attributes Logic (With Auto-Reload) ---
    def run_attribute(self, attr_type):
        if self.data_manager is None: 
            return
        
        # 1. Get current view range
        view_range = self.view.plot_widget.viewRange()
        x_min, x_max = view_range[0]
        
        # 2. Convert coordinates back to trace indices
        start_trace, end_trace = 0, 0
        header = self.view.combo_header.currentText()
        
        if header == "Trace Index":
            start_trace = int(x_min)
            end_trace = int(x_max)
        elif self.active_header_map is not None:
            try:
                if self.active_header_map[0] < self.active_header_map[-1]:
                    start_trace = np.searchsorted(self.active_header_map, x_min)
                    end_trace = np.searchsorted(self.active_header_map, x_max)
                else:
                    start_trace = np.searchsorted(self.active_header_map[::-1], x_min)
                    end_trace = np.searchsorted(self.active_header_map[::-1], x_max)
                    n = len(self.active_header_map)
                    start_trace, end_trace = n - end_trace, n - start_trace
            except:
                start_trace = max(0, int(x_min))
                end_trace = min(self.data_manager.n_traces, int(x_max))

        start_trace = max(0, start_trace)
        end_trace = min(self.data_manager.n_traces, end_trace)
        
        # 3. Reload High Res
        self.view.update_status(f"Fetching high-res data for {attr_type}...")
        QApplication.processEvents()
        
        self.view.spin_x_min.setValue(x_min)
        self.view.spin_x_max.setValue(x_max)
        self.view.chk_manual_step.setChecked(True)
        self.view.spin_step.setValue(1)
        self.load_data_internal(start_trace, end_trace, step=1, auto_fit=False)

        # 4. Calculate
        if self.current_data is None: 
            return
        
        self.view.update_status(f"Calculating {attr_type}...")
        QApplication.processEvents()
        
        try:
            sr = self.data_manager.sample_rate
            if attr_type == "Envelope":
                self.current_data = SeismicProcessing.attribute_envelope(self.current_data)
            elif attr_type == "Phase":
                self.current_data = SeismicProcessing.attribute_phase(self.current_data)
                self.view.combo_cmap.setCurrentText("seismic")
            elif attr_type == "Frequency":
                self.current_data = SeismicProcessing.attribute_frequency(self.current_data, sr)
            elif attr_type == "Cosine Phase":
                self.current_data = SeismicProcessing.attribute_cosine_phase(self.current_data)
            elif attr_type == "RMS":
                window, ok = QInputDialog.getInt(self.view, "RMS Settings", "Window (ms):", 100, 10, 1000)
                if not ok: 
                    return
                self.current_data = SeismicProcessing.attribute_rms(self.current_data, sr, window)
            
            self.update_display_only()
            self.view.update_status(f"Displayed: {attr_type} (High Res)")
        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self.view, "Attribute Error", str(e))
            self.view.update_status("Error calculating attribute")

    # --- Updated Display Only (Fixes Squeezed View) ---
    def update_display_only(self):
        if self.current_data is None: 
            return
        
        # Use actual data bounds
        if hasattr(self, 'x_vals') and self.x_vals is not None and self.x_vals.size > 0:
            x_min = self.x_vals[0]
            x_max = self.x_vals[-1]
        else:
            x_min = self.view.spin_x_min.value()
            x_max = self.view.spin_x_max.value()
            
        if hasattr(self, 't_vals') and self.t_vals is not None:
            y_min = self.t_vals[0]
            y_max = self.t_vals[-1]
        else:
            y_min = self.view.spin_y_min.value()
            y_max = self.view.spin_y_max.value()
        
        self.view.display_seismic(self.current_data.T, x_range=(x_min, x_max), y_range=(y_min, y_max))
        self.update_contrast()
        self.draw_horizons()

    # --- Histogram Feature ---
    def show_amplitude_histogram(self):
        if self.current_data is None: 
            return
        try:
            # Use matplotlib locally to avoid overhead if unused
            import matplotlib.pyplot as plt
            
            percentile = self.view.spin_contrast.value()
            amps = self.current_data.flatten()
            amps = amps[np.isfinite(amps)]
            clip_val = np.percentile(np.abs(amps), percentile)
            
            # below_clip = np.sum(amps < -clip_val) # Unused
            within_clip = np.sum((amps >= -clip_val) & (amps <= clip_val))
            # above_clip = np.sum(amps > clip_val) # Unused
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            n_bins_full = min(100, int(np.sqrt(len(amps))))
            n_bins_zoom = min(80, int(np.sqrt(within_clip))) 
            
            ax1.hist(amps, bins=n_bins_full, color='steelblue', alpha=0.7, edgecolor='black', log=True)
            ax1.axvline(-clip_val, color='red', ls='--', lw=2)
            ax1.axvline(clip_val, color='red', ls='--', lw=2)
            ax1.axvspan(amps.min(), -clip_val, alpha=0.15, color='blue', label='Saturated Low')
            ax1.axvspan(clip_val, amps.max(), alpha=0.15, color='red', label='Saturated High')
            ax1.set_title(f'Amplitude Distribution - All {len(amps):,} samples')
            ax1.legend()

            clipped_amps = amps[(amps >= -clip_val) & (amps <= clip_val)]
            ax2.hist(clipped_amps, bins=n_bins_zoom, color='green', alpha=0.7, edgecolor='black')
            ax2.axvline(-clip_val, color='red', ls='--', lw=2)
            ax2.axvline(clip_val, color='red', ls='--', lw=2)
            ax2.set_title(f'Dynamic Range ({within_clip/len(amps)*100:.2f}% mapped)')
            
            plt.tight_layout()
            plt.show()
        except Exception as e: 
            traceback.print_exc()
            QMessageBox.critical(self.view, "Histogram Error", str(e))

    def get_x_label(self):
        """
        Return a descriptive X-axis label based on the current header selection
        and distance unit (if using cumulative distance).
        """
        header = self.view.combo_header.currentText()

        if header == "Trace Index":
            return "Trace Index"

        if header == "Cumulative Distance":
            # Use stored distance unit if available (defaults to 'm')
            unit = getattr(self, "dist_unit", None) or "m"
            return f"Cumulative Distance ({unit})"

        # Fallback: just show the header name
        return str(header)

    def update_labels(self):
        """
        Update the labels on the seismic view based on:
        - current X header selection
        - current domain selection (Time / Depth)
        """
        x_label = self.get_x_label()
        y_domain = self.view.combo_domain.currentText()  # e.g. "Time" or "Depth"
        # SeismicView has update_labels(x_label, y_domain)
        self.view.update_labels(x_label, y_domain)

    
    def export_figure(self):
        if self.current_data is None:
            QMessageBox.warning(self.view, "Warning", "No data to export.")
            return
        
        dpi, ok = QInputDialog.getInt(self.view, "Export Settings", "DPI (Resolution):", 300, 72, 1200)
        if not ok: 
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Save Figure", "seismic_plot.pdf", "PDF Documents (*.pdf);;PNG Images (*.png)")
        if not file_path: 
            return
        
        try:
            w = self.view.spin_fig_width.value()
            h = self.view.spin_fig_height.value()
            fig, ax = plt.subplots(figsize=(w, h))
            
            p = self.view.spin_contrast.value()
            clip_val = np.percentile(np.abs(self.current_data), p) if self.current_data.size > 0 else 1.0
            
            extent = [self.x_vals[0], self.x_vals[-1], self.t_vals[-1], self.t_vals[0]]
            
            im = ax.imshow(self.current_data, cmap=self.view.combo_cmap.currentText(), 
                          aspect='auto', extent=extent, vmin=-clip_val, vmax=clip_val, interpolation='bilinear')
            
            if self.view.chk_grid.isChecked():
                ax.grid(True, alpha=0.3, linestyle='--')
            else:
                ax.grid(False)
            
            ax.set_xlabel(self.get_x_label()) 
            
            ylabel = "TWT (ms)" if self.view.combo_domain.currentText() == "Time" else "Depth (m)"
            ax.set_ylabel(ylabel)
            
            ax.set_xlim(self.view.spin_x_min.value(), self.view.spin_x_max.value())
            ax.set_ylim(self.view.spin_y_max.value(), self.view.spin_y_min.value())
            
            if self.view.chk_flip_x.isChecked(): 
                ax.invert_xaxis()
            
            # Draw Horizons
            for h in self.horizon_manager.horizons:
                if h['visible'] and h['points']:
                    idx_data, y_data = zip(*h['points'])
                    idx_arr = np.array(idx_data, dtype=int)
                    
                    # Map Indices -> X Values
                    header = self.view.combo_header.currentText()
                    if header == "Trace Index": 
                        map_array = None
                    elif header == "Cumulative Distance": 
                        map_array = self.full_cum_dist
                    elif self.active_header_map is not None: 
                        map_array = self.active_header_map
                    else: 
                        map_array = None
                        
                    if map_array is not None:
                        idx_arr = np.clip(idx_arr, 0, len(map_array)-1)
                        x_d = map_array[idx_arr]
                    else: 
                        x_d = idx_arr
                        
                    ax.plot(x_d, y_data, color=h['color'], linewidth=1.0)
                    
            fig.savefig(file_path, dpi=dpi, bbox_inches='tight', metadata={'Creator': 'SeisPlotPy'})
            plt.close(fig)
            QMessageBox.information(self.view, "Success", f"Exported to:\n{file_path}")
            
        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self.view, "Export Failed", str(e))

    # --- Rest of Standard Logic ---
    def reset_view(self):
        if not self.data_manager: 
            return
        
        header = self.view.combo_header.currentText()
        x_min, x_max = 0, 0
        if header == "Trace Index": 
            x_min, x_max = 0, self.data_manager.n_traces
        elif header == "Cumulative Distance" and self.full_cum_dist is not None: 
            x_min, x_max = self.full_cum_dist[0], self.full_cum_dist[-1]
        elif self.active_header_map is not None: 
            x_min, x_max = np.min(self.active_header_map), np.max(self.active_header_map)
        
        t_min, t_max = self.data_manager.time_axis[0], self.data_manager.time_axis[-1]
        self.view.spin_x_min.setValue(x_min)
        self.view.spin_x_max.setValue(x_max)
        self.view.spin_y_min.setValue(t_min)
        self.view.spin_y_max.setValue(t_max)
        
        self.view.chk_manual_step.setChecked(False)
        self.apply_changes()

    def calculate_distance(self, settings):
        self.view.update_status("Calculating Distance...")
        QApplication.processEvents()
        
        try:
            raw_x = self.data_manager.get_header_slice(settings['x_key'], 0, self.data_manager.n_traces, 1)
            raw_y = self.data_manager.get_header_slice(settings['y_key'], 0, self.data_manager.n_traces, 1)
            
            if settings['use_header']:
                scalars = self.data_manager.get_header_slice(settings['scalar_key'], 0, self.data_manager.n_traces, 1)
                scaled_x = SeismicProcessing.apply_scalar(raw_x, scalars)
                scaled_y = SeismicProcessing.apply_scalar(raw_y, scalars)
            else: 
                s = settings['manual_val']
                scaled_x = raw_x * s
                scaled_y = raw_y * s
            
            dist = SeismicProcessing.calculate_cumulative_distance(scaled_x, scaled_y)
            max_dist = dist[-1]
            if max_dist > 10000: 
                dist = dist / 1000.0
                self.dist_unit = "km"
            else: 
                self.dist_unit = "m"
            
            self.full_cum_dist = dist
            if self.view.combo_header.findText("Cumulative Distance") == -1: 
                self.view.combo_header.insertItem(1, "Cumulative Distance")
            
            self.view.combo_header.setCurrentText("Cumulative Distance")
            self.on_header_changed()
            QMessageBox.information(self.view, "Success", f"Calculated distance. Length: {self.full_cum_dist[-1]:.2f} {self.dist_unit}")
        except Exception as e: 
            traceback.print_exc()
            QMessageBox.critical(self.view, "Error", f"Calculation failed:\n{str(e)}")

    def get_scaled_header(self, header_name, start, end, step):
        if header_name == "Cumulative Distance":
            if self.full_cum_dist is not None: 
                return self.full_cum_dist[start:end:step]
            else: 
                return np.arange(start, end, step)
        
        raw = self.data_manager.get_header_slice(header_name, start, end, step)
        coord_keys = ['SourceX', 'SourceY', 'GroupX', 'GroupY', 'CDP_X', 'CDP_Y']
        
        if header_name in coord_keys and 'SourceGroupScalar' in self.data_manager.available_headers:
            scalars = self.data_manager.get_header_slice('SourceGroupScalar', start, end, step)
            return SeismicProcessing.apply_scalar(raw, scalars)
        
        return raw

    def show_dist_tool(self):
        if not self.data_manager: 
            return
        
        dlg = GeometryDialog(self.data_manager.available_headers, self.view)
        if dlg.exec() == QDialog.DialogCode.Accepted: 
            settings = dlg.get_settings()
            self.calculate_distance(settings)

    def on_header_changed(self):
        if not self.data_manager: 
            return
        
        header = self.view.combo_header.currentText()
        if header == "Trace Index": 
            self.active_header_map = None
        elif header == "Cumulative Distance": 
            self.active_header_map = self.full_cum_dist
        else: 
            self.active_header_map = self.get_scaled_header(header, 0, self.data_manager.n_traces, 1)
        
        start = self.loaded_start_trace
        end = self.loaded_end_trace
        num_traces = self.current_data.shape[1]
        
        step = max(1, int((end-start)/num_traces)) if num_traces > 0 else 1
        
        if header == "Trace Index": 
            self.x_vals = np.arange(start, end, step)
        else: 
            self.x_vals = self.get_scaled_header(header, start, end, step)
        
        x_min = self.x_vals[0] if self.x_vals.size > 0 else 0
        x_max = self.x_vals[-1] if self.x_vals.size > 0 else 1
        y_min = self.view.spin_y_min.value()
        y_max = self.view.spin_y_max.value()
        
        self.view.display_seismic(self.current_data.T, x_range=(x_min, x_max), y_range=(y_min, y_max))
        self.is_programmatic_update = True
        self.view.spin_x_min.setValue(x_min)
        self.view.spin_x_max.setValue(x_max)
        self.is_programmatic_update = False
        
        self.update_labels() 
        self.draw_horizons()
    
    def reset_for_new_file(self):
        """
        Clear current data, geometry and horizons so a new SEG-Y
        can be loaded into the same window.
        """
        # Core data/state
        self.data_manager = None
        self.current_data = None
        self.active_header_map = None
        self.full_cum_dist = None
        self.dist_unit = "m"

        # Trace range / axes caches
        self.loaded_start_trace = 0
        self.loaded_end_trace = 0
        self.x_vals = None
        self.t_vals = None

        # Reset header combo + controls
        self.view.combo_header.clear()
        self.view.combo_header.addItem("Trace Index")
        self.view.chk_manual_step.setChecked(False)
        self.view.spin_step.setEnabled(False)

        # Clear any drawn horizon graphics from the plot
        for item in self.horizon_items:
            self.view.plot_widget.removeItem(item)
        self.horizon_items = []

        # Reset picking / cursor
        self.is_picking_mode = False
        self.view.plot_widget.setCursor(Qt.CursorShape.ArrowCursor)

        # Reset Horizon Manager state
        self.horizon_manager.horizons = []
        self.horizon_manager.active_horizon_index = -1
        self.horizon_manager.is_picking = False
        self.horizon_manager.refresh_table()
        self.horizon_manager.lbl_status.setText("Status: Viewing Mode")
        self.horizon_manager.lbl_status.setStyleSheet(
            "font-weight: bold; color: gray;"
        )
        self.horizon_manager.btn_pick.setChecked(False)
        self.horizon_manager.btn_pick.setEnabled(False)

        # Status text
        self.view.update_status("No file loaded")

    
    def apply_changes(self):
        if not self.data_manager: 
            return
        
        self.view.update_status("Reloading data...")
        QApplication.processEvents()
        
        target_x_min = self.view.spin_x_min.value()
        target_x_max = self.view.spin_x_max.value()
        start_trace = int(target_x_min)
        end_trace = int(target_x_max)
        
        header = self.view.combo_header.currentText()
        if header != "Trace Index" and self.active_header_map is not None:
            if np.all(np.diff(self.active_header_map) >= 0):
                start_trace = np.searchsorted(self.active_header_map, target_x_min)
                end_trace = np.searchsorted(self.active_header_map, target_x_max)
            else:
                mask = (self.active_header_map >= min(target_x_min, target_x_max)) & (self.active_header_map <= max(target_x_min, target_x_max))
                indices = np.where(mask)[0]
                if indices.size > 0: 
                    start_trace = indices[0]
                    end_trace = indices[-1] + 1
                else: 
                    QMessageBox.warning(self.view, "Warning", f"No data found for range.")
                    return
                    
        start_trace = max(0, start_trace)
        end_trace = min(self.data_manager.n_traces, end_trace)
        
        if self.view.chk_manual_step.isChecked(): 
            step = int(self.view.spin_step.value())
        else:
            trace_count = abs(end_trace - start_trace)
            step = max(1, int(trace_count / 2000))
            if trace_count < 5000: 
                step = 1
                
        self.load_data_internal(start_trace, end_trace, step, auto_fit=False)
        
        self.is_programmatic_update = True
        self.view.plot_widget.setXRange(target_x_min, target_x_max, padding=0)
        self.view.plot_widget.setYRange(self.view.spin_y_min.value(), self.view.spin_y_max.value(), padding=0)
        self.is_programmatic_update = False
        
        self.view.update_status(f"Loaded: {self.data_manager.file_path.split('/')[-1]} (Subset)")

    def handle_horizon_export(self, index):
        if not self.data_manager: 
            return
        
        h = self.horizon_manager.horizons[index]
        points = h['points']
        if not points: 
            QMessageBox.warning(self.view, "Error", "Horizon is empty.")
            return
            
        dlg = HeaderExportDialog(self.data_manager.available_headers, self.view)
        if dlg.exec() != QDialog.DialogCode.Accepted: 
            return
            
        selected_headers = dlg.get_selected_headers()
        path, _ = QFileDialog.getSaveFileName(self.view, "Save Horizon CSV", f"{h['name']}.csv", "CSV (*.csv)")
        if not path: 
            return
            
        try:
            x_vals, y_vals = zip(*points)
            x_arr = np.array(x_vals)
            y_arr = np.array(y_vals)
            
            df = pd.DataFrame()
            current_x_mode = self.view.combo_header.currentText()
            df[current_x_mode] = x_arr
            df[self.view.combo_domain.currentText()] = y_arr
            
            trace_indices = np.zeros(len(x_arr), dtype=int)
            if current_x_mode == "Trace Index": 
                trace_indices = np.round(x_arr).astype(int)
            elif self.active_header_map is not None:
                if np.all(np.diff(self.active_header_map) >= 0): 
                    trace_indices = np.searchsorted(self.active_header_map, x_arr)
                    trace_indices = np.clip(trace_indices, 0, len(self.active_header_map)-1)
                else:
                    for i, val in enumerate(x_arr): 
                        trace_indices[i] = (np.abs(self.active_header_map - val)).argmin()
                        
            for hdr in selected_headers: 
                df[hdr] = self.data_manager.get_header_slice(hdr, 0, self.data_manager.n_traces, 1)[trace_indices]
                
            df.to_csv(path, index=False)
            QMessageBox.information(self.view, "Success", f"Saved horizon with {len(selected_headers)} extra headers.")
        except Exception as e: 
            traceback.print_exc()
            QMessageBox.critical(self.view, "Export Error", str(e))

    # --- UI Logic ---
    def on_plot_clicked(self, event):
        if not self.is_picking_mode: 
            return
        
        pos = event.scenePos()
        if self.view.plot_widget.plotItem.sceneBoundingRect().contains(pos):
            mousePoint = self.view.plot_widget.getPlotItem().vb.mapSceneToView(pos)
            click_x = mousePoint.x()
            click_y = mousePoint.y()
            
            trace_idx = int(click_x)
            header = self.view.combo_header.currentText()
            
            if header == "Trace Index": 
                trace_idx = int(round(click_x))
            elif self.active_header_map is not None:
                if len(self.active_header_map) > 0: 
                    trace_idx = int((np.abs(self.active_header_map - click_x)).argmin())
                    
            if event.button() == Qt.MouseButton.LeftButton: 
                self.horizon_manager.add_point(trace_idx, click_y)
            elif event.button() == Qt.MouseButton.RightButton:
                view_range = self.view.plot_widget.viewRange()
                y_height = abs(view_range[1][1] - view_range[1][0])
                y_tol = y_height * 0.02
                self.horizon_manager.delete_closest_point(trace_idx, click_y, tolerance_x=5, tolerance_y=y_tol)
                
    def sync_view_to_controls(self, _, ranges):
        if self.is_programmatic_update: 
            return
            
        x_range, y_range = ranges
        self.view.spin_x_min.blockSignals(True)
        self.view.spin_x_max.blockSignals(True)
        self.view.spin_y_min.blockSignals(True)
        self.view.spin_y_max.blockSignals(True)
        
        self.view.spin_x_min.setValue(x_range[0])
        self.view.spin_x_max.setValue(x_range[1])
        self.view.spin_y_min.setValue(y_range[0])
        self.view.spin_y_max.setValue(y_range[1])
        
        if not self.view.chk_manual_step.isChecked(): 
            visible_width = abs(x_range[1] - x_range[0])
            self.view.spin_step.setValue(max(1, int(visible_width / 2000)))
            
        self.view.spin_x_min.blockSignals(False)
        self.view.spin_x_max.blockSignals(False)
        self.view.spin_y_min.blockSignals(False)
        self.view.spin_y_max.blockSignals(False)

    def toggle_manual_step(self, state): 
        self.view.spin_step.setEnabled(state == 2)
        
    def toggle_flip_x(self, state): 
        self.view.plot_widget.getPlotItem().invertX(state == 2)
        
    def toggle_grid(self, state): 
        self.view.plot_widget.showGrid(x=(state == 2), y=(state == 2))
        
    def change_colormap(self, text): 
        self.view.set_colormap(text)
        
    def set_picking_mode(self, active, horizon_name): 
        self.is_picking_mode = active
        self.view.plot_widget.setCursor(Qt.CursorShape.CrossCursor if active else Qt.CursorShape.ArrowCursor)

    def draw_horizons(self):
        for item in self.horizon_items: 
            self.view.plot_widget.removeItem(item)
        self.horizon_items = []
        
        header = self.view.combo_header.currentText()
        if header == "Trace Index": 
            map_array = None
        elif header == "Cumulative Distance": 
            map_array = self.full_cum_dist
        elif self.active_header_map is not None: 
            map_array = self.active_header_map
        else: 
            map_array = None
            
        for h in self.horizon_manager.horizons:
            if not h['visible'] or not h['points']: 
                continue
                
            idx_data, y_data = zip(*h['points'])
            idx_arr = np.array(idx_data, dtype=int)
            y_arr = np.array(y_data)
            
            if map_array is not None: 
                idx_arr = np.clip(idx_arr, 0, len(map_array)-1)
                x_arr = map_array[idx_arr]
            else: 
                x_arr = idx_arr
                
            curve = pg.PlotCurveItem(x=x_arr, y=y_arr, pen=pg.mkPen(color=h['color'], width=2))
            self.view.plot_widget.addItem(curve)
            self.horizon_items.append(curve)
            
            scatter = pg.ScatterPlotItem(x=x_arr, y=y_arr, size=5, brush=h['color'], pen=None)
            self.view.plot_widget.addItem(scatter)
            self.horizon_items.append(scatter)
    
    # --- MISSING METHODS RESTORED ---
    def match_aspect_ratio(self):
        try:
            target_w = self.view.spin_fig_width.value()
            target_h = self.view.spin_fig_height.value()
            if target_h == 0: 
                return
                
            target_ratio = target_w / target_h
            current_plot_h = self.view.plot_widget.height()
            new_plot_w = int(current_plot_h * target_ratio)
            current_plot_w = self.view.plot_widget.width()
            diff_w = new_plot_w - current_plot_w
            
            self.view.resize(self.view.width() + diff_w, self.view.height())
        except Exception: 
            traceback.print_exc()
    
    def update_contrast(self):
        if self.current_data is None: 
            return
        try:
            p = self.view.spin_contrast.value()
            if self.current_data.size > 0: 
                clip_val = np.percentile(np.abs(self.current_data), p)
            else: 
                clip_val = 1.0
            
            self.view.img_item.setImage(self.current_data.T, levels=[-clip_val, clip_val], autoLevels=False)
        except Exception: 
            traceback.print_exc()
        
    def setup_menu(self):
        menu_bar = self.view.menuBar()
        file_menu = menu_bar.addMenu("File")
        self.action_load_menu = file_menu.addAction("Load SEG-Y", self.load_file)
        file_menu.addAction("Export PDF/PNG", self.export_figure)
        
        proc_menu = menu_bar.addMenu("Processing")
        self.action_agc = QAction("Apply AGC", self.view)
        self.action_agc.triggered.connect(self.run_agc)
        self.action_agc.setEnabled(False)
        proc_menu.addAction(self.action_agc)
        
        self.action_filter = QAction("Bandpass Filter", self.view)
        self.action_filter.triggered.connect(self.run_filter)
        self.action_filter.setEnabled(False)
        proc_menu.addAction(self.action_filter)
        
        proc_menu.addSeparator()
        self.action_reset = QAction("Reset to Raw Data", self.view)
        self.action_reset.triggered.connect(self.reset_processing)
        self.action_reset.setEnabled(False)
        proc_menu.addAction(self.action_reset)

        attr_menu = menu_bar.addMenu("Attributes")
        self.act_env = QAction("Instantaneous Amplitude (Envelope)", self.view)
        self.act_env.triggered.connect(lambda: self.run_attribute("Envelope"))
        self.act_env.setEnabled(False)
        attr_menu.addAction(self.act_env)
        
        self.act_phase = QAction("Instantaneous Phase", self.view)
        self.act_phase.triggered.connect(lambda: self.run_attribute("Phase"))
        self.act_phase.setEnabled(False)
        attr_menu.addAction(self.act_phase)
        
        self.act_cos = QAction("Cosine of Phase", self.view)
        self.act_cos.triggered.connect(lambda: self.run_attribute("Cosine Phase"))
        self.act_cos.setEnabled(False)
        attr_menu.addAction(self.act_cos)
        
        self.act_freq = QAction("Instantaneous Frequency", self.view)
        self.act_freq.triggered.connect(lambda: self.run_attribute("Frequency"))
        self.act_freq.setEnabled(False)
        attr_menu.addAction(self.act_freq)
        
        attr_menu.addSeparator()
        self.act_rms = QAction("RMS Amplitude", self.view)
        self.act_rms.triggered.connect(lambda: self.run_attribute("RMS"))
        self.act_rms.setEnabled(False)
        attr_menu.addAction(self.act_rms)

        tools_menu = menu_bar.addMenu("Tools")
        self.action_dist = QAction("Setup Geometry / Distance", self.view)
        self.action_dist.triggered.connect(self.show_dist_tool)
        self.action_dist.setEnabled(False)
        tools_menu.addAction(self.action_dist)
        
        self.action_horizons = QAction("Horizon Manager & Picking", self.view)
        self.action_horizons.triggered.connect(lambda: self.horizon_manager.show())
        tools_menu.addAction(self.action_horizons)
        
        self.action_text_header = QAction("View Text Header", self.view)
        self.action_text_header.triggered.connect(self.show_text_header)
        self.action_text_header.setEnabled(False)
        tools_menu.addAction(self.action_text_header)
        
        self.action_header_qc = QAction("Trace Header QC Plot", self.view)
        self.action_header_qc.triggered.connect(self.show_header_qc)
        self.action_header_qc.setEnabled(False)
        tools_menu.addAction(self.action_header_qc)
        
        self.action_spectrum = QAction("Frequency Spectrum", self.view)
        self.action_spectrum.triggered.connect(self.show_spectrum)
        self.action_spectrum.setEnabled(False)
        tools_menu.addAction(self.action_spectrum)
        
        self.action_histogram = QAction("View Amplitude Histogram", self.view)
        self.action_histogram.triggered.connect(self.show_amplitude_histogram)
        self.action_histogram.setEnabled(False)
        tools_menu.addAction(self.action_histogram)
        
        about_menu = menu_bar.addMenu("About")
        self.action_about = QAction("About SeisPlotPy", self.view)
        self.action_about.triggered.connect(self.show_about_dialog)
        about_menu.addAction(self.action_about)

    def show_text_header(self): 
        if self.data_manager: 
            TextHeaderDialog(self.data_manager.get_text_header(), self.view).exec()

    def show_header_qc(self): 
        if self.data_manager: 
            HeaderQCPlot(self.data_manager.available_headers, self.data_manager, self.view).exec()

    def show_about_dialog(self):
        """Show About info for the standalone SeisPlotPy app."""
        text = (
            "SeisPlotPy (Standalone Desktop)\n"
            "Developed and maintained by: Arjun V H\n"
            "Contact: arjunvelliyidathu@gmail.com\n\n"
            "SeisPlotPy is released under the GPL license.\n\n"
            "Found a bug? Need a feature?\n"
            "Please report it here:\n"
            "https://github.com/arjun-vh/SeisPlotPy-Desktop/issues"
        )

        QMessageBox.information(self.view, "About SeisPlotPy", text)

    def show_spectrum(self):
        if self.current_data is None: 
            return
        
        try: 
            freqs, amps = SeismicProcessing.calculate_spectrum(self.current_data, self.data_manager.sample_rate)
            self.spectrum_dlg = SpectrumPlot(freqs, amps, self.view)
            self.spectrum_dlg.show()
        except Exception as e: 
            traceback.print_exc()
            QMessageBox.critical(self.view, "Error", str(e))

    def run_agc(self):
        if self.current_data is None: 
            return
            
        window, ok = QInputDialog.getInt(self.view, "AGC Settings", "Window Size (ms):", 500, 10, 5000)
        if not ok: 
            return
            
        try: 
            self.current_data = SeismicProcessing.apply_agc(self.current_data, self.data_manager.sample_rate, window)
            self.update_display_only()
            self.view.update_status("Applied AGC")
        except Exception as e: 
            traceback.print_exc()
            QMessageBox.critical(self.view, "Processing Error", str(e))

    def run_filter(self):
        if self.current_data is None: 
            return
            
        dlg = BandpassDialog(self.view)
        if dlg.exec():
            low, high = dlg.get_values()
            try: 
                self.current_data = SeismicProcessing.apply_bandpass(self.current_data, self.data_manager.sample_rate, low, high)
                self.update_display_only()
                self.view.update_status(f"Applied Bandpass {low}-{high} Hz")
            except Exception as e: 
                traceback.print_exc()
                QMessageBox.critical(self.view, "Processing Error", str(e))

    def reset_processing(self): 
        self.apply_changes()
        self.view.update_status("Reset to Raw Data")

def main():
    app = QApplication(sys.argv)
    
    # Force a consistent light style regardless of OS dark mode
    apply_light_style(app)
    if os.path.exists(resource_path("seisplotpy.ico")):
        app.setWindowIcon(QIcon(resource_path("seisplotpy.ico")))
    
    controller = MainController()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()