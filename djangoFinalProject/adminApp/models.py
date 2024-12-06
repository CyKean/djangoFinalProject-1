from django.db import models

class SoilData(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    soilpH = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'soil_data'
        app_label = 'adminApp'

    def __str__(self):
        return f"Soil Data {self.id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

# Remove the Prediction model since we're using a single table
# If you need prediction functionality, use the SoilData model

class Predicted(models.Model):
    soil_data = models.ForeignKey(SoilData, on_delete=models.CASCADE)
    predicted_crops = models.JSONField()  # Store crop prediction details (could be a list of dictionaries)
    prediction_datetime = models.DateTimeField()  # Store the datetime when prediction was made

    class Meta:
        db_table = 'predicted_crop'
        app_label = 'adminApp'

    def __str__(self):
        return f"Prediction for Soil Data ID {self.soil_data.id} at {self.prediction_datetime}"