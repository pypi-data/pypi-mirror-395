from seraschars import Character
from openai import OpenAI
from my_tokens import BOT_TOKEN

debugger = Character()
debugger.client = OpenAI()
debugger.bot_token = BOT_TOKEN
debugger.knowledge_dir = './seraschars'

debugger.start()