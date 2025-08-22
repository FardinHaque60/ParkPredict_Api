import logging
from fastapi import APIRouter
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Request, Response
import re
from datetime import datetime, timedelta, timezone
from app.utils.lib import get_minutes_from_week_start
from app.ml_models.load_models import get_model_helper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
model_helper = get_model_helper()

MESSAGE_FORMATS = '''\n\nq - quick predictions, gives parking garage predictions for the next 30 mins, 1 hr, and 2 hrs\n
p HH:MM AM/PM - returns the predictions for a given time, example: p 10:34 AM\n\nhello - enter "hello" to see this message again
\ncheck out https://sjsuparkpredict.vercel.app/ if you'd prefer a web version!'''

# top level reply method that is called
@router.post("/reply")
async def reply_sms(request: Request):
    form = await request.form()
    logger.info(f"REQ sms: {form}")
    req = form.get("Body")

    response_obj = MessagingResponse()
    try:
        response = generate_response(req)

        response_obj.message(response)
        logger.info(f"RESP sms: {response_obj}")
    except:
        response_obj.message("Error generating response, try again later")
        return Response(content=str(response_obj), media_type="application/xml")

    return Response(content=str(response_obj), media_type="application/xml")

def generate_response(req):
    req = req.strip().lower().split(" ")

    if (req[0] == "q"):
        # Get minutes from week start
        pacific = timezone(timedelta(hours=-7))
        timestamp = datetime.now(pacific)
        minutes = get_minutes_from_week_start(timestamp)
        
        # Make predictions
        start_time = datetime.now()
        predictions = {}
        for interval in [30, 60, 120]:  # 30 mins, 1 hour, 2 hours    
            predictions[interval] = model_helper.production_model(minutes + interval)
        end_time = datetime.now()
        logger.info(f"predictions: {predictions}")
        
        # return prediction object
        prediction_time = round((end_time - start_time).total_seconds(), 4)
        logger.info(f"prediction elapsed time (s): {prediction_time}")

        response = f'''Parking Garage Predictions:
        
In the next 30 mins:
- North Garage: {predictions[30]["North Garage"]}%
- West Garage:  {predictions[30]["West Garage"]}%
- South Garage: {predictions[30]["South Garage"]}%

In the next 1 hr:
- North Garage: {predictions[60]["North Garage"]}%
- West Garage:  {predictions[60]["West Garage"]}%
- South Garage: {predictions[60]["South Garage"]}%

In the next 2 hrs:
- North Garage: {predictions[120]["North Garage"]}%
- West Garage:  {predictions[120]["West Garage"]}%
- South Garage: {predictions[120]["South Garage"]}%'''
        return response
    elif (req[0] == "p"):
        time_pattern = r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$"
        if len(req) > 2:
            time_str = f"{req[1]} {req[2]}"
            if re.match(time_pattern, time_str):
                # Get minutes from week start
                timestamp = datetime.strptime(time_str, "%I:%M %p")
                minutes = get_minutes_from_week_start(timestamp)
                
                # Make prediction
                start_time = datetime.now()
                predictions = model_helper.production_model(minutes)
                end_time = datetime.now()
                logger.info(f"prediction: {predictions}")
                
                # return prediction object
                prediction_time = round((end_time - start_time).total_seconds(), 4)
                logger.info(f"prediction elapsed time: {prediction_time}")

                response = f'''Parking Garage Predictions at {time_str}:

North Garage: {predictions["North Garage"]}%
West Garage:  {predictions["West Garage"]}%
South Garage: {predictions["South Garage"]}%'''

                return response
        return "Please provide a time in the format HH:MM AM/PM (e.g., p 10:34 AM)."
    elif (req[0] == "hello"):
        return f"Welcome to the SJSU park predict sms service! Message me in the following formats to get started: {MESSAGE_FORMATS}"
    else:
        return f"Hmm, don't think I know that one, reference the message formats and try again: {MESSAGE_FORMATS}"