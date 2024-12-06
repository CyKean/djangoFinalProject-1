from django.shortcuts import render
from django.utils import timezone
from .models import SoilData  # Import the SoilData model
from adminApp.models import Predicted
from django.http import JsonResponse
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model

def prediction(request):
    prediction_result = None
    
    # Fetch the latest soil data
    latest_soil_data = SoilData.objects.latest('timestamp')
    
    if request.method == 'POST':
        # Add your prediction logic here
        field1 = request.POST.get('field1')
        field2 = request.POST.get('field2')
        # Process the prediction
        prediction_result = "Sample prediction result"
    
    context = {
        'prediction_result': prediction_result,
        'latest_soil_data': latest_soil_data
    }
    
    return render(request, 'userApp/prediction.html', context)


# Load the model when the server starts
model = load_model('userApp/predictor/crop_recommendation_model.h5')

@csrf_exempt
def predict_crop(request):
    if request.method == "POST":
        # Extract form data
        nitrogen = float(request.POST.get('nitrogen'))
        phosphorus = float(request.POST.get('phosphorus'))
        potassium = float(request.POST.get('potassium'))
        ph = float(request.POST.get('ph'))
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))
        soil_data_id = request.POST.get('soil_data_id')  # Get the soil data id

        # Preprocess the data for the model
        input_data = np.array([[nitrogen, phosphorus, potassium, ph, temperature, humidity]])
        
        # Make a prediction
        prediction = model.predict(input_data)
        predicted_indices = prediction[0].argsort()[-3:][::-1]  # Get top 3 crops

        # Map index to crop name
        crop_mapping = {
            0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea', 4: 'coconut',
            5: 'coffee', 6: 'corn', 7: 'cotton', 8: 'grapes', 9: 'jute',
            10: 'kidneybeans', 11: 'lentil', 12: 'maize', 13: 'mango', 14: 'mothbeans',
            15: 'mungbean', 16: 'muskmelon', 17: 'orange', 18: 'papaya', 19: 'pigeonpeas',
            20: 'pineapple', 21: 'pomegranate', 22: 'rice', 23: 'sugarcane', 24: 'watermelon'
        }

        top_crops = []
        for idx in predicted_indices:
            crop_name = crop_mapping.get(idx, "Unknown Crop")
            success_rate = prediction[0][idx] * 100  # Convert to percentage
            top_crops.append({
                'crop_name': crop_name,
                'success_rate': f"{success_rate:.2f}%"
            })

        # Save the prediction result in the Predicted model
        Predicted.objects.create(
            soil_data_id=soil_data_id,  # Associate with the correct soil data
            predicted_crops=top_crops,
            prediction_datetime=timezone.now()
        )

        # Return the top 3 recommended crops as JSON
        return JsonResponse({
            'top_crops': top_crops
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

# @csrf_exempt
# def predict_crop(request):
#     if request.method == "POST":
#         # # Extract form data
#         nitrogen = float(request.POST.get('nitrogen'))
#         phosphorus = float(request.POST.get('phosphorus'))
#         potassium = float(request.POST.get('potassium'))
#         ph = float(request.POST.get('ph'))
#         temperature = float(request.POST.get('temperature'))
#         humidity = float(request.POST.get('humidity'))

#         # Preprocess the data for the model
#         input_data = np.array([[nitrogen, phosphorus, potassium, ph, temperature, humidity]])
        
#         # Make a prediction (Assume 'model' is your trained model)
#         prediction = model.predict(input_data)
#         predicted_indices = prediction[0].argsort()[-3:][::-1]  # Get top 3 crops

#         # Map index to crop name
#         crop_mapping = {
#             0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea', 4: 'coconut',
#             5: 'coffee', 6: 'corn', 7: 'cotton', 8: 'grapes', 9: 'jute',
#             10: 'kidneybeans', 11: 'lentil', 12: 'maize', 13: 'mango', 14: 'mothbeans',
#             15: 'mungbean', 16: 'muskmelon', 17: 'orange', 18: 'papaya', 19: 'pigeonpeas',
#             20: 'pineapple', 21: 'pomegranate', 22: 'rice', 23: 'sugarcane', 24: 'watermelon'
#         }
        
#         top_crops = []
#         for idx in predicted_indices:
#             crop_name = crop_mapping.get(idx, "Unknown Crop")
#             success_rate = prediction[0][idx] * 100  # Convert to percentage
#             top_crops.append({
#                 'crop_name': crop_name,
#                 'success_rate': f"{success_rate:.2f}%"
#             })

#         # Return the top 3 recommended crops as JSON
#         return JsonResponse({
#             'top_crops': top_crops
#         })

#     return JsonResponse({"error": "Invalid request"}, status=400)
