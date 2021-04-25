from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
import joblib
import pickle

from DiseasePredictor import handleDb
from .serializers import FourInputDiabetes, EightInputDiabetes

# 8 input models
rf_normal_8ip = joblib.load('models/diabetes/8input/randomForest(Normal).pkl')
rf_unskewed_8ip = joblib.load('models/diabetes/8input/randomForest(unskewed).pkl')
knn_8ip = joblib.load('models/diabetes/8input/knn(unskewed).pkl')

# 4 input models
gbm_4ip = joblib.load('models/diabetes/4input/GBM(unskewed+standardised).pkl')
rf_std_4ip = joblib.load('models/diabetes/4input/randomForest(standardised).pkl')
rf_unskewed_4ip = joblib.load('models/diabetes/4input/randomForest(unskewed+standardised).pkl')
knn_4ip = joblib.load('models/diabetes/4input/KNN(unskewed+standardised).pkl')

class DiabetesViewSet(viewsets.ViewSet):
	"""
	A simple ViewSet for predicting diabetes.
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
			isDataSaved = handleDb.addDiabatesRecord(uid, serializer.data, result)

			# return result to frontend
			if isDataSaved:
				return Response(result, status = status.HTTP_200_OK)

			# user not registered
			return Response("User not registered.", status = status.HTTP_401_UNAUTHORIZED)

		return Response('Incomplete data', status = status.HTTP_400_BAD_REQUEST)

	def eightInput(self, request):
		# get user identification number
		uid = request.GET.get('uid', '')
		if uid == '':
			return Response('No UID provided.', status = status.HTTP_400_BAD_REQUEST)

		# convert data to serializer
		serializer = EightInputDiabetes(data = request.data)

		# check if data is valid
		if (serializer.is_valid()):
			seq = [
				serializer.data['pregnancies'],
				serializer.data['glucose'],
				serializer.data['bp'],
				serializer.data['skin_thickness'],
				serializer.data['insulin'],
				serializer.data['bmi'],
				serializer.data['dp_function'],
				serializer.data['age']
			]

			# prediction according to different models
			rf_normal_outcome = rf_normal_8ip.predict([seq])
			rf_unskewed_outcome = rf_unskewed_8ip.predict([seq])
			knn_outcome = knn_8ip.predict([seq])
			ones = [rf_normal_outcome[0], rf_unskewed_outcome[0], knn_outcome[0]].count(1)

			# storing as json
			result = {
				"RandomForestNormal": rf_normal_outcome[0],
				"RandomForestUnskewed": rf_unskewed_outcome[0],
				"KNNUnskewed": knn_outcome[0],
				"Ones": ones
			}

			# save to database in past record
			isDataSaved = handleDb.addDiabatesRecord(uid, serializer.data, result)

			# return result to frontend
			if isDataSaved:
				return Response(result, status = status.HTTP_200_OK)

			# user not registered
			return Response("User not registered.", status = status.HTTP_401_UNAUTHORIZED)

		return Response('Incomplete data', status = status.HTTP_400_BAD_REQUEST)


"""
{
	"glucose": 1,
	"bmi": 2,
	"dp_function": 3,
	"age": 4
}

{
	"pregnancies": 1,
	"glucose": 1,
	"bp": 2,
	"skin_thickness": 5,
	"insulin": 6,
	"bmi": 2,
	"dp_function": 3,
	"age": 4
}
"""