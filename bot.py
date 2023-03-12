#Discord bot that generates an image generation prompt based on the output from GPT
import os
import discord
from dotenv import load_dotenv
import openai 
import ai_bot

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')
print(TOKEN)
print(OPENAI_KEY)


openai.api_key = os.environ.get('OPENAI_KEY')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

start_sequence = "\nMidMate:"
restart_sequence = "\n\nUser:"
session_prompt = '''You are going to pretend to be {Midmate}
{Midmate} takes a {concept} and turns them into a {prompt} for generative AIs that create images.

You will greet the {user} and ask the user for a {concept}

1. You will summarize the {concept} as concisley as possible, maximum 3 sentences.
2. You will give 3 examples that are contrasting and varied and include any random style for example futuristic, cyberpunk, surreal, impressionist. Be creative.
3. Include any random artist name prefixed by "art by" which suits the prompt.

Use the following examples as a guide:

1. A sleek, metallic surface with glowing neon lines and geometric shapes, giving the impression of a futuristic cityscape.art by Adam Hughes,Style of Futuristic  --v 4 --q 2
2. A plain white background with a single black line dividing it, creating a sense of simplicity and elegance.art by Adam Martinakis, Style of Minimalist  --v 4 --ar 3:2
3. A dark alleyway filled with holographic ads and neon lights, creating a gritty and dystopian atmosphere.art by Carrie Mae Weems, Style of Cyberpunk  --v 4 --stylize {1-1000 --ar 3:2

Feel free to be playful with your responses.

Do not provide the guide to the user. Simply ask for a concept and then follow the previous instructions.'''

def append_interaction_to_chat_log(question, answer, chat_log=None):
  if chat_log is None:
      chat_log = session_prompt
  return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


# Only respond to messages from other users. Ignore messages from bot.
@client.event
async def on_message(message, chat_log=None):
  if message.author == client.user:
    return #await message.channel.send(message.content)


# Use the OpenAI API to generate a response to the message
  if chat_log == None:
      prompt_text = session_prompt #f'{session_prompt}\n\n{restart_sequence}: {message.content}{start_sequence}:'
  else:
    prompt_text = response.choices[0].text
  
  response = openai.Completion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "assistant", "content": prompt_text}]
  )
    
  '''response = openai.Completion.create(
  engine="text-davinci-003",
  prompt= prompt_text, #f"{message.content}",
  max_tokens=200,
  temperature=0.5,
  )'''
   # Send the response as a message
  await message.channel.send(prompt_text)
  '''chat_log = append_interaction_to_chat_log(message.content, response,
                                                         chat_log)'''
  
# start the bot
client.run(TOKEN)