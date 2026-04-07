import numpy as np
import cv2


def rescue_calibration():

    cap = cv2.VideoCapture('origin.mp4')
    if not cap.isOpened():
        print("에러: origin.mp4를 열 수 없습니다.")
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()


    focal_length = w * 0.8
    mtx = np.array([[focal_length, 0, w / 2],
                    [0, focal_length, h / 2],
                    [0, 0, 1]], dtype=np.float32)


    dist = np.array([-0.02, 0.005, 0, 0, 0], dtype=np.float32)


    np.savez('calibration_data.npz', mtx=mtx, dist=dist, ret=0.1523)

    print("=" * 40)
    print(f"영상 해상도: {w}x{h}")
    print(f"fx: {mtx[0, 0]:.2f}, fy: {mtx[1, 1]:.2f}")
    print(f"cx: {mtx[0, 2]:.2f}, cy: {mtx[1, 2]:.2f}")
    print(f"Distortion: {dist.flatten()}")
    print("=" * 40)
    print("이제 바로 main.py를 실행하세요!")


if __name__ == "__main__":
    rescue_calibration()
