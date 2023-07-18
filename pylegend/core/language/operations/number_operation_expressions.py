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

from pylegend._typing import (
    PyLegendSequence,
    PyLegendDict,
)
from pylegend.core.language.expression import (
    PyLegendExpressionNumberReturn,
)
from pylegend.core.language.operations.binary_expression import PyLegendBinaryExpression
from pylegend.core.sql.metamodel import (
    Expression,
    QuerySpecification,
    ArithmeticType,
    ArithmeticExpression,
)
from pylegend.core.tds.tds_frame import FrameToSqlConfig


__all__: PyLegendSequence[str] = [
    "PyLegendNumberAddExpression",
]


class PyLegendNumberAddExpression(PyLegendBinaryExpression, PyLegendExpressionNumberReturn):

    @staticmethod
    def __to_sql_func(
            expression1: Expression,
            expression2: Expression,
            frame_name_to_base_query_map: PyLegendDict[str, QuerySpecification],
            config: FrameToSqlConfig
    ) -> Expression:
        return ArithmeticExpression(ArithmeticType.ADD, expression1, expression2)

    def __init__(self, operand1: PyLegendExpressionNumberReturn, operand2: PyLegendExpressionNumberReturn) -> None:
        PyLegendExpressionNumberReturn.__init__(self)
        PyLegendBinaryExpression.__init__(
            self,
            operand1,
            operand2,
            PyLegendNumberAddExpression.__to_sql_func
        )
