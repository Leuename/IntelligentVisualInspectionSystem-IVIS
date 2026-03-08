"""
- CameraInferenceThread(QThread): Background thread that captures frames, performs inference, optionally applies Region of Interest (ROI), and emits annotated frames/detections to the UI.
Functions/Methods:
- get_dshow_camera_names: Parses the Windows Registry to identify physical DirectShow camera names, specifically filtering out virtual cameras like OBS.
- CameraInferenceThread.__init__: Configures the thread with camera ROIs, YOLO model paths, confidence thresholds, and initializes event flags.
- CameraInferenceThread.run: The main thread loop. Automatically selects the optimal physical camera using DSHOW indices, falls back to a black screen if none is found, reads frames, runs YOLO inference, draws bounding boxes/ROIs, and emits annotated QImages back to the main GUI thread.
- CameraInferenceThread.stop: Safely sets event flags to terminate the thread loop.
- CameraInferenceThread.pause_inference: Pauses or resumes the active frame capture and inference loop without killing the thread.
Workflows/Interactions:
- Evaluates the local system for external physical cameras via DSHOW.
- Injects QImage snapshots and detection lists directly into the PyQt UI thread via PyQt Signals to ensure non-blocking UI behavior.
- Supports dynamically toggling a black screen fallback when hardware is missing.
"""

import cv2
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
from ultralytics import YOLO
import torch
import threading
import numpy as np
import winreg

def get_dshow_camera_names():
    names = []
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\CLSID\{860BB310-5D01-11d0-BD3B-00A0C911CE86}\Instance")
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                friendly_name = winreg.QueryValueEx(subkey, "FriendlyName")[0]
                names.append(friendly_name)
                winreg.CloseKey(subkey)
            except OSError:
                names.append("Unknown")
        winreg.CloseKey(key)
    except OSError:
        pass
    return names

class CameraInferenceThread(QThread):
    frame_ready = Signal(QImage)
    detections_ready = Signal(list)
    boxes_ready = Signal(list)
    init_failed = Signal(str)

    def __init__(self, camera_rois: dict, model_path: str, conf_thresh: float = 0.75, parent=None):
        super().__init__(parent)
        self.camera_rois = camera_rois
        self.model_path = model_path
        self.conf_thresh = conf_thresh
        
        self.active_camera_index = None
        self.roi = None
        self.use_black_screen = False
        
        self._init_error: str | None = None
        
        self._running = threading.Event()
        self._pause = threading.Event() 
        self._pause.set()
        
        try:
            self.model = YOLO(self.model_path)
            self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.conf = self.conf_thresh
        except Exception as e:
            self._init_error = f"Failed to load YOLO model from {self.model_path}. Error: {e}"
            print(f"[CameraThread] {self._init_error}")
        
        self.cap = None

    def run(self):
        if self._init_error:
            self.init_failed.emit(self._init_error)
            return
        
        try:
            dshow_cameras = get_dshow_camera_names()
            print(f"[CameraInferenceThread] Detected DSHOW cameras: {dshow_cameras}")
            
            valid_indices = []
            for idx, name in enumerate(dshow_cameras):
                lower_name = name.lower()
                if "obs" not in lower_name and "virtual" not in lower_name:
                    valid_indices.append(idx)
                    
            print(f"[CameraInferenceThread] Valid DSHOW indices (skipping OBS/Virtual): {valid_indices}")
            
            selected_cap = None
            selected_idx = None
            
            for idx in reversed(valid_indices):
                cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                if cap.isOpened():
                    ret, test_frame = cap.read()
                    if ret:
                        selected_cap = cap
                        selected_idx = idx
                        break
                cap.release()
                
            if selected_cap:
                self.cap = selected_cap
                self.active_camera_index = selected_idx
                self.roi = self.camera_rois.get(selected_idx) if self.camera_rois else None
                print(f"[CameraInferenceThread] Successfully opened physical camera at index {selected_idx} using DSHOW")
            else:
                print(f"[CameraInferenceThread] No valid physical camera found. Falling back to black screen.")
                self.cap = None
                self.active_camera_index = None
                self.roi = None
                self.use_black_screen = True
                
        except Exception as e:
            error_msg = f"An unexpected error occurred while initializing cameras: {e}"
            print(f"[CameraInferenceThread] {error_msg}")
            self.init_failed.emit(error_msg)
            return
            
        self._running.set()
        print("[CameraThread] Thread started, camera open. Pausing and waiting for 'go' signal.")
        
        roi_y1, roi_y2, roi_x1, roi_x2 = (0, 0, 0, 0)
        use_roi = False
        if self.roi and len(self.roi) == 4:
            roi_y1, roi_y2, roi_x1, roi_x2 = self.roi
            use_roi = True
            print(f"[CameraThread] Using ROI: y=({roi_y1}:{roi_y2}), x=({roi_x1}:{roi_x2})")

        while self._running.is_set():
            try:
                self._pause.wait() 
                
                if not self._running.is_set():
                    break
                
                if self.use_black_screen:
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    ret = True
                else:
                    ret, frame = self.cap.read()
                    if not ret:
                        time.sleep(0.05)
                        continue
                
                inference_frame = frame
                annotated_frame = frame.copy() 
                
                if use_roi:
                    frame_h, frame_w = frame.shape[:2]
                    if roi_y2 > frame_h or roi_x2 > frame_w or roi_y1 < 0 or roi_x1 < 0:
                        cv2.rectangle(annotated_frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 0, 255), 2)
                        cv2.putText(annotated_frame, "INVALID ROI", (roi_x1, roi_y1 - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        inference_frame = frame
                        use_roi = False
                    else:
                        inference_frame = frame[roi_y1:roi_y2, roi_x1:roi_x2]
                        cv2.rectangle(annotated_frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
                
                results = self.model(inference_frame, verbose=False)[0]
                
                boxes = results.boxes
                names = []
                boxes_info = []
                
                if boxes is not None and len(boxes) > 0:
                    for box in boxes:
                        cls = int(box.cls.item())
                        conf = float(box.conf.item())
                        xyxy_crop = tuple(map(float, box.xyxy[0].tolist()))
                        
                        if cls < len(self.model.names):
                            names.append(self.model.names[cls])
                        else:
                            names.append(f"Unknown Class {cls}")
                        
                        if use_roi:
                            xyxy_full = (
                                xyxy_crop[0] + roi_x1,
                                xyxy_crop[1] + roi_y1,
                                xyxy_crop[2] + roi_x1,
                                xyxy_crop[3] + roi_y1
                            )
                            boxes_info.append({'xyxy': xyxy_full, 'cls': cls, 'conf': conf})
                        else:
                            boxes_info.append({'xyxy': xyxy_crop, 'cls': cls, 'conf': conf})

                annotated_crop = results.plot()

                if use_roi:
                    if annotated_crop.shape == annotated_frame[roi_y1:roi_y2, roi_x1:roi_x2].shape:
                        annotated_frame[roi_y1:roi_y2, roi_x1:roi_x2] = annotated_crop
                else:
                    annotated_frame = annotated_crop
                
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

                self.frame_ready.emit(qt_image.copy())
                self.detections_ready.emit(names)
                self.boxes_ready.emit(boxes_info)

                time.sleep(0.03)

            except Exception as e:
                error_msg = f"A critical error occurred during camera inference: {e}\nThe camera thread has stopped."
                print(f"[CameraThread] {error_msg}")
                self.init_failed.emit(error_msg)
                self.stop()

        if self.cap:
            self.cap.release()
        print("[CameraThread] Stopped and camera released.")

    def stop(self):
        self._pause.set()
        self._running.clear()

    def pause_inference(self, pause: bool):
        if pause:
            self._pause.clear()
            print("[CameraThread] Paused.")
        else:
            self._pause.set()
            print("[CameraThread] Resumed.")