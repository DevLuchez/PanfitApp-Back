def create_match_pipeline(limit=None, **kwargs):
    pipeline = [{"$match":kwargs}]
    if limit:
        pipeline.append({"$limit":limit})
    return pipeline