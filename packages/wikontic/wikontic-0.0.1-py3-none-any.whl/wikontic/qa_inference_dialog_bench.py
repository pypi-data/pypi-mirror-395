from utils.inference_with_db import InferenceWithDB
from utils.openai_utils import LLMTripletExtractor
from utils.dynamic_aligner import Aligner
import json

with open('datasets/memory_benchmark.json', 'r') as f:
    bench = json.load(f)

from pymongo.mongo_client import MongoClient
from tqdm import tqdm

def get_mongo_client(mongo_uri):
    client = MongoClient(mongo_uri)
    return client

mongo_client = get_mongo_client("mongodb://localhost:27018/?directConnection=true")

triplets_db = mongo_client.get_database('dialog_eval_qwen')
unique_sample_ids = triplets_db.get_collection('triplets').distinct('sample_id')

# model_name = 'Meta-llama/Llama-3.3-70B-Instruct'
model_name = 'qwen/qwen3-32b'

aligner = Aligner(triplets_db=triplets_db)
extractor = LLMTripletExtractor(model=model_name, hotpot=False)
inference_with_db = InferenceWithDB(extractor=extractor, aligner=aligner, triplets_db=triplets_db)

id2ans = {}
K = 10
print("K: ", K)
for sample_id in tqdm(unique_sample_ids):
    for elem in bench[sample_id]['qa']:
        try:
            question = elem['question']
            answer = elem['answer']
            entities = inference_with_db.identify_relevant_entities_from_question(question, str(sample_id))
            supporting_triplets, ans = inference_with_db.answer_question(question=question, relevant_entities=entities, use_qualifiers=True, k=K, sample_id=sample_id)
            print(question, " | ", ans, " | ", answer)
            with open(f'results_dialog_bench/qa_inference_dialog_bench_K={K}.jsonlines', 'a') as f:
                f.write(json.dumps({
                    'question': question,
                    'answer': answer,
                    # 'supporting_triplets': supporting_triplets,
                    'ans': ans
                }, ensure_ascii=False) + '\n')
        except Exception as e:
            print(e)
            continue