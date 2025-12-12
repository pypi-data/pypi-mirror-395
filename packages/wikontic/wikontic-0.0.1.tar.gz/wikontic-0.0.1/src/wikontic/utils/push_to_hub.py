"""
Script to push prompts and pipeline to LangChain Hub.

Usage:
    python utils/push_to_hub.py --username your-username
"""

import argparse
from pathlib import Path
from langchain_hub import Client
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import json


def push_prompts_to_hub(username: str, prompts_dir: str = "utils/prompts"):
    """Push all prompts to LangChain Hub."""
    
    hub = Client()
    
    # Map of prompt names to their file paths
    prompts_to_push = {
        'triplet-extraction': {
            'path': 'triplet_extraction/propmt_1_types_qualifiers.txt',
            'description': 'Prompt for extracting knowledge graph triplets from text with types and qualifiers',
            'template_type': 'chat'  # or 'text'
        },
        'entity-types-ranker': {
            'path': 'ontology_refinement/prompt_choose_entity_types.txt',
            'description': 'Prompt for ranking and selecting appropriate entity types from candidates',
            'template_type': 'chat'
        },
        'relation-ranker': {
            'path': 'ontology_refinement/prompt_choose_relation.txt',
            'description': 'Prompt for ranking and selecting appropriate relations from candidates',
            'template_type': 'chat'
        },
        'subject-ranker': {
            'path': 'name_refinement/rank_subject_names.txt',
            'description': 'Prompt for ranking and selecting appropriate subject entity names from candidates',
            'template_type': 'chat'
        },
        'object-ranker': {
            'path': 'name_refinement/rank_object_names.txt',
            'description': 'Prompt for ranking and selecting appropriate object entity names from candidates',
            'template_type': 'chat'
        },
    }
    
    prompts_path = Path(prompts_dir)
    
    for prompt_name, prompt_info in prompts_to_push.items():
        prompt_file = prompts_path / prompt_info['path']
        
        if not prompt_file.exists():
            print(f"Warning: Prompt file not found: {prompt_file}")
            continue
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        
        # Create appropriate prompt template
        if prompt_info['template_type'] == 'chat':
            # For chat prompts, we create a system message template
            # Users will need to add the human message with their input
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", prompt_content)
            ])
        else:
            prompt_template = PromptTemplate.from_template(prompt_content)
        
        repo_id = f"{username}/{prompt_name}"
        
        try:
            # Push to hub
            result = hub.push(
                repo_id=repo_id,
                object=prompt_template,
                description=prompt_info['description']
            )
            print(f"✓ Successfully pushed {repo_id}")
            print(f"  Description: {prompt_info['description']}")
        except Exception as e:
            print(f"✗ Failed to push {repo_id}: {e}")
    
    print("\n" + "="*50)
    print("Prompts pushed! Users can now load them with:")
    print(f"  hub.pull('{username}/triplet-extraction')")
    print(f"  hub.pull('{username}/entity-types-ranker')")
    print("  etc.")


def create_pipeline_metadata(username: str, output_file: str = "pipeline_metadata.json"):
    """Create metadata file for the complete pipeline."""
    
    metadata = {
        "name": "triplet-extraction-pipeline",
        "version": "0.1.0",
        "description": "Sequential pipeline for extracting and refining knowledge graph triplets from text",
        "author": username,
        "prompts": {
            "triplet_extraction": f"{username}/triplet-extraction",
            "entity_types_ranker": f"{username}/entity-types-ranker",
            "relation_ranker": f"{username}/relation-ranker",
            "subject_ranker": f"{username}/subject-ranker",
            "object_ranker": f"{username}/object-ranker",
        },
        "dependencies": {
            "langchain": ">=0.1.0",
            "langchain-openai": ">=0.1.0",
            "langchain-hub": ">=0.1.0",
        },
        "usage": {
            "import": "from utils.structured_inference_langchain_hub import TripletExtractionPipeline",
            "example": """
from langchain_openai import ChatOpenAI
from utils.structured_inference_langchain_hub import TripletExtractionPipeline

llm = ChatOpenAI(model="gpt-4o")
pipeline = TripletExtractionPipeline(
    llm=llm,
    aligner=your_aligner,
    triplets_db=your_triplets_db,
    prompts_from_hub=True,
    hub_username="{}"
)

initial, final, filtered, ontology_filtered = pipeline.extract_triplets_with_ontology_filtering(
    text="Your text here",
    sample_id="sample_123"
)
""".format(username)
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Created pipeline metadata: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Push prompts to LangChain Hub")
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="Your LangChain Hub username"
    )
    parser.add_argument(
        "--prompts-dir",
        type=str,
        default="utils/prompts",
        help="Directory containing prompt files"
    )
    parser.add_argument(
        "--create-metadata",
        action="store_true",
        help="Create pipeline metadata file"
    )
    
    args = parser.parse_args()
    
    print(f"Pushing prompts to LangChain Hub as: {args.username}")
    print("="*50)
    
    push_prompts_to_hub(args.username, args.prompts_dir)
    
    if args.create_metadata:
        create_pipeline_metadata(args.username)


if __name__ == "__main__":
    main()

