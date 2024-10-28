from bson import ObjectId

def create_match_pipeline(limit=None, **kwargs):
    pipeline = [{"$match":kwargs}]
    if limit:
        pipeline.append({"$limit":limit})
    return pipeline

def in_multiples_id_pipeline(id_list: list[ObjectId]) -> dict:
    return [{
        "_id":{"$in":id_list}
    }]