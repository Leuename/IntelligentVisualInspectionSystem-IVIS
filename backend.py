"""
- OpState(Enum): Finite state machine enumerations for the operation lifecycles.
- SerialThread(threading.Thread): Non-blocking thread handling Arduino communication via PySerial.
- MainWindow(QMainWindow): Main GUI application class orchestrating camera feeds, DB saves, Arduino interactions, and Excel exports.
- SplashScreen(QMainWindow): Initial loading splash screen delay window.
Functions/Methods:
- resource_path: Determines correct absolute paths for PyInstaller bundling compatibility.
- SerialThread.run: Connects to Arduino and loops reading/writing to the serial port queues.
- SerialThread.send: Queues messages to be sent to the Arduino.
- SerialThread.stop: Safely closes the serial port and ends the thread loop.
- MainWindow.*: Various Qt Slots handling UI events, Arduino signals (ESTOP, ACK, RESET), and database triggers.
- MainWindow._find_arduino_port: Auto-detects the Arduino COM port using hardware identifiers.
- MainWindow.on_export_button_clicked: Aggregates SQLite data and formats it into an Excel sheet.
Workflows/Interactions:
- MainWindow coordinates interactions between CameraInferenceThread (camera_module), CaptureDB (db), and SerialThread.
- Heavily relies on PySide6 Signals/Slots to safely transfer data from background threads (DB/Camera/Serial) back to the main GUI thread.
"""

from __future__ import annotations
import sys
import os
import time
import threading
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtCore
from frontend import Ui_MainWindow
from splashscreen import Ui_MainWindow as SplashScreenUI
from camera_module import CameraInferenceThread
from db import CaptureDB
from typing import *
import numpy as np
import xlsxwriter
import serial
import queue
import serial.tools.list_ports
from enum import Enum, auto

class OpState(Enum):
    IDLE = auto()      
    STARTING = auto()  
    RUNNING = auto()   
    PAUSING = auto()
    PAUSED = auto()    
    RESUMING = auto()
    PACKAGE_GAP = auto()
    MAG_COMPLETE = auto()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SerialThread(threading.Thread):
    def __init__(self, port: str, baudrate: int, on_message_received: Callable, on_connection_error: Callable):
        super().__init__()
        self.serial_port = None
        self.port = port
        self.baudrate = baudrate
        self.daemon = True
        self.running = True
        self.send_queue = queue.Queue()
        self.on_message_received = on_message_received
        self.on_connection_error = on_connection_error

    def run(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=0.1)
            print(f"[Serial] Successfully connected to {self.port}")
        except serial.SerialException as e:
            print(f"[Serial] FAILED to connect to {self.port}: {e}")
            self.on_connection_error(str(e))
            return

        while self.running:
            if self.serial_port and self.serial_port.is_open:
                try:
                    if self.serial_port.in_waiting > 0:
                        line = self.serial_port.readline().decode('utf-8').strip()
                        if line:
                            self.on_message_received(line)
                except UnicodeDecodeError:
                    pass
                except serial.SerialException as e:
                    print(f"[Serial] Read error: {e}. Device may be disconnected.")
                    self.on_connection_error(f"Device disconnected (read error): {e}")
                    self.running = False
                    break

            try:
                msg = self.send_queue.get(block=False)
                if msg is None: continue
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.write(msg.encode('utf-8'))
                self.send_queue.task_done()
            except queue.Empty:
                pass
            except serial.SerialException as e:
                print(f"[Serial] Write error: {e}. Device may be disconnected.")
                self.on_connection_error(f"Device disconnected (write error): {e}")
                self.running = False
                break
            
            time.sleep(0.05) 
        
        print("[Serial] Thread stopping.")

    def send(self, msg):
        if self.serial_port and self.serial_port.is_open:
            self.send_queue.put(msg)
        else:
            print(f"[Serial] Skipping send: Port {self.port} is not connected or thread is not running.")

    def stop(self):
        self.running = False
        self.send_queue.put(None)
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

class MainWindow(QMainWindow):
    serial_message_received = Signal(str)
    serial_connection_error = Signal(str)
    db_save_failed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.live_camera.setScaledContents(True)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("IVIS")

        self.capture_db = CaptureDB()
        model_path = resource_path("train8.1.pt")
        
        self.camera_rois = {
            0: (40, 400, 100, 500),
            1: (0, 1000, 150, 500)
        }

        self.current_camera_index = 0
        self.active_roi = self.camera_rois.get(self.current_camera_index)
        
        self.thread = CameraInferenceThread(
            camera_rois=self.camera_rois,
            model_path=model_path, 
            conf_thresh=0.75
        )
        self.thread.frame_ready.connect(self.on_frame_ready)
        self.thread.detections_ready.connect(self.on_detections_ready)
        self.thread.init_failed.connect(self.on_camera_init_failed)

        self.serial_message_received.connect(self._handle_serial_message)
        self.serial_connection_error.connect(self._on_serial_connection_error)
        self.db_save_failed.connect(self.on_db_save_failed)
        
        arduino_port = self._find_arduino_port()
        
        if arduino_port:
            self.serial_thread = SerialThread(
                port=arduino_port,
                baudrate=115200, 
                on_message_received=self._on_message_from_thread,
                on_connection_error=self._on_serial_error_from_thread
            )
            self.serial_thread.start()
        else:
            self.serial_thread = None
            QMessageBox.critical(
                self, 
                "Arduino Connection Error",
                "Could not find an Arduino.\n\nPlease check the USB connection and restart the application."
            )
            self.ui.action_button.setEnabled(False)

        self.ui.minimize.clicked.connect(self.showMinimized)
        self.ui.close.clicked.connect(self.close)
        self.ui.export_button.clicked.connect(self.on_export_button_clicked)
        self.ui.action_button.clicked.connect(self.toggle_operation)

        self._state = OpState.IDLE
        self._inference_history = []
        self._reset_count = 0
        self._magazine_run_count = 0
        
        self._pause_timer = QTimer(self)
        self._pause_timer.setSingleShot(True)
        self._pause_timer.timeout.connect(self._resume_listing)

        self._start_delay_timer = QTimer(self)
        self._start_delay_timer.setSingleShot(True)
        self._start_delay_timer.timeout.connect(self._start_listing_after_delay)

        self._ack_timer = QTimer(self)
        self._ack_timer.setSingleShot(True)
        self._ack_timer.timeout.connect(self._on_ack_timeout)
        self._ack_revert_state = OpState.IDLE

        self._bg_save_thread: Optional[threading.Thread] = None

        self._update_ui_state()
        self.showMaximized()
        
    @Slot(str)
    def on_camera_init_failed(self, error_msg: str):
        QMessageBox.critical(
            self,
            "Critical Camera/Model Error",
            f"The application cannot start:\n\n{error_msg}\n\nPlease check the model file (best11.pt) and camera connection."
        )
        self.ui.action_button.setEnabled(False)
        
    @Slot(str)
    def on_db_save_failed(self, error_msg: str):
        QMessageBox.warning(
            self,
            "Database Save Error",
            f"Warning: Could not save the last detection to the database.\n\nError: {error_msg}\n\nPlease check system permissions or restart the application."
        )
        
    def _find_arduino_port(self) -> Optional[str]:
        print("[Serial] Searching for Arduino...")
        ports = serial.tools.list_ports.comports()
        
        arduino_identifiers = ["arduino", "ch340", "cp210x"]
        
        for port in ports:
            port_desc = (port.description or "").lower()
            port_hwid = (port.hwid or "").lower()
            port_mfr = (port.manufacturer or "").lower()
            
            print(f"[Serial] Checking port: {port.device}, Desc: {port_desc}, HWID: {port_hwid}")
            
            for identifier in arduino_identifiers:
                if (identifier in port_desc or 
                    identifier in port_hwid or 
                    identifier in port_mfr):
                    print(f"[Serial] Arduino found at: {port.device}")
                    return port.device
                    
        print("[Serial] No Arduino found.")
        return None

    def _start_listing_after_delay(self):
        print("[Backend] 10s delay complete. Starting inference.")
        self._state = OpState.RUNNING
        self.thread.pause_inference(False)
        self._update_ui_state()

    def _on_message_from_thread(self, msg: str):
        self.serial_message_received.emit(msg)

    def _on_serial_error_from_thread(self, error_msg: str):
        self.serial_connection_error.emit(error_msg)

    @Slot(str)
    def _on_serial_connection_error(self, error_msg: str):
        QMessageBox.critical(
            self, 
            "Arduino Connection Error",
            f"Failed to connect to Arduino:\n{error_msg}\n\nPlease check the USB connection and restart the application."
        )
        self.ui.action_button.setEnabled(False)
        
    def _cancel_all_timers(self):
        self._pause_timer.stop()
        self._start_delay_timer.stop()
        self._ack_timer.stop()

    def _on_ack_timeout(self):
        self._cancel_all_timers()
        print(f"[Backend] ACK Timeout! Reverting to {self._ack_revert_state.name}")
        QMessageBox.warning(self, "Arduino Error", "No response from Arduino. Operation canceled.")
        self._state = self._ack_revert_state
        self._update_ui_state()

    @Slot(str)
    def _handle_serial_message(self, msg: str):
        print(f"[Serial RX] {msg}")
        
        if "ESTOP" in msg.upper():
            print("[Backend] E-STOP received! Triggering pause.")
            if self._state in (OpState.RUNNING, OpState.PACKAGE_GAP):
                self._cancel_all_timers()
                self._state = OpState.PAUSED
                self.thread.pause_inference(True)
                self.send_signal_to_arduino("pause\n")
                self._update_ui_state()
            return

        elif "ACK_PAUSE" in msg.upper():
            if self._state == OpState.PAUSING:
                print("[Backend] ACK_PAUSE received. Operation is paused.")
                self._ack_timer.stop()
                self._state = OpState.PAUSED
                self.thread.pause_inference(True)
                self._update_ui_state()
                
        elif "ACK_PLAY" in msg.upper():
            if self._state == OpState.RESUMING:
                print("[Backend] ACK_PLAY received. Operation is resuming.")
                self._ack_timer.stop()
                self._state = OpState.RUNNING
                self.thread.pause_inference(False)
                self._update_ui_state()

        elif "HOMING COMPLETE" in msg.upper():
            print("[Backend] Arduino physical reset detected (HOMING COMPLETE).")
            self._perform_soft_reset()
            
        elif "RESET" in msg.upper():
            self.ui.action_button.setChecked(self.ui.action_button.isChecked())
            print("[Backend] Arduino 'RESET' command received. Performing soft reset.")
            self._perform_soft_reset()

    def _perform_soft_reset(self):
        print("[Backend] Physical RESET received. Resetting state...")
        
        self._cancel_all_timers()
        self.thread.pause_inference(True)
        
        self._state = OpState.IDLE
        self._reset_count = 0
        self._inference_history.clear()
        
        try:
            self.capture_db.reset_package_counter()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to reset package counter: {e}")
            
        self._update_ui_state()
        print("[Backend] Soft reset complete. Ready for new operation.")

    def _save_stripe(self, description: str, operator: str, mag_from: str, mag_to: str):
        try:
            self.capture_db.add_stripe(
                description=description,
                operator=operator,
                mag_from=mag_from,
                mag_to=mag_to
            )
        except Exception as e:
            error_msg = f"Failed to save stripe in background: {e}"
            print(error_msg)
            self.db_save_failed.emit(error_msg)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.thread.isRunning():
            self.thread.start()

    def closeEvent(self, event):
        operator_name = self.ui.operator_lineEdit.text().strip()
        title = "Confirm Exit"
        
        message = f"This will reset the current package count and close the app. Are you sure, {operator_name}?" \
                    if operator_name else \
                    "This will reset the current package count and close the app. Are you sure?"
        
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("Resetting package count and closing application...")
            
            try:
                self.capture_db.reset_package_counter()
                print("[Backend] Package counter has been reset.")
            except Exception as e:
                print(f"Error resetting package counter on close: {e}")

            self._cancel_all_timers()
            
            if self.serial_thread:
                self.serial_thread.stop()
                self.serial_thread.join()
                print("[Backend] Serial thread joined.")
            
            if self.thread:
                self.thread.stop()
                self.thread.wait()
                print("[Backend] Camera thread waited.")
            
            event.accept()
        else:
            event.ignore()
            
    def toggle_operation(self):
        if self._state in (OpState.STARTING, OpState.PAUSING, OpState.RESUMING):
            print(f"[Backend] Ignoring toggle: Operation already in progress ({self._state.name})")
            return

        if self._state == OpState.IDLE:
            if not self.check_line_edit_changes():
                return
            
            print("[Backend] Starting new session in 10s...")
            self._state = OpState.STARTING
            self._update_ui_state()
            
            self.send_signal_to_arduino("play\n")
            
            self._cancel_all_timers()
            self._start_delay_timer.start(9000)

        elif self._state == OpState.RUNNING:
            print("[Backend] Requesting pause... waiting for ACK.")
            self._state = OpState.PAUSING
            self._update_ui_state()
            self.send_signal_to_arduino("pause\n")

            self._cancel_all_timers()
            self._ack_revert_state = OpState.RUNNING
            self._ack_timer.start(3000)

        elif self._state == OpState.PAUSED:
            print("[Backend] Requesting resume... waiting for ACK.")
            self._state = OpState.RESUMING
            self._update_ui_state()
            self.send_signal_to_arduino("play\n")

            self._cancel_all_timers()
            self._ack_revert_state = OpState.PAUSED
            self._ack_timer.start(3000)

    def check_line_edit_changes(self):
        operator = self.ui.operator_lineEdit.text().strip()
        mag_from = self.ui.magazine_from.text().strip()
        mag_to = self.ui.magazine_to.text().strip()
        
        missing_fields = []
        if not operator: missing_fields.append("Operator")
        if not mag_from: missing_fields.append("Magazine From")
        if not mag_to: missing_fields.append("Magazine To")
        
        if missing_fields:
            QMessageBox.warning(
                self,
                "Missing Information",
                f"Please fill in the following field(s):\n- " + "\n- ".join(missing_fields)
            )
            return False
        return True

    def _resume_listing(self):
        if self._state == OpState.PACKAGE_GAP:
            print("[Backend] 40s gap complete. Resuming.")
            self._state = OpState.RUNNING
            self._inference_history.clear()
            self._update_ui_state()

    def send_signal_to_arduino(self, msg):
        if self.serial_thread:
            self.serial_thread.send(msg)
        else:
            print(f"[Serial] Cannot send '{msg}': No Arduino connected.")

    @Slot(QImage)
    def on_frame_ready(self, image: QImage):
        self.ui.live_camera.setPixmap(QPixmap.fromImage(image))

    def filter_unique_labels(self, detections) -> list[str]:
        seen = set()
        unique_labels: list[str] = []
        for d in detections:
            if isinstance(d, str): label = d
            elif isinstance(d, dict): label = d.get("label")
            else: label = None
            
            if not label: continue
            if label not in seen:
                seen.add(label)
                unique_labels.append(label)
        return unique_labels
    
    def _update_ui_state(self):
        is_running = self._state not in (OpState.IDLE, OpState.MAG_COMPLETE)
        self.ui.operator_lineEdit.setDisabled(is_running)
        self.ui.magazine_from.setDisabled(is_running)
        self.ui.magazine_to.setDisabled(is_running)
        
        label_names = ['one','two','three','four','five','six','seven','eight','nine','ten']
        
        if self._state != OpState.PACKAGE_GAP:
            for label_name in label_names:
                label = getattr(self.ui, label_name, None)
                if label:
                    label.setText("")

        for i, text in enumerate(self._inference_history):
            if i < len(label_names):
                label_widget = getattr(self.ui, label_names[i], None)
                if label_widget:
                    label_widget.setText(text)

        is_checked_state = self._state in (
            OpState.RUNNING, 
            OpState.PAUSING,
            OpState.PACKAGE_GAP
        )
        self.ui.action_button.setChecked(is_checked_state)

    @Slot(list)
    def on_detections_ready(self, names: list):
        if self._state != OpState.RUNNING:
            return

        current_time = time.time()
        if current_time - getattr(self, "_last_inference_update", 0.0) < 1.2:
            return
        self._last_inference_update = current_time

        unique_names = self.filter_unique_labels(names)
        text = ", ".join(unique_names) if unique_names else "No detections"

        if self._bg_save_thread and self._bg_save_thread.is_alive():
            print("Skipping stripe save, previous save still in progress.")
            return 

        operator = self.ui.operator_lineEdit.text().strip()
        mag_from = self.ui.magazine_from.text().strip()
        mag_to = self.ui.magazine_to.text().strip()
        
        if not operator or not mag_from or not mag_to:
            print("Missing session info, pausing.")
            self.toggle_operation()
            return

        self._bg_save_thread = threading.Thread(
            target=self._save_stripe,
            args=(text, operator, mag_from, mag_to),
            daemon=True
        )
        self._bg_save_thread.start()
        
        self._inference_history.append(text)
        if len(self._inference_history) > 10:
             self._inference_history = self._inference_history[-10:]

        if len(self._inference_history) == 10:
            self._state = OpState.PACKAGE_GAP
            
            self._cancel_all_timers()
            self._pause_timer.start(27000)
            
            self._reset_count += 1
            print(f"--- UI Package {self._reset_count} complete ---")
            
            if self._reset_count >= 20:
                print(f"--- Magazine complete. Stopping operation. ---")
                
                self._state = OpState.MAG_COMPLETE
                self._pause_timer.stop()
                
                self.ui.operator_lineEdit.clear()
                self.ui.magazine_from.clear()
                self.ui.magazine_to.clear()

                self._reset_count = 0
                self._magazine_run_count += 1
                self._inference_history.clear()

                QMessageBox.information(self, 
                                        "Operation Complete", 
                                        f"Magazine {self._magazine_run_count} is done processing.")
                
                self._state = OpState.IDLE
                self._update_ui_state()
                return

        self._update_ui_state()

    def on_export_button_clicked(self):
        if self._bg_save_thread and self._bg_save_thread.is_alive():
            QMessageBox.information(self, "Export", "Waiting for a database save to finish... Please try again in a moment.")
            return

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Select Export File Type")
        msg_box.setText("Choose the file type for export:")
        msg_box.addButton("Excel", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)
        msg_box.exec()

        if msg_box.clickedButton() == cancel_button:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Exported File", "", "Excel files (*.xlsx)")
        if not save_path:
            return
        
        if not save_path.lower().endswith(".xlsx"):
            save_path += ".xlsx"

        try:
            data = self.capture_db.get_all_capture_data()
            if not data:
                QMessageBox.information(self, "Export", "No data found to export.")
                return

            magazines = {}
            for row in data:
                mag_id, operator, mag_from, mag_to, pkg_num, stripe_num, description = row
                
                if mag_id not in magazines:
                    magazines[mag_id] = {
                        'operator': operator, 
                        'mag_from': mag_from, 
                        'mag_to': mag_to,
                        'grid': {}
                    }
                
                if pkg_num not in magazines[mag_id]['grid']:
                    magazines[mag_id]['grid'][pkg_num] = {}
                
                magazines[mag_id]['grid'][pkg_num][stripe_num] = description

            workbook = xlsxwriter.Workbook(save_path)
            
            top_header_format = workbook.add_format({
                'bold': True,
                'font_size': 11,
                'align': 'left',
                'valign': 'vcenter',
                'bg_color': '#E0E0E0',
                'border': 1
            })
            
            grid_header_format = workbook.add_format({
                'bold': True, 
                'align': 'center', 
                'valign': 'vcenter', 
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'align': 'center', 
                'valign': 'vcenter', 
                'border': 1, 
                'text_wrap': True
            })
            
            unit_header_format = workbook.add_format({
                'bold': True, 
                'align': 'center', 
                'valign': 'vcenter', 
                'border': 1, 
                'bg_color': '#F0F0F0'
            })

            if not magazines:
                QMessageBox.information(self, "Export", "No processed data to export.")
                workbook.close()
                return

            for mag_id, mag_data in magazines.items():
                sheet_name = f"Magazine {mag_id}"
                worksheet = workbook.add_worksheet(sheet_name)
                grid_data = mag_data['grid']

                worksheet.set_column('A:A', 10)
                worksheet.set_column('B:K', 10)
                
                worksheet.set_row(0, 20)
                worksheet.set_row(1, 20)
                worksheet.set_row(2, 20)
                worksheet.set_row(3, 20)
                
                for i in range(4, 24):
                    worksheet.set_row(i, 45) 

                worksheet.merge_range('A1:K1', f"Magazine To:     {mag_data['mag_to']}", top_header_format)
                worksheet.merge_range('A2:K2', f"Magazine From:   {mag_data['mag_from']}", top_header_format)
                worksheet.merge_range('A3:K3', f"Operator:        {mag_data['operator']}", top_header_format)

                worksheet.write('A4', "UNIT NO.", grid_header_format) 
                for i in range(1, 11):
                    worksheet.write(3, i, i, grid_header_format) 

                for i in range(1, 21):
                    worksheet.write(i + 3, 0, i, unit_header_format) 
                
                for pkg_num in range(1, 21):
                    for stripe_num in range(1, 11):
                        description = grid_data.get(pkg_num, {}).get(stripe_num, "")
                        worksheet.write(pkg_num + 3, stripe_num, description, cell_format)

            workbook.close()
            QMessageBox.information(self, "Export Successful", f"Data exported successfully to:\n{save_path}")

        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"Failed to export data:\n{str(e)}")

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SplashScreenUI()
        self.ui.setupUi(self)
        QTimer.singleShot(2500, self.openMainWindow)
        self.show()

    def openMainWindow(self):
        self.main_win = MainWindow()
        self.main_win.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())