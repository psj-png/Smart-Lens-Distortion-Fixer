import cv2
import numpy as np
import os


class LensDistortionFixer:
    def __init__(self, calib_file, input_vid, output_vid):
        self.calib_file = calib_file
        self.input_vid = input_vid
        self.output_vid = output_vid
        self.mtx, self.dist = self._load_parameters()

    def _load_parameters(self):
        if not os.path.exists(self.calib_file):
            print(f"[!] 시스템 에러: '{self.calib_file}' 파일을 먼저 생성해주세요.")
            exit()

        saved_data = np.load(self.calib_file)
        print(f"[*] 캘리브레이션 데이터 로드 완료.")
        return saved_data['mtx'], saved_data['dist']

    def run_correction(self):
        video_stream = cv2.VideoCapture(self.input_vid)

        if not video_stream.isOpened():
            print(f"[!] 시스템 에러: '{self.input_vid}' 영상을 찾을 수 없습니다.")
            return

        cam_width = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        cam_height = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_fps = video_stream.get(cv2.CAP_PROP_FPS)
        total_frames = int(video_stream.get(cv2.CAP_PROP_FRAME_COUNT))

        # [요청사항 반영] 20%, 40%, 60%, 80% 구간에서 스냅샷 저장
        snapshot_points = [int(total_frames * ratio) for ratio in (0.20, 0.40, 0.60, 0.80)]
        shot_count = 0

        codec = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(self.output_vid, codec, video_fps, (cam_width * 2, cam_height))

        optimal_mtx, _ = cv2.getOptimalNewCameraMatrix(
            self.mtx, self.dist, (cam_width, cam_height), 0, (cam_width, cam_height)
        )

        print("[*] 비디오 왜곡 보정 프로세스를 시작합니다...")
        current_idx = 0

        while True:
            success, frame = video_stream.read()
            if not success:
                break

            fixed_frame = cv2.undistort(frame, self.mtx, self.dist, None, optimal_mtx)
            comparison_view = cv2.hconcat([frame, fixed_frame])

            cv2.putText(comparison_view, 'Origin', (40, 60),
                        cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(comparison_view, 'Fixed', (cam_width + 40, 60),
                        cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0), 2)

            # demo1.jpg ~ demo4.jpg까지 생성됩니다.
            if current_idx in snapshot_points:
                shot_count += 1
                cv2.imwrite(f'demo{shot_count}.jpg', comparison_view)

            writer.write(comparison_view)

            display_screen = cv2.resize(comparison_view, (cam_width, cam_height // 2))
            cv2.imshow('Lens Correction Result', display_screen)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            current_idx += 1

        video_stream.release()
        writer.release()
        cv2.destroyAllWindows()
        print(f"[*] 프로세스 종료. 결과 영상: {self.output_vid}")


if __name__ == "__main__":
    app = LensDistortionFixer(
        calib_file='calibration_data.npz',
        input_vid='origin.mp4',
        output_vid='output.mp4'
    )
    app.run_correction()