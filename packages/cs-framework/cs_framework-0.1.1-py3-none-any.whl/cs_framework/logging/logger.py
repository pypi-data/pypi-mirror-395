import sys
import uuid
import json
from datetime import datetime
from typing import Any, Optional
from rdflib import Graph, Literal, RDF, URIRef, XSD
from loguru import logger
from .ontology import CS, CONCEPT, ACTION, EVENT, SYNCHRONIZATION, HAS_NAME, HAS_STATE, BELONGS_TO, TRIGGERED_BY, CAUSED_BY, STATUS

import time

class RDFLogger:
    def __init__(self, log_file: str = "execution.ttl", console_output: bool = True, save_interval: float = 0.0):
        self.graph = Graph()
        self.graph.bind("cs", CS)
        self.log_file = log_file
        self.console_output = console_output
        self.save_interval = save_interval
        self.last_save_time = 0.0
        
        # Configure loguru
        logger.remove() # Remove default handler
        if self.console_output:
            logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
        
        # Also log to a text file for easier reading
        text_log = log_file.replace(".ttl", ".log")
        logger.add(text_log, rotation="1 MB")

    def _log_to_console(self, message: str):
        logger.info(message)

    def log_concept(self, concept_id: uuid.UUID, name: str, state: Any):
        concept_uri = CS[str(concept_id)]
        self.graph.add((concept_uri, RDF.type, CONCEPT))
        self.graph.add((concept_uri, HAS_NAME, Literal(name)))
        self.graph.add((concept_uri, HAS_STATE, Literal(json.dumps(str(state))))) # Simplified state serialization
        self._log_to_console(f"Registered Concept: {name} ({concept_id})")

    def log_synchronization(self, sync_id: uuid.UUID, name: str):
        sync_uri = CS[str(sync_id)]
        self.graph.add((sync_uri, RDF.type, SYNCHRONIZATION))
        self.graph.add((sync_uri, HAS_NAME, Literal(name)))
        self._log_to_console(f"Registered Sync: {name} ({sync_id})")

    def log_action(self, action_id: uuid.UUID, name: str, concept_id: uuid.UUID, triggered_by: Optional[uuid.UUID] = None):
        action_uri = CS[str(action_id)]
        self.graph.add((action_uri, RDF.type, ACTION))
        self.graph.add((action_uri, HAS_NAME, Literal(name)))
        self.graph.add((action_uri, BELONGS_TO, CS[str(concept_id)]))
        if triggered_by:
            self.graph.add((action_uri, TRIGGERED_BY, CS[str(triggered_by)]))
        self._log_to_console(f"Action: {name} on {concept_id}")

    def log_event(self, event_id: uuid.UUID, name: str, source_id: uuid.UUID, causal_link: Optional[uuid.UUID] = None, status: str = "Success", payload: Any = None):
        event_uri = CS[str(event_id)]
        self.graph.add((event_uri, RDF.type, EVENT))
        self.graph.add((event_uri, HAS_NAME, Literal(name)))
        self.graph.add((event_uri, BELONGS_TO, CS[str(source_id)]))
        self.graph.add((event_uri, STATUS, Literal(status)))
        if payload:
             self.graph.add((event_uri, HAS_STATE, Literal(json.dumps(str(payload)))))
        if causal_link:
            self.graph.add((event_uri, CAUSED_BY, CS[str(causal_link)]))
        self._log_to_console(f"Event: {name} from {source_id} (Status: {status})")

    def save(self):
        import os
        
        # Check throttle
        current_time = time.time()
        if current_time - self.last_save_time < self.save_interval:
            return

        # Write to a temp file first to avoid read/write race conditions
        temp_file = self.log_file + ".tmp"
        try:
            self.graph.serialize(destination=temp_file, format="turtle")
            # Atomic replace
            os.replace(temp_file, self.log_file)
            self._log_to_console(f"Log saved to {self.log_file}")
            self.last_save_time = current_time
        except Exception as e:
            self._log_to_console(f"Error saving log: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
