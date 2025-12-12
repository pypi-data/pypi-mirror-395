from cidc_api.models.pydantic.stage2 import all_models
from cidc_api.models.db.stage2 import all_models as all_db_models

standard_data_categories = [model.__data_category__ for model in all_models if hasattr(model, "__data_category__")]


# A class to hold the representation of a trial's dataset all at once
class Dataset(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for data_category in standard_data_categories:
            self[data_category] = []


# Maps data categories like "treatment" to their associated pydantic model
data_category_to_model = {model.__data_category__: model for model in all_models if hasattr(model, "__data_category__")}
data_category_to_db_model = {
    model.__data_category__: model for model in all_db_models if hasattr(model, "__data_category__")
}
