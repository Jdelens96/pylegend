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
    PyLegendList,
    PyLegendSequence
)
from pylegend.core.sql.metamodel import (
    QualifiedName,
    QualifiedNameReference,
    QuerySpecification,
    Select,
    SingleColumn,
    Table,
    AliasedRelation
)
from pylegend.core.tds.legend_api.frames.legend_api_input_tds_frame import LegendApiNonExecutableInputTdsFrame
from pylegend.core.tds.tds_column import TdsColumn
from pylegend.core.tds.tds_frame import FrameToSqlConfig


__all__: PyLegendSequence[str] = [
    "LegendApiTableSpecInputFrame"
]


class LegendApiTableSpecInputFrame(LegendApiNonExecutableInputTdsFrame):
    table: QualifiedName

    def __init__(self, table_name_parts: PyLegendList[str], columns: PyLegendSequence[TdsColumn]) -> None:
        super().__init__(columns=columns)
        self.table = QualifiedName(table_name_parts)

    def to_sql_query_object(self, config: FrameToSqlConfig) -> QuerySpecification:
        db_extension = config.sql_to_string_generator().get_db_extension()
        root_alias = db_extension.quote_identifier("root")
        return QuerySpecification(
            select=Select(
                selectItems=[
                    SingleColumn(
                        alias=db_extension.quote_identifier(x.get_name()),
                        expression=QualifiedNameReference(name=QualifiedName(parts=[root_alias, x.get_name()]))
                    )
                    for x in self.columns()
                ],
                distinct=False
            ),
            from_=[
                AliasedRelation(
                    relation=Table(name=self.table),
                    alias=root_alias,
                    columnNames=[x.get_name() for x in self.columns()]
                )
            ],
            where=None,
            groupBy=[],
            having=None,
            orderBy=[],
            limit=None,
            offset=None
        )

    def __str__(self) -> str:
        return "LegendApiTableSpecInputFrame({qualified})".format(qualified=".".join(self.table.parts))
