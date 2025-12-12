from typing import Dict, Any, Optional, List
import os
import json
import re
from pathlib import Path
from PIL import Image

from dolze_image_templates.core.template_engine import Template
from dolze_image_templates.core.template_samples import get_sample_url


class TemplateRegistry:
    """
    Registry for managing and accessing all available templates.
    Acts as a single point of contact for template-related operations.
    """

    # Template form values mapping
    _template_form_values = {}

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the template registry.

        Args:
            templates_dir: Directory containing template definition files
        """
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "html_templates",
        )
        self._load_templates()
        self._initialize_form_values()

    def _get_template_directories(self) -> List[str]:
        """
        Get all template directories to search.
        
        Returns:
            List of directory paths containing templates
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_html_templates = os.path.join(base_dir, "html_templates")
        template_dirs = [
            os.path.join(base_dir, "html_templates"),
            os.path.join(base_dir, "email_templates"),
            os.path.join(base_dir, "sms_templates"),
        ]
        
        # If custom templates_dir is provided and it's different from default, use it instead
        if self.templates_dir:
            normalized_custom = os.path.normpath(os.path.abspath(self.templates_dir))
            normalized_default = os.path.normpath(os.path.abspath(default_html_templates))
            if normalized_custom != normalized_default:
                return [self.templates_dir]
        
        return template_dirs

    def _load_templates(self) -> None:
        """Load all templates from all template directories."""
        template_dirs = self._get_template_directories()
        
        for templates_dir in template_dirs:
            if not os.path.exists(templates_dir):
                continue

            # Load all JSON files in the templates directory
            for file_path in Path(templates_dir).glob("*.json"):
                try:
                    with open(file_path, "r") as f:
                        template_data = json.load(f)
                        if isinstance(template_data, dict) and "name" in template_data:
                            self.templates[template_data["name"]] = template_data
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading template from {file_path}: {e}")

    def _has_image_upload(self, config: Any) -> bool:
        """Check if the template configuration contains any image upload fields.

        Args:
            config: Template configuration or part of it

        Returns:
            bool: True if any field value is "${image_url}", False otherwise
        """
        if isinstance(config, str):
            return config == "${image_url}"

        if not isinstance(config, (dict, list)):
            return False

        if isinstance(config, dict):
            for value in config.values():
                if value == "${image_url}":
                    return True
                if isinstance(value, (dict, list)) and self._has_image_upload(value):
                    return True
        elif isinstance(config, list):
            for item in config:
                if item == "${image_url}":
                    return True
                if isinstance(item, (dict, list)) and self._has_image_upload(item):
                    return True

        return False

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """
        Get all available templates.

        Returns:
            List[Dict[str, Any]]: List of template metadata. Each dictionary contains:
                - template_name (str): Name of the template
                - description (str, optional): Template description
                - categories (List[str]): List of category tags for the template
                - isImageUploadPresent (bool): Whether the template has image upload fields
                - sample_url (str): URL to a sample image for the template
        """
        templates = []
        template_dirs = self._get_template_directories()
        
        for templates_dir in template_dirs:
            if not os.path.exists(templates_dir):
                continue
                
            for file_path in Path(templates_dir).glob("*.json"):
                try:
                    with open(file_path, "r") as f:
                        template_data = json.load(f)
                        if isinstance(template_data, dict) and "name" in template_data:
                            
                            template_info = {
                                "template_name": template_data["name"],
                                "description": template_data.get("description"),
                                "categories": template_data.get("categories", []),
                                "tags": template_data.get("tags", []),
                                "type": template_data.get("type"),
                                "isImageUploadPresent": self._has_image_upload(template_data),
                                "validation": template_data.get("validation", {}),
                                "sample_url": get_sample_url(template_data["name"]),
                            }
                            
                            templates.append(template_info)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error loading template from {file_path}: {e}")
        return templates

    def register_template(self, name: str, config: Dict[str, Any]) -> None:
        """
        Register a new template.

        Args:
            name: Name of the template
            config: Template configuration dictionary
        """
        if not name:
            raise ValueError("Template name cannot be empty")

        # Ensure required fields are present
        required_fields = ["components"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Template config is missing required field: {field}")

        # Set default values
        config.setdefault("name", name)
        config.setdefault("size", {"width": 1080, "height": 1080})
        config.setdefault("background_color", [255, 255, 255])
        config.setdefault("use_base_image", False)

        self.templates[name] = config

        # Save to file
        self._save_template(name, config)

    def _save_template(self, name: str, config: Dict[str, Any]) -> None:
        """
        Save a template to a JSON file.

        Args:
            name: Name of the template
            config: Template configuration
        """
        try:
            os.makedirs(self.templates_dir, exist_ok=True)
            file_path = os.path.join(self.templates_dir, f"{name}.json")
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving template {name}: {e}")

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a template configuration by name.

        Args:
            name: Name of the template

        Returns:
            Template configuration dictionary or None if not found
        """
        return self.templates.get(name)

    def get_template_form_values(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Get form values for a specific template by name.

        Args:
            template_name: Name of the template to get form values for

        Returns:
            Dictionary of form values or None if not found
        """
        template_data = self.get_template(template_name)
        if not template_data:
            return None

        # Return validation directly
        if "validation" in template_data:
            return template_data["validation"]
        elif "validations" in template_data:
            return template_data["validations"]

        return None

    def _initialize_form_values(self) -> None:
        """
        Initialize the form values mapping for all templates.
        This separates the form values from the template configurations.
        """
        # Clear existing form values
        self._template_form_values = {}

    def get_template_names(self) -> List[str]:
        """
        Get a list of all available template names.

        Returns:
            List of template names
        """
        return list(self.templates.keys())

    def create_template_instance(
        self, name: str, variables: Optional[Dict[str, Any]] = None
    ) -> Optional[Template]:
        """
        Create a template instance with the given variables.

        Args:
            name: Name of the template
            variables: Dictionary of variables to substitute in the template

        Returns:
            A Template instance or None if the template is not found
        """
        template_config = self.get_template(name)
        if not template_config:
            return None

        # Create a deep copy of the config to avoid modifying the original
        config = json.loads(json.dumps(template_config))

        # Apply variable substitution (always call to enable placeholder fallback)
        config = self._substitute_variables(config, variables or {}, name)

        return Template.from_config(config, variables)

    def _substitute_variables(
        self, config: Any, variables: Dict[str, Any], template_name: str = None
    ) -> Any:
        """
        Recursively substitute variables in the template configuration with smart placeholder fallback.

        Priority: User variable > Template placeholder > Original text

        Args:
            config: Template configuration or part of it
            variables: Dictionary of variables to substitute
            template_name: Name of the template (for accessing placeholders)

        Returns:
            Configuration with variables substituted
        """
        if isinstance(config, dict):
            result = {}
            for key, value in config.items():
                result[key] = self._substitute_variables(
                    value, variables, template_name
                )
            return result
        elif isinstance(config, list):
            return [
                self._substitute_variables(item, variables, template_name)
                for item in config
            ]
        elif isinstance(config, str):
            # Replace ${variable} with the corresponding value
            def replace_match(match):
                var_name = match.group(1)

                # Priority 1: User provided variable
                if var_name in variables:
                    return str(variables[var_name])

                # Priority 2: Template samples (if template_name is provided)
                if template_name:
                    template_config = self.get_template(template_name)
                    if (
                        template_config
                        and "validation" in template_config
                        and "samples" in template_config["validation"]
                    ):
                        samples = template_config["validation"]["samples"]
                        if var_name in samples:
                            return str(samples[var_name])

                # Priority 3: Original text (fallback)
                return match.group(0)

            return re.sub(r"\${([^}]+)}", replace_match, config)
        else:
            return config

    async def render_template(
        self,
        template_name: str,
        variables: Dict[str, Any],
        output_path: Optional[str] = None,
    ) -> Optional[Image.Image]:
        """
        Render a template with the given variables.

        Args:
            template_name: Name of the template to render
            variables: Dictionary of variables to substitute in the template
            output_path: Optional path to save the rendered image

        Returns:
            Rendered PIL Image or None if rendering fails
        """
        template = self.create_template_instance(template_name, variables)
        if not template:
            return None

        # Render the template - now async
        rendered_image = await template.render()

        # Save to file if output path is provided
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            rendered_image.save(output_path)

        return rendered_image

    def validate_template_data(self, template_name: str, data: Dict[str, str]) -> Dict[str, Optional[str]]:
        """
        Validate template data using validation schema.
        
        Args:
            template_name: Name of the template
            data: Field data to validate
            
        Returns:
            Dictionary mapping field names to error messages (None if valid)
        """
        template_config = self.get_template(template_name)
        if not template_config:
            return {"error": "Template not found"}
            
        # Basic validation using validation schema
        validation = template_config.get("validation", {})
        errors = {}
        
        for field_name, field_config in validation.items():
            if field_name in ["samples", "fieldPrompt", "custom_css", "custom_html"]:
                continue
                
            value = data.get(field_name, "")
            field_type = field_config.get("type", "text")
            min_length = field_config.get("minLength", 0)
            max_length = field_config.get("maxLength", 10000)
            
            if field_type == "text" and value:
                if len(value) < min_length:
                    errors[field_name] = f"Minimum length is {min_length}"
                elif len(value) > max_length:
                    errors[field_name] = f"Maximum length is {max_length}"
            elif field_type == "image" and value:
                if len(value) < min_length:
                    errors[field_name] = "Invalid image URL"
                    
        return errors if errors else {}


# Singleton instance for easy access
_instance = None


def get_template_registry(templates_dir: Optional[str] = None) -> TemplateRegistry:
    """
    Get the singleton instance of the template registry.

    Args:
        templates_dir: Optional directory containing template definitions

    Returns:
        TemplateRegistry instance
    """
    global _instance
    if _instance is None:
        _instance = TemplateRegistry(templates_dir)
    return _instance