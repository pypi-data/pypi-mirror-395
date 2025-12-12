import requests
import time
from typing import Dict, Any, Optional, Type
from pydantic import BaseModel, create_model, Field
from enum import Enum
from .exceptions import ValidationError, ContractNotFoundError, AuthenticationError, DCSException

class DCS:
    def __init__(self, api_key: str, base_url: str = "https://dcs-backend-4pjj.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": api_key})
        
        # Cache for contract definitions: {contract_name: (contract_data, timestamp)}
        self._contract_cache: Dict[str, tuple] = {}
        self._cache_ttl = 300  # 5 minutes

    def _get_contract(self, contract_name: str) -> Dict[str, Any]:
        """Fetch contract definition from server or cache"""
        now = time.time()
        
        if contract_name in self._contract_cache:
            data, timestamp = self._contract_cache[contract_name]
            if now - timestamp < self._cache_ttl:
                return data

        # Fetch from API
        try:
            # We need to find the contract by name. 
            # Ideally, the API should support fetching by name directly.
            # For now, we list all and filter, or we assume we have an endpoint.
            # Let's assume we use the list endpoint and filter, or better, we implemented a get by name?
            # Looking at backend/main.py, we have GET /api/contracts/{contract_id}
            # We don't have GET /api/contracts/name/{name}.
            # So we must list and find. This is inefficient but works for V1.
            # TODO: Add GET /api/contracts/name/{name} to backend for performance.
            
            resp = self.session.get(f"{self.base_url}/api/contracts")
            if resp.status_code == 401:
                raise AuthenticationError("Invalid API Key")
            if resp.status_code != 200:
                raise DCSException(f"Failed to fetch contracts: {resp.text}")
            
            contracts = resp.data if hasattr(resp, 'data') else resp.json()
            
            # Find the contract with the highest version for this name
            matching = [c for c in contracts if c['name'] == contract_name]
            if not matching:
                raise ContractNotFoundError(f"Contract '{contract_name}' not found")
            
            # Sort by version desc
            matching.sort(key=lambda x: x['version'], reverse=True)
            latest = matching[0]
            
            self._contract_cache[contract_name] = (latest, now)
            return latest

        except requests.RequestException as e:
            raise DCSException(f"Network error: {e}")

    def validate(self, contract_name: str, data: Dict[str, Any]) -> bool:
        """
        Validate data against the contract.
        Raises ValidationError if invalid.
        Returns True if valid.
        """
        # For V1, we can use the backend's validation endpoint to be sure, 
        # BUT the goal of a client is often to validate LOCALLY to save latency.
        # However, implementing full local validation that matches backend logic exactly 
        # requires duplicating the logic.
        # Given the "Concept" explanation I gave: "Le client télécharge le contrat... et vérifie localement",
        # I should implement local validation using Pydantic dynamic models.
        
        model = self.get_model(contract_name)
        try:
            model(**data)
            return True
        except Exception as e:
            raise ValidationError(str(e))

    def get_model(self, contract_name: str) -> Type[BaseModel]:
        """
        Returns a Pydantic model class for the given contract.
        """
        contract_def = self._get_contract(contract_name)
        return self._create_model_recursive(contract_name, contract_def['fields'])

    def _create_model_recursive(self, model_name_prefix: str, fields: list) -> Type[BaseModel]:
        fields_dict = {}
        safe_name = ''.join(x for x in model_name_prefix.title() if x.isalnum()) + "Model"

        for field in fields:
            field_name = field['name']
            field_type = field['type']
            is_required = field.get('required', True)
            description = field.get('description')
            constraints = field.get('constraints') or {}
            children = field.get('children') or []

            # Map types
            python_type = str
            if field_type == 'integer':
                python_type = int
            elif field_type == 'float':
                python_type = float
            elif field_type == 'boolean':
                python_type = bool
            elif field_type == 'object':
                python_type = self._create_model_recursive(f"{model_name_prefix}_{field_name}", children)
            elif field_type == 'array':
                from typing import List
                item_type_str = constraints.get('item_type', 'string') if constraints else 'string'
                
                if item_type_str == 'object':
                    item_model = self._create_model_recursive(f"{model_name_prefix}_{field_name}_Item", children)
                    python_type = List[item_model]
                elif item_type_str == 'array':
                    python_type = List[list]
                else:
                    primitive_map = {
                        'string': str,
                        'integer': int,
                        'float': float,
                        'boolean': bool
                    }
                    python_type = List[primitive_map.get(item_type_str, str)]
            
            # Map constraints
            field_kwargs = {}
            if is_required:
                field_kwargs['default'] = ...
            else:
                field_kwargs['default'] = None

            if description:
                field_kwargs['description'] = description

            if constraints:
                if 'min' in constraints:
                    field_kwargs['ge'] = constraints['min']
                if 'max' in constraints:
                    field_kwargs['le'] = constraints['max']
                if 'pattern' in constraints:
                    field_kwargs['regex'] = constraints['pattern']

            field_info = Field(**field_kwargs)
            
            fields_dict[field_name] = (python_type, field_info)

        return create_model(safe_name, **fields_dict)

    def refresh_cache(self):
        """Clear the contract cache"""
        self._contract_cache = {}
