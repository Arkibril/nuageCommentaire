import re

def update_config():
    # Read the base64 string
    with open('bg_base64.txt', 'r') as f:
        base64_str = f.read().strip()

    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update backgroundImagePath
    # We look for: backgroundImagePath: '...',
    # We replace with: backgroundImagePath: 'base64_str',
    
    # Regex to find the current line. 
    # Use re.DOTALL is not strictly needed if it's single line, but good practice.
    # We assume standard JS syntax with single quotes as currently in file.
    
    # Update Image Path
    # Note: The quote might be ' or " so we handle both, capture the key and the following quote
    pattern_img = r"(backgroundImagePath:\s*)(['\"])(.*?)(['\"])(,)"
    
    # We want to replace group 3 with our base64_str
    # But since the base64 string is massive, let's just construct the replacement string manually
    # Finding the start and end indices might be safer or just string replacement if unique.
    
    # Let's try the regex sub.
    # We use a lambda to insert the file content.
    new_content = re.sub(
        pattern_img, 
        lambda m: f"{m.group(1)}'{base64_str}'{m.group(5)}", 
        content, 
        count=1
    )

    # 2. Update dropZone coordinates using regex for each property
    # Target: x: ..., 
    new_content = re.sub(r"(x:\s*)(\d+)", r"\g<1>22", new_content)
    new_content = re.sub(r"(y:\s*)(\d+)", r"\g<1>737", new_content)
    new_content = re.sub(r"(width:\s*)(\d+)", r"\g<1>1033", new_content)
    new_content = re.sub(r"(height:\s*)(\d+)", r"\g<1>514", new_content)

    # Write back
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Updated index.html successfully.")

if __name__ == "__main__":
    update_config()
