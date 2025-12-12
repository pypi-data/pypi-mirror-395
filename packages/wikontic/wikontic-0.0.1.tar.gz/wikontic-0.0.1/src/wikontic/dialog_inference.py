import json
from tqdm import tqdm
import argparse
import warnings
from pymongo.mongo_client import MongoClient
import logging
import re

logger = logging.getLogger('DialogEval')
logger.setLevel(logging.DEBUG)

from utils.openai_utils import LLMTripletExtractor
from utils.inference_with_db import InferenceWithDB
from utils.dynamic_aligner import Aligner as DynamicDBAligner

warnings.filterwarnings('ignore')

def get_mongo_client(mongo_uri):
    client = MongoClient(mongo_uri)
    return client

def get_dataset(dataset_path):
    with open(dataset_path, "r") as f:
        ds = json.load(f)
    return ds

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo_uri", type=str, default="mongodb://localhost:27018/?directConnection=true")
    parser.add_argument("--triplets_db_name", type=str, default="triplets_db")
    parser.add_argument("--model_name", type=str, default="gpt-4o-mini")
    parser.add_argument("--dataset_path", type=str, default="datasets/memory_benchmark.json")
    parser.add_argument("--num_samples", type=int, default=50)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    
    mongo_client = get_mongo_client(args.mongo_uri)
    triplets_db = mongo_client.get_database(args.triplets_db_name)
    model_name = args.model_name
    dataset_path = args.dataset_path
    num_samples = args.num_samples

    ds = get_dataset(dataset_path)
    logger.info("Structured inference disabled, using dynamic inference")

    aligner = DynamicDBAligner(triplets_db=triplets_db)
    extractor = LLMTripletExtractor(model=model_name)
    inference_with_db = InferenceWithDB(extractor=extractor, aligner=aligner, triplets_db=triplets_db)

    ds = ds[:num_samples]

    for user_id, user_dialog in enumerate(ds):
        id2dialog_line = {}

        for session_id in user_dialog['conversation']:
            if re.fullmatch("session_[\d]+", session_id, flags=0):
                for dialog_line in user_dialog['conversation'][session_id]:
                    dialog_line['date_time'] = user_dialog['conversation'][session_id+"_date_time"]
                    id2dialog_line[dialog_line['dia_id']] = dialog_line
                
            else:
                continue
        
        dialog_ids = list(id2dialog_line.keys())
    
        for dialog_id in tqdm(dialog_ids, total=len(dialog_ids)):

            dialog = id2dialog_line[dialog_id]
            if dialog['speaker'] == 'assistant':
                continue
            
            text = dialog['text']
            
            try:
                initial_triplets, final_triplets, filtered_triplets = inference_with_db.extract_triplets(text, role=dialog['speaker'], sample_id=str(user_id), source_text_id=str(dialog_id))
 
                for triplet in initial_triplets:
                    triplet['date_time'] = dialog['date_time']
                    triplet['role'] = dialog['speaker']
                
                for triplet in final_triplets:
                    triplet['date_time'] = dialog['date_time']
                    triplet['role'] = dialog['speaker']
                
                for triplet in filtered_triplets:
                    triplet['date_time'] = dialog['date_time']
                    triplet['role'] = dialog['speaker']

                if len(initial_triplets) > 0:
                    aligner.add_initial_triplets(initial_triplets, sample_id=user_id)
                if len(final_triplets) > 0:
                    aligner.add_triplets(final_triplets, sample_id=user_id)
                if len(filtered_triplets) > 0:
                    aligner.add_filtered_triplets(filtered_triplets, sample_id=user_id)

                print("CURRENT COST: ", extractor.calculate_cost())
            
            except Exception as e:
                logger.error("Error extracting triplets: %s" % (str(e)))
                continue