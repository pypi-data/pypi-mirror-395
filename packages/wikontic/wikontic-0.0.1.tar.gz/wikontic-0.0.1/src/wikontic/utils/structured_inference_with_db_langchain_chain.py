"""
LangChain Chain-based implementation for extract_triplets_with_ontology_filtering.

This module provides a sequential, strict pipeline using LangChain chains where each step
has its own prompt, following the exact workflow of the original method.

The pipeline is composed of sequential chains that process triplets through:
1. Triplet extraction
2. Entity type refinement
3. Relation refinement
4. Entity name refinement
5. Validation

Each step uses LangChain's LLMChain with custom prompts, making it convenient for
LangChain users while maintaining the strict sequential flow.

Key Features:
- Sequential and strict: Follows the exact same workflow as the original method
- Separate prompts: Each LLM step uses its own prompt from the extractor
- LangChain-native: Uses LangChain's chain abstraction for easy integration
- Same interface: Drop-in replacement for the original method

Usage:
    from utils.structured_inference_with_db_langchain_chain import StructuredInferenceWithDBLangChainChain
    
    chain_pipeline = StructuredInferenceWithDBLangChainChain(extractor, aligner, triplets_db)
    initial, final, filtered, ontology_filtered = chain_pipeline.extract_triplets_with_ontology_filtering(
        text="...", sample_id="..."
    )
"""

from typing import Dict, List, Tuple, Optional
from unidecode import unidecode
import re
import logging
import json

from langchain.chains import LLMChain, SequentialChain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

logger = logging.getLogger('StructuredInferenceWithDBLangChainChain')
logger.setLevel(logging.DEBUG)


class StructuredInferenceWithDBLangChainChain:
    """
    Sequential LangChain chain implementation of StructuredInferenceWithDB.
    
    This class uses LangChain chains to create a strict, sequential pipeline
    where each step has its own prompt and LLM chain.
    """
    
    def __init__(
        self, 
        extractor, 
        aligner, 
        triplets_db, 
        llm_model: str = "gpt-4o", 
        temperature: float = 0
    ):
        """
        Initialize the LangChain chain pipeline.
        
        Args:
            extractor: The LLMTripletExtractor instance (for prompts and token tracking)
            aligner: The Aligner instance
            triplets_db: The triplets database instance
            llm_model: The LLM model to use for all chains
            temperature: The temperature for the LLM
        """
        self.extractor = extractor
        self.aligner = aligner
        self.triplets_db = triplets_db
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        
        # Create chains for each step
        self._create_chains()
    
    def _create_chains(self):
        """Create LangChain chains for each step of the pipeline."""
        
        # Chain 1: Extract triplets from text
        self.extract_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", self.extractor.prompts['triplet_extraction']),
                ("human", 'Text: "{text}"')
            ]),
            output_key="extracted_triplets",
            output_parser=JsonOutputParser(),
            verbose=True
        )
        
        # Chain 2: Refine entity types
        self.refine_entity_types_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", self.extractor.prompts['entity_types_ranker']),
                ("human", """Text: "{text}"
Extracted Triplet: {triplet}
Candidate Subject Types: {candidate_subject_types}
Candidate Object Types: {candidate_object_types}""")
            ]),
            output_key="refined_entity_types",
            output_parser=JsonOutputParser(),
            verbose=True
        )
        
        # Chain 3: Refine relation
        self.refine_relation_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", self.extractor.prompts['relation_ranker']),
                ("human", """Text: "{text}"
Extracted Triplet: {triplet}
Candidate relations: {candidate_relations}""")
            ]),
            output_key="refined_relation",
            output_parser=JsonOutputParser(),
            verbose=True
        )
        
        # Chain 4: Refine subject name
        self.refine_subject_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", self.extractor.prompts['subject_ranker']),
                ("human", """Text: "{text}"
Role: user
Extracted Triplet: {triplet}
Original Subject: {original_subject}
Candidate Subjects: {candidate_subjects}""")
            ]),
            output_key="refined_subject",
            output_parser=StrOutputParser(),
            verbose=True
        )
        
        # Chain 5: Refine object name
        self.refine_object_chain = LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", self.extractor.prompts['object_ranker']),
                ("human", """Text: "{text}"
Role: user
Extracted Triplet: {triplet}
Original Object: {original_object}
Candidate Objects: {candidate_objects}""")
            ]),
            output_key="refined_object",
            output_parser=StrOutputParser(),
            verbose=True
        )
    
    def extract_triplets_with_ontology_filtering(
        self, 
        text: str, 
        sample_id: str, 
        source_text_id: Optional[str] = None
    ) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
        """
        Extract and refine knowledge graph triplets from text using sequential LangChain chains.
        
        This method follows the exact sequential workflow of the original implementation,
        but uses LangChain chains for LLM interactions.
        
        Args:
            text: Input text to extract triplets from
            sample_id: Sample ID for tracking
            source_text_id: Optional source text ID
            
        Returns:
            tuple: (initial_triplets, final_triplets, filtered_triplets, ontology_filtered_triplets)
        """
        # Reset extractor state
        self.extractor.reset_tokens()
        self.extractor.reset_messages()
        self.extractor.reset_error_state()
        
        # Step 1: Extract triplets using LangChain chain
        extracted_result = self.extract_chain.run(text=text)
        
        # Parse the result (handle both dict and string formats)
        if isinstance(extracted_result, str):
            try:
                extracted_result = json.loads(extracted_result)
            except json.JSONDecodeError:
                # Try to extract JSON from text
                json_match = re.search(r'\{.*\}', extracted_result, re.DOTALL)
                if json_match:
                    extracted_result = json.loads(json_match.group(0))
                else:
                    logger.error(f"Could not parse extracted triplets: {extracted_result}")
                    return [], [], [], []
        
        # Handle different response formats
        if isinstance(extracted_result, dict) and 'triplets' in extracted_result:
            extracted_triplets = extracted_result['triplets']
        elif isinstance(extracted_result, list):
            extracted_triplets = extracted_result
        else:
            logger.error(f"Unexpected format for extracted triplets: {extracted_result}")
            return [], [], [], []
        
        # Prepare initial triplets with metadata
        initial_triplets = []
        for triplet in extracted_triplets:
            triplet['prompt_token_num'], triplet['completion_token_num'] = self.extractor.calculate_used_tokens()
            triplet['source_text_id'] = source_text_id
            triplet['sample_id'] = sample_id
            initial_triplets.append(triplet.copy())
        
        final_triplets = []
        filtered_triplets = []
        ontology_filtered_triplets = []
        
        # Process each triplet through the sequential pipeline
        for triplet in extracted_triplets:
            self.extractor.reset_tokens()
            backbone_triplet = triplet.copy()
            
            try:
                logger.log(logging.DEBUG, "Triplet: %s\n%s" % (str(triplet), "-" * 100))
                
                # ___________________________ Step 2: Refine entity types ___________________________
                subj_type_ids, obj_type_ids = self.get_candidate_entity_type_ids(triplet)
                
                entity_type_id_2_label = self.get_candidate_entity_labels(
                    subj_type_ids=subj_type_ids, obj_type_ids=obj_type_ids
                )
                entity_type_label_2_id = {
                    entity_label: entity_id 
                    for entity_id, entity_label in entity_type_id_2_label.items()
                }
                
                candidate_subject_types = [entity_type_id_2_label[t] for t in subj_type_ids]
                candidate_object_types = [entity_type_id_2_label[t] for t in obj_type_ids]
                
                # Check if refinement is needed
                if triplet['subject_type'] in candidate_subject_types and \
                   triplet['object_type'] in candidate_object_types:
                    refined_subject_type, refined_object_type = triplet['subject_type'], triplet['object_type']
                else:
                    # Prepare candidate types (only refine what's needed)
                    refine_subj_types = candidate_subject_types
                    refine_obj_types = candidate_object_types
                    
                    if triplet['subject_type'] in candidate_subject_types:
                        refine_subj_types = [triplet['subject_type']]
                    if triplet['object_type'] in candidate_object_types:
                        refine_obj_types = [triplet['object_type']]
                    
                    # Use LangChain chain to refine entity types
                    self.extractor.reset_error_state()
                    triplet_filtered = {k: triplet[k] for k in 
                                      ['subject', 'relation', 'object', 'subject_type', 'object_type']}
                    refined_result = self.refine_entity_types_chain.run(
                        text=text,
                        triplet=json.dumps(triplet_filtered, ensure_ascii=False),
                        candidate_subject_types=json.dumps(refine_subj_types, ensure_ascii=False),
                        candidate_object_types=json.dumps(refine_obj_types, ensure_ascii=False)
                    )
                    
                    # Parse result
                    if isinstance(refined_result, str):
                        try:
                            refined_result = json.loads(refined_result)
                        except json.JSONDecodeError:
                            json_match = re.search(r'\{.*\}', refined_result, re.DOTALL)
                            if json_match:
                                refined_result = json.loads(json_match.group(0))
                    
                    refined_subject_type = refined_result.get('subject_type', triplet['subject_type'])
                    refined_object_type = refined_result.get('object_type', triplet['object_type'])
                
                # ___________________________ Step 3: Refine relation ___________________________
                if refined_subject_type in candidate_subject_types and \
                   refined_object_type in candidate_object_types:
                    refined_subject_type_id = entity_type_label_2_id[refined_subject_type]
                    refined_object_type_id = entity_type_label_2_id[refined_object_type]
                    
                    relation_direction_candidate_pairs, prop_2_label_and_constraint = \
                        self.get_candidate_entity_properties(
                            triplet=triplet,
                            subj_type_ids=[refined_subject_type_id],
                            obj_type_ids=[refined_object_type_id]
                        )
                    candidate_relations = [
                        prop_2_label_and_constraint[p[0]]['label'] 
                        for p in relation_direction_candidate_pairs
                    ]
                    
                    # Check if refinement is needed
                    if triplet['relation'] in candidate_relations:
                        refined_relation = triplet['relation']
                    else:
                        # Use LangChain chain to refine relation
                        self.extractor.reset_error_state()
                        triplet_filtered = {k: triplet[k] for k in 
                                          ['subject', 'relation', 'object', 'subject_type', 'object_type']}
                        refined_result = self.refine_relation_chain.run(
                            text=text,
                            triplet=json.dumps(triplet_filtered, ensure_ascii=False),
                            candidate_relations=json.dumps(candidate_relations, ensure_ascii=False)
                        )
                        
                        # Parse result
                        if isinstance(refined_result, str):
                            try:
                                refined_result = json.loads(refined_result)
                            except json.JSONDecodeError:
                                json_match = re.search(r'\{.*\}', refined_result, re.DOTALL)
                                if json_match:
                                    refined_result = json.loads(json_match.group(0))
                        
                        refined_relation = refined_result.get('relation', triplet['relation'])
                else:
                    refined_relation = triplet['relation']
                    prop_2_label_and_constraint = {}
                    candidate_relations = []
                
                # ___________________________ Step 4: Determine relation direction ___________________________
                if refined_relation in candidate_relations:
                    refined_relation_id_candidates = [
                        p_id for p_id in prop_2_label_and_constraint 
                        if prop_2_label_and_constraint[p_id]['label'] == refined_relation
                    ]
                    refined_relation_id = refined_relation_id_candidates[0]
                    refined_relation_directions = [
                        p[1] for p in relation_direction_candidate_pairs 
                        if p[0] == refined_relation_id
                    ]
                    refined_relation_direction = 'direct' if 'direct' in refined_relation_directions else 'inverse'
                    
                    if refined_relation_direction == 'inverse':
                        refined_subject_type_id, refined_object_type_id = refined_object_type_id, refined_subject_type_id
                        refined_subject_type, refined_object_type = refined_object_type, refined_subject_type
                        candidate_subject_types, candidate_object_types = candidate_object_types, candidate_subject_types
                else:
                    refined_relation_direction = 'direct'
                
                # ___________________________ Step 5: Build backbone triplet ___________________________
                backbone_triplet = {
                    "subject": triplet['subject'] if refined_relation_direction == 'direct' else triplet['object'],
                    "relation": refined_relation,
                    "object": triplet['object'] if refined_relation_direction == 'direct' else triplet['subject'],
                    "subject_type": refined_subject_type,
                    "object_type": refined_object_type,
                }
                backbone_triplet['qualifiers'] = triplet.get('qualifiers', [])
                
                # ___________________________ Step 6: Refine entity names ___________________________
                if refined_subject_type in candidate_subject_types:
                    refined_subject = self.refine_entity_name_with_chain(
                        text, backbone_triplet, sample_id, is_object=False
                    )
                else:
                    refined_subject = triplet['subject']
                
                if refined_object_type in candidate_object_types:
                    refined_object = self.refine_entity_name_with_chain(
                        text, backbone_triplet, sample_id, is_object=True
                    )
                else:
                    refined_object = triplet['object']
                
                logger.log(logging.DEBUG, "Original subject name: %s\n%s" % (str(backbone_triplet['subject']), "-" * 100))
                logger.log(logging.DEBUG, "Original object name: %s\n%s" % (str(backbone_triplet['object']), "-" * 100))
                logger.log(logging.DEBUG, "Refined subject name: %s\n%s" % (str(refined_subject), "-" * 100))
                logger.log(logging.DEBUG, "Refined object name: %s\n%s" % (str(refined_object), "-" * 100))
                
                backbone_triplet['subject'] = refined_subject
                backbone_triplet['object'] = refined_object
                
                backbone_triplet['prompt_token_num'], backbone_triplet['completion_token_num'] = \
                    self.extractor.calculate_used_tokens()
                backbone_triplet['source_text_id'] = source_text_id
                backbone_triplet['sample_id'] = sample_id
                
                # ___________________________ Step 7: Validate backbone triplet ___________________________
                backbone_triplet_valid, backbone_triplet_exception_msg = self.validate_backbone(
                    backbone_triplet['subject_type'],
                    backbone_triplet['object_type'],
                    backbone_triplet['relation'],
                    candidate_subject_types,
                    candidate_object_types,
                    candidate_relations,
                    prop_2_label_and_constraint
                )
                
                if backbone_triplet_valid:
                    final_triplets.append(backbone_triplet.copy())
                    logger.log(logging.DEBUG, "Final triplet: %s\n%s" % (str(backbone_triplet), "-" * 100))
                else:
                    logger.log(logging.ERROR, "Final triplet is ontology filtered: %s\n%s" % (str(backbone_triplet), "-" * 100))
                    logger.log(logging.ERROR, "Exception: %s" % (str(backbone_triplet_exception_msg)))
                    backbone_triplet['candidate_subject_types'] = candidate_subject_types
                    backbone_triplet['candidate_object_types'] = candidate_object_types
                    backbone_triplet['candidate_relations'] = candidate_relations
                    backbone_triplet['exception_text'] = backbone_triplet_exception_msg
                    ontology_filtered_triplets.append(backbone_triplet.copy())
            
            except Exception as e:
                logger.log(logging.ERROR, f"Error processing triplet: {e}")
                backbone_triplet['prompt_token_num'], backbone_triplet['completion_token_num'] = \
                    self.extractor.calculate_used_tokens()
                backbone_triplet['source_text_id'] = source_text_id
                backbone_triplet['sample_id'] = sample_id
                backbone_triplet['exception_text'] = str(e)
                filtered_triplets.append(backbone_triplet.copy())
        
        return initial_triplets, final_triplets, filtered_triplets, ontology_filtered_triplets
    
    def refine_entity_name_with_chain(
        self, 
        text: str, 
        triplet: Dict, 
        sample_id: str, 
        is_object: bool = False
    ) -> str:
        """
        Refine entity name using LangChain chain.
        
        This method follows the same logic as the original but uses LangChain chains
        for the LLM refinement step.
        """
        self.extractor.reset_error_state()
        
        if is_object:
            entity = unidecode(triplet['object'])
            entity_type = triplet['object_type']
            entity_hierarchy = self.aligner.retrieve_entity_type_hierarchy(entity_type)
        else:
            entity = unidecode(triplet['subject'])
            entity_type = triplet['subject_type']
            entity_hierarchy = []
        
        # Do not change time or quantity entities (of objects!)
        if any([t in ['Q186408', 'Q309314'] for t in entity_hierarchy]):
            updated_entity = entity
        else:
            # Retrieve similar entities by type and name similarity
            similar_entities = self.aligner.retrieve_entity_by_type(
                entity_name=entity,
                entity_type=entity_type,
                sample_id=sample_id
            )
            
            # If there are similar entities -> refine entity name
            if len(similar_entities) > 0:
                # If exact match found -> return the exact match
                if entity in similar_entities:
                    updated_entity = similar_entities[entity]
                else:
                    # Use LangChain chain to refine entity name
                    if is_object:
                        refined_result = self.refine_object_chain.run(
                            text=text,
                            triplet=json.dumps({k: triplet[k] for k in ['subject', 'relation', 'object']}, ensure_ascii=False),
                            original_object=entity,
                            candidate_objects=json.dumps(list(similar_entities.values()), ensure_ascii=False)
                        )
                    else:
                        refined_result = self.refine_subject_chain.run(
                            text=text,
                            triplet=json.dumps({k: triplet[k] for k in ['subject', 'relation', 'object']}, ensure_ascii=False),
                            original_subject=entity,
                            candidate_subjects=json.dumps(list(similar_entities.values()), ensure_ascii=False)
                        )
                    
                    # Clean up the result
                    updated_entity = unidecode(refined_result.strip())
                    # Remove any JSON formatting if present
                    updated_entity = re.sub(r'^["\']|["\']$', '', updated_entity)
                    
                    # If the updated entity is None -> return the original entity
                    if re.sub(r'[^\w\s]', '', updated_entity) == 'None':
                        updated_entity = entity
            else:
                # If no similar entities -> return the original entity
                updated_entity = entity
        
        self.aligner.add_entity(
            entity_name=updated_entity,
            alias=entity,
            entity_type=entity_type,
            sample_id=sample_id
        )
        
        return updated_entity
    
    # Delegate methods to original implementation for non-LLM steps
    def get_candidate_entity_type_ids(
        self, triplet: Dict[str, str]
    ) -> Tuple[List[str], List[str]]:
        """Retrieve candidate subject and object entity type IDs."""
        subj_type_ids, obj_type_ids = self.aligner.retrieve_similar_entity_types(triplet=triplet)
        return subj_type_ids, obj_type_ids
    
    def get_candidate_entity_labels(
        self,
        subj_type_ids: List[str],
        obj_type_ids: List[str]
    ) -> Dict[str, dict]:
        """Retrieve entity type labels for subject and object types."""
        entity_type_id_2_label = self.aligner.retrieve_entity_type_labels(
            subj_type_ids + obj_type_ids
        )
        return entity_type_id_2_label
    
    def get_candidate_entity_properties(
        self,
        triplet: Dict[str, str],
        subj_type_ids: List[str],
        obj_type_ids: List[str]
    ) -> Tuple[List[Tuple[str, str]], Dict[str, dict]]:
        """Retrieve candidate properties and their labels/constraints."""
        properties = self.aligner.retrieve_properties_for_entity_type(
            target_relation=triplet['relation'],
            object_types=obj_type_ids,
            subject_types=subj_type_ids,
            k=10
        )
        prop_2_label_and_constraint = self.aligner.retrieve_properties_labels_and_constraints(
            property_id_list=[p[0] for p in properties]
        )
        return properties, prop_2_label_and_constraint
    
    def validate_backbone(
        self,
        refined_subject_type: str,
        refined_object_type: str,
        refined_relation: str,
        candidate_subject_types: List[str],
        candidate_object_types: List[str],
        candidate_relations: List[str],
        prop_2_label_and_constraint: Dict[str, dict]
    ):
        """Check if the selected backbone_triplet's types and relation are in the valid sets."""
        exception_msg = ''
        if refined_relation not in candidate_relations:
            exception_msg += "Refined relation not in candidate relations\n"
        if refined_subject_type not in candidate_subject_types:
            exception_msg += "Refined subject type not in candidate subject types\n"
        if refined_object_type not in candidate_object_types:
            exception_msg += "Refined object type not in candidate object types\n"
        
        if exception_msg != '':
            return False, exception_msg
        
        subject_type_hierarchy = self.aligner.retrieve_entity_type_hierarchy(refined_subject_type)
        object_type_hierarchy = self.aligner.retrieve_entity_type_hierarchy(refined_object_type)
        
        prop_subject_type_ids = [
            prop_2_label_and_constraint[prop]['valid_subject_type_ids'] 
            for prop in prop_2_label_and_constraint 
            if prop_2_label_and_constraint[prop]['label'] == refined_relation
        ][0]
        prop_object_type_ids = [
            prop_2_label_and_constraint[prop]['valid_object_type_ids'] 
            for prop in prop_2_label_and_constraint 
            if prop_2_label_and_constraint[prop]['label'] == refined_relation
        ][0]
        
        if prop_subject_type_ids == ['ANY']:
            prop_subject_type_ids = subject_type_hierarchy
        if prop_object_type_ids == ['ANY']:
            prop_object_type_ids = object_type_hierarchy
        
        if any([t in subject_type_hierarchy for t in prop_subject_type_ids]) and \
           any([t in object_type_hierarchy for t in prop_object_type_ids]):
            return True, exception_msg
        else:
            exception_msg += 'Triplet backbone violates property constraints\n'
            return False, exception_msg

