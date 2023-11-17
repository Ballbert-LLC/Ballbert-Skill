import base64
import threading
import zlib
from Hal.Classes import Response
from Hal.Decorators import reg
from Hal.Skill import Skill
from Hal import initialize_assistant

from Event_Handler import event_handler

import speech_recognition as sr

assistant = initialize_assistant()


class Ballbert(Skill):
    def __init__(self):
        super().__init__()
        self.recogniser = sr.Recognizer()

        self.setup_routes()

    def setup_routes(self):
        #Websocket Rotues
        
        def sentament(sentament : str):
            event_handler.trigger("sentament", sentament)
        
        assistant.websocket_client.add_route(sentament)
        
        def indecator_bar_color(color : str):
            event_handler.trigger("indecator_bar_color", color)
        
        assistant.websocket_client.add_route(indecator_bar_color)

        def handle_audio(audio):
            if audio == "stop!":
                event_handler.trigger("Audio_End")
                return 
            decoded_compressed_data = base64.b64decode(audio)
            decompressed_frame_data = zlib.decompress(decoded_compressed_data)

            event_handler.trigger("Audio", audio_data=decompressed_frame_data)

        assistant.websocket_client.add_route(handle_audio, "audio")
        

    @reg(name="get_available")
    def get_available(self, double_check=False):
        """
        Checks if the backend is available

        :param boolean double_check: (Optional) If true the code double checks to make sure it is online
        """

        return True
