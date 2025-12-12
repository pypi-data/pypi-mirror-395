"""
LangChain Hub-compatible implementation for triplet extraction pipeline.

This module provides a serializable, shareable version using LCEL (LangChain Expression Language)
that can be pushed to LangChain Hub and used by other users.

The pipeline is designed to be:
- Serializable: Can be saved/loaded using LangChain's serialization
- Shareable: Can be pushed to LangChain Hub
- Modular: Prompts can be loaded from LangChain Hub
- Injectable: Database dependencies are injected at runtime
"""

from typing import Dict, List, Tuple, Optional, Any
from unidecode import unidecode
import re
import logging
import json

from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate, load_prompt
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_hub import Client

logger = logging.getLogger('StructuredInferenceLangChainHub')
logger.setLevel(logging.DEBUG)


class TripletExtractionPipeline:
    """
    LangChain Hub-compatible triplet extraction pipeline.
    
    This class uses LCEL (LangChain Expression Language) to create a serializable
    pipeline that can be shared on LangChain Hub.
    
    Usage:
        # Load from LangChain Hub
        from langchain_hub import Client
        hub = Client()
        pipeline = hub.pull("your-username/triplet-extraction-pipeline")
        
        # Or use locally
        pipeline = TripletExtractionPipeline(
            llm=ChatOpenAI(),
            aligner=aligner,
            triplets_db=triplets_db,
            prompts_from_hub=True  # Load prompts from LangChain Hub
        )
    """
    
    def __init__(
        self,
        llm: ChatOpenAI,
        aligner: Any,
        triplets_db: Any,
        prompts_from_hub: bool = False,
        hub_username: Optional[str] = None,
        prompt_paths: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the pipeline.
        
        Args:
            llm: LangChain LLM instance
            aligner: Aligner instance for ontology alignment
            triplets_db: Triplets database instance
            prompts_from_hub: Whether to load prompts from LangChain Hub
            hub_username: Username for LangChain Hub (if prompts_from_hub=True)
            prompt_paths: Dictionary mapping prompt names to LangChain Hub paths
        """
        self.llm = llm
        self.aligner = aligner
        self.triplets_db = triplets_db
        self.prompts_from_hub = prompts_from_hub
        self.hub_username = hub_username or "default"
        
        # Load prompts
        self.prompts = self._load_prompts(prompt_paths)
        
        # Create the pipeline using LCEL
        self.pipeline = self._create_pipeline()
    
    def _load_prompts(self, prompt_paths: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Load prompts from LangChain Hub or use defaults."""
        default_prompt_paths = {
            'triplet_extraction': f'{self.hub_username}/triplet-extraction',
            'entity_types_ranker': f'{self.hub_username}/entity-types-ranker',
            'relation_ranker': f'{self.hub_username}/relation-ranker',
            'subject_ranker': f'{self.hub_username}/subject-ranker',
            'object_ranker': f'{self.hub_username}/object-ranker',
        }
        
        prompt_paths = prompt_paths or default_prompt_paths
        prompts = {}
        
        if self.prompts_from_hub:
            hub = Client()
            for name, path in prompt_paths.items():
                try:
                    prompt_template = hub.pull(path)
                    prompts[name] = prompt_template
                    logger.info(f"Loaded prompt '{name}' from LangChain Hub: {path}")
                except Exception as e:
                    logger.warning(f"Could not load prompt '{name}' from Hub: {e}. Using default.")
                    # Fallback to local prompts if Hub fails
                    prompts[name] = self._get_default_prompt(name)
        else:
            # Use local prompts (from extractor or defaults)
            for name in prompt_paths.keys():
                prompts[name] = self._get_default_prompt(name)
        
        return prompts
    
    def _get_default_prompt(self, name: str) -> str:
        """Get default prompt text (fallback if Hub unavailable)."""
        # These would typically be loaded from local files
        # For now, return placeholder - user should provide these
        default_prompts = {
            'triplet_extraction': 'Extract knowledge graph triplets from text...',
            'entity_types_ranker': 'Select the most appropriate entity types...',
            'relation_ranker': 'Select the most appropriate relation...',
            'subject_ranker': 'Select the most appropriate subject name...',
            'object_ranker': 'Select the most appropriate object name...',
        }
        return default_prompts.get(name, '')
    
    def _create_pipeline(self) -> Runnable:
        """Create the LCEL pipeline."""
        
        # Step 1: Extract triplets
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompts['triplet_extraction']),
            ("human", 'Text: "{text}"')
        ])
        extract_chain = extract_prompt | self.llm | JsonOutputParser()
        
        # Step 2: Refine entity types
        refine_entity_types_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompts['entity_types_ranker']),
            ("human", """Text: "{text}"
Extracted Triplet: {triplet}
Candidate Subject Types: {candidate_subject_types}
Candidate Object Types: {candidate_object_types}""")
        ])
        refine_entity_types_chain = refine_entity_types_prompt | self.llm | JsonOutputParser()
        
        # Step 3: Refine relation
        refine_relation_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompts['relation_ranker']),
            ("human", """Text: "{text}"
Extracted Triplet: {triplet}
Candidate relations: {candidate_relations}""")
        ])
        refine_relation_chain = refine_relation_prompt | self.llm | JsonOutputParser()
        
        # Step 4: Refine subject name
        refine_subject_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompts['subject_ranker']),
            ("human", """Text: "{text}"
Role: user
Extracted Triplet: {triplet}
Original Subject: {original_subject}
Candidate Subjects: {candidate_subjects}""")
        ])
        refine_subject_chain = refine_subject_prompt | self.llm | StrOutputParser()
        
        # Step 5: Refine object name
        refine_object_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompts['object_ranker']),
            ("human", """Text: "{text}"
Role: user
Extracted Triplet: {triplet}
Original Object: {original_object}
Candidate Objects: {candidate_objects}""")
        ])
        refine_object_chain = refine_object_prompt | self.llm | StrOutputParser()
        
        # Return the chains (they will be used in the main method)
        return {
            'extract': extract_chain,
            'refine_entity_types': refine_entity_types_chain,
            'refine_relation': refine_relation_chain,
            'refine_subject': refine_subject_chain,
            'refine_object': refine_object_chain,
        }
    
    def extract_triplets_with_ontology_filtering(
        self,
        text: str,
        sample_id: str,
        source_text_id: Optional[str] = None
    ) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
        """
        Extract and refine knowledge graph triplets from text.
        
        This method follows the same workflow as the original but uses LCEL chains.
        """
        # Step 1: Extract triplets
        extracted_result = self.pipeline['extract'].invoke({"text": text})
        
        # Parse result
        if isinstance(extracted_result, dict) and 'triplets' in extracted_result:
            extracted_triplets = extracted_result['triplets']
        elif isinstance(extracted_result, list):
            extracted_triplets = extracted_result
        else:
            logger.error(f"Unexpected format: {extracted_result}")
            return [], [], [], []
        
        # Prepare initial triplets
        initial_triplets = []
        for triplet in extracted_triplets:
            triplet['source_text_id'] = source_text_id
            triplet['sample_id'] = sample_id
            initial_triplets.append(triplet.copy())
        
        final_triplets = []
        filtered_triplets = []
        ontology_filtered_triplets = []
        
        # Process each triplet
        for triplet in extracted_triplets:
            try:
                # Step 2: Get candidate entity types
                subj_type_ids, obj_type_ids = self.aligner.retrieve_similar_entity_types(triplet=triplet)
                entity_type_id_2_label = self.aligner.retrieve_entity_type_labels(
                    subj_type_ids + obj_type_ids
                )
                candidate_subject_types = [entity_type_id_2_label[t] for t in subj_type_ids]
                candidate_object_types = [entity_type_id_2_label[t] for t in obj_type_ids]
                
                # Step 3: Refine entity types (if needed)
                if triplet['subject_type'] in candidate_subject_types and \
                   triplet['object_type'] in candidate_object_types:
                    refined_subject_type = triplet['subject_type']
                    refined_object_type = triplet['object_type']
                else:
                    refine_subj_types = candidate_subject_types
                    refine_obj_types = candidate_object_types
                    if triplet['subject_type'] in candidate_subject_types:
                        refine_subj_types = [triplet['subject_type']]
                    if triplet['object_type'] in candidate_object_types:
                        refine_obj_types = [triplet['object_type']]
                    
                    triplet_filtered = {k: triplet[k] for k in 
                                      ['subject', 'relation', 'object', 'subject_type', 'object_type']}
                    refined_result = self.pipeline['refine_entity_types'].invoke({
                        "text": text,
                        "triplet": json.dumps(triplet_filtered, ensure_ascii=False),
                        "candidate_subject_types": json.dumps(refine_subj_types, ensure_ascii=False),
                        "candidate_object_types": json.dumps(refine_obj_types, ensure_ascii=False)
                    })
                    refined_subject_type = refined_result.get('subject_type', triplet['subject_type'])
                    refined_object_type = refined_result.get('object_type', triplet['object_type'])
                
                # Step 4: Refine relation (if needed)
                if refined_subject_type in candidate_subject_types and \
                   refined_object_type in candidate_object_types:
                    entity_type_label_2_id = {v: k for k, v in entity_type_id_2_label.items()}
                    refined_subject_type_id = entity_type_label_2_id[refined_subject_type]
                    refined_object_type_id = entity_type_label_2_id[refined_object_type]
                    
                    relation_direction_candidate_pairs = \
                        self.aligner.retrieve_properties_for_entity_type(
                            target_relation=triplet['relation'],
                            object_types=[refined_object_type_id],
                            subject_types=[refined_subject_type_id],
                            k=10
                        )
                    # Get property labels and constraints
                    prop_2_label_and_constraint = self.aligner.retrieve_properties_labels_and_constraints(
                        property_id_list=[p[0] for p in relation_direction_candidate_pairs]
                    )
                    candidate_relations = [
                        prop_2_label_and_constraint[p[0]]['label'] 
                        for p in relation_direction_candidate_pairs
                    ]
                    
                    if triplet['relation'] in candidate_relations:
                        refined_relation = triplet['relation']
                    else:
                        triplet_filtered = {k: triplet[k] for k in 
                                          ['subject', 'relation', 'object', 'subject_type', 'object_type']}
                        refined_result = self.pipeline['refine_relation'].invoke({
                            "text": text,
                            "triplet": json.dumps(triplet_filtered, ensure_ascii=False),
                            "candidate_relations": json.dumps(candidate_relations, ensure_ascii=False)
                        })
                        refined_relation = refined_result.get('relation', triplet['relation'])
                else:
                    refined_relation = triplet['relation']
                    prop_2_label_and_constraint = {}
                    candidate_relations = []
                
                # Step 5: Determine direction and build backbone
                if refined_relation in candidate_relations:
                    refined_relation_id = [
                        p_id for p_id in prop_2_label_and_constraint 
                        if prop_2_label_and_constraint[p_id]['label'] == refined_relation
                    ][0]
                    refined_relation_directions = [
                        p[1] for p in relation_direction_candidate_pairs 
                        if p[0] == refined_relation_id
                    ]
                    direction = 'direct' if 'direct' in refined_relation_directions else 'inverse'
                else:
                    direction = 'direct'
                
                backbone_triplet = {
                    "subject": triplet['subject'] if direction == 'direct' else triplet['object'],
                    "relation": refined_relation,
                    "object": triplet['object'] if direction == 'direct' else triplet['subject'],
                    "subject_type": refined_subject_type,
                    "object_type": refined_object_type,
                    "qualifiers": triplet.get('qualifiers', [])
                }
                
                # Step 6: Refine entity names
                if refined_subject_type in candidate_subject_types:
                    refined_subject = self._refine_entity_name(
                        text, backbone_triplet, sample_id, is_object=False
                    )
                else:
                    refined_subject = triplet['subject']
                
                if refined_object_type in candidate_object_types:
                    refined_object = self._refine_entity_name(
                        text, backbone_triplet, sample_id, is_object=True
                    )
                else:
                    refined_object = triplet['object']
                
                backbone_triplet['subject'] = refined_subject
                backbone_triplet['object'] = refined_object
                backbone_triplet['source_text_id'] = source_text_id
                backbone_triplet['sample_id'] = sample_id
                
                # Step 7: Validate
                is_valid, exception_msg = self._validate_backbone(
                    refined_subject_type, refined_object_type, refined_relation,
                    candidate_subject_types, candidate_object_types,
                    candidate_relations, prop_2_label_and_constraint
                )
                
                if is_valid:
                    final_triplets.append(backbone_triplet)
                else:
                    backbone_triplet['exception_text'] = exception_msg
                    ontology_filtered_triplets.append(backbone_triplet)
            
            except Exception as e:
                logger.error(f"Error processing triplet: {e}")
                filtered_triplets.append({
                    **triplet,
                    'exception_text': str(e),
                    'source_text_id': source_text_id,
                    'sample_id': sample_id
                })
        
        return initial_triplets, final_triplets, filtered_triplets, ontology_filtered_triplets
    
    def _refine_entity_name(
        self, text: str, triplet: Dict, sample_id: str, is_object: bool = False
    ) -> str:
        """Refine entity name using LCEL chain."""
        if is_object:
            entity = unidecode(triplet['object'])
            entity_type = triplet['object_type']
            entity_hierarchy = self.aligner.retrieve_entity_type_hierarchy(entity_type)
        else:
            entity = unidecode(triplet['subject'])
            entity_type = triplet['subject_type']
            entity_hierarchy = []
        
        if any([t in ['Q186408', 'Q309314'] for t in entity_hierarchy]):
            return entity
        
        similar_entities = self.aligner.retrieve_entity_by_type(
            entity_name=entity, entity_type=entity_type, sample_id=sample_id
        )
        
        if len(similar_entities) == 0:
            return entity
        
        if entity in similar_entities:
            return similar_entities[entity]
        
        # Use chain to refine
        triplet_filtered = {k: triplet[k] for k in ['subject', 'relation', 'object']}
        if is_object:
            refined = self.pipeline['refine_object'].invoke({
                "text": text,
                "triplet": json.dumps(triplet_filtered, ensure_ascii=False),
                "original_object": entity,
                "candidate_objects": json.dumps(list(similar_entities.values()), ensure_ascii=False)
            })
        else:
            refined = self.pipeline['refine_subject'].invoke({
                "text": text,
                "triplet": json.dumps(triplet_filtered, ensure_ascii=False),
                "original_subject": entity,
                "candidate_subjects": json.dumps(list(similar_entities.values()), ensure_ascii=False)
            })
        
        updated_entity = unidecode(refined.strip())
        updated_entity = re.sub(r'^["\']|["\']$', '', updated_entity)
        
        if re.sub(r'[^\w\s]', '', updated_entity) == 'None':
            updated_entity = entity
        
        self.aligner.add_entity(
            entity_name=updated_entity,
            alias=entity,
            entity_type=entity_type,
            sample_id=sample_id
        )
        
        return updated_entity
    
    def _validate_backbone(
        self, refined_subject_type: str, refined_object_type: str, refined_relation: str,
        candidate_subject_types: List[str], candidate_object_types: List[str],
        candidate_relations: List[str], prop_2_label_and_constraint: Dict
    ) -> Tuple[bool, str]:
        """Validate backbone triplet."""
        exception_msg = ''
        if refined_relation not in candidate_relations:
            exception_msg += "Refined relation not in candidate relations\n"
        if refined_subject_type not in candidate_subject_types:
            exception_msg += "Refined subject type not in candidate subject types\n"
        if refined_object_type not in candidate_object_types:
            exception_msg += "Refined object type not in candidate object types\n"
        
        if exception_msg:
            return False, exception_msg
        
        subject_hierarchy = self.aligner.retrieve_entity_type_hierarchy(refined_subject_type)
        object_hierarchy = self.aligner.retrieve_entity_type_hierarchy(refined_object_type)
        
        prop_subj_ids = [
            prop_2_label_and_constraint[prop]['valid_subject_type_ids']
            for prop in prop_2_label_and_constraint
            if prop_2_label_and_constraint[prop]['label'] == refined_relation
        ][0]
        prop_obj_ids = [
            prop_2_label_and_constraint[prop]['valid_object_type_ids']
            for prop in prop_2_label_and_constraint
            if prop_2_label_and_constraint[prop]['label'] == refined_relation
        ][0]
        
        if prop_subj_ids == ['ANY']:
            prop_subj_ids = subject_hierarchy
        if prop_obj_ids == ['ANY']:
            prop_obj_ids = object_hierarchy
        
        if any([t in subject_hierarchy for t in prop_subj_ids]) and \
           any([t in object_hierarchy for t in prop_obj_ids]):
            return True, ''
        else:
            return False, 'Triplet backbone violates property constraints\n'

