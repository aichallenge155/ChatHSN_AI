from config import RESPONSE_STYLES

def get_available_styles():
    """Return a list of available response styles."""
    return list(RESPONSE_STYLES.keys())

def get_style_description(style):
    """Return the description of a specific style."""
    return RESPONSE_STYLES.get(style, "Style not found")

def format_response(response, style="default"):
    """
    Format the AI response based on the selected style.
    This can be extended to add additional formatting specific to each style.
    
    Args:
        response (str): The AI-generated response
        style (str): The style used for generation
    
    Returns:
        str: The formatted response
    """
    # Basic formatting based on style
    if style == "default":
        return response
    elif style == "kid":
        # Maybe add some emoji for kid style
        return f"🤔 {response} 🌈"
    elif style == "physics_teacher":
        # Add a scholarly note
        return f"📚 {response}\n\n*Bu elmi bir açıqlamadır.*"
    elif style == "poet":
        # Add decorative elements for poetic style
        return f"✨ {response} ✨\n~ 🖋️ ~"
    elif style == "historian":
        # Add a historical note
        return f"📜 {response}\n\n*Tarixi perspektivdən.*"
    else:
        return response

def get_style_emoji(style):
    """Return an emoji representing the style."""
    style_emojis = {
        "default": "🤖",
        "kid": "👶",
        "physics_teacher": "🔬",
        "poet": "🎭",
        "historian": "📜"
    }
    return style_emojis.get(style, "🤖")

def get_rich_style_info():
    """Return a dictionary with rich information about all styles."""
    info = {}
    for style in RESPONSE_STYLES.keys():
        info[style] = {
            "description": RESPONSE_STYLES[style],
            "emoji": get_style_emoji(style),
            "example": get_example_response(style)
        }
    return info

def get_example_response(style):
    """Return an example response for a specific style."""
    examples = {
        "default": "Bu, standart üslubdakı bir cavabdır. Dəqiq və faydalı.",
        "kid": "Vauuu! Bu, doğrudan da maraqlı bir şeydir! Mən bunu heç vaxt bilmirdim!",
        "physics_teacher": "Əgər F = ma düsturunu nəzərdən keçirsək, qüvvənin kütlə ilə təcilin hasili olduğunu görərik.",
        "poet": "Dan yeri sökülür, günəş qızılı şəfəqlərilə dünyaya can verir...",
        "historian": "19-cu əsrin ortalarında baş verən bu hadisə, dövrün sosial-iqtisadi şərtlərinin təsiri altında idi."
    }
    return examples.get(style, "Nümunə yoxdur.")