def get_schema_map(schema):
    return schema.model_dump(mode='json', exclude_defaults=True)
