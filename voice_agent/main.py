import speech_recognition as sr
from dotenv import load_dotenv
import os
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio
import pygame
import edge_tts

load_dotenv()
openai = AsyncOpenAI()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

def main():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2


        SYSTEM_PROMPT = f"""
            You're an expert ai voice agent. You are given the transcript of what the user has said using voice.
            You need to output as if you are an voice agent and whatever you speak will be converted back o audio
            using AI and played back to user
            """

        messages=[{"role" :"system", "content": SYSTEM_PROMPT }]
        while True:
            
            print("Speak something")
            audio = r.listen(source)

            print("Processing audio... (STT)")
            stt = r.recognize_google(audio)

            print("You said - ", stt)

            messages.append({"role" :"user", "content": stt })
            response = client.chat.completions.parse(
            model = "gpt-4o-mini",
            messages=messages
            )

            ai_response_text = response.choices[0].message.content
            print("AI resopnse", ai_response_text)
            asyncio.run(speak_text(ai_response_text))
    

async def speak_text(text: str):
    # 'en-US-AriaNeural' is a great, cheerful female voice. 
    # You can also try 'en-US-GuyNeural' for a male voice.
    voice = "en-US-AriaNeural" 
    output_file = "response.mp3"
    
    print("Generating audio...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    
    # Play the generated audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    # Cleanup the audio file so we don't clutter your drive
    pygame.mixer.quit()
    os.remove(output_file)
    
main()