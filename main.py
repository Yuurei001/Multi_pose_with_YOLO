import cv2
import time
from ultralytics import YOLO

# Tải mô hình YOLOv8 phiên bản pose
model = YOLO('yolov8n-pose.pt')  # Sử dụng mô hình YOLOv8 cho pose detection

# Khởi động webcam
cap = cv2.VideoCapture(0)  # Sử dụng webcam, nếu bạn có nhiều webcam, bạn có thể thay 0 bằng 1, 2,...

prev_time = 0  # Thời gian khung hình trước

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Không thể lấy khung hình từ webcam")
        break

    # Phát hiện pose và bounding box
    results = model(frame)

    # Vẽ bounding box và keypoints
    annotated_frame = results[0].plot()

    # Tính toán FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Hiển thị FPS trên khung hình
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị kết quả
    cv2.imshow("Pose Detection", annotated_frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng webcam và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
