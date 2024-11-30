from django.shortcuts import render
from adminApp.models import SoilData  # Import SoilData from adminApp

def prediction(request):
    prediction_result = None
    
    # Fetch the latest soil data
    try:
        latest_soil_data = SoilData.objects.latest('timestamp')
    except SoilData.DoesNotExist:
        latest_soil_data = None
    
    context = {
        'prediction_result': prediction_result,
        'latest_soil_data': latest_soil_data
    }
    
    return render(request, 'userApp/prediction.html', context)