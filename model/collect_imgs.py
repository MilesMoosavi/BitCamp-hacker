from app.gui.fields import *
import os
import cv2

sign_labels = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I',
    9: 'K', 10: 'L', 11: 'M', 12: 'N', 13: 'O', 14: 'P', 15: 'Q', 16: 'R',
    17: 'S', 18: 'T', 19: 'U', 20: 'V', 21: 'W', 22: 'X', 23: 'Y'
}

DATA_DIR = './model/data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)
for j in range(0,len(sign_labels)):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print(f'Collecting data for {sign_labels[j]}')

    for k in range(2):
        hand = 'left' if k == 0 else 'right'

        while True:
            ret, frame = cap.read()
            cv2.putText(frame, f'Press Spacebar to sign "{sign_labels[j]}" for {hand} hand', (0, 50), font, 1.75, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord(' '): # frames per millsecond
                break

        counter = 0
        
        while counter < dataset_size/2:
            ret, frame = cap.read()
            cv2.putText(frame, f'Collected  {(dataset_size//2)*k + counter}/{dataset_size} for "{sign_labels[j]}"', (50, 50), font, 1.25, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            cv2.waitKey(delay_between_data_captures) # milliseconds delay per sign
            cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)
            counter += 1

cap.release()
cv2.destroyAllWindows()
