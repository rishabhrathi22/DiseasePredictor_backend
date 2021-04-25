from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status

import base64

from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2

from DiseasePredictor import handleDb
from .serializers import PneumoniaSerializer

model = load_model("models/pneumonia/PneumoniaClassifier.h5")
# model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

class PneumoniaViewSet(viewsets.ViewSet):
	default_serializer_class = PneumoniaSerializer

	def saveBase64Image(self, base64Image):
		try:
			imgFormat, imgStr = base64Image.split(';base64,')
			ext = imgFormat.split('/')[-1]
			imgName = "pneumonia/testImage." + ext

			with open(imgName, "wb") as fh:
				fh.write(base64.decodebytes(bytes(imgStr, 'utf-8')))

			return imgName

		except Exception as e:
			print(e)
			return None

	def predict(self, request):
		# get user identification number
		uid = request.GET.get('uid', '')
		if uid == '':
			return Response('No UID provided.', status = status.HTTP_400_BAD_REQUEST)

		# convert data to serializer
		serializer = PneumoniaSerializer(data = request.data)

		# check if data is valid
		if (serializer.is_valid()):
			base64Image = serializer.data['base64Image']
			imgName = self.saveBase64Image(base64Image)

			if imgName == None:
				return Response("Error in image", status = status.HTTP_400_BAD_REQUEST)

			img_size = 150
			img_arr = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
			resized_arr = cv2.resize(img_arr, (img_size, img_size))
			# Normalize the data
			resized_arr = np.array(resized_arr) / 255
			resized_arr = resized_arr.reshape(-1, img_size, img_size, 1)

			# predict the result
			prediction = model.predict_classes(resized_arr).reshape(1, -1)[0][0]
			accuracy = model.predict(resized_arr).reshape(1, -1)[0][0]
			result = {
				"Prediction": 1-prediction,
				"Accuracy": accuracy
			}

			# save to database in past record
			isDataSaved = handleDb.addPneumoniaRecord(uid, base64Image, result)

			# return result to frontend
			if isDataSaved:
				return Response(result, status = status.HTTP_200_OK)

			# user not registered
			return Response("User not registered.", status = status.HTTP_401_UNAUTHORIZED)

		return Response('Incomplete data', status = status.HTTP_400_BAD_REQUEST)

	"""
	A simple ViewSet for predicting diabetes.
	"""

	"""
	serializer_classes = {
		'fourInput': FourInputDiabetes,
		'eightInput': EightInputDiabetes,
	}
	default_serializer_class = EightInputDiabetes

	def get_serializer_class(self):
		return self.serializer_classes.get(self.action, self.default_serializer_class)

	def fourInput(self, request):
		# get user identification number
		uid = request.GET.get('uid', '')
		if uid == '':
			return Response('No UID provided.', status = status.HTTP_400_BAD_REQUEST)

		# convert data to serializer
		serializer = FourInputDiabetes(data = request.data)
		# check if data is valid
		if (serializer.is_valid()):
			seq = [
				serializer.data['glucose'],
				serializer.data['bmi'],
				serializer.data['dp_function'],
				serializer.data['age']
			]

			# prediction according to different models
			gbm_outcome = gbm_4ip.predict([seq])
			rf_std_outcome = rf_std_4ip.predict([seq])
			rf_unskewed_outcome = rf_unskewed_4ip.predict([seq])
			knn_outcome = knn_4ip.predict([seq])
			ones = [gbm_outcome[0], rf_std_outcome[0], rf_unskewed_outcome[0], knn_outcome[0]].count(1)

			# storing as json
			result = {
				"GBM": gbm_outcome[0],
				"RandomForestNormal": rf_std_outcome[0],
				"RandomForestUnskewed": rf_unskewed_outcome[0],
				"KNNUnskewed": knn_outcome[0],
				"Ones": ones
			}

			# save to database in past record
			isDataSaved = handleDb.addDiabatesRecord(uid, result)

			# return result to frontend
			if isDataSaved:
				return Response(result, status = status.HTTP_200_OK)

			# user not registered
			return Response("User not registered.", status = status.HTTP_401_UNAUTHORIZED)

		return Response('Incomplete data', status = status.HTTP_400_BAD_REQUEST)
	"""