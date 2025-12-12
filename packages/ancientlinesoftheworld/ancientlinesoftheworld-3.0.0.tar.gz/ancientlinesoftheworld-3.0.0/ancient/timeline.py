from datetime import datetime
from .mappings import (
    convert_to_cuneiform,
    convert_to_pahlavi,
    convert_to_manichaean,
    convert_to_hieroglyph,
    convert_to_akkadian,
    convert_to_oracle_bone,
    convert_to_avestan,
)


class AncientTimeline:
    """
    نمایش تایم‌لاین (زمان کنونی) با خطوط باستانی هخامنشی/اوستایی
    نویسنده: امیرحسین خزاعی
    """

    # ماه‌های اوستایی هخامنشی
    _avestan_months = [
        "Fravaṣi", "Ardawahishta", "Haurvatāt", "Tištrya",
        "Amərətāt", "Xšaθra Vairya", "Miθra", "Ābān",
        "Ātar", "Daiθi", "Vohu Manah", "Spənta Ārmaiti"
    ]

    def __init__(self, script: str = 'cuneiform', ancient_format: bool = False):
        self.supported_scripts = [
            'cuneiform', 'pahlavi', 'manichaean',
            'hieroglyph', 'akkadian', 'oracle_bone', 'avestan'
        ]

        if script not in self.supported_scripts:
            raise ValueError(
                f"❌ زبان نامعتبر است.\nگزینه‌های معتبر:\n{self.supported_scripts}"
            )

        self.script = script
        self.ancient_format = ancient_format

    def _convert_text(self, text: str) -> str:
        if self.script == 'cuneiform':
            return convert_to_cuneiform(text)
        elif self.script == 'pahlavi':
            return convert_to_pahlavi(text)
        elif self.script == 'manichaean':
            return convert_to_manichaean(text)
        elif self.script == 'hieroglyph':
            return convert_to_hieroglyph(text)
        elif self.script == 'akkadian':
            return convert_to_akkadian(text)
        elif self.script == 'oracle_bone':
            return convert_to_oracle_bone(text)
        elif self.script == "avestan":
            return convert_to_avestan(text)
        return text


    def _format_ancient_persian(self, now: datetime) -> str:
        day = now.day
        month_index = now.month - 1  # 0-indexed
        year = now.year

        # نام ماه اوستایی
        month_name = self._avestan_months[month_index]

        # ساعت، دقیقه، ثانیه
        time_str = f"{now.hour:02d} Hours | {now.minute:02d} Minutes | {now.second:02d} Seconds"

        
        return (
            f"𐎹 Year of Ahura Mazda: {year} 𐎹\n"
            f"𐎹 Month: {month_name} 𐎹\n"
            f"𐎹 Day: {day} 𐎹\n"
            f"𐎹 Time: {time_str} 𐎹"
        )


    def get_ancient_time(self) -> str:
        now = datetime.now()
        if self.ancient_format:
            formatted = self._format_ancient_persian(now)
        else:
            formatted = now.strftime("%Y-%m-%d | %H:%M:%S")
        return self._convert_text(formatted)


    def show(self):
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("        📜 Ancient Timeline")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🔹 Script      : {self.script}")
        print(f"🔹 Ancient     : {self.ancient_format}")
        print(f"🔸 Time        :\n{self.get_ancient_time()}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    def as_text(self):
        return self.get_ancient_time()
