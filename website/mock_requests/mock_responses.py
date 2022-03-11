
from website.models import MoodTypes, ReturnStatus, update_mood_table

def get_api_cell_response(user_name, location, mood, location_name):
    if not user_name or not location or not mood:
        return ReturnStatus.ERROR
    
    if mood not in MoodTypes().mood_types.values():
        return ReturnStatus.ERROR
        
    payload = {
        'user_name': user_name,
        'location': location,
        'mood': mood,
        'registered_name_location': location_name,
    }

    response = update_mood_table(payload)

    return response