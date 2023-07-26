from figaro.agents.base_agent import BaseAgent
from figaro.llms.base_llm import BaseLLM
from figaro.memory.base_memory import BaseMemory
from jinja2 import Environment
from typing import Union


PROMPT_TEMPLATE = """
SYSTEM: {{personality}}

CONTEXT: {{context}}

{{chat_history}}
{{subject_name}}: {{user_input}}
{{ai_name}}: """

class TurnBasedChatAgent(BaseAgent):

    def __init__(self,
                 llm: Union[BaseLLM, None] = None,
                 memory: Union[BaseMemory, None] = None,
                 verbose: bool = False,
                 personality: str = '',
                 subject_name: str = 'HUMAN',
                 ai_name: str = 'ASSISTANT',
                 ):
        super().__init__(
            llm=llm,
            memory=memory,
            verbose=verbose
        )
        self._personality = personality
        self._subject_name = subject_name
        self._ai_name = ai_name
        self._subject_name = subject_name.upper()
        self._ai_name = ai_name.upper()


    @property
    def personality(self):
        return self._personality or None

    @personality.setter
    def personality(self, desc: str):
        self._personality = desc

    def _render_chat_history(self):
        output = []
        chat_history = self._memory.get_chat_history()
        for history in chat_history:
            role = self._subject_name if history['role'] == 'human' else self._ai_name
            content = history['content']
            output.append(f'{role}: {content}')
        return '\n'.join(output)

    def _get(self, user_input: Union[str, None] = None):
        env = Environment()
        template = env.from_string(PROMPT_TEMPLATE)

        prompt = template.render(
            personality=self._personality,
            context=self._memory.get_summary(),
            chat_history=self._render_chat_history(),
            subject_name=self._subject_name,
            user_input=user_input,
            ai_name=self._ai_name,
        )
        if self._verbose: print(prompt)
        return self._llm.call(prompt)