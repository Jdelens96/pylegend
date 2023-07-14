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
    PyLegendUnion,
)
from pylegend.core.language.primitives.primitive import PyLegendPrimitive
from pylegend.core.language.primitives.integer import PyLegendInteger
from pylegend.core.language.expression import PyLegendExpressionNumberReturn
from pylegend.core.sql.metamodel import (
    Expression,
    QuerySpecification
)
from pylegend.core.tds.tds_frame import FrameToSqlConfig


__all__: PyLegendSequence[str] = [
    "PyLegendNumber"
]


class PyLegendNumber(PyLegendPrimitive):
    __value: PyLegendExpressionNumberReturn

    def __init__(
            self,
            value: PyLegendExpressionNumberReturn
    ) -> None:
        self.__value = value

    def to_sql_expression(
            self,
            frame_name_to_base_query_map: PyLegendDict[str, QuerySpecification],
            config: FrameToSqlConfig
    ) -> Expression:
        return self.__value.to_sql_expression(frame_name_to_base_query_map, config)

    @staticmethod
    def __validate__param_to_be_number(
            param: PyLegendUnion[int, float, "PyLegendInteger", "PyLegendNumber"],
            desc: str
    ) -> None:
        if not isinstance(param, (int, float, PyLegendInteger, PyLegendNumber)):
            raise TypeError(desc + " should be a int/float or a int/float/number expression"
                                   " (PyLegendInteger/PyLegendFloat/PyLegendNumber)."
                                   " Got value " + str(param) + " of type: " + str(type(param)))