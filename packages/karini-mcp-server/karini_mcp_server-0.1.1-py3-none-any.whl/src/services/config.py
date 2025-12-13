import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:    
    api_base: str
    karini_api_key: Optional[str] = None
    copilot_id: Optional[str] = None
    webhook_api_key: Optional[str] = None
    webhook_recipe_id: Optional[str] = None
    karini_dataset_id: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            api_base=os.getenv("KARINI_API_BASE"),
            copilot_id=os.getenv("KARINI_COPILOT_ID"),
            karini_api_key=os.getenv("KARINI_API_KEY"),
            webhook_api_key=os.getenv("WEBHOOK_API_KEY"),
            webhook_recipe_id=os.getenv("WEBHOOK_RECIPE_ID"),
            karini_dataset_id=os.getenv("KARINI_DATASET_ID"),
        )
    
    def validate_copilot_config(self) -> bool:
        """Validate that required copilot configuration is present."""
        return all([
            self.api_base,
            self.copilot_id,
            self.karini_api_key,
        ])
    
    def validate_webhook_config(self) -> bool:
        """Validate that required webhook configuration is present."""
        return all([
            self.api_base,
            self.webhook_api_key,
            self.webhook_recipe_id,
        ])
    
    def validate_dataset_config(self) -> bool:
        "Validate that dataset configurations are present"
        return all([
            self.api_base,
            self.karini_api_key,
            self.karini_dataset_id
        ])
    
    def validate_tracing_config(self) -> bool:
        """Validate that required tracing configuration is present."""
        return all([
            self.api_base,
            self.karini_api_key
        ])