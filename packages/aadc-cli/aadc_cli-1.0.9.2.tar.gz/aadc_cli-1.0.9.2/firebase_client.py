"""
Firebase Client for CLI
Direct Firestore access for credit management.

NOTE: This requires Firestore security rules that allow read/write access.
For production, you should use Firebase Admin SDK with a service account,
or create Cloud Functions to handle credit operations securely.

Firestore Rules needed (in Firebase Console):
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read: if true;
      allow write: if true;  // For demo - restrict in production!
    }
  }
}
```
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Tuple

# Firebase configuration (same as website)
FIREBASE_PROJECT_ID = "aadc-81e83"

# Firestore REST API base URL
FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"


def get_user_data(uid: str) -> Optional[Dict[str, Any]]:
    """
    Get user data from Firestore using REST API.
    Returns user data dict or None if not found.
    """
    try:
        url = f"{FIRESTORE_BASE}/users/{uid}"
        req = urllib.request.Request(url, headers={'User-Agent': 'AADC-CLI/1.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            # Parse Firestore document format
            fields = data.get('fields', {})
            return {
                'uid': uid,
                'email': _get_field_value(fields.get('email', {})),
                'displayName': _get_field_value(fields.get('displayName', {})),
                'credits': int(_get_field_value(fields.get('credits', {})) or 0),
                'plan': _get_field_value(fields.get('plan', {})) or 'free',
                'photoURL': _get_field_value(fields.get('photoURL', {})),
                'betaAccess': bool(_get_field_value(fields.get('betaAccess', {})) or False),
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        # Permission denied or other error
        return None
    except Exception:
        return None


def _get_field_value(field: dict) -> Any:
    """Extract value from Firestore field format."""
    if 'stringValue' in field:
        return field['stringValue']
    elif 'integerValue' in field:
        return int(field['integerValue'])
    elif 'doubleValue' in field:
        return float(field['doubleValue'])
    elif 'booleanValue' in field:
        return field['booleanValue']
    elif 'nullValue' in field:
        return None
    return None


def update_credits(uid: str, new_credits: int) -> bool:
    """
    Update user credits in Firestore using REST API.
    Returns True if successful.
    """
    try:
        url = f"{FIRESTORE_BASE}/users/{uid}?updateMask.fieldPaths=credits"
        
        payload = {
            "fields": {
                "credits": {"integerValue": str(new_credits)}
            }
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'AADC-CLI/1.0'
            },
            method='PATCH'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except urllib.error.HTTPError as e:
        # Log error for debugging
        return False
    except Exception:
        return False


def deduct_credit_firestore(uid: str) -> Tuple[bool, int]:
    """
    Deduct one credit from user in Firestore.
    Returns (success, remaining_credits).
    """
    # First get current credits
    user_data = get_user_data(uid)
    if not user_data:
        return False, 0
    
    current_credits = user_data.get('credits', 0)
    if current_credits <= 0:
        return False, 0
    
    new_credits = current_credits - 1
    success = update_credits(uid, new_credits)
    
    return success, new_credits if success else current_credits
