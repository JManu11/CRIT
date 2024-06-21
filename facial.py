import face_recognition
import cv2
import numpy as np

def register_face():
    video_capture = cv2.VideoCapture(0)
    print("Por favor, coloca tu cara frente a la cámara y presiona 'q' para capturar la imagen.")

    while True:
        ret, frame = video_capture.read()
        cv2.imshow('Video', frame)

        # Presiona 'q' para capturar la imagen y registrar la cara
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("registered_face.jpg", frame)
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Cargar la imagen y codificar la cara
    registered_image = face_recognition.load_image_file("registered_face.jpg")
    registered_face_encoding = face_recognition.face_encodings(registered_image)[0]

    # Guardar la codificación de la cara registrada
    np.save("registered_face_encoding.npy", registered_face_encoding)
    print("Registro completo. La codificación de la cara ha sido guardada.")

def verify_face():
    # Cargar la codificación de la cara registrada
    registered_face_encoding = np.load("registered_face_encoding.npy")

    # Inicializar la captura de video
    video_capture = cv2.VideoCapture(0)
    print("Por favor, coloca tu cara frente a la cámara para verificar tu identidad.")

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]

        # Encontrar todas las caras en el frame actual
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([registered_face_encoding], face_encoding)
            if True in matches:
                print("Acceso Concedido")
            else:
                print("Acceso Denegado")

        cv2.imshow('Video', frame)

        # Presiona 'q' para salir del loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Registrar la cara (comentar esta línea si ya has registrado la cara)
register_face()

# Verificar la cara para el login
verify_face()
