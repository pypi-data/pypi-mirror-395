################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
#################################################################################
from typing import Any, Callable

from docstring_parser import parse
from typing_extensions import override

from flink_agents.api.tools.tool import Tool, ToolMetadata, ToolType
from flink_agents.api.tools.utils import create_schema_from_function
from flink_agents.plan.function import JavaFunction, PythonFunction


class FunctionTool(Tool):
    """Tool that takes in a function.

    Attributes:
    ----------
    func : Function
        User defined function.
    """

    func: PythonFunction | JavaFunction

    @classmethod
    @override
    def tool_type(cls) -> ToolType:
        """Get the tool type."""
        return ToolType.FUNCTION

    def call(self, *args: Any, **kwargs: Any) -> Any:
        """Call the function tool."""
        return self.func(*args, **kwargs)


def from_callable(func: Callable) -> FunctionTool:
    """Create FunctionTool from a user defined function.

    Parameters
    ----------
    func : Callable
        The function to analyze.
    """
    description = parse(func.__doc__).description
    metadata = ToolMetadata(
        name=func.__name__,
        description=description,
        args_schema=create_schema_from_function(func.__name__, func=func),
    )
    return FunctionTool(func=PythonFunction.from_callable(func), metadata=metadata)
