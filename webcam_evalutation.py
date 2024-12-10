# 1) load the model
from tensorflow import keras
model = keras.models.load_model('model/blink_mobilenetv3_finetuned_ariel4.keras')


import cv2

def __draw_label(img, text, pos, bg_color):
   font_face = cv2.FONT_HERSHEY_SIMPLEX
   scale = 0.7
   color = (255, 255, 255)
   thickness = cv2.FILLED
   margin = 3
   txt_size = cv2.getTextSize(text, font_face, scale, thickness)

   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin

   cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
   cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

# Open the device at the ID 0
# Use the camera ID based on
# /dev/videoID needed
cap = cv2.VideoCapture(0)

#Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")

# 2) fetch one frame at a time from your camera
while(True):
    
    # frame is a numpy array, that you can predict on 
    ret, frame = cap.read()
    frame_show = frame
    # 3) obtain the prediction
    # depending on your model, you may have to reshape frame
    frame = cv2.resize(frame, (224, 224))
    frame_tensor = frame.reshape(1, 224, 224, 3)
    prediction = model(frame_tensor, training=False)
    # you may need then to process prediction to obtain a label of your data, depending on your model. Probably you'll have to apply an argmax to prediction to obtain a label.
    
    # 4) Adding the label on your frame
    __draw_label(frame_show, 'Label: {}'.format(prediction), (20,20), (255,0,0))

    # 5) Display the resulting frame
    cv2.imshow("preview",frame_show)
   
    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()