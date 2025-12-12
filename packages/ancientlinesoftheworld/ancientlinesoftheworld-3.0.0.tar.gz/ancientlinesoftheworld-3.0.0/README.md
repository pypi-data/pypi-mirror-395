# Ancient Scripts Converter

📜 A Python package for converting text to ancient writing systems

## How It Works / نحوه کارکرد

The converter works **character by character** using **mapping dictionaries**.  
مبدل به صورت **حرف به حرف** و با استفاده از **دایره‌المعارف‌های نگارشی** کار می‌کند.
# Text Conversion Flow

```
Input Text
│
▼
[Iterate Character by Character]
│
▼
[Check Character Type]
├─ Persian Letter → Persian Mapping Dictionary
├─ English Letter → English Mapping Dictionary
├─ Number → Number Mapping Dictionary
└─ Symbol → Symbol Mapping Dictionary
│
▼
[Convert or Keep Original]
│
▼
Output Text in Ancient Script
```


### Explanation / توضیح مرحله به مرحله:

1. **Character Mapping / نگاشت حروف**  
   - Each ancient script has its own dictionary mapping **Persian, English, numbers, and symbols**.  
     هر خط باستانی دارای دیکشنری مخصوص خود است که **حروف فارسی، انگلیسی، اعداد و علائم** را به نمادهای مربوطه تبدیل می‌کند.

2. **Conversion / تبدیل**  
   - Iterate through each character of the input text.  
   - Replace it with the mapped symbol from the dictionary.  
   - If a character is not found, keep it unchanged.  
   - هر حرف متن ورودی بررسی می‌شود، جایگزین نماد متناظر می‌شود، و اگر در دیکشنری نبود، بدون تغییر باقی می‌ماند.

3. **Supported Types / انواع پشتیبانی شده**  
   - Persian letters / حروف فارسی  
   - English letters / حروف انگلیسی  
   - Numbers / اعداد  
   - Some punctuation and symbols / برخی علائم نگارشی و سمبل‌ها

4. **Optimized Scripts / خطوط بهینه شده**  
   - Some scripts like **Linear B** or **Oracle Bone** use optimized mappings for **faster and more accurate conversion**.  
     برخی خطوط مانند **خط ب یا اوراکل بون** دارای **دایره‌المعارف بهینه** برای تبدیل سریع‌تر و دقیق‌تر هستند.

## Installation
```bash
pip install --upgrade  ancientlinesoftheworld
```

## Usage
```python
from   ancient import AncientScripts

converter = AncientScripts()

#  تبدیل  متن به خط باستانی میخی
cuneiform_text = converter.cuneiform("سلام")

print(cuneiform_text)

# تبدیل متن به خط باستانی مصری 
hieroglyph_text = converter.hieroglyph("خدا")

print(hieroglyph_text)

# تبدیل متن  تاریخی اوستایی

avesta = converter.avestan("hiسلام")
print(avesta)

print(c.get_supported_scripts())

brahmi = converter.brahmi ("HI سلام")

print(brahmi)
```

## Project :
```python

from ancient import AncientScripts, AncientTimeline

# ایجاد نمونه از کلاس اصلی
c = AncientScripts()

# ایجاد تایم‌لاین با خط پهلوی
t = AncientTimeline(script='pahlavi')

print("🕊️ Welcome to AncientLinesOfTheWorld 🏛️")
print("=" * 60)
print("🔹 Supported Ancient Scripts:")
for name, desc in c.get_supported_scripts().items():
    print(f"  - {name:<12} → {desc}")
print("=" * 60)


text = "hi"
print(f"\nOriginal text: {text}\n")

print("🪶 Converted Texts:")
print(f"  🔸 Pahlavi:       {c.pahlavi(text)}")
print(f"  🔸 Akkadian:      {c.akkadian(text)}")
print(f"  🔸 Avestan:       {c.avestan(text)}")
print(f"  🔸 Manichaean:    {c.manichaean(text)}")
print(f"  🔸 Linear B:      {c.linear_b(text)}")
print(f"  🔸 Hebrew:        {c.hebrew(text)}")
print(f"  🔸 Hieroglyph:    {c.hieroglyph(text)}")
print(f"  🔸 Sanskrit:      {c.sanskrit(text)}")
print(f"  🔸 Oracle Bone:   {c.oracle_bone(text)}")
print(f"  🔸 : cuneiform :  {c.cuneiform(text)}")
print(f"  🔸 brahmi :  {c.brahmi (text)}")

print("\n" + "=" * 60)

# 🕰️ نمایش زمان زنده با خط پهلوی
print("📜 Real-time Ancient Timeline (Pahlavi Script):")
t.show()

print("=" * 60)
print("💫 Powered by AncientLinesOfTheWorld | Created by AmirHossein Kader")
```

## generate image

```python
from ancient import AncientImageGenerator

# ساخت شیء از کلاس و تعیین نوع خط
generator = AncientImageGenerator(script="cuneiform")

# متنی که می‌خوای تبدیل بشه
text = "تمدن از اینجا آغاز شد"

# تولید تصویر با متن باستانی
output_image = generator.generate_image(text)

print(f"📜 تصویر آماده شد و در این مسیر ذخیره شد:\n{output_image}")

```
#  AncientTimeline

کلاس `AncientTimeline` برای **نمایش زمان فعلی به خطوط باستانی** (میخی، پهلوی، منیایی، هیروگلیف، اکدی، اوراکل بون، اوستایی) طراحی شده است.

### ⚙️ پارامترها

| پارامتر | نوع | توضیح |
|---------|-----|-------|
| `script` | `str` | خط باستانی برای نمایش (`'cuneiform'`, `'pahlavi'`, `'manichaean'`, `'hieroglyph'`, `'akkadian'`, `'oracle_bone'`, `'avestan'`) |
| `ancient_format` | `bool` | اگر `True` باشد، تاریخ به سبک باستانی نمایش داده می‌شود |

### 🖥️ نمونه استفاده

# 🏺 AncientTimeline

کلاس `AncientTimeline` برای **نمایش زمان فعلی به خطوط باستانی** (میخی، پهلوی، منیایی، هیروگلیف، اکدی، اوراکل بون، اوستایی) طراحی شده است.

### ⚙️ پارامترها

| پارامتر | نوع | توضیح |
|---------|-----|-------|
| `script` | `str` | خط باستانی برای نمایش (`'cuneiform'`, `'pahlavi'`, `'manichaean'`, `'hieroglyph'`, `'akkadian'`, `'oracle_bone'`, `'avestan'`) |
| `ancient_format` | `bool` | اگر `True` باشد، تاریخ به سبک باستانی نمایش داده می‌شود |

### 🖥️ نمونه استفاده

```python
from ancient import AncientTimeline

timeline = AncientTimeline(script='pahlavi', ancient_format=True)

print(timeline.as_text())  # دریافت زمان فعلی به صورت متن
timeline.show()            # نمایش زمان روی کنسول


```
## 🔑 پیش‌نیاز

برای استفاده از این کلاس شما نیاز دارید:

1. ثبت‌نام در لیارا و دریافت **API Key**:
   [https://console.liara.ir/ai](https://console.liara.ir/ai)



```python
from ancient import  AncientScriptAI

# وارد کردن توکن API خود
api_key = ""
ai_bot =  AncientScriptAI(api_key=api_key)

# متن ورودی کاربر
text = "سلام باستانی"
script = "cuneiform"


# گرفتن پاسخ AI
response = ai_bot.get_ancient_response(text, script)
print(response)



```


## Supported Scripts
- Cuneiform
- Egyptian Hieroglyphs
- Pahlavi script
- Manichaean script
- Linear B
-avestan
-brahmi
-

- And more...

# 🌐 بخش WebApp — کلاس `AncientWeb`

کلاس **`AncientWeb`** یکی از قابلیت‌های منحصربه‌فرد کتابخانه `ancientlinesoftheworld` است.  
این کلاس یک **وب‌اپلیکیشن لوکال** فراهم می‌کند که به شما اجازه می‌دهد متن‌ها را به **خطوط باستانی** تبدیل کنید، بدون نیاز به هاست یا سرور خارجی.

---


## 🎯 وظیفه کلاس

- اجرای خودکار یک **وب‌اپ Flask** روی سیستم شما  
- نمایش رابط کاربری ساده و کاربرپسند  
- پشتیبانی از **تمام خطوط باستانی موجود در کتابخانه**  
- امکان استفاده آفلاین و لوکال  
- مناسب برای تست، دمو یا استفاده شخصی و آموزشی  

---

## 🚀 نمونه استفاده

```python
from ancient.web_app import AncientWeb

# ایجاد نمونه کلاس
app = AncientWeb(version="2.5.0")

# اجرای وب‌اپ لوکال
app.run_app()

```

## لیست کلاس‌های کتابخانه و قابلیت‌های آن‌ها:

AncientScripts – تبدیل متن به خطوط باستانی مختلف

AncientTimeline – نمایش زمان فعلی به فرمت باستانی (میخی، پهلوی، اوستایی و …)

AncientImageGenerator – تولید تصاویر مرتبط با خطوط باستانی و طرح‌های تاریخی

AncientScriptAI – پردازش و تولید محتوای هوشمند با خطوط باستانی

AncientWeb – ابزارهای وب برای نمایش خطوط باستانی


## یاداشت علمی درباره این پروژه:





**1. سایت علمی civilica**
   [https://civilica.com/note/17282/](https://civilica.com/note/17282/)
   




