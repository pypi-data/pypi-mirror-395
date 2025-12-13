"""
Request Interpreter for Custom Tasks

This module provides AI-assisted interpretation of natural language
pentesting requests, using an LLM to understand user intent.
"""

import json
import re
from typing import Optional, Tuple, List
from dataclasses import dataclass

import httpx

from twpt_cli.config import load_credentials, get_api_endpoint


@dataclass
class InterpretedTask:
    """Represents an AI-interpreted custom task request."""
    understood_request: str  # AI's summary of what the user wants
    task_description: str    # Cleaned task description for execution
    target: Optional[str]    # Extracted target
    parameters: List[str]    # Any parameters/flags
    tools_suggested: List[str]  # Tools the AI suggests using
    needs_target: bool       # Whether target is still needed
    confidence: str          # high, medium, low
    # Command mapping fields
    is_builtin_command: bool = False  # True if maps to a built-in command
    maps_to_command: Optional[str] = None  # e.g., "run", "list", "get"
    command_args: List[str] = None  # Arguments for the command
    command_flags: List[str] = None  # Flags for the command (--safe, --watch)

    def __post_init__(self):
        if self.command_args is None:
            self.command_args = []
        if self.command_flags is None:
            self.command_flags = []


class AIRequestInterpreter:
    """
    Uses the pt-agent /api/v1/interpret endpoint to interpret natural language
    pentesting requests with AI assistance.

    The AI will:
    1. Understand what the user wants to do
    2. Extract the target if present
    3. Suggest appropriate tools/approaches
    4. Fix typos and clean up the request
    5. Summarize back to the user for confirmation
    """

    def __init__(self):
        self.credentials = load_credentials()
        self.api_endpoint = get_api_endpoint()

    def interpret(self, user_input: str) -> Optional[InterpretedTask]:
        """
        Use AI to interpret the user's request.

        Args:
            user_input: The raw user input

        Returns:
            InterpretedTask with AI's understanding, or None if failed
        """
        if not self.credentials:
            return self._fallback_interpret(user_input)

        try:
            # Call the pt-agent interpret API
            response = self._call_ai(user_input)
            if not response:
                return self._fallback_interpret(user_input)

            # Parse the response dict directly
            parsed = self._parse_response(response)
            if parsed:
                return parsed

            return self._fallback_interpret(user_input)

        except Exception:
            # Silently fall back to regex interpretation
            return self._fallback_interpret(user_input)

    def _call_ai(self, user_input: str) -> Optional[dict]:
        """Call the pt-agent interpret API."""
        try:
            url = f"{self.api_endpoint}/api/v1/interpret"

            headers = {
                "Content-Type": "application/json",
                "api-key": self.credentials.api_key,
                "api-secret": self.credentials.api_secret,
            }

            payload = {
                "user_input": user_input
            }

            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError:
            # API not available - silently fall back to regex
            return None
        except Exception:
            # Other errors - silently fall back to regex
            return None

    def _parse_response(self, data: dict) -> Optional[InterpretedTask]:
        """Parse the API response dict into an InterpretedTask."""
        try:
            # Check if this maps to a built-in command
            is_builtin = data.get("is_builtin_command", False)

            if is_builtin:
                # Built-in command mapping
                return InterpretedTask(
                    understood_request=data.get("understood_request", ""),
                    task_description=data.get("task_description", ""),
                    target=data.get("target"),
                    parameters=data.get("parameters", []),
                    tools_suggested=data.get("tools_suggested", []),
                    needs_target=data.get("needs_target", False),
                    confidence=data.get("confidence", "medium"),
                    is_builtin_command=True,
                    maps_to_command=data.get("maps_to_command"),
                    command_args=data.get("command_args", []),
                    command_flags=data.get("command_flags", [])
                )
            else:
                # Custom task
                return InterpretedTask(
                    understood_request=data.get("understood_request", ""),
                    task_description=data.get("task_description", ""),
                    target=data.get("target"),
                    parameters=data.get("parameters", []),
                    tools_suggested=data.get("tools_suggested", []),
                    needs_target=data.get("needs_target", True),
                    confidence=data.get("confidence", "medium"),
                    is_builtin_command=False,
                    maps_to_command=None,
                    command_args=[],
                    command_flags=[]
                )

        except (KeyError, TypeError):
            # Invalid response - fall back to regex
            return None

    # Common typos and their corrections
    TYPO_CORRECTIONS = {
        'svcan': 'scan', 'scna': 'scan', 'sacn': 'scan', 'scann': 'scan',
        'prot': 'port', 'prto': 'port', 'pors': 'ports', 'prots': 'ports',
        'taret': 'target', 'taregt': 'target', 'tagret': 'target',
        'vulnarability': 'vulnerability', 'vulnrability': 'vulnerability',
        'vuln': 'vulnerability', 'vulns': 'vulnerabilities',
        'pentest': 'pentest', 'pentset': 'pentest', 'pnetest': 'pentest',
        'enumeration': 'enumeration', 'enumeraiton': 'enumeration',
        'direcotry': 'directory', 'driectory': 'directory', 'dir': 'directory',
        'chekc': 'check', 'chedk': 'check', 'cehck': 'check',
        'quikc': 'quick', 'qucik': 'quick', 'quik': 'quick',
        'websiet': 'website', 'wesbite': 'website',
        'servre': 'server', 'sevrer': 'server', 'sever': 'server',
        'opne': 'open', 'oepn': 'open',
        'conneciton': 'connection', 'connectoin': 'connection',
        'serivce': 'service', 'servcie': 'service', 'svc': 'service',
        'sql': 'SQL', 'xss': 'XSS', 'csrf': 'CSRF', 'ssrf': 'SSRF',
        'rce': 'RCE', 'lfi': 'LFI', 'rfi': 'RFI',
    }

    # Task patterns for understanding intent
    # Format: (regex_pattern, task_description, tools)
    # Note: task_description should NOT start with "perform" - that's added by _fallback_interpret
    TASK_PATTERNS = [
        # Port scanning
        (r'(?:do\s+)?(?:a\s+)?(?:quick\s+)?port\s*scan(?:ning)?', 'port scan', ['nmap']),
        (r'scan\s*(?:the\s+)?ports?', 'port scan', ['nmap']),
        (r'check\s+(?:for\s+)?open\s+ports?', 'open ports check', ['nmap']),
        (r'nmap\s+scan', 'nmap scan', ['nmap']),
        # Web scanning
        (r'(?:web\s+)?vuln(?:erability)?\s+scan', 'web vulnerability scan', ['nikto', 'nuclei']),
        (r'scan\s+(?:for\s+)?vulnerabilities', 'vulnerability scan', ['nikto', 'nuclei']),
        (r'nikto\s+scan', 'Nikto web scan', ['nikto']),
        (r'nuclei\s+scan', 'Nuclei scan', ['nuclei']),
        # Directory enumeration
        (r'(?:dir(?:ectory)?\s+)?enum(?:erat(?:e|ion))?', 'directory enumeration', ['gobuster', 'dirb']),
        (r'find\s+(?:hidden\s+)?(?:files|directories|paths)', 'hidden files/directories discovery', ['gobuster']),
        (r'(?:gobuster|dirb|dirbuster)\s+scan', 'directory enumeration', ['gobuster']),
        # Subdomain enumeration
        (r'(?:sub)?domain\s+(?:enum(?:erat(?:e|ion))?|discovery)', 'subdomain discovery', ['subfinder', 'amass']),
        (r'find\s+subdomains?', 'subdomain discovery', ['subfinder']),
        # SQL injection
        (r'(?:check|test|scan)\s+(?:for\s+)?sql\s*inject(?:ion)?', 'SQL injection test', ['sqlmap']),
        (r'sqlmap', 'SQLMap scan', ['sqlmap']),
        # XSS
        (r'(?:check|test|scan)\s+(?:for\s+)?xss', 'XSS vulnerability test', ['dalfox']),
        (r'cross[- ]?site\s+scripting', 'XSS vulnerability test', ['dalfox']),
        # SSL/TLS
        (r'(?:check|test|scan)\s+ssl', 'SSL/TLS configuration check', ['sslscan', 'testssl']),
        (r'ssl\s+(?:scan|check|test)', 'SSL/TLS configuration check', ['sslscan']),
        # DNS
        (r'dns\s+(?:recon|enum(?:erat(?:e|ion))?|lookup)', 'DNS reconnaissance', ['dig', 'dnsenum']),
        # Service detection
        (r'(?:detect|identify|find)\s+services?', 'service detection', ['nmap']),
        (r'service\s+(?:detection|enum(?:eration)?)', 'service enumeration', ['nmap']),
        # General scan
        (r'(?:full|complete|comprehensive)\s+scan', 'comprehensive scan', ['nmap', 'nikto']),
    ]

    def _correct_typos(self, text: str) -> str:
        """Correct common typos in the input."""
        words = text.split()
        corrected = []
        for word in words:
            lower_word = word.lower()
            if lower_word in self.TYPO_CORRECTIONS:
                corrected.append(self.TYPO_CORRECTIONS[lower_word])
            else:
                corrected.append(word)
        return ' '.join(corrected)

    def _identify_task(self, text: str) -> tuple:
        """Identify ALL task types from text. Returns (description, tools, confidence).

        Handles multiple tasks connected by 'and', 'then', commas, etc.
        """
        text_lower = text.lower()
        matched_tasks = []
        matched_tools = []

        for pattern, description, tools in self.TASK_PATTERNS:
            if re.search(pattern, text_lower):
                if description not in matched_tasks:
                    matched_tasks.append(description)
                for tool in tools:
                    if tool not in matched_tools:
                        matched_tools.append(tool)

        if matched_tasks:
            # Combine all tasks into a single description
            if len(matched_tasks) == 1:
                combined_desc = matched_tasks[0]
            else:
                combined_desc = ' and '.join(matched_tasks)
            confidence = 'medium' if len(matched_tasks) <= 2 else 'high'
            return combined_desc, matched_tools, confidence

        return None, [], 'low'

    # Patterns for mapping to built-in commands (fallback when AI unavailable)
    BUILTIN_COMMAND_PATTERNS = [
        # list command patterns
        (r'^(?:list|show)\s+(?:my\s+)?(?:recent\s+)?pentests?', 'list', False),
        # status command
        (r'^(?:show|check|get)\s+(?:current\s+)?(?:status|config(?:uration)?)', 'status', False),
        # memory command patterns
        (r'^(?:list|show)\s+(?:my\s+)?(?:saved\s+)?memory', 'memory', False),
        (r'^(?:edit|modify)\s+(?:the\s+)?(?:default\s+)?memory', 'memory', False),
        (r'^memory\s+', 'memory', False),
        # plan command patterns
        (r'^(?:list|show)\s+(?:my\s+)?(?:saved\s+)?plans?', 'plan', False),
        (r'^plan\s+', 'plan', False),
        # run/pentest command patterns
        (r'^(?:run|pentest|scan|start|launch)\s+(?:a\s+)?(?:full\s+)?(?:pentest|security\s+(?:test|audit))\s+(?:on|against)\s+', 'run', True),
        (r'^(?:run|pentest)\s+', 'run', True),
    ]

    # Target extraction pattern
    TARGET_PATTERN = re.compile(
        r'((?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?|'  # IP or CIDR
        r'(?:https?://)?[\w.-]+\.[a-zA-Z]{2,}(?:/[\w.-]*)?)',  # Domain or URL
        re.IGNORECASE
    )

    def _try_builtin_command_match(self, text: str) -> Optional[InterpretedTask]:
        """Try to match input to a built-in command using regex patterns."""
        text_lower = text.lower().strip()

        for pattern, command, has_target in self.BUILTIN_COMMAND_PATTERNS:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                target = None
                if has_target:
                    # Extract target from the text
                    target_match = self.TARGET_PATTERN.search(text_lower)
                    if target_match:
                        target = target_match.group(1).strip()

                args = [target] if target else []

                # Check for common flags in the original text
                flags = []
                if re.search(r'\b(?:safe(?:ly)?|non[- ]?destructive)\b', text_lower):
                    flags.append('--safe')
                if re.search(r'\b(?:watch|monitor|real[- ]?time|live)\b', text_lower):
                    flags.append('--watch')
                if re.search(r'\b(?:no[- ]?exploit|recon[- ]?only|reconnaissance[- ]?only)\b', text_lower):
                    flags.append('--no-exploit')

                # Check for memory/context keywords
                memory_patterns = [
                    r'(?:and\s+)?remember(?:ing)?\s+(?:to\s+)?(.+?)(?:\s*$)',
                    r'focus(?:ing)?\s+on\s+(.+?)(?:\s*$)',
                    r'prioritiz(?:e|ing)\s+(.+?)(?:\s*$)',
                    r'keep\s+in\s+mind\s+(.+?)(?:\s*$)',
                ]
                for mem_pattern in memory_patterns:
                    memory_match = re.search(mem_pattern, text_lower)
                    if memory_match:
                        memory_text = memory_match.group(1).strip()
                        if memory_text:
                            flags.extend(['-m', memory_text])
                        break

                # Check for plan references
                plan_match = re.search(r'(?:using|with)\s+(?:the\s+)?(\S+?)(?:[- ]?plan|[- ]?playbook)\b', text_lower)
                if plan_match:
                    flags.extend(['--plan', plan_match.group(1)])

                return InterpretedTask(
                    understood_request=f"Execute {command} command" + (f" on {target}" if target else ""),
                    task_description="",
                    target=target,
                    parameters=[],
                    tools_suggested=[],
                    needs_target=has_target and not target,
                    confidence='medium',
                    is_builtin_command=True,
                    maps_to_command=command,
                    command_args=args,
                    command_flags=flags
                )

        return None

    def _fallback_interpret(self, user_input: str) -> InterpretedTask:
        """Fallback to regex-based interpretation when AI is unavailable."""
        # Correct common typos
        corrected_input = self._correct_typos(user_input)

        # FIRST: Try to match to a built-in command
        # This takes priority over task pattern matching
        builtin_match = self._try_builtin_command_match(corrected_input)
        if builtin_match:
            return builtin_match

        # SECOND: If no builtin match, treat as custom task
        # Extract target
        target = self._extract_target(corrected_input)

        # Identify the task type
        task_desc, tools, confidence = self._identify_task(corrected_input)

        if task_desc and target:
            # We understood both task and target
            understood = f"Perform {task_desc} on {target}"
            description = task_desc
            confidence = 'medium'
        elif task_desc:
            # We understood the task but no target
            understood = f"Perform {task_desc}"
            description = task_desc
        elif target:
            # We have a target but unclear task
            understood = f"{corrected_input}"
            description = corrected_input
        else:
            # Couldn't understand much
            understood = corrected_input
            description = corrected_input

        return InterpretedTask(
            understood_request=understood,
            task_description=description,
            target=target,
            parameters=[],
            tools_suggested=tools,
            needs_target=target is None,
            confidence=confidence
        )

    def _extract_target(self, text: str) -> Optional[str]:
        """Extract target using regex patterns."""
        patterns = [
            r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',  # IPv4
            r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})',  # CIDR
            r'((?:https?://)?[\w.-]+\.[a-zA-Z]{2,}(?:/[\w.-]*)?)',  # URL/Domain
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip('.')

        return None


def interpret_request(user_input: str) -> Optional[InterpretedTask]:
    """
    Convenience function to interpret a user request.

    Args:
        user_input: The user's natural language request

    Returns:
        InterpretedTask with AI's understanding
    """
    interpreter = AIRequestInterpreter()
    return interpreter.interpret(user_input)


def extract_target_from_text(text: str) -> Optional[str]:
    """
    Extract just the target from text using regex.

    Args:
        text: Text that may contain a target

    Returns:
        Extracted target or None
    """
    interpreter = AIRequestInterpreter()
    return interpreter._extract_target(text)


# Keep the old class for backwards compatibility
@dataclass
class ParsedTask:
    """Represents a parsed custom task request (legacy)."""
    description: str
    target: Optional[str]
    parameters: List[str]
    category: str
    needs_clarification: bool
    clarification_question: Optional[str] = None


class RequestInterpreter:
    """Legacy interpreter - now wraps AIRequestInterpreter."""

    def parse(self, raw_input: str) -> ParsedTask:
        """Parse using AI interpreter and convert to legacy format."""
        ai_interpreter = AIRequestInterpreter()
        result = ai_interpreter.interpret(raw_input)

        if result:
            return ParsedTask(
                description=result.task_description,
                target=result.target,
                parameters=result.parameters,
                category="general",
                needs_clarification=result.needs_target,
                clarification_question="What target would you like to test?" if result.needs_target else None
            )

        return ParsedTask(
            description=raw_input,
            target=None,
            parameters=[],
            category="general",
            needs_clarification=True,
            clarification_question="What target would you like to test?"
        )
