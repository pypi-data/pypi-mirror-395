from .core import AncientScripts
from .mappings import (
    persian_to_cuneiform_mapping, persian_to_manichaean_mapping, 
    persian_to_hieroglyph_mapping, english_to_cuneiform_mapping,
    english_to_pahlavi_mapping, persian_to_pahlavi_mapping,
    english_to_manichaean_mapping, english_to_hieroglyph_mapping,
    linear_b_dict, conversion_dict, convert_to_cuneiform,
    convert_to_pahlavi, convert_to_manichaean, convert_to_hieroglyph,
    text_to_linear_b_optimized, convert_to_akkadian, convert_to_oracle_bone,convert_to_avestan
)
from .timeline import AncientTimeline
from .visualizer import AncientImageGenerator
from .ai_chat import AncientScriptAI
from .releases import get_releases
from .web_app import AncientWeb



__version__ = "3.0.0"
__all__ = ['AncientScripts','AncientTimeline','AncientImageGenerator','AncientScriptAI','AncientWeb']
__author__ = "Amir Hossein Khazaei"
__website__ = "https://civilica.com/note/17282/"


__description__ = (
    "A comprehensive Python library for converting modern text into ancient scripts, "
    "offering precise, character-by-character transformations across more than 12 historical writing systems. "
    "Includes rich historical datasets for accurate conversions, AI-powered chat functionality for intelligent text analysis, "
    "automatic text generation in ancient styles, and customizable image creation from generated text. "
    "Perfect for researchers, educators, artists, and developers interested in historical scripts and creative projects."
)


__license__ = "MIT"


__platform__ = ["Windows", "Linux", "MacOS"]

__status__ = "Stable"

__copyright__ = "© 2025 Amir Hossein Khazaei"

__docs__ = "https://github.com/amirhossinpython/ancientlinesoftheworld-"

__long_description__ = "This library allows converting modern text to ancient scripts with AI chat, image generation, and precise text transformations..."


__topics__ = ["Text Conversion", "Ancient Scripts", "AI", "Image Generation", "Digital Humanities",'ancientlinesoftheworld','ancient scripts',
    "خطوط باستانی",'کتابخانه تبدیل متن به خطوط باستانی']

__repository__ = "https://github.com/amirhossinpython/ancientlinesoftheworld-"


__dependencies__ = ["Flask", "Pillow", "feedparser", "openai","deep-translator"]

__maintainer__ = "Amir Hossein Khazaei"


__keywords__ = [

    "ancient scripts",
    "ancient writing",
    "ancient text converter",
    "historical scripts",
    "epigraphy",
    "paleography",
    "linguistics",
    "ancient linguistics",
    "ancientlinesoftheworld"

    # Specific scripts supported
    "cuneiform",
    "akkadian",
    "old persian",
    "pahlavi",
    "avestan",
    "manichaean",
    "hieroglyph",
    "egyptian hieroglyphs",
    "linear b",
    "oracle bone script",
    "sanskrit",
    "brahmi",
    "hebrew ancient",
    "aramaic",
    "middle persian",

    # AI / NLP features
    "AI",
    "artificial intelligence",
    "NLP",
    "language model",
    "text transformation",
    "script generation",
    "ancient script AI",
    "text to script",

    # Persian/Iran-related
    "Iranian studies",
    "ancient Iran",
    "Persian scripts",
    "تبدیل متن",
    "تبدیل متن به خطوط باستانی",
    "خطوط باستانی",
    "خط میخی",
    "خط پهلوی",
    "خط اوستایی",
    "باستان شناسی",
    "فرهنگ ایران باستان",

    # Software & library
    "python library",
    "text converter",
    "visual generator",
    "image generator",
    "web app",
    "script visualizer",
    "timeline generator",
    "ancient timeline",

    # General tags for better SEO
    "unicode converter",
    "script mapping",
    "historical tools",
    "cultural heritage",
    "digital humanities",
    "linguistic tools",
]

__license__ = "MIT"