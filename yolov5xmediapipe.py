import tkinter as tk
from tkinter import filedialog, Label
import cv2
from ultralytics import YOLO
import mediapipe as mp
from PIL import Image, ImageTk

# Khởi tạo mô hình YOLO
yolo_model = YOLO('yolov5su.pt')

# Khởi tạo Mediapipe Pose và Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def process_video(video_path):
    # Mở tệp video
    cap = cv2.VideoCapture(video_path)

    # Khởi tạo Mediapipe Pose
    pose = mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3)

    # Khởi tạo VideoWriter để ghi video kết quả
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, size)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển đổi từ BGR sang RGB cho Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Dự đoán bằng YOLO model, chỉ lấy kết quả phát hiện người
        results = yolo_model(image, classes=[0])  # 0 là class index của người

        # Chuyển đổi ảnh từ RGB sang BGR để hiển thị
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Xử lý pose trên các vùng bounding box
        img_list = []
        MARGIN = 10
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                pose_results = pose.process(image[y1 + MARGIN:y2 + MARGIN, x1 + MARGIN:x2 + MARGIN])
                if pose_results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image[y1 + MARGIN:y2 + MARGIN, x1 + MARGIN:x2 + MARGIN],
                        pose_results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS
                    )
                img_list.append(image[y1:y2, x1:x2])

        # Ghi video kết quả
        out.write(image)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def open_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if video_path:
        process_video(video_path)
        display_frames(video_path)


def display_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    # Hiển thị một vài frame đầu
    for _ in range(10):
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển đổi frame từ OpenCV sang định dạng của Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        label = Label(root, image=img_tk)
        label.image = img_tk  # Giữ tham chiếu để ảnh không bị xóa
        label.pack()

    cap.release()


# Khởi tạo ứng dụng Tkinter
root = tk.Tk()
root.title("Multi-Person Pose Detection App")

# Nút để tải video
upload_button = tk.Button(root, text="Upload Video", command=open_video)
upload_button.pack()

root.mainloop()