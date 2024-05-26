from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.schema import ChannelAccount
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class SentimentAnalysisBot(ActivityHandler):
    def __init__(self, config):
        self.client = TextAnalyticsClient(
            endpoint=config.ENDPOINT_URI,
            credential=AzureKeyCredential(config.API_KEY)
        )

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text
        sentiment_result = self.analyze_sentiment(text)
        await turn_context.send_activity(f"Sentiment: {sentiment_result.sentiment}")

    def analyze_sentiment(self, text):
        response = self.client.analyze_sentiment(documents=[text])[0]
        return response
