from PIL import Image, ImageDraw, ImageFont
from .core import AncientScripts
import textwrap
import os
import datetime


class AncientImageGenerator:
    """
    Generate an image with ancient script text overlay automatically.
    Uses the default background image inside the package,
    but saves the output in the USER PROJECT directory.

    Example:
        from ancient.visualizer import AncientImageGenerator

        gen = AncientImageGenerator(script='cuneiform')
        gen.generate_image("سلام دنیا")
    """

    def __init__(self, script="cuneiform"):
        self.converter = AncientScripts()
        self.script = script

    def generate_image(self, text):
        """Convert text to ancient script and draw on image (output in user path)."""

        # مسیر فایل‌های پکیج
        package_dir = os.path.dirname(__file__)

        background_path = os.path.join(package_dir, "background.jpg")
        font_path = os.path.join(package_dir, "NotoSansCuneiform-Regular.ttf")

        # بررسی فایل‌ها
        if not os.path.exists(background_path):
            raise FileNotFoundError("❌ background.jpg not found in package folder.")
        if not os.path.exists(font_path):
            raise FileNotFoundError("❌ Font file not found in package folder.")

        # انتخاب متد تبدیل
        convert_func = getattr(self.converter, self.script, None)
        if not convert_func:
            raise ValueError(f"Unsupported script: {self.script}")

        ancient_text = convert_func(text)

        # بارگذاری تصویر
        img = Image.open(background_path)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # تابع اندازه
        def get_text_size(font, text):
            bbox = font.getbbox(text)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]

        # تنظیم اندازه متن
        def fit_text(text, font_path, max_width, max_height):
            font_size = 100
            font = ImageFont.truetype(font_path, font_size)
            wrapped = textwrap.wrap(text, width=40)

            while True:
                total_height = sum(get_text_size(font, line)[1] for line in wrapped)
                if total_height <= max_height and all(get_text_size(font, line)[0] <= max_width for line in wrapped):
                    break

                font_size -= 2
                if font_size < 10:
                    break

                font = ImageFont.truetype(font_path, font_size)

            return font, wrapped

        font, lines = fit_text(ancient_text, font_path, width - 50, height - 50)

        # نوشتن متن وسط تصویر
        y_text = (height - sum(get_text_size(font, line)[1] for line in lines)) // 2

        for line in lines:
            line_width, line_height = get_text_size(font, line)
            x_text = (width - line_width) // 2
            draw.text((x_text, y_text), line, font=font, fill=(0, 0, 0))
            y_text += line_height

        # مسیر خروجی: مسیر اجرای کاربر!
        user_dir = os.getcwd()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(user_dir, f"ancient_text_{timestamp}.png")

        img.save(output_path)

        print(f"✅ تصویر با متن باستانی ساخته شد: {output_path}")
        return output_path
