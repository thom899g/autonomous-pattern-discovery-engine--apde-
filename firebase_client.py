"""
Firebase Client for APDE State Management
Handles all Firestore operations with robust error handling
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    from firebase_admin.exceptions import FirebaseError
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logging.warning("firebase-admin not installed. Firebase features disabled.")

class FirebaseClient:
    """Firebase Firestore client for APDE state management"""
    
    def __init__(self, project_id: str, collection_prefix: str = "apde_"):
        """Initialize Firebase client with error handling"""
        self.project_id = project_id
        self.collection_prefix = collection_prefix
        self.db = None
        self._initialized = False
        
        if not FIREBASE_AVAILABLE:
            logging.error("firebase-admin library not available. Install with: pip install firebase-admin")
            return
            
        try:
            # Initialize with default credentials (reads from GOOGLE_APPLICATION_CREDENTIALS)
            if not firebase_admin._apps:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, {
                    'projectId': project_id
                })
            
            self.db = firestore.client()
            self._initialized = True
            logging.info(f"Firebase client initialized for project: {project_id}")
            
        except ValueError as e:
            logging.error(f"Firebase configuration error: {e}")
        except FirebaseError as e:
            logging.error(f"Firebase initialization error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error initializing Firebase: {e}")
    
    def store_pattern(self, pattern_id: str, pattern_data: Dict[str, Any]) -> bool:
        """Store discovered pattern in Firestore"""
        if not self._initialized:
            logging.error("Firebase not initialized. Cannot store pattern.")
            return False
            
        try:
            pattern_ref = self.db.collection(f"{self.collection_prefix}patterns").document(pattern_id)
            pattern_data['discovered_at'] = firestore.SERVER_TIMESTAMP
            pattern_data['last_updated'] = firestore.SERVER_TIMESTAMP
            pattern_ref.set(pattern_data)
            logging.info(f"Pattern {pattern_id} stored successfully")
            return True
            
        except FirebaseError as e:
            logging.error(f"Firestore error storing pattern