from django.shortcuts import render
from .models import SoilData  # Import the SoilData model

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