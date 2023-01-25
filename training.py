
import faceRecognition as fr



faces,faceID=fr.labels_for_training_data('trainingImages')
face_recognizer=fr.train_classifier(faces,faceID)
face_recognizer.write('trainingData.yml')







