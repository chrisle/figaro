import logging
from jinja2 import Environment
from jinja2.environment import Environment
from figaro.llms.vertex_ai import VertexAI
import re
from abc import abstractmethod
from jinja2 import nodes
from jinja2.ext import Extension
import typing

log = logging.getLogger(__name__)

CALL_PATTERN = r'(\{ _call\(.*\) \})'


class Chain:

    def __init__(self, template, llm=None, verbose=False):
        self._template = template
        self._verbose = verbose

    def __call__(self, **kwargs):
        # Convert input template to execution template
        call_env = Environment(extensions=[GeneratorExtension])
        call_template = call_env.from_string(self._template).render(**kwargs)

        # Split by the _calls
        stages = re.split(CALL_PATTERN, call_template)
        print (stages)

        # execte each stage
        prompt = ''
        for prompt_stage in stages:
            if bool(re.search(pattern=CALL_PATTERN, string=prompt_stage)):
                vertexai = VertexAI()
                response = vertexai.call(prompt)
                print (response)
                prompt = prompt + response
            else:
                print (prompt_stage)
                prompt = prompt + prompt_stage


class GeneratorExtension(Extension):
    tags = { 'gen' }

    default_options = {}

    def __init__(self, environment: typing.Union[Environment, None] = None) -> None:
        if environment is not None:
            super().__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        self._llm_name = parser.parse_expression()
        self._output_key = parser.parse_expression()

        self.options: typing.Dict[str, nodes.Expr] = self.default_options

        while parser.stream.current.type != 'block_end':
            if parser.stream.skip_if('colon'):
                break

            token = parser.stream.expect('name')
            if parser.stream.current.type == 'assign':
                next(parser.stream)
                self.options[token.value] = parser.parse_expression()

        return nodes.Output(
            [self.call_method('_output')], lineno=lineno
        )

    def _output(self):
        obj = {}
        for key in self.options.keys():
            obj[key] = self.options[key].value
        obj['llm'] = self._llm_name.name
        obj['output_key'] = self._output_key.value
        return f'{{ _call({obj}) }}'
