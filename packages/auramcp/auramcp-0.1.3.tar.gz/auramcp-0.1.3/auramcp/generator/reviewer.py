"""
LLM Reviewer - Use Claude to review and enhance generated servers.

Provides optional AI-powered review and enhancement of generated code.
"""

from __future__ import annotations

import os
from typing import Any

from auramcp.generator.converter import MCPTool


class LLMReviewer:
    """Use Claude to review and enhance generated MCP servers."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the reviewer.

        Args:
            api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client = None

    @property
    def client(self):
        """Lazy-load Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                if not self.api_key:
                    raise ValueError("ANTHROPIC_API_KEY required for LLM review")
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "anthropic package required for LLM review. "
                    "Install with: pip install auramcp[llm]"
                )
        return self._client

    async def review_tools(
        self,
        tools: list[MCPTool],
        api_name: str,
    ) -> list[MCPTool]:
        """
        Review tool definitions for issues.

        Checks for:
        - Missing descriptions
        - Incorrect parameter types
        - Unclear naming
        - Missing required fields

        Args:
            tools: List of MCP tools to review
            api_name: Name of the API

        Returns:
            Enhanced list of tools
        """
        if not tools:
            return tools

        # Build tool summary for review
        tool_summaries = []
        for tool in tools:
            params = [
                f"  - {p.name}: {p.type} ({'required' if p.required else 'optional'})"
                for p in tool.parameters
            ]
            summary = f"""
Tool: {tool.name}
Description: {tool.description[:200] if tool.description else 'MISSING'}
Parameters:
{chr(10).join(params) if params else '  (none)'}
"""
            tool_summaries.append(summary)

        prompt = f"""Review these MCP tool definitions for the {api_name} API.

Identify any issues with:
1. Missing or unclear descriptions
2. Parameter naming (should be snake_case)
3. Type correctness
4. Required vs optional parameters

{chr(10).join(tool_summaries[:20])}

For each issue found, explain the problem and suggest a fix.
If the tools look good, say "No issues found."
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )

        # For now, just return the original tools
        # In a full implementation, we'd parse the response and apply fixes
        return tools

    async def enhance_descriptions(
        self,
        tools: list[MCPTool],
        api_name: str,
    ) -> list[MCPTool]:
        """
        Enhance tool descriptions using AI.

        Args:
            tools: List of MCP tools
            api_name: Name of the API

        Returns:
            Tools with enhanced descriptions
        """
        enhanced = []

        for tool in tools:
            if tool.description and len(tool.description) > 50:
                # Already has a good description
                enhanced.append(tool)
                continue

            # Generate better description
            prompt = f"""Write a clear, helpful description for this {api_name} API tool.

Tool name: {tool.name}
Method: {tool.method.value.upper()}
Path: {tool.path}
Current description: {tool.description or 'None'}
Parameters: {', '.join(p.name for p in tool.parameters)}

Write a 1-2 sentence description that explains what this tool does and when to use it.
Be specific and practical. Only output the description, nothing else.
"""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )

            # Create new tool with enhanced description
            enhanced_tool = MCPTool(
                name=tool.name,
                description=message.content[0].text.strip(),
                parameters=tool.parameters,
                category=tool.category,
                method=tool.method,
                path=tool.path,
                base_url=tool.base_url,
                content_type=tool.content_type,
                operation_id=tool.operation_id,
                tags=tool.tags,
                deprecated=tool.deprecated,
                body_schema=tool.body_schema,
                body_required=tool.body_required,
            )
            enhanced.append(enhanced_tool)

        return enhanced

    async def review_generated_code(
        self,
        code: str,
        api_name: str,
    ) -> dict[str, Any]:
        """
        Review generated code for issues.

        Args:
            code: Generated Python code
            api_name: Name of the API

        Returns:
            Review results with issues and suggestions
        """
        prompt = f"""Review this auto-generated MCP server code for the {api_name} API.

Check for:
1. Syntax errors
2. Logic issues
3. Missing error handling
4. Security concerns
5. Best practices violations

```python
{code[:8000]}
```

Provide a JSON response with:
{{
    "issues": [
        {{"severity": "error|warning|info", "line": null, "message": "..."}}
    ],
    "suggestions": ["..."],
    "overall_quality": "good|acceptable|needs_work"
}}
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse response (basic extraction)
        response_text = message.content[0].text

        # Try to extract JSON
        import json
        try:
            # Find JSON in response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response_text[start:end])
        except json.JSONDecodeError:
            pass

        # Fallback response
        return {
            "issues": [],
            "suggestions": [response_text[:500]],
            "overall_quality": "acceptable",
        }

    async def suggest_tool_grouping(
        self,
        tools: list[MCPTool],
        api_name: str,
    ) -> dict[str, list[str]]:
        """
        Suggest logical groupings for tools.

        Args:
            tools: List of MCP tools
            api_name: Name of the API

        Returns:
            Dictionary mapping group names to tool names
        """
        tool_names = [t.name for t in tools]

        prompt = f"""Group these {api_name} API tools into logical categories.

Tools: {', '.join(tool_names[:50])}

Provide a JSON response with category names as keys and lists of tool names as values.
Use clear category names like "Users", "Messages", "Files", etc.
Each tool should appear in exactly one category.
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        import json
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response_text[start:end])
        except json.JSONDecodeError:
            pass

        # Fallback: group by tags
        groups: dict[str, list[str]] = {}
        for tool in tools:
            tag = tool.tags[0] if tool.tags else "general"
            if tag not in groups:
                groups[tag] = []
            groups[tag].append(tool.name)

        return groups
