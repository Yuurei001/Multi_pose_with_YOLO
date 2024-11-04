import cv2
import time
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import threading

<<<<<<< HEAD
=======

>>>>>>> origin/main
class PoseDetector:
    def __init__(self):
        # Khởi tạo giao diện
        self.setup_gui()

        # Khởi tạo biến
        self.cap = None
        self.is_running = False
        self.model = YOLO('yolov8n-pose.pt')

        # Tối ưu cho CPU
<<<<<<< HEAD
        cv2.setNumThreads(8)  # Điều chỉnh số thread phù hợp với CPU
=======
        cv2.setNumThreads(4)  # Điều chỉnh số thread phù hợp với CPU
>>>>>>> origin/main
        self.frame_count = 0
        self.fps = 0
        self.prev_time = time.time()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.title("Pose Detection")
        self.window.geometry("200x150")

        # Tạo các nút
        tk.Button(self.window, text="Mở Webcam", command=self.start_webcam).pack(pady=10)
        tk.Button(self.window, text="Mở Video", command=self.open_video).pack(pady=10)
        tk.Button(self.window, text="Thoát", command=self.stop).pack(pady=10)

    def start_webcam(self):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(0)
        self.start_detection()

    def open_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if self.cap is not None:
                self.cap.release()
            self.cap = cv2.VideoCapture(file_path)
            self.start_detection()

    def start_detection(self):
        self.is_running = True
        # Chạy detection trong thread riêng
        threading.Thread(target=self.run_detection, daemon=True).start()

    def calculate_fps(self):
        self.frame_count += 1
        if self.frame_count % 30 == 0:  # Cập nhật FPS mỗi 30 frame
            current_time = time.time()
            self.fps = 30 / (current_time - self.prev_time)
            self.prev_time = current_time

    def run_detection(self):
        while self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Giảm kích thước frame để tăng tốc độ xử lý
            scale = 0.5
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

            # Thực hiện detection
            results = self.model(small_frame, verbose=False)

            # Vẽ kết quả
            output_frame = results[0].plot()

            # Phóng to lại kích thước gốc
            output_frame = cv2.resize(output_frame, (frame.shape[1], frame.shape[0]))

            # Tính và hiển thị FPS
            self.calculate_fps()
            cv2.putText(output_frame, f"FPS: {int(self.fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Hiển thị frame
            cv2.imshow("Pose Detection", output_frame)

            # Thoát nếu nhấn 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Dọn dẹp
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self.window.quit()

    def run(self):
        self.window.mainloop()

<<<<<<< HEAD
=======

>>>>>>> origin/main
if __name__ == "__main__":
    detector = PoseDetector()
    detector.run()