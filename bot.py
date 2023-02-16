#Bot file for discord

# bot.py
import os
import discord
from dotenv import load_dotenv
import openai 


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')


openai.api_key = os.environ.get('OPENAI_KEY')




intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

start_sequence = "\nHonnold:"
restart_sequence = "\n\nClimber:"
session_prompt = "You are the rock climbing professional Alex Honnold who lives in a van in Yoeemite and has  climbed in Patagonia, the USA, Canada during your 25 year career. A climber wants advice on climbing safely. Your greatest achievement is climbing El Capitan free solo. You are friendly and polite.\n\nClimber: Who are you?\nGuide: I am Alex Honnold\n\nClimber: I’d like to know more about safety please?\nGuide: I can help you with that based on my experience. Have you been climbing a long time?\n\nClimber: Can you tell me about your greatest achievement?\nGuide:Honnold:\n\nMy greatest achievement is climbing El Capitan free solo.ClimberHonnold:\n\nFantastic. Tell me more about safety?\n\n\nThere are a few things to keep in mind when climbing. First, always use a partner when possible. Second, be aware of your surroundings and be cautious when climbing. Finally, always take safety precautions, like wearing a helmet and climbing with proper gear"

def append_interaction_to_chat_log(question, answer, chat_log=None):
  if chat_log is None:
      chat_log = session_prompt
  return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'



# Only respond to messages from other users. Ignore messages from bot.
@client.event
async def on_message(message, chat_log=None):
  if message.author == client.user:
    return #await message.channel.send(message.content)

  prompt = ""
# Use the OpenAI API to generate a response to the message
  prompt_text = f'{chat_log}{restart_sequence}: {message.content}{start_sequence}:'
  response = openai.Completion.create(
  engine="text-davinci-003",
  prompt= prompt_text, #f"{message.content}",
  max_tokens=200,
  temperature=0.5,
  )
   # Send the response as a message
  await message.channel.send(response.choices[0].text)
  chat_log = append_interaction_to_chat_log(message.content, response,
                                                         chat_log)
  


    

# start the bot
client.run(TOKEN)