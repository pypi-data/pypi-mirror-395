import dataclasses
from inspect import signature

from suite_py.lib.config import Config
from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.okta_handler import Okta
from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.tokens import Tokens


@dataclasses.dataclass
class Context:
    captainhook: CaptainHook
    config: Config
    git_handler: GitHandler
    okta: Okta
    project: str
    tokens: Tokens
    youtrack_handler: YoutrackHandler

    # Call the function to_call with kwargs, injecting fields from self as default arguments
    def call(self, to_call, **kwargs):
        provided = self.shallow_dict()
        needed = signature(to_call).parameters.keys()
        provided = {k: provided[k] for k in needed if k in provided}

        kwargs = provided | kwargs

        return to_call(**kwargs)

    def shallow_dict(self):
        """
        Converts the dataclass to a dict.

        Unlike dataclasses.asdict this function only shallow copies the fields
        instead of using copy.deepcopy()
        """
        return {
            field.name: getattr(self, field.name) for field in dataclasses.fields(self)
        }
