import os
import json
from datetime import datetime

import discord
from discord.ext import commands

from openai import OpenAI

def load_files(root_dir: str):
    """
    Walk through `root_dir` and convert every file into a string of the form:
        f"{path}\n---\n{content}\n---"
    Returns a list of these file strings.
    """

    file_strings = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            try:
                with open(
                    full_path, 
                    "r", 
                    encoding="utf-8", 
                    errors="replace"
                ) as f:
                    content = f.read()
            except Exception as e:
                content = f"[ERROR READING FILE: {e}]"

            formatted = f"{full_path}\n---\n{content}\n---"
            file_strings.append(formatted)

    return file_strings

class Character:
    def __init__(self):
        self.client:OpenAI = None
        self.convo_messages:list[dict] = []
        self.knowledge:list[str] = []
        self.system_message:dict = {
            'role': 'system',
            'content': None,
        }
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix="!", intents=intents)
        self.bot:commands.Bot = bot
        self.bot_token:str = None
        self.system_content:str = (
            "You have access to a knowledge base provided by the user in the form of a bunch of labeled documents that you have read and learned. You have perfect memory of this knowledge base and can answer any question about it.\n"
        )
        self.knowledge_dir:str = './content'
        
        @bot.event
        async def on_message(message: discord.Message):
            await self.on_message(message)

    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if '.' in message.content or isinstance(message.channel, discord.DMChannel):
            content = self.respond(message)
            await message.channel.send(content[:2000])

        await self.bot.process_commands(message)

    def start(self):
        bot = self.bot
        bot.run(self.bot_token)

    def respond(self, message:discord.Message):
        content = message.content
        self.system_message['content'] = self.system_content
        self.knowledge.clear()
        self.knowledge.extend(load_files(self.knowledge_dir))
        file_messages = [
            {
                'role': 'user',
                'content': f'{knowledge_content}',
                'name': 'information',
            }
            for knowledge_content in self.knowledge
        ]
        user_message = {
            'role': 'user',
            'content': f'{content}',
            'name': f'{message.author.display_name}'
        }
        self.convo_messages.append(user_message)
        messages = [
            self.system_message,
            *file_messages,
            *self.convo_messages,
        ]      
        print(messages)
        completion = self.client.chat.completions.create(
            messages=messages,
            model='gpt-4o',
        )
        message = completion.choices[0].message
        assistant_message = {
            'role': message.role,
            'content': f'{message.content}',
        }
        self.convo_messages.append(assistant_message)
        return message.content