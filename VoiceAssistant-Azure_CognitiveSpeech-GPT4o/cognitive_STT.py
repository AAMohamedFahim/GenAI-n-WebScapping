import azure.cognitiveservices.speech as speechsdk
import os 
from dotenv import load_dotenv

load_dotenv()

def STT():
    
    speech_config = speechsdk.SpeechConfig(subscription=os.environ['Cognitive_Speech'], region=os.environ['region'])


    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")

    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            cancellation_details = result.cancellation_details
            return(f"Speech Recognition canceled: {cancellation_details.reason}\nError details: {cancellation_details.error_details}")
        else:
            cancellation_details = result.cancellation_details
            return("Speech Recognition canceled: {}".format(cancellation_details.reason))
            