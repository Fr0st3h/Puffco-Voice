import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

url = "http://18f0-96-51-169-147.ngrok.io"

def sendPreheatCommand(temperature, seconds):
    req = requests.get(url+"/preheat?temperature="+temperature+"&seconds="+seconds)
    return req.text

def sendCommand(command, profile):
    req = requests.get(url+"/cmd?command="+command+"&profile="+profile)
    return req.text

def sendConnectionRequest():
    req = requests.get(url)
    return req.text


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to puffco voice. You can say things like, tell my puffco to preheat, or tell my puffco to preheat profile and then a profile number. You can also say preheat my puffco to 280 for 60 seconds."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class ConnectionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ConnectionIntent")(handler_input)

    def handle(self, handler_input):
        try:
            speak_output = sendConnectionRequest()
        except:
            speak_output = "Failed to connect to puffco. You are now ready to use puffco voice"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class PreheatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PreheatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        temp = ask_utils.request_util.get_slot(handler_input, "temperature")
        secs = ask_utils.request_util.get_slot(handler_input, "seconds")
        profile = ask_utils.request_util.get_slot(handler_input, "number")
        if(temp.value):
            speak_output = sendPreheatCommand(temp.value, secs.value)
        else:
            if(profile.value):
                speak_output = sendCommand("preheat", profile.value)
            else:
                speak_output = sendCommand("preheat", "")
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say things like, tell my puffco to preheat, or tell my puffco to preheat profile and then a profile number. You can also say, for example, preheat my puffco to 280 for 60 seconds."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speak = "You can say things like, tell my puffco to preheat, or tell my puffco to preheat profile and then a profile number. You can also say, for example, preheat my puffco to 280 for 60 seconds."
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ConnectionIntentHandler())
sb.add_request_handler(PreheatIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()