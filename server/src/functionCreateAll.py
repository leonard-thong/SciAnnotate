

from utils import get_entity_index, clean_cached_config, add_common_info, merge_ann_files, GLOBAL_LOGGER, annotation_file_generate
from labelFunctionExecutor import _function_executor
from document import real_directory
from os.path import join as path_join

def function_create_annotation_all(**kwargs):
    directory = kwargs["collection"]
    documents = kwargs["documents"]
    real_dir = real_directory(directory)

    if type(kwargs["function[]"]) == str:
        kwargs["function[]"] = [kwargs["function[]"]]
    functions = list(kwargs["function[]"])

    if collection is None:
        GLOBAL_LOGGER.log_error("INVALID DIRECTORY")
    elif documents is None:
        GLOBAL_LOGGER.log_error("INVALID DOCUMENT, CANNOT FETCH DOCUMENT")

    # all_collections: for all collection
    if documents[0] == 'all_collections':
        dirs = os.listdir('/')
        # get all collections, and loop through all the collection
        doucments_temp = []
        for root, dirs, files in os.walk(dirs  ):
            for file in files:
                if(file.endswith(".txt")):
                    doucments_temp.append(os.path.join(root,file))
        GLOBAL_LOGGER.log_normal(doucments_temp)
        for document in doucments_temp:
            clean_cached_config()
            collection = document.replace(document_name,'')
            collection = collection[:-1]
            out = _function_executor(collection, document, functions)
            out["document"] = document
            out["collection"] = collection
            if out is None:
                continue
    # all_documents: all documents in the collection
    elif documents[0] == 'all_documents':
        dirs = os.listdir(real_dir)
        for document in dirs:
            if document[-4:] == ".txt":
                clean_cached_config()
                out = _function_executor(collection, document, functions)
                out["document"] = document
                out["collection"] = collection
                if out is None:
                    continue
    # else expects list of documents
    else:
        for document in documents:
            name_list = document.split('/')
            document_name = name_list[-1]
            collection = document.replace(document_name,'')
            collection = collection[:-1]
            clean_cached_config()
            out = _function_executor(collection, document_name, functions)
            out["document"] = document_name
            out["collection"] = collection
            if out is None:
                continue
    return out