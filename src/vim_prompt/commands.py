# src/vim_prompt/commands.py
import json
import os
from typing import Dict, List, Optional

class CommandManager:
    def __init__(self, db_path: str = "db"):
        self.db_path = db_path
        self.mappings = self._load_mappings()
        self.sources = self._load_sources()

    def _load_mappings(self) -> Dict:
        """Load the canonical command mappings."""
        with open(os.path.join(self.db_path, "command_mappings.json")) as f:
            return json.load(f)["command_mappings"]

    def _load_sources(self) -> Dict:
        """Load all available source files."""
        sources = {}
        for filename in os.listdir(self.db_path):
            if filename.endswith("_commands.json"):
                source_name = filename.replace("_commands.json", "")
                with open(os.path.join(self.db_path, filename)) as f:
                    sources[source_name] = json.load(f)
        return sources

    def search_commands(self, query: str, source: Optional[str] = None) -> List[Dict]:
        """Search for commands across all sources or a specific source."""
        results = []
        
        # Find matching commands
        for cmd, data in self.mappings.items():
            # Check if query matches command or any alias
            if (query.lower() in cmd.lower() or 
                query.lower() in data["canonical_description"].lower() or
                any(query.lower() in alias.lower() for alias in data["aliases"])):
                
                # Get source-specific information
                source_results = []
                for src_name, src_data in self.sources.items():
                    if source and src_name != source:
                        continue
                    
                    if cmd in src_data["commands"] and src_data["commands"][cmd]["available"]:
                        source_results.append({
                            "command": cmd,
                            "description": data["canonical_description"],
                            "source": src_name,
                            "url": src_data["url"],
                            "fragment": src_data["commands"][cmd]["fragment"]
                        })
                
                results.extend(source_results)
        
        return results

    def get_url_for_command(self, command: str, source: str) -> Optional[str]:
        """Generate the full URL with text fragment for a command."""
        if source in self.sources and command in self.sources[source]["commands"]:
            base_url = self.sources[source]["url"]
            fragment = self.sources[source]["commands"][command]["fragment"]
            return f"{base_url}#:~:text={urllib.parse.quote(fragment)}"
        return None