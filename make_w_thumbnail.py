from PIL import Image, ImageDraw, ImageFont
import random

def create_whatsup_thumbnail():
    print("🟢 What's-Up Thumbnail Generating...")
    WIDTH, HEIGHT = 1280, 720
    
    # WhatsApp Colors
    WA_TEAL = (7, 94, 84)
    WA_LIGHT = (37, 211, 102)
    BG_DARK = (18, 18, 18) # Dark Mode
    WHITE = (255, 255, 255)
    
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Background Pattern (Chat Doodles)
    for _ in range(30):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        r = random.randint(20, 100)
        draw.ellipse([(x,y), (x+r, y+r)], outline=(30,30,30), width=2)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 150)
        sub_font = ImageFont.truetype("arial.ttf", 40)
        name_font = ImageFont.truetype("arialbd.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        name_font = ImageFont.load_default()

    # Chat Bubbles Graphic
    # Left Bubble (Incoming)
    draw.rounded_rectangle([(100, 200), (500, 350)], radius=20, fill=(40, 40, 40))
    draw.text((130, 240), "Hello World!", font=sub_font, fill=WHITE)
    draw.text((380, 300), "10:00 AM", font=name_font, fill=(150,150,150))
    
    # Right Bubble (Outgoing)
    draw.rounded_rectangle([(700, 380), (1100, 530)], radius=20, fill=WA_TEAL)
    draw.text((730, 420), "Project 'W' is Ready!", font=sub_font, fill=WHITE)
    draw.text((980, 480), "10:01 AM ✓✓", font=name_font, fill=(100, 200, 255))

    # Title
    draw.text((350, 50), "What's-Up", font=title_font, fill=WA_LIGHT)
    draw.text((450, 180), "PYTHON LAN MESSENGER", font=sub_font, fill=WHITE)

    # Python Logo / Icon hint
    draw.ellipse([(580, 580), (700, 700)], fill=WA_LIGHT)
    draw.text((610, 610), "</>", font=ImageFont.truetype("arialbd.ttf", 50), fill=WA_TEAL)

    # Footer
    draw.rectangle([(0, HEIGHT - 60), (WIDTH, HEIGHT)], fill=WA_TEAL)
    draw.text((30, HEIGHT - 45), "Socket Programming | Multi-Threading | Tkinter", font=name_font, fill=WHITE)
    draw.rectangle([(WIDTH - 420, HEIGHT - 60), (WIDTH, HEIGHT)], fill=(0,0,0))
    draw.text((WIDTH - 400, HEIGHT - 45), "Developer: Laxmi Sanas", font=name_font, fill=WA_LIGHT)

    img.save("whatsup_thumbnail.png")
    img.show()

if __name__ == "__main__":
    create_whatsup_thumbnail()