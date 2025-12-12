from .core import AncientScripts
from openai import OpenAI


class AncientScriptAI:
    """
    تولید پاسخ با هوش مصنوعی به زبان های باستانی
    """

    SUPPORTED_SCRIPTS = [
        'cuneiform', 'pahlavi', 'manichaean',
        'hieroglyph', 'akkadian', 'oracle_bone',
        'avestan', 'linear_b',"hebrew","sanskrit"
        ,"brahmi"
    ]

    def __init__(self, api_key: str, base_url: str = "https://ai.liara.ir/api/v1/6825d0c28c48644ab8263648"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.converter = AncientScripts()

    def get_ancient_response(self, user_input: str, script: str) -> str:
        """
        دریافت پاسخ هوش مصنوعی به زبان باستانی

        Args:
            user_input (str): متن ورودی کاربر
            script (str): زبان باستانی هدف (یکی از SUPPORTED_SCRIPTS)

        Returns:
            str: پاسخ هوش مصنوعی به زبان باستانی
        """

        if script not in self.SUPPORTED_SCRIPTS:
            return f"❌ زبان نامعتبر است. گزینه‌های معتبر: {self.SUPPORTED_SCRIPTS}"

        system_prompt = (
            f"شما یک دستیار باستان‌شناس هستید. "
            f"کاربر به شما متنی می‌دهد و شما فقط و فقط "
            f"به زبان {script} پاسخ می‌دهید. "
            f"هیچ کلمه‌ای به فارسی یا انگلیسی استفاده نکنید. "
            f"اگر لازم است توضیح دهید، حتماً با همان زبان باستانی باشد."
        )

        try:
            completion = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = completion.choices[0].message.content.strip()

            # تبدیل پاسخ به خط باستانی انتخابی
            if hasattr(self.converter, script):
                ancient_text = getattr(self.converter, script)(ai_response)
                return ancient_text
            else:
                return ai_response

        except Exception as e:
            return f"خطا در ارتباط با API: {str(e)}"




