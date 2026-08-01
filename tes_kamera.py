import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Kamera tidak bisa dibuka")
    raise SystemExit

print("Tekan q untuk keluar")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame")
        break

    cv2.imshow("Test Kamera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()