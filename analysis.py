import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """ 3点(a, b, c)の角度を計算 """
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine_angle))
    return angle

def process_video(video_path, arm_side, mode):
    """ 動画を解析し、関節角度を計算 """
    cap = cv2.VideoCapture(video_path)
    output_path = video_path.replace("uploaded_video", "processed_video")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    angles_data = []
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                if arm_side == "右腕":
                    shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                    hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                else:
                    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                
                if mode == "肩関節外転":
                    angle = calculate_angle((hip.x, hip.y), (shoulder.x, shoulder.y), (elbow.x, elbow.y))
                else:  # 肩関節屈曲
                    angle = calculate_angle((shoulder.x, shoulder.y), (elbow.x, elbow.y), (hip.x, hip.y))
                
                angles_data.append(angle)
                
                cv2.putText(frame, f"Angle: {int(angle)} deg", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            out.write(frame)
    
    cap.release()
    out.release()
    return output_path, angles_data

def get_maximum_range_of_motion(angles_data):
    """ 最大可動域（ROM）を算出 """
    if len(angles_data) == 0:
        return 0
    return max(angles_data) - min(angles_data)

