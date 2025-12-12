"""
MoodSpeak AI Library
Detects user's emotion + generates emotional, personalized AI replies.
"""

import os
from openai import OpenAI

client = None

def _get_client():
    global client
    if client is None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("Please set OPENAI_API_KEY environment variable.")
        client = OpenAI(api_key=key)
    return client


def detect_emotion(text: str) -> str:
    """
    Detects emotion from user text.
    """
    prompt = f"""
    Read the message and classify its emotion in ONE WORD from:
    happy, sad, angry, excited, neutral

    Message: "{text}"
    Only output a single word.
    """

    response = _get_client().responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    emotion = response.output[0].content[0].text.lower().strip()

    if emotion not in ["happy", "sad", "angry", "excited", "neutral"]:
        emotion = "neutral"

    return emotion


def get_ai_reply(text: str, emotion: str) -> str:
    """
    Generates an emotion-aware AI response.
    """
    prompt = f"""
    The user feels {emotion}.
    Respond in a personalized, friendly, warm tone.
    Add creativity and empathy.

    User message:
    {text}
    """

    response = _get_client().responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text.strip()


def mood_emoji(emotion: str) -> str:
    """
    Maps emotion → emoji.
    """
    return {
        "happy": "😊",
        "sad": "😔",
        "angry": "😡",
        "excited": "🤩",
        "neutral": "😐"
    }.get(emotion, "😐")
