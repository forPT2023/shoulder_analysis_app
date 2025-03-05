import streamlit as st
import os
import analysis
import visualization

# 保存ディレクトリ
SAVE_DIR = "saved_results"
os.makedirs(SAVE_DIR, exist_ok=True)

# Streamlit UI
st.title("肩関節解析アプリ（外転・屈曲）")

# 動作モード選択（外転 or 屈曲）
mode = st.radio("解析モードを選択", ("肩関節外転", "肩関節屈曲"))

# 解析する腕（右 or 左）
arm_side = st.radio("解析する腕を選択", ("右腕", "左腕"))

# 動画アップロード
uploaded_file = st.file_uploader("動画をアップロード", type=["mp4", "avi", "mov"])

if uploaded_file:
    video_path = os.path.join(SAVE_DIR, "uploaded_video.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.write("動画を解析中...")
    output_video_path, angles_data = analysis.process_video(video_path, arm_side, mode)

    max_rom = analysis.get_maximum_range_of_motion(angles_data)
    st.write(f"最大可動域（ROM）: {max_rom:.2f}°")

    fig = visualization.plot_joint_angles(angles_data)
    st.pyplot(fig)

    st.video(output_video_path)

