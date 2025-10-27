from applicationinsights import TelemetryClient
import os
from dotenv import load_dotenv
load_dotenv()
#from src.env import INSTRUMENTAL_KEY


class ApplicationInsightsLogger:
    def __init__(self):
        """
        Initializes the ApplicationInsightsLogger with the given instrumentation key.
        """
        instrumentation_key = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")
        self.tc = TelemetryClient(instrumentation_key)


        # Initialize class variables with meaningful names
        self.source_type = "RAIAgent Function App"

    def track_event(self, event_name: str, properties: dict):
        """
        Tracks an event in Application Insights with custom properties.

        Args:
            event_name (str): The name of the event to track.
            properties (dict): A dictionary of properties (dimensions) to be logged with the event.
        """
        properties["sourceType"] = self.source_type

        self.tc.track_event(event_name, properties=properties)
        self.tc.flush()

    def track_exception(self, exception_name: str, properties: dict):
        """
        Tracks an exception in Application Insights with custom properties.

        Args:
            exception_name (str): The name or type of the exception.
            properties (dict): A dictionary of properties (dimensions) to be logged with the exception.
        """
        
        properties["sourceType"] = self.source_type

        self.tc.track_exception(exception_name, properties=properties)
        self.tc.flush()