# Copyright 2023 Goldman Sachs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from abc import ABCMeta, abstractmethod
from pylegend._typing import (
    PyLegendSequence
)
from pylegend.core.sql.metamodel import Expression


__all__: PyLegendSequence[str] = [
    "PyLegendExpression",
    "PyLegendExpressionBooleanReturn"
]


class PyLegendExpression(metaclass=ABCMeta):
    @abstractmethod
    def to_sql_expression(self) -> Expression:
        pass


class PyLegendExpressionBooleanReturn(PyLegendExpression, metaclass=ABCMeta):
    pass
