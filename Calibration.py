import cv2 as cv
import numpy as np
import glob
import os


def solve_distortion_save(video_path, window_name):
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        return

    img_w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    img_h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    img_size = (img_w, img_h)
    fps = cap.get(cv.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 30

    try:
        data = np.load('calibration_result.npz')
        K = data['K']
        D = data['D']
    except:
        K = np.array([[1250, 0, img_w / 2], [0, 1250, img_h / 2], [0, 0, 1]], dtype=np.float64)
        D = np.array([-0.15, 0.03, 0, 0, -0.005], dtype=np.float64)

    new_K, roi = cv.getOptimalNewCameraMatrix(K, D, img_size, alpha=0, newImgSize=img_size)
    map1, map2 = cv.initUndistortRectifyMap(K, D, None, new_K, img_size, cv.CV_16SC2)

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter('output.mp4', fourcc, fps, (img_w * 2, img_h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fixed_img = cv.remap(frame, map1, map2, interpolation=cv.INTER_LINEAR)

        cv.putText(frame, "Original", (40, 80), cv.FONT_HERSHEY_DUPLEX, 2.0, (0, 255, 0), 3)
        cv.putText(fixed_img, "Fixed", (40, 80), cv.FONT_HERSHEY_DUPLEX, 2.0, (0, 255, 0), 3)

        combined = np.hstack((frame, fixed_img))

        out.write(combined)

        display = cv.resize(combined, (img_w, img_h // 2))
        cv.imshow(window_name, display)

        if cv.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    video_list = sorted(glob.glob("origin.mp4"))
    for path in video_list:
        solve_distortion_save(path, f"Lens Correction: {os.path.basename(path)}")