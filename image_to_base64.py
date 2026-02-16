import base64

with open('billboard_mockup_background.png', 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
with open('bg_base64.txt', 'w') as f:
    f.write(f"data:image/png;base64,{encoded_string}")
