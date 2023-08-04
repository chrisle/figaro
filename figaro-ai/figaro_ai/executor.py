from figaro_ai.llms import EXTENSION_MAP
from figaro_ai.types import HookMap
from jinja2 import Environment
from jinja2 import nodes
from jinja2.ext import Extension
from typing import Any
import json
import logging
import re
import sys
import typing

class Executor:

    def __init__(self,
                 template: str,
                 hooks: HookMap = {},
                 verbose=False,
                 level=logging.INFO,
                 **kwargs):
        if verbose: logging.basicConfig(stream=sys.stdout, level=level)
        self._template = template
        self._global_args: dict[str, Any] = kwargs
        self._hooks = hooks

    def __call__(self, type=str, **kwargs):
        """Execute a chain.

        Args:
            type: Data type to cast the final LLM response as (default=str)
            **kwargs: Keywords sent to the template as variables.

        Returns:
            Final response from the LLM.
        """

        # How it works:
        # 1) Split up the Jinja2 template by {% gen %}. So we have prompts and
        #    calls to the LLM for each "stage".
        # 2) Replace {% gen %} with { _call() } which actually does the LLM call.
        # 3) Update the Jinja2 environment with responses from the LLM.
        # 4) Repeat until there are no more stages and return the last response
        #    to the caller of the Figaro function.

        prompt = ''
        prev_stage_vars = ''

        # Split template up into stages where we need to call the LLM.
        stages = re.split(r'(\{\% gen .* \%\})', self._template)
        logging.debug(f'Stages: {stages}'.strip())

        for stage_template in stages:

            # Carry forward the previous stage's variables in the environment.
            stage_template = prev_stage_vars + '\n' + stage_template
            logging.debug(f'stage_template: {stage_template}'.strip())

            # Create the prompt for this stage include the GeneratorExtension
            # with the Jinja2 parser.
            stage_env = Environment(extensions=[GeneratorExtension])
            stage_env.globals = self._global_args
            stage_prompt = stage_env.from_string(stage_template).render(**kwargs)
            logging.debug(f'stage_prompt: {stage_template}'.strip())

            # Call the LLM if this stage uses the _call function.
            if bool(re.search(pattern=r'\{ _call\(.*\) \}', string=stage_prompt)):

                # Parse the arguments from the template.
                args = json.loads(re.search(r'_call\((.*)\)', stage_prompt)[1])

                # Instanciate the LLM class.
                llm_klass = EXTENSION_MAP[args['llm']](**stage_env.globals)

                # Repeat multiple calls to the LLM if n > 1 in the arguments.
                if 'n' in args and args['n'] > 1:
                    generations = args['n']
                else:
                    generations = 1

                for n in range(generations):

                    if 'before_response' in self._hooks:
                        for hook in self._hooks['before_response']:
                            prompt, args, kwargs = hook(prompt, args, kwargs)

                    # Call the LLM.
                    response = llm_klass.call(prompt, **args)

                    # Escape single quotes and double quotes in the response
                    # so that it can be used in the Jinja2 template.
                    response = response.replace("'", "\\'").replace('"', '\\"')

                    if 'after_response' in self._hooks:
                        for hook in self._hooks['after_response']:
                            response = hook(response)

                    # Include previous part of the chain to the next stage.
                    prompt = prompt + response

                    # Update the output key in the environment for the next stage.
                    logging.debug(f'{args["output_key"]} = "{response}"'.strip())
                    prev_stage_vars = f'{{% set {args["output_key"]} = \'{response}\' %}}'

                    logging.info(response.strip())
            else:
                logging.info(stage_prompt.strip())

                # Append this stage to the prompt.
                prompt = prompt + stage_prompt

        # Return output cast to type.
        result = response.strip()
        if type == typing.Dict or type == dict:
            return json.loads(result)
        return result


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
