"""
Ancient Scripts Conversion Core Module

This module contains the main class for converting text to ancient scripts.
"""

from typing import Dict, Union
from deep_translator import GoogleTranslator
from .mappings import (
    persian_to_cuneiform_mapping, persian_to_manichaean_mapping, 
    persian_to_hieroglyph_mapping, english_to_cuneiform_mapping,
    english_to_pahlavi_mapping, persian_to_pahlavi_mapping,
    english_to_manichaean_mapping, english_to_hieroglyph_mapping,
    linear_b_dict, conversion_dict, convert_to_cuneiform,
    convert_to_pahlavi, convert_to_manichaean, convert_to_hieroglyph,
    text_to_linear_b_optimized, convert_to_akkadian, convert_to_oracle_bone,convert_to_avestan
)

class AncientScripts:
    """Main class for ancient scripts conversion"""
    
    def __init__(self):
        """Initialize with supported scripts"""
        self.supported_scripts = {
            'cuneiform': 'Convert to Cuneiform script',
            'pahlavi': 'Convert to Pahlavi script',
            'manichaean': 'Convert to Manichaean script',
            'hieroglyph': 'Convert to Egyptian Hieroglyphs',
            'hebrew': 'Translate to Modern Hebrew',
            'linear_b': 'Convert to Linear B script',
            'sanskrit': 'Translate to Sanskrit',
            'akkadian': 'Convert to Akkadian cuneiform',
            'oracle_bone': 'Convert to Oracle Bone script',
            'avestan' : 'Convert to avestan'
        }
    
    def get_supported_scripts(self) -> Dict[str, str]:
        """Return dictionary of supported scripts with descriptions"""
        return self.supported_scripts
    
    def convert(self, text: str, script: str) -> Union[str, None]:
        """
        Convert text to specified ancient script
        
        Args:
            text: Input text to convert
            script: Target script name
            
        Returns:
            Converted text or None if script not supported
        """
        converter = getattr(self, script, None)
        if converter:
            return converter(text)
        raise ValueError(f"Unsupported script. Available: {list(self.supported_scripts.keys())}")
    
    def cuneiform(self, text: str) -> str:
        """Convert text to Cuneiform script"""
        return convert_to_cuneiform(text)
    
    def pahlavi(self, text: str) -> str:
        """Convert text to Pahlavi script"""
        return convert_to_pahlavi(text)
    
    def manichaean(self, text: str) -> str:
        """Convert text to Manichaean script"""
        return convert_to_manichaean(text)
    
    def hieroglyph(self, text: str) -> str:
        """Convert text to Egyptian Hieroglyphs"""
        return convert_to_hieroglyph(text)
    
    def hebrew(self, text: str) -> str:
        """Translate text to Modern Hebrew"""
        return GoogleTranslator(source='auto', target='iw').translate(text)
    
    def linear_b(self, text: str) -> str:
        """Convert text to Linear B script"""
        return text_to_linear_b_optimized(text)
    
    def sanskrit(self, text: str) -> str:
        """Translate text to Sanskrit"""
        return GoogleTranslator(source='auto', target='sa').translate(text)
    
    def akkadian(self, text: str) -> str:
        """Convert text to Akkadian cuneiform"""
        return convert_to_akkadian(text)
    
    def oracle_bone(self, text: str) -> str:
        """Convert text to Oracle Bone script"""
        return convert_to_oracle_bone(text)

    def avestan(self, text: str) -> str:
        """Convert text to Avestan script"""
        return convert_to_avestan(text)
    