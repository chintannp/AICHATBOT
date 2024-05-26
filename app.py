import os
from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from config import DefaultConfig
from bot import SentimentAnalysisBot

app = Flask(__name__)
config = DefaultConfig()

adapter_settings = BotFrameworkAdapterSettings(config.APP_ID, config.APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

bot = SentimentAnalysisBot(config)

@app.route("/api/messages", methods=["POST"])
async def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    async def aux_func(turn_context: TurnContext):
        await bot.on_turn(turn_context)

    try:
        await adapter.process_activity(activity, auth_header, aux_func)
        return Response(status=201)
    except Exception as e:
        print(f"Exception: {e}")
        return Response(status=500)

if __name__ == "__main__":
    app.run(port=3978)
