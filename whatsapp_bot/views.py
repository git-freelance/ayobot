import os
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import json
import openai
from .models import WhatsAppConversation
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


# Configuration (move to environment variables in production)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MESSAGING_SERVICE_SID = os.getenv("MESSAGING_SERVICE_SID")

# Initialize clients
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

class ConversationHandler:
    def __init__(self, wa_id: str, from_number: str, incoming_message: str, btn_payload: Optional[str] = None):
        self.wa_id = wa_id
        self.from_number = from_number
        self.incoming_message = incoming_message.lower()
        self.btn_payload = btn_payload
        self.last_conversation = self._get_last_conversation()

    def _get_last_conversation(self) -> Optional[WhatsAppConversation]:
        return WhatsAppConversation.objects.filter(
            wa_id=self.wa_id
        ).order_by('-created_at').first()

    def get_message_by_content_sid(self, content_sid: str) -> Optional[str]:
        conversation = WhatsAppConversation.objects.filter(
            wa_id=self.wa_id,
            content_sid=content_sid
        ).order_by('-created_at').first()
        return conversation.message if conversation else None

    def send_message(self, content_sid: Optional[str] = None, body: Optional[str] = None) -> Any:
        """Send message via Twilio"""
        try:
            message_params = {
                "to": self.from_number,
                "from_": TWILIO_PHONE_NUMBER,
            }
            
            if content_sid:
                message_params.update({
                    "content_sid": content_sid,
                    "content_variables": json.dumps({"1": "Name"}),
                    "messaging_service_sid": MESSAGING_SERVICE_SID,
                })
            else:
                message_params["body"] = body
                
            return client.messages.create(**message_params)
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise

    def save_conversation(self, response: str, content_sid: str) -> None:
        """Save conversation to database"""
        try:
            WhatsAppConversation.objects.create(
                wa_id=self.wa_id,
                message=self.incoming_message,
                response=response,
                content_sid=content_sid
            )
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            raise

    def handle_ai_query(self, nationality: Optional[str] = None, 
                       course: Optional[str] = None, 
                       country: Optional[str] = None) -> bool:
        """Handle AI query and response"""
        try:
            # Construct prompt based on available information
            if course and country:
                prompt = f"""I am a {nationality} citizen and I want to study {course} in {country}. 
                In brief, get me the list of all universities and colleges offering {course} in {country}, 
                their application cost, tuition cost, course start date, ranking, and admission document 
                requirements for {nationality}?"""
                logger.info(f"Calling openai with prompt {prompt}")
            else:
                prompt = f"""I am a {nationality} citizen and I want to study in Ireland related to my previous study and work. 
                '{self.incoming_message}' is my previous job role, job title and industry. In brief, 
                get me the list of all universities and colleges in Ireland, their application cost, tuition cost, 
                course start date, ranking, and admission document requirements for {nationality}?"""
                logger.info(f"Calling openai with prompt {prompt}")

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_response = response.choices[0].message.content

            chunks = [ai_response[i:i+1600] for i in range(0, len(ai_response), 1600)]
            for chunk in chunks:
                self.send_message(body=chunk)

            self.save_conversation(ai_response, "AI_RESPONSE")

            if self.last_conversation and self.last_conversation.content_sid == "HX6111ef91274335111f998197603cd649":
                    self.send_message(content_sid="HX2cfb26cd180b5ee3ed54b0af2eeaf80e")
                    self.save_conversation("END", "HX2cfb26cd180b5ee3ed54b0af2eeaf80e")
                    return True
            
            if self.last_conversation and self.last_conversation.content_sid == "HX2cfb26cd180b5ee3ed54b0af2eeaf80e":
                message = client.messages.create(
                            to=self.from_number,
                            from_="whatsapp:+15057264211",
                            body="Thank you"
                        )
                return True
            
            follow_up_message = self.send_message(content_sid="HXc5f81ceade11d60d56e3dda353c5e5af")
            self.save_conversation(follow_up_message.body, "HXc5f81ceade11d60d56e3dda353c5e5af")
            
            
            return True

        except Exception as e:
            logger.error(f"Error in AI query: {str(e)}")
            return False

    def handle_conversation(self) -> HttpResponse:
        """Main conversation flow handler"""
        try:
            # Handle button payloads first
            if self.btn_payload and self.incoming_message not in ["graduate", "ph.d", "undergraduate"]:
                return self.handle_button_payload()

            # Handle initial message if no previous conversation
            if not self.last_conversation:
                return self.handle_initial_message()
            
            if self.incoming_message in ["graduate", "ph.d", "undergraduate"]:
                message = self.send_message(content_sid="HXb523d5bca6512765e0048b57cb7ecaad")
                return self.save_conversation(message.body, "HXb523d5bca6512765e0048b57cb7ecaad")

            # Handle different content_sid cases
            handlers = {
                "HXb523d5bca6512765e0048b57cb7ecaad": self.handle_course_confirmation,
                "HXd7e089d4b38f62b087d1590ace17777b": self.handle_name_input,
                "HXf172cce6d30a506bf56e3b67cabce607": self.handle_work_experience,
                "HX43d6748e214fd2100bfb2392ee8d8909": self.handle_course_input,
                "HX6111ef91274335111f998197603cd649": self.handle_country_input,
                "HX007d0c1d83fe7f01d9b64b9c9e38bea9": self.handle_nationality_input,
                "HXa02842077f93c4b7e8590709e9194508": self.handle_country_selection,
                "HX2cfb26cd180b5ee3ed54b0af2eeaf80e": self.handle_final_response,
                "HXc5f81ceade11d60d56e3dda353c5e5af": self.handle_additional_query,
            }

            handler = handlers.get(self.last_conversation.content_sid)
            if handler:
                return handler()

            return self.handle_default_response()

        except Exception as e:
            logger.error(f"Error in conversation handler: {str(e)}")
            return HttpResponse("An error occurred", status=500)

    def handle_button_payload(self) -> HttpResponse:
        """Handle button payload responses"""
        try:
            if self.btn_payload == "Yes_course_study":
                message = self.send_message(content_sid="HX43d6748e214fd2100bfb2392ee8d8909")
                self.save_conversation(message.body, "HX43d6748e214fd2100bfb2392ee8d8909")
                return
            elif self.btn_payload == "No_course_study":
                message = self.send_message(content_sid="HXd7e089d4b38f62b087d1590ace17777b")
                self.save_conversation(message.body, "HXd7e089d4b38f62b087d1590ace17777b")
                return
            elif self.btn_payload == "No":
                message = self.send_message(content_sid="HXec08ecb4c19bc9e2e70e4528ada26829")
                self.save_conversation("END", "END")
                return
            elif self.btn_payload == "Admission":
                message = self.send_message(content_sid="HX007d0c1d83fe7f01d9b64b9c9e38bea9")
                self.save_conversation(message.body, "HX007d0c1d83fe7f01d9b64b9c9e38bea9")
                return
            elif self.btn_payload == "Yes":
                message = self.send_message(content_sid="HXf172cce6d30a506bf56e3b67cabce607")
                self.save_conversation(message.body, "HXf172cce6d30a506bf56e3b67cabce607")
                return
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling button payload: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_initial_message(self) -> HttpResponse:
        """Handle initial message"""
        try:
            if self.incoming_message == "admission":
                message = self.send_message(content_sid="HX0fac383db6158da097611eeca941ca3a")
                self.save_conversation(message.body, "HX0fac383db6158da097611eeca941ca3a")
                return
            elif self.incoming_message in ["graduate", "ph.d", "undergraduate"]:
                message = self.send_message(content_sid="HXb523d5bca6512765e0048b57cb7ecaad")
                self.save_conversation(message.body, "HXb523d5bca6512765e0048b57cb7ecaad")
                return
            else:
                message = self.send_message(content_sid="HX228db51c85512780a5509d80054f5536")
                self.save_conversation(message.body, "HX228db51c85512780a5509d80054f5536")
                return
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling initial message: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_course_confirmation(self) -> HttpResponse:
        """Handle course confirmation response"""
        try:
            if self.incoming_message == "no":
                message = self.send_message(content_sid="HXd7e089d4b38f62b087d1590ace17777b")
                self.save_conversation(message.body, "HXd7e089d4b38f62b087d1590ace17777b")
            elif self.incoming_message == "yes":
                message = self.send_message(content_sid="HX007d0c1d83fe7f01d9b64b9c9e38bea9")
                self.save_conversation(message.body, "HX007d0c1d83fe7f01d9b64b9c9e38bea9")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling course confirmation: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_name_input(self) -> HttpResponse:
        """Handle name input"""
        try:
            message = self.send_message(content_sid="HXf172cce6d30a506bf56e3b67cabce607")
            self.save_conversation(message.body, "HXf172cce6d30a506bf56e3b67cabce607")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling name input: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_work_experience(self) -> HttpResponse:
        """Handle work experience input"""
        try:
            nationality = self.get_message_by_content_sid("HX540d0f516020f0140e119b75840cea49")
            if nationality:
                self.handle_ai_query(nationality=nationality)
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling work experience: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_course_input(self) -> HttpResponse:
        """Handle course input"""
        try:
            message = self.send_message(content_sid="HXa02842077f93c4b7e8590709e9194508")
            self.save_conversation(message.body, "HXa02842077f93c4b7e8590709e9194508")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling course input: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_country_input(self) -> HttpResponse:
        """Handle country input"""
        try:
            nationality = self.get_message_by_content_sid("HX540d0f516020f0140e119b75840cea49")
            course = self.get_message_by_content_sid("HX6111ef91274335111f998197603cd649")
            
            if nationality and course:
                self.handle_ai_query(nationality=nationality, course=course, country=self.incoming_message)
            
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling country input: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_nationality_input(self) -> HttpResponse:
        """Handle nationality input"""
        try:
            from utils import countries, nations
            if self.incoming_message in countries or self.incoming_message in nations:
                message = self.send_message(content_sid="HX540d0f516020f0140e119b75840cea49")
                self.save_conversation(message.body, "HX540d0f516020f0140e119b75840cea49")
            else:
                self.send_message(content_sid="HX0ad28a9d9dd9dd919b3daf2c4ea0dfbf")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling nationality input: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_country_selection(self) -> HttpResponse:
        """Handle country selection"""
        try:
            nationality = self.get_message_by_content_sid("HX540d0f516020f0140e119b75840cea49")
            course = self.get_message_by_content_sid("HXa02842077f93c4b7e8590709e9194508")
            
            if nationality and course:
                self.handle_ai_query(nationality=nationality, course=course, country=self.incoming_message)
            
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling country selection: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_final_response(self) -> HttpResponse:
        """Handle final response"""
        try:
            message = self.send_message(body="Thank you")
            self.save_conversation(message.body, "END")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling final response: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_additional_query(self) -> HttpResponse:
        """Handle additional query"""
        try:
            message = self.send_message(content_sid="HX6111ef91274335111f998197603cd649")
            self.save_conversation(message.body, "HX6111ef91274335111f998197603cd649")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling additional query: {str(e)}")
            return HttpResponse("Error", status=500)

    def handle_default_response(self) -> HttpResponse:
        """Handle default response"""
        try:
            message = self.send_message(content_sid="HX228db51c85512780a5509d80054f5536")
            self.save_conversation(message.body, "HX228db51c85512780a5509d80054f5536")
            return HttpResponse("Success")
        except Exception as e:
            logger.error(f"Error handling default response: {str(e)}")
            return HttpResponse("Error", status=500)

@csrf_exempt
def webhook_whatsapp(request) -> HttpResponse:
    """Main webhook endpoint"""
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
        # Extract request data
        incoming_message = request.POST.get('Body', '')
        from_number = request.POST.get('From', '')
        wa_id = request.POST.get('WaId', '')
        btn_payload = request.POST.get('ButtonPayload')

        # Validate required parameters
        if not all([incoming_message, from_number, wa_id]):
            logger.error("Missing required parameters")
            return HttpResponse("Missing required parameters", status=400)

        # Handle conversation
        handler = ConversationHandler(wa_id, from_number, incoming_message, btn_payload)
        return handler.handle_conversation()

    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return HttpResponse("An error occurred", status=500)