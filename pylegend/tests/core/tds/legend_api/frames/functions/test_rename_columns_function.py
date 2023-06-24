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

import json
import pytest
from textwrap import dedent
from pylegend.core.tds.tds_column import PrimitiveTdsColumn
from pylegend.core.tds.tds_frame import FrameToSqlConfig
from pylegend.core.tds.legend_api.frames.legend_api_tds_frame import LegendApiTdsFrame
from pylegend.extensions.tds.legend_api.frames.legend_api_table_spec_input_frame import LegendApiTableSpecInputFrame
from pylegend.tests.test_helpers.legend_service_frame import simple_person_service_frame
from pylegend._typing import (
    PyLegendDict,
    PyLegendUnion,
)


class TestRenameColumnsAppliedFunction:

    def test_rename_columns_error_on_different_sizes(self) -> None:
        columns = [
            PrimitiveTdsColumn.integer_column("col1"),
            PrimitiveTdsColumn.string_column("col2")
        ]
        frame: LegendApiTdsFrame = LegendApiTableSpecInputFrame(['test_schema', 'test_table'], columns)
        with pytest.raises(ValueError) as v:
            frame.rename_columns(["col1"], ["col3", "col4"])
        assert v.value.args[0] == \
               ("column_names list and renamed_column_names list should have same size when renaming columns.\n"
                "column_names list - (Count: 1) - ['col1']\n"
                "renamed_column_names_list - (Count: 2) - ['col3', 'col4']\n")

    def test_rename_columns_error_on_duplicates_in_columns(self) -> None:
        columns = [
            PrimitiveTdsColumn.integer_column("col1"),
            PrimitiveTdsColumn.string_column("col2")
        ]
        frame: LegendApiTdsFrame = LegendApiTableSpecInputFrame(['test_schema', 'test_table'], columns)
        with pytest.raises(ValueError) as v:
            frame.rename_columns(["col1", "col1"], ["col3", "col4"])
        assert v.value.args[0] == \
               ("column_names list shouldn't have duplicates when renaming columns.\n"
                "column_names list - (Count: 2) - ['col1', 'col1']\n")

    def test_rename_columns_error_on_duplicates_in_renamed_columns(self) -> None:
        columns = [
            PrimitiveTdsColumn.integer_column("col1"),
            PrimitiveTdsColumn.string_column("col2")
        ]
        frame: LegendApiTdsFrame = LegendApiTableSpecInputFrame(['test_schema', 'test_table'], columns)
        with pytest.raises(ValueError) as v:
            frame.rename_columns(["col1", "col2"], ["col3", "col3"])
        assert v.value.args[0] == \
               ("renamed_column_names_list list shouldn't have duplicates when renaming columns.\n"
                "renamed_column_names_list - (Count: 2) - ['col3', 'col3']\n")

    def test_sql_gen_rename_columns_function(self) -> None:
        columns = [
            PrimitiveTdsColumn.integer_column("col1"),
            PrimitiveTdsColumn.string_column("col2")
        ]
        frame: LegendApiTdsFrame = LegendApiTableSpecInputFrame(['test_schema', 'test_table'], columns)

        frame = frame.rename_columns(["col2"], ["col3"])
        assert "[" + ", ".join([str(c) for c in frame.columns()]) + "]" == \
               "[TdsColumn(Name: col1, Type: Integer), TdsColumn(Name: col3, Type: String)]"
        expected = '''\
            SELECT
                "root".col1 AS "col1",
                "root".col2 AS "col3"
            FROM
                test_schema.test_table AS "root"'''
        assert frame.to_sql_query(FrameToSqlConfig()) == dedent(expected)

        frame = frame.rename_columns(["col1", "col3"], ["col4", "col5"])
        assert "[" + ", ".join([str(c) for c in frame.columns()]) + "]" == \
               "[TdsColumn(Name: col4, Type: Integer), TdsColumn(Name: col5, Type: String)]"
        expected = '''\
            SELECT
                "root".col1 AS "col4",
                "root".col2 AS "col5"
            FROM
                test_schema.test_table AS "root"'''
        assert frame.to_sql_query(FrameToSqlConfig()) == dedent(expected)

    def test_e2e_rename_columns_function(self, legend_test_server: PyLegendDict[str, PyLegendUnion[int, ]]) -> None:
        frame: LegendApiTdsFrame = simple_person_service_frame(legend_test_server["engine_port"])
        frame = frame.take(5)
        frame = frame.rename_columns(["First Name", "Firm/Legal Name"], ["Name", "Firm Name"])
        frame = frame.restrict(["Name", "Firm Name"])
        assert "[" + ", ".join([str(c) for c in frame.columns()]) + "]" == \
               "[TdsColumn(Name: Name, Type: String), TdsColumn(Name: Firm Name, Type: String)]"
        expected = {'columns': ['Name', 'Firm Name'],
                    'rows': [{'values': ['Peter', 'Firm X']},
                             {'values': ['John', 'Firm X']},
                             {'values': ['John', 'Firm X']},
                             {'values': ['Anthony', 'Firm X']},
                             {'values': ['Fabrice', 'Firm A']}]}
        res = frame.execute_frame_to_string()
        assert json.loads(res)["result"] == expected
