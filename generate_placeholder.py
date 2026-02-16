from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder():
    # Dimensions matching the index.html logic
    width, height = 800, 600
    
    # Create background (Dark Gray / Urban context)
    img = Image.new('RGB', (width, height), color=(50, 50, 60))
    draw = ImageDraw.Draw(img)
    
    # Draw the "Standard Billboard" area
    # Matches CONFIG.dropZone: x=100, y=50, w=600, h=400
    rect_x, rect_y = 100, 50
    rect_w, rect_h = 600, 400
    
    # Draw a border/frame for the billboard
    frame_thickness = 10
    draw.rectangle(
        [rect_x - frame_thickness, rect_y - frame_thickness, rect_x + rect_w + frame_thickness, rect_y + rect_h + frame_thickness], 
        fill=(30, 30, 30)
    )
    
    # Draw the white canvas area
    draw.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], fill=(255, 255, 255))
    
    # Draw a "pole" or stand
    pole_w = 40
    pole_h = 100
    pole_x = width // 2 - pole_w // 2
    pole_y = rect_y + rect_h + frame_thickness
    draw.rectangle([pole_x, pole_y, pole_x + pole_w, pole_y + pole_h], fill=(40, 40, 40))
    
    print(f"Generating image at {os.getcwd()}\\billboard_mockup_background.png")
    img.save('billboard_mockup_background.png')

if __name__ == "__main__":
    create_placeholder()
