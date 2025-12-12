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



__version__ = "2.5.5"
__all__ = ['AncientScripts','AncientTimeline','AncientImageGenerator','AncientScriptAI','AncientWeb']
__author__ = "Amir Hossein Khazaei"
__description__ = "A library for converting Persian and English texts into ancient scripts such as Pahlavi, Avestan, Cuneiform, Manichaean, and more."
__license__ = "MIT"