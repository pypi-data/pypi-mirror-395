"""
Experimental LangChain agent implementation for extract_triplets_with_ontology_filtering.

This module provides a LangChain-based agent that orchestrates the triplet extraction
and refinement workflow using tools for each step.

NOTE: This is an experimental implementation. The original method has a very structured,
sequential workflow that may not benefit significantly from an agent's decision-making
capabilities. This implementation is provided for experimentation and may require refinement
based on actual usage patterns.

The agent uses structured tools to:
1. Extract triplets from text
2. Get candidate entity types and labels
3. Refine entity types, relations, and entity names
4. Validate triplets against ontology constraints

Usage:
    from utils.structured_inference_with_db_langchain import StructuredInferenceWithDBLangChain
    
    agent = StructuredInferenceWithDBLangChain(extractor, aligner, triplets_db)
    initial, final, filtered, ontology_filtered = agent.extract_triplets_with_ontology_filtering(
        text="...", sample_id="..."
    )
"""

from typing import Dict, List, Tuple, Optional
from unidecode import unidecode
import re
import logging
import json

from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

logger = logging.getLogger('StructuredInferenceWithDBLangChain')
logger.setLevel(logging.DEBUG)


class ExtractTripletsInput(BaseModel):
    """Input for extracting triplets from text."""
    text: str = Field(description="The input text to extract triplets from")


class GetCandidateEntityTypesInput(BaseModel):
    """Input for getting candidate entity type IDs."""
    triplet: Dict = Field(description="The triplet dictionary with subject, relation, object, subject_type, object_type")


class GetCandidateEntityLabelsInput(BaseModel):
    """Input for getting candidate entity labels."""
    subj_type_ids: List[str] = Field(description="List of subject type IDs")
    obj_type_ids: List[str] = Field(description="List of object type IDs")


class GetCandidateEntityPropertiesInput(BaseModel):
    """Input for getting candidate entity properties."""
    triplet: Dict = Field(description="The triplet dictionary")
    subj_type_ids: List[str] = Field(description="List of subject type IDs")
    obj_type_ids: List[str] = Field(description="List of object type IDs")


class RefineEntityTypesInput(BaseModel):
    """Input for refining entity types."""
    text: str = Field(description="The original text")
    triplet: Dict = Field(description="The triplet to refine")
    candidate_subject_types: List[str] = Field(description="List of candidate subject types")
    candidate_object_types: List[str] = Field(description="List of candidate object types")


class RefineRelationInput(BaseModel):
    """Input for refining relation."""
    text: str = Field(description="The original text")
    triplet: Dict = Field(description="The triplet to refine")
    candidate_relations: List[str] = Field(description="List of candidate relations")


class RefineEntityNameInput(BaseModel):
    """Input for refining entity name."""
    text: str = Field(description="The original text")
    triplet: Dict = Field(description="The triplet containing the entity")
    sample_id: str = Field(description="The sample ID")
    is_object: bool = Field(description="Whether to refine object (True) or subject (False)")


class ValidateBackboneInput(BaseModel):
    """Input for validating backbone triplet."""
    refined_subject_type: str = Field(description="The refined subject type")
    refined_object_type: str = Field(description="The refined object type")
    refined_relation: str = Field(description="The refined relation")
    candidate_subject_types: List[str] = Field(description="List of candidate subject types")
    candidate_object_types: List[str] = Field(description="List of candidate object types")
    candidate_relations: List[str] = Field(description="List of candidate relations")
    prop_2_label_and_constraint: Dict = Field(description="Property to label and constraint mapping")


class StructuredInferenceWithDBLangChain:
    """
    LangChain agent-based implementation of StructuredInferenceWithDB.
    
    This class wraps the original StructuredInferenceWithDB methods as tools
    and uses a LangChain agent to orchestrate the triplet extraction workflow.
    """
    
    def __init__(self, extractor, aligner, triplets_db, llm_model: str = "gpt-4o", temperature: float = 0):
        """
        Initialize the LangChain agent.
        
        Args:
            extractor: The LLMTripletExtractor instance
            aligner: The Aligner instance
            triplets_db: The triplets database instance
            llm_model: The LLM model to use for the agent
            temperature: The temperature for the LLM
        """
        self.extractor = extractor
        self.aligner = aligner
        self.triplets_db = triplets_db
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        
        # Create tools from the original methods
        self.tools = self._create_tools()
        
        # Create the agent
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[StructuredTool]:
        """Create LangChain tools from the original methods."""
        
        def extract_triplets_from_text(text: str) -> Dict:
            """Extract triplets from text using the extractor."""
            self.extractor.reset_tokens()
            self.extractor.reset_messages()
            self.extractor.reset_error_state()
            return self.extractor.extract_triplets_from_text(text)
        
        def get_candidate_entity_type_ids(triplet: Dict) -> Tuple[List[str], List[str]]:
            """Get candidate entity type IDs for subject and object."""
            subj_type_ids, obj_type_ids = self.aligner.retrieve_similar_entity_types(triplet=triplet)
            return {"subj_type_ids": subj_type_ids, "obj_type_ids": obj_type_ids}
        
        def get_candidate_entity_labels(subj_type_ids: List[str], obj_type_ids: List[str]) -> Dict:
            """Get entity type labels for the given type IDs."""
            entity_type_id_2_label = self.aligner.retrieve_entity_type_labels(
                subj_type_ids + obj_type_ids
            )
            return {"entity_type_id_2_label": entity_type_id_2_label}
        
        def refine_entity_types(
            text: str, 
            triplet: Dict, 
            candidate_subject_types: List[str], 
            candidate_object_types: List[str]
        ) -> Dict:
            """Refine entity types using LLM."""
            self.extractor.reset_error_state()
            refined_entity_types = self.extractor.refine_entity_types(
                text=text, 
                triplet=triplet, 
                candidate_subject_types=candidate_subject_types, 
                candidate_object_types=candidate_object_types
            )
            return {
                "subject_type": refined_entity_types['subject_type'],
                "object_type": refined_entity_types['object_type']
            }
        
        def refine_relation(text: str, triplet: Dict, candidate_relations: List[str]) -> Dict:
            """Refine relation using LLM."""
            self.extractor.reset_error_state()
            refined_relation = self.extractor.refine_relation(
                text=text, triplet=triplet, candidate_relations=candidate_relations
            )
            return {"relation": refined_relation['relation']}
        
        def get_candidate_entity_properties(
            triplet: Dict,
            subj_type_ids: List[str],
            obj_type_ids: List[str]
        ) -> Dict:
            """Get candidate properties for entity types."""
            properties = self.aligner.retrieve_properties_for_entity_type(
                target_relation=triplet['relation'],
                object_types=obj_type_ids,
                subject_types=subj_type_ids,
                k=10
            )
            prop_2_label_and_constraint = self.aligner.retrieve_properties_labels_and_constraints(
                property_id_list=[p[0] for p in properties]
            )
            return {
                "relation_direction_candidate_pairs": properties,
                "prop_2_label_and_constraint": prop_2_label_and_constraint
            }
        
        def refine_entity_name(text: str, triplet: Dict, sample_id: str, is_object: bool = False) -> Dict:
            """Refine entity name using type constraints."""
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
                        # If not exact match -> refine entity name
                        updated_entity = self.extractor.refine_entity(
                            text=text,
                            triplet=triplet,
                            candidates=list(similar_entities.values()),
                            is_object=is_object
                        )
                        # Unidecode the updated entity
                        updated_entity = unidecode(updated_entity)
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
            
            return {"entity": updated_entity}
        
        def validate_backbone(
            refined_subject_type: str,
            refined_object_type: str,
            refined_relation: str,
            candidate_subject_types: List[str],
            candidate_object_types: List[str],
            candidate_relations: List[str],
            prop_2_label_and_constraint: Dict
        ) -> Dict:
            """Validate backbone triplet against ontology constraints."""
            exception_msg = ''
            if refined_relation not in candidate_relations:
                exception_msg += "Refined relation not in candidate relations\n"
            if refined_subject_type not in candidate_subject_types:
                exception_msg += "Refined subject type not in candidate subject types\n"
            if refined_object_type not in candidate_object_types:
                exception_msg += "Refined object type not in candidate object types\n"
            
            if exception_msg != '':
                return {"valid": False, "exception_msg": exception_msg}
            
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
                return {"valid": True, "exception_msg": ""}
            else:
                exception_msg += 'Triplet backbone violates property constraints\n'
                return {"valid": False, "exception_msg": exception_msg}
        
        def get_token_counts() -> Dict:
            """Get current token counts from the extractor."""
            prompt_tokens, completion_tokens = self.extractor.calculate_used_tokens()
            return {"prompt_token_num": prompt_tokens, "completion_token_num": completion_tokens}
        
        # Create structured tools
        tools = [
            StructuredTool.from_function(
                func=extract_triplets_from_text,
                name="extract_triplets_from_text",
                description="Extract knowledge graph triplets from text. Returns a dictionary with 'triplets' key containing a list of triplets.",
                args_schema=ExtractTripletsInput
            ),
            StructuredTool.from_function(
                func=get_candidate_entity_type_ids,
                name="get_candidate_entity_type_ids",
                description="Get candidate entity type IDs for subject and object based on a triplet. Returns dict with 'subj_type_ids' and 'obj_type_ids'.",
                args_schema=GetCandidateEntityTypesInput
            ),
            StructuredTool.from_function(
                func=get_candidate_entity_labels,
                name="get_candidate_entity_labels",
                description="Get entity type labels for given type IDs. Returns dict with 'entity_type_id_2_label' mapping.",
                args_schema=GetCandidateEntityLabelsInput
            ),
            StructuredTool.from_function(
                func=refine_entity_types,
                name="refine_entity_types",
                description="Refine entity types using LLM. Returns dict with 'subject_type' and 'object_type'.",
                args_schema=RefineEntityTypesInput
            ),
            StructuredTool.from_function(
                func=refine_relation,
                name="refine_relation",
                description="Refine relation using LLM. Returns dict with 'relation' key.",
                args_schema=RefineRelationInput
            ),
            StructuredTool.from_function(
                func=get_candidate_entity_properties,
                name="get_candidate_entity_properties",
                description="Get candidate properties for entity types. Returns dict with 'relation_direction_candidate_pairs' and 'prop_2_label_and_constraint'.",
                args_schema=GetCandidateEntityPropertiesInput
            ),
            StructuredTool.from_function(
                func=refine_entity_name,
                name="refine_entity_name",
                description="Refine entity name using type constraints. Returns dict with 'entity' key.",
                args_schema=RefineEntityNameInput
            ),
            StructuredTool.from_function(
                func=validate_backbone,
                name="validate_backbone",
                description="Validate backbone triplet against ontology constraints. Returns dict with 'valid' (bool) and 'exception_msg' (str).",
                args_schema=ValidateBackboneInput
            ),
            StructuredTool.from_function(
                func=get_token_counts,
                name="get_token_counts",
                description="Get current token counts (prompt_token_num and completion_token_num) from the extractor. Use this to add metadata to triplets.",
            ),
        ]
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Create and configure the LangChain agent."""
        
        system_message = """You are an expert knowledge graph extraction agent. Your task is to extract and refine knowledge graph triplets from text.

IMPORTANT: Follow this exact workflow for each triplet:

1. First, extract all triplets from the text using extract_triplets_from_text
2. For EACH triplet in the extracted triplets:
   a. Get candidate entity type IDs using get_candidate_entity_type_ids
   b. Get candidate entity labels using get_candidate_entity_labels (pass subj_type_ids and obj_type_ids)
   c. Check if the triplet's types are already in candidate types:
      - If both subject_type and object_type are in candidates, skip refinement
      - Otherwise, refine entity types using refine_entity_types
   d. If refined types are in candidates, get candidate properties using get_candidate_entity_properties
   e. Check if the triplet's relation is in candidate relations:
      - If yes, use the original relation
      - Otherwise, refine relation using refine_relation
   f. Determine relation direction (direct or inverse) from the property pairs
   g. Build the backbone triplet with correct direction
   h. Refine entity names using refine_entity_name (for both subject and object if their types are in candidates)
   i. Validate the backbone triplet using validate_backbone
   j. If valid, add to final_triplets; if invalid, add to ontology_filtered_triplets with exception_text

For each triplet, you must add metadata:
- prompt_token_num and completion_token_num (from extractor.calculate_used_tokens())
- source_text_id (provided in the input)
- sample_id (provided in the input)

Return the final results as a JSON structure with these keys:
- initial_triplets: List of original triplets with metadata
- final_triplets: List of validated triplets
- filtered_triplets: Empty list []
- ontology_filtered_triplets: List of invalid triplets with exception_text"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=50,
            return_intermediate_steps=True
        )
        
        return agent_executor
    
    def extract_triplets_with_ontology_filtering(
        self, 
        text: str, 
        sample_id: str, 
        source_text_id: Optional[str] = None
    ) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
        """
        Extract and refine knowledge graph triplets from text using LangChain agent.
        
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
        
        # Create the agent input
        agent_input = f"""Extract and refine knowledge graph triplets from the following text:

Text: "{text}"

Sample ID: {sample_id}
Source Text ID: {source_text_id if source_text_id else 'None'}

Follow the workflow described in the system message. Process each triplet sequentially through all refinement steps.

After processing all triplets, return a JSON structure with exactly these keys:
- initial_triplets: List of original triplets (each with: subject, relation, object, subject_type, object_type, qualifiers, prompt_token_num, completion_token_num, source_text_id, sample_id)
- final_triplets: List of validated triplets (same structure as initial_triplets)
- filtered_triplets: Empty list []
- ontology_filtered_triplets: List of invalid triplets (same structure plus: candidate_subject_types, candidate_object_types, candidate_relations, exception_text)

Make sure to process ALL triplets from the extraction step."""
        
        # Run the agent
        result = self.agent.invoke({"input": agent_input, "chat_history": []})
        
        # Parse the result
        # The agent returns a dictionary with 'output' key containing the final answer
        # We need to extract the structured data from the output
        
        # For now, we'll need to parse the output or use a different approach
        # Since the agent might return text, we'll need to handle JSON parsing
        
        try:
            # Try to extract JSON from the output
            output_text = result.get('output', '')
            # Look for JSON in the output
            json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
            if json_match:
                parsed_result = json.loads(json_match.group(0))
                initial_triplets = parsed_result.get('initial_triplets', [])
                final_triplets = parsed_result.get('final_triplets', [])
                filtered_triplets = parsed_result.get('filtered_triplets', [])
                ontology_filtered_triplets = parsed_result.get('ontology_filtered_triplets', [])
            else:
                # Fallback: return empty lists if parsing fails
                logger.warning("Could not parse agent output as JSON. Returning empty lists.")
                initial_triplets, final_triplets, filtered_triplets, ontology_filtered_triplets = [], [], [], []
        except Exception as e:
            logger.error(f"Error parsing agent output: {e}")
            initial_triplets, final_triplets, filtered_triplets, ontology_filtered_triplets = [], [], [], []
        
        return initial_triplets, final_triplets, filtered_triplets, ontology_filtered_triplets

