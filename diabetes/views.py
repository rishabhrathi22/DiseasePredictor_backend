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
		serializer = FourInputDiabetes(data = request.data)
		if (serializer.is_valid()):
			seq = [
					serializer.data['glucose'],
					serializer.data['bmi'],
					serializer.data['dp_function'],
					serializer.data['age']
				]

			gbm_outcome = gbm_4ip.predict([seq])
			rf_std_outcome = rf_std_4ip.predict([seq])
			rf_unskewed_outcome = rf_unskewed_4ip.predict([seq])
			knn_outcome = knn_4ip.predict([seq])

			result = {
				"GBM": gbm_outcome[0],
				"RandomForestNormal": rf_std_outcome[0],
				"RandomForestUnskewed": rf_unskewed_outcome[0],
				"KNNUnskewed": knn_outcome[0]
			}

			return Response(result, status = status.HTTP_200_OK)

		return Response('Incomplete data', status = status.HTTP_400_BAD_REQUEST)

	def eightInput(self, request):
		serializer = EightInputDiabetes(data = request.data)
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

			rf_normal_outcome = rf_normal_8ip.predict([seq])
			rf_unskewed_outcome = rf_unskewed_8ip.predict([seq])
			knn_outcome = knn_8ip.predict([seq])

			result = {
				"RandomForestNormal": rf_normal_outcome[0],
				"RandomForestUnskewed": rf_unskewed_outcome[0],
				"KNNUnskewed": knn_outcome[0]
			}

			return Response(result, status = status.HTTP_200_OK)

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

# def index(request):
# 	return render(request,'index.html')

# def predict(request):
# 	sentence = [request.POST.get('sentence')]                   # get the sentence
# 	# sentence_trans = cv.transform(sentence).toarray()           # transform the sentence
# 	# prediction = model.predict(sentence_trans)[0]               # get the prediction
# 	prediction = 1
# 	user_input = sentence[0]
# 	context = {'result':prediction,'sentence':user_input}
# 	return render(request,'result.html',context)