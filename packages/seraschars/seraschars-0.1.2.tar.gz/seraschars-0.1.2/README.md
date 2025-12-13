hi hello yes i wrote a small python package for making personas and stuff here it is
theres some example code below if you like to copy and paste example code i also like to copy and paste example code too yepyep oiuv;hsdbdi;ouvgho8v7gh 23o89f7vgh3fo8

```python
from seraschars import Character
from openai import OpenAI
from my_tokens import BOT_TOKEN

debugger = Character()
debugger.client = OpenAI()
debugger.bot_token = BOT_TOKEN
debugger.knowledge_dir = './seraschars'

debugger.start()
```