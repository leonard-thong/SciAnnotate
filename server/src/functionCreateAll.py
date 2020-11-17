

from utils import get_entity_index, clean_cached_config, add_common_info, merge_ann_files, GLOBAL_LOGGER, annotation_file_generate
from labelFunctionExecutor import _function_executor
from document import real_directory
from os.path import join as path_join
def function_create_annotation_all(**kwargs):
    collection = kwargs["collection"]
    documents = kwargs["document"]
    directory = collection
    real_dir = real_directory(directory)
    if type(kwargs["function[]"]) == str:
        kwargs["function[]"] = [kwargs["function[]"]]
    functions = list(kwargs["function[]"])
    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif document is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")
    if documents[0] == 'All':
        dirs = os.listdir(real_dir)
        for document in dirs:
            clean_cached_config()
            out = _function_executor(collection, document, functions)
            out["document"] = document
            out["collection"] = collection
            if out is None:
                continue
    elif documents[0] == 'All_collection':
        dirs = os.listdir(real_dir)
        for document in dirs:
            clean_cached_config()
            out = _function_executor(collection, document, functions)
            out["document"] = document
            out["collection"] = collection
            if out is None:
                continue
    else:
        for document in documents:
            clean_cached_config()
            out = _function_executor(collection, document, functions)
            out["document"] = document
            out["collection"] = collection
            if out is None:
                continue
    return out