from figaro.llms import EXTENSION_MAP
from jinja2 import Environment
from jinja2 import nodes
from jinja2.ext import Extension
import json
import logging
import re
import typing

class Chain:

    def __init__(self, template, llm=None):
        self._template = template

    def __call__(self, **kwargs):
        """Execute a chain.

        How it works:
        1) Split up the Jinja2 template by {% gen %}. So we have prompts and
           calls to the LLM for each "stage".
        2) Replace {% gen %} with { _call() } which actually does the LLM call.
        3) Update the Jinja2 environment with responses from the LLM.
        4) Repeat until there are no more stages and return the last response
           to the caller of the Figaro function.

        """

        prompt = ''
        prev_stage_vars = ''

        # Split template up into stages where we need to call the LLM.
        stages = re.split(r'(\{\% gen .* \%\})', self._template)
        logging.debug(f'Stages: {stages}')

        for stage_template in stages:

            # Carry forward the previous stage's variables in the environment.
            stage_template = prev_stage_vars + '\n' + stage_template

            # Create the prompt for this stage include the GeneratorExtension
            # with the Jinja2 parser.
            stage_env = Environment(extensions=[GeneratorExtension])
            stage_prompt = stage_env.from_string(stage_template).render(**kwargs)

            # Call the LLM if this stage uses the _call function.
            if bool(re.search(pattern=r'\{ _call\(.*\) \}', string=stage_prompt)):

                # Parse the arguments from the template.
                args = json.loads(re.search(r'_call\((.*)\)', stage_prompt)[1])

                # Instanciate the LLM class.
                llm_klass = EXTENSION_MAP[args['llm']]()

                # Repeat multiple calls to the LLM if n > 1 in the arguments.
                if 'n' in args and args['n'] > 1:
                    generations = args['n']
                else:
                    generations = 1

                for n in range(generations):
                    # Call the LLM.
                    response = llm_klass.call(prompt, **args)

                    # Include previous part of the chain to the next stage.
                    prompt = prompt + response

                    # Update the output key in the environment for the next stage.
                    prev_stage_vars = f'{{% set {args["output_key"]} = "{response}" %}}'

                    logging.info(response.strip())
            else:
                logging.info(stage_prompt.strip())

                # Append this stage to the prompt.
                prompt = prompt + stage_prompt

        return response.strip()


class GeneratorExtension(Extension):
    """Jinja2 extension that calls an LLM."""
    tags = { 'gen' }

    default_options = {}

    def __init__(self, environment: typing.Union[Environment, None] = None) -> None:
        if environment is not None:
            super().__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # Extract LLM name from 1st parameter.
        self._llm_name = parser.parse_expression()

        # Extract output key from 2nd parameter.
        self._output_key = parser.parse_expression()

        # Parse any options from the rest of the parameters.
        self.options: typing.Dict[str, nodes.Expr] = self.default_options
        while parser.stream.current.type != 'block_end':
            if parser.stream.skip_if('colon'):
                break
            token = parser.stream.expect('name')
            if parser.stream.current.type == 'assign':
                next(parser.stream)
                self.options[token.value] = parser.parse_expression()

        # Return output node back to the Jinja parser.
        return nodes.Output(
            [self.call_method('_output')], lineno=lineno
        )

    def _output(self):
        """Replace {% gen %} command with an actual function call { _call() }."""
        obj = {}
        for key in self.options.keys():
            obj[key] = self.options[key].value
        obj['llm'] = self._llm_name.name
        obj['output_key'] = self._output_key.value
        return f'{{ _call({json.dumps(obj)}) }}'
