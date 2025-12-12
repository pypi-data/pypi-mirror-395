from typing import List, Dict


class Relation:
    def __init__(self, referencing_table: str, referenced_table: str, columns_references: List[Dict[str, str]]):
        """
        Represents a relation between tables.

        :param referencing_table: The table that references another table.
        :param referenced_table: The table being referenced.
        :param columns_references: A list of column references between the tables.
        """
        self.referencing_table = referencing_table
        self.referenced_table = referenced_table
        self.columns_references = [(d['referencingColumn'], d['referencedColumn']) for d in columns_references]

    def to_dict(self) -> Dict:
        """
        Converts the Relation object back to a dictionary.
        """
        columns_references = [{'referencingColumn': s, 'referencedColumn': t} for s, t in self.columns_references]
        return {
            'referencingTable': self.referencing_table,
            'referencedTable': self.referenced_table,
            'columnsReferences': columns_references,
        }

    def __repr__(self):
        return (
            f"Relation(referencing_table={self.referencing_table}, "
            f"referenced_table={self.referenced_table}, "
            f"columns_references={self.columns_references})"
        )


class SchemaRelation:
    def __init__(self, schema_relation: Dict):
        self.workspace_id = schema_relation['workspaceId']
        self.datasource_id = schema_relation['datasourceId']
        self.schema = schema_relation['schema']
        # Automatically create Relation objects from the relations JSON
        self.relations = [
            Relation(
                referencing_table=relation['referencingTable'],
                referenced_table=relation['referencedTable'],
                columns_references=relation['columnsReferences']
            )
            for relation in schema_relation['relations']
        ]

    def to_dict(self) -> Dict:
        """
        Converts the SchemaRelation object back to a dictionary matching the data structure.
        """
        return {
            'workspaceId': self.workspace_id,
            'datasourceId': self.datasource_id,
            'schema': self.schema,
            'relations': [relation.to_dict() for relation in self.relations],
        }

    def __repr__(self):
        return f"SchemaRelation(schema={self.schema}, relations={self.relations})"


class DatasourceRelations:
    def __init__(self, schema_relation: Dict):
        self.schema_relations = [SchemaRelation(item) for item in schema_relation]

    def __repr__(self):
        return (
            f"DatasourceRelations({self.schema_relations})"
        )

    def to_payload(self) -> List[Dict]:
        """
        Converts the DatasourceRelations object back to the original data object format.
        """
        return [schema_relation.to_dict() for schema_relation in self.schema_relations]

