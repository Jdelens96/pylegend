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
    PyLegendDict,
    PyLegendUnion,
)
from pylegend.core.tds.legend_api.frames.legend_api_tds_frame import LegendApiTdsFrame
from pylegend.core.tds.tds_column import PrimitiveTdsColumn
from pylegend.extensions.tds.legend_api.frames.legend_api_table_spec_input_frame import LegendApiTableSpecInputFrame
from pylegend.tests.test_helpers.legend_service_frame import simple_person_service_frame


class TestColumnsApi:

    def test_columns_api_table_spec_frame(self) -> None:
        columns = [
            PrimitiveTdsColumn.integer_column("col1"),
            PrimitiveTdsColumn.string_column("col2")
        ]
        frame: LegendApiTdsFrame = LegendApiTableSpecInputFrame(['test_schema', 'test_table'], columns)
        assert "[" + ", ".join(str(s) for s in frame.columns()) + "]" == \
               "[TdsColumn(Name: col1, Type: Integer), TdsColumn(Name: col2, Type: String)]"

    def test_columns_api_legend_service_frame(self, legend_test_server: PyLegendDict[str, PyLegendUnion[int, ]])\
            -> None:
        frame: LegendApiTdsFrame = simple_person_service_frame(legend_test_server["engine_port"])
        assert "[" + ", ".join(str(s) for s in frame.columns()) + "]" == \
               "[TdsColumn(Name: First Name, Type: String), TdsColumn(Name: Last Name, Type: String), " \
               "TdsColumn(Name: Age, Type: Integer), TdsColumn(Name: Firm/Legal Name, Type: String)]"
