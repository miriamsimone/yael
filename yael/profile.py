"""
User profile building at session startup.

Queries the graph for persistent context about the user,
so Yael knows who she's talking to before the conversation begins.
"""

PROFILE_QUERIES = [
    "user name identity who",
    "current projects working on",
    "profession work job background", 
    "recent topics discussed",
    "interests hobbies preferences",
]


async def build_user_profile(graph, max_per_query: int = 3) -> str:
    """
    Query graph at session start for persistent user context.

    Returns formatted string for system prompt injection.
    """
    facts = []
    seen = set()

    for query in PROFILE_QUERIES:
        try:
            # Use get_context_string which properly formats graph results
            context = await graph.get_context_string(query, max_items=max_per_query)

            if context and "Relevant context from memory:" in context:
                # Extract the bulleted items
                lines = context.split("\n")[1:]  # Skip the "Relevant context" header
                for line in lines:
                    if line.startswith("- "):
                        fact = line[2:].strip()  # Remove "- " prefix
                        key = fact[:100].lower()
                        if key not in seen and fact:
                            seen.add(key)
                            facts.append(fact)
        except Exception:
            continue

    if not facts:
        return ""

    lines = ["What I know about you:"]
    for fact in facts[:12]:
        # Clean up the fact text
        fact = " ".join(fact.split())[:300]
        lines.append(f"- {fact}")

    return "\n".join(lines)


def inject_profile(base_prompt: str, profile: str) -> str:
    """Combine base system prompt with user profile."""
    if not profile:
        return base_prompt
    
    return f"""{base_prompt}

## About This Person

{profile}

Use this naturally - don't announce you're reading from memory."""
