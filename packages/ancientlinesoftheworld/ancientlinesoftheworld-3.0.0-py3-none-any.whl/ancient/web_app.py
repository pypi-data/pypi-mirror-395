# web_app.py

from flask import Flask, render_template, request, jsonify, send_from_directory
from deep_translator import GoogleTranslator
import logging
import os
from .core import AncientScripts

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AncientWeb:
    """
    اجرای وب اپلیکیشن لوکال برای تبدیل متن به خطوط باستانی
    """

    def __init__(self, version="2.4.3"):
        self.version = version
        self.convert = AncientScripts()

        # مسیر قالب‌ها و فایل‌های استاتیک داخل پکیج
        base_dir = os.path.dirname(__file__)
        template_dir = os.path.join(base_dir, "templates")
        static_dir = os.path.join(base_dir, "static")

        self.app = Flask(__name__, 
                         template_folder=template_dir, 
                         static_folder=static_dir)
        
        self._setup_routes()

    # --------------------------- Routes ---------------------------
    def _setup_routes(self):

        @self.app.route('/')
        def index():
            return render_template('index.html', version=self.version)

        @self.app.route('/convert', methods=['POST'])
        def convert_text():
            data = request.get_json()
            text = data.get('text', '')
            language = data.get('language', '')

            logger.info(f'Request: text="{text}", language="{language}"')

            converted = self._convert(text, language)
            return jsonify({'result': converted})

        @self.app.route('/service-worker.js')
        def service_worker():
            return send_from_directory(self.app.static_folder, 'service-worker.js')


    # --------------------------- Converter ---------------------------
    def _convert(self, text, language):
        try:
            if language == 'cuneiform':
                return self.convert.cuneiform(text)

            elif language == 'pahlavi':
                return self.convert.pahlavi(text)

            elif language == 'manichaean':
                return self.convert.manichaean(text)

            elif language == 'hieroglyph':
                return self.convert.hieroglyph(text)

            elif language == 'Hebrew':
                return GoogleTranslator(source='auto', target='iw').translate(text)

            elif language == "linear_b_optimized":
                return self.convert.linear_b(text)

            elif language == "sanskrit":
                return GoogleTranslator(source='auto', target='sa').translate(text)

            elif language == 'akkadian':
                return self.convert.akkadian(text)

            elif language == 'oracle_bone':
                return self.convert.oracle_bone(text)

            elif language == 'avestan':
                return self.convert.avestan(text)

            return "Invalid language selection."

        except Exception as e:
            logger.error(f"Conversion Error: {e}")
            return f"❌ Error: {e}"

    # --------------------------- Runner ---------------------------
    def run_app(self, host='127.0.0.1', port=5000, debug=True):
        print(f"🌐 WebApp running: http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
