from PIL import Image, ImageDraw, ImageFont

width, height = 200, 200
img = Image.new("RGB", (width, height), color=0)
draw = ImageDraw.Draw(img)


def draw_gradient() -> None:
    bottom_color = (135, 206, 250)
    top_color = (99, 135, 191)
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def draw_box() -> None:
    panel_box = [0, height // 1.5, width, height]
    draw.rounded_rectangle(panel_box, radius=20, fill=(255, 255, 255))


def draw_text(*, temp: str, city) -> None:
    font_big = ImageFont.truetype("arialbd.ttf", 24)
    font_small = ImageFont.truetype("arialbd.ttf", 12)
    draw.text(xy=(10, 10), text=temp, font=font_big, fill="white")
    draw.text(xy=(width / 20, height // 1.4), text=city, font=font_big, fill="black")
    img.save("weather_final.png")


def draw_icon(weather: str, user_id) -> None:
    background = Image.open("weather_final.png").convert("RGBA")
    weather_icons = {
        'Clouds': 'cloud.png'
    }
    try:
        icon = Image.open(weather_icons[weather]).convert("RGBA")
        icon = icon.resize((64, 64))
        background.paste(icon, (background.width - 64 - 10, 10), icon)
    except:
        print("icon not found, saving without icon")
    background.save(f"weather_final{user_id}.png")


def draw_image(weather_info, user_id):
    draw_gradient()
    draw_box()
    draw_text(temp=weather_info['temp'], city=weather_info['city'])
    draw_icon(weather=weather_info['weather'], user_id=user_id)
