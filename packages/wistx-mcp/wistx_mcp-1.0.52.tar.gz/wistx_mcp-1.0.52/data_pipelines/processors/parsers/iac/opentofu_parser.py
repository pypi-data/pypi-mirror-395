"""OpenTofu parser (Terraform-compatible)."""

from data_pipelines.processors.parsers.iac.terraform_parser import TerraformParser


class OpenTofuParser(TerraformParser):
    """Parser for OpenTofu code (Terraform-compatible syntax).
    
    OpenTofu uses the same syntax as Terraform, so we inherit from TerraformParser
    and override only the validation to check for OpenTofu-specific indicators.
    """

    def validate_syntax(self, code: str) -> bool:
        """Basic OpenTofu syntax validation.
        
        Args:
            code: OpenTofu code content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        
        has_opentofu = "opentofu" in code_lower or "tofu" in code_lower
        has_terraform = "terraform" in code_lower
        has_resource = "resource" in code_lower or "data" in code_lower or "module" in code_lower
        
        return (has_opentofu or has_terraform) and has_resource

