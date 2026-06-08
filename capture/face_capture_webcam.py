import cv2
import numpy as np
import os
import re


def cadastro(person_name: str):
    from recognition.train_recognizers import treino
    from utils.helper_functions import resize_video

    detector = "haarcascade"
    max_width = 800
    max_samples = 10
    starting_sample_number = 0

    def parse_name(name):
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", "_", name)
        return name

    def create_folders(final_path, final_path_full):
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        if not os.path.exists(final_path_full):
            os.makedirs(final_path_full)

    def detect_face(face_detector, orig_frame):
        frame = orig_frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.1, 5)
        face_roi = None
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            face_roi = orig_frame[y : y + h, x : x + w]
            face_roi = cv2.resize(face_roi, (140, 140))
        return face_roi, frame

    def detect_face_ssd(network, orig_frame, show_conf=True, conf_min=0.7):
        frame = orig_frame.copy()
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0)
        )
        network.setInput(blob)
        detections = network.forward()
        face_roi = None
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_min:
                bbox = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                start_x, start_y, end_x, end_y = bbox.astype("int")
                if start_x < 0 or start_y < 0 or end_x > w or end_y > h:

                    continue

                face_roi = orig_frame[start_y:end_y, start_x:end_x]
                face_roi = cv2.resize(face_roi, (90, 120))
                cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                if show_conf:
                    text_conf = "{:.2f}%".format(confidence * 100)
                    cv2.putText(
                        frame,
                        text_conf,
                        (start_x, start_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2,
                    )

        return face_roi, frame

    if detector == "ssd":
        network = cv2.dnn.readNetFromCaffe(
            "deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel"
        )
    else:
        face_detector = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

    cam = cv2.VideoCapture(0)
    folder_faces = "dataset/"
    folder_full = "dataset_full/"
    person_name = parse_name(person_name)
    final_path = os.path.sep.join([folder_faces, person_name])
    final_path_full = os.path.sep.join([folder_full, person_name])
    print("All photos are going to be saved in {}".format(final_path))
    create_folders(final_path, final_path_full)
    sample = 0
    try:
        if not cam.isOpened():
            print("Error: camera not accessible")
            return False

        user_closed = False

        while True:
            ret, frame = cam.read()
            if not ret or frame is None:
                print("Error: failed to read frame from camera")
                return False
            if max_width is not None:
                video_width, video_height = resize_video(
                    frame.shape[1], frame.shape[0], max_width
                )
                frame = cv2.resize(frame, (video_width, video_height))
            if detector == "ssd":
                face_roi, processed_frame = detect_face_ssd(network, frame)
            else:
                face_roi, processed_frame = detect_face(face_detector, frame)

            # show the face ROI window when available
            if face_roi is not None:
                cv2.imshow("face", face_roi)

            # show the main capturing window
            cv2.imshow("Capturing face", processed_frame)

            # check for keypress; allow 'q' to capture
            key = cv2.waitKey(1)
            if face_roi is not None and (key & 0xFF) == ord("q"):
                sample = sample + 1
                photo_sample = (
                    sample + starting_sample_number - 1
                    if starting_sample_number > 0
                    else sample
                )
                image_name = person_name + "." + str(photo_sample) + ".jpg"
                cv2.imwrite(final_path + "/" + image_name, face_roi)
                cv2.imwrite(final_path_full + "/" + image_name, frame)
                print("=> photo " + str(sample))

            # detect if user closed the capturing window via the X button
            try:
                visible = cv2.getWindowProperty("Capturing face", cv2.WND_PROP_VISIBLE)
            except Exception:
                visible = 0

            if visible < 1:
                print("User closed the capture window.")
                user_closed = True
                break

            if sample >= max_samples:
                break

        if user_closed:
            return False

        print("Completed!")
        treino()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        try:
            cam.release()
        except:
            pass
        cv2.destroyAllWindows()
