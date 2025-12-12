import re
import logging
import typing as t

logger = logging.getLogger(__name__)

class SecretDetector:
    """
    Detects and redact sensitive information like API keys, tokens, and passwords.
    """
    
    # Common patterns for secrets
    PATTERNS = {
        'AWS Access Key': r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])',
        'AWS Secret Key': r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])',
        'Google API Key': r'AIza[0-9A-Za-z\\-_]{35}',
        'Slack Token': r'xox[baprs]-([0-9a-zA-Z]{10,48})?',
        'GitHub Token': r'(gh[pousr]_[A-Za-z0-9_]{36,255})',
        'Generic Private Key': r'-----BEGIN (?:RSA|DSA|EC|PGP|OPENSSH) PRIVATE KEY-----',
        'Generic API Key': r'(?i)(?:api_key|apikey|secret|token|password|passwd|pwd)\s*[:=]\s*[\"\']([A-Za-z0-9_\-]{16,})[\"\']'
    }

    def __init__(self):
        self.compiled_patterns = {
            name: re.compile(pattern) 
            for name, pattern in self.PATTERNS.items()
        }

    def redact(self, content: str) -> t.Tuple[str, int]:
        """
        Redacts found secrets from the content.
        Returns (redacted_content, count_of_redactions).
        """
        redacted_content = content
        total_redactions = 0
        
        for name, pattern in self.compiled_patterns.items():
            # We use a callback to count replacements
            def replace_callback(match):
                nonlocal total_redactions
                total_redactions += 1
                # Keep the structure if it's a key-value pair (Generic API Key)
                if name == 'Generic API Key':
                    # This pattern captures the value in group 1
                    full_match = match.group(0)
                    secret_val = match.group(1)
                    return full_match.replace(secret_val, f"REDACTED_SECRET:{name.upper().replace(' ', '_')}")
                
                return f"REDACTED_SECRET:{name.upper().replace(' ', '_')}"

            # For Generic API Key, we need to be careful not to replace the key name
            # The regex for Generic API Key is a bit specific.
            # For others, it's just the secret itself.
            
            try:
                redacted_content = pattern.sub(replace_callback, redacted_content)
            except Exception as e:
                logger.warning(f"Error redacting {name}: {e}")

        return redacted_content, total_redactions
