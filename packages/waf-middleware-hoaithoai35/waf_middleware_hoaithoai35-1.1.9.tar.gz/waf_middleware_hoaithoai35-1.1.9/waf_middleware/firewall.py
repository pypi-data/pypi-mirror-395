import logging
from flask import request, abort
import time
import json
import re
import hashlib
import requests 
import threading
import os # <--- [QUAN TRỌNG] Phải có cái này

# --- CẤU HÌNH TELEGRAM ---
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN" 
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# --- [QUAN TRỌNG] XÁC ĐỊNH VỊ TRÍ GỐC CỦA THƯ VIỆN ---
# Giúp tìm thấy file rules.json dù thư viện được cài ở bất cứ đâu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_waf_logger():
    logger = logging.getLogger('WAF')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler('waf.log', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(handler)
    return logger

waf_logger = setup_waf_logger()

class Firewall:
    RATE_LIMIT_COUNT = 100
    RATE_LIMIT_PERIOD = 60
    SCAN_DETECTION_COUNT = 20
    SCAN_DETECTION_PERIOD = 60
    BLOCKED_COUNTRIES = ['CN', 'RU', 'KP']
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
    MAGIC_BYTES = {
        b'\xff\xd8\xff': 'jpg',
        b'\x89PNG\r\n\x1a\n': 'png',
        b'GIF87a': 'gif',
        b'GIF89a': 'gif'
    }

    def __init__(self, app=None, db_callback=None):
        self.ip_requests = {}
        self.ip_404_counts = {}
        self.blacklisted_ips = set()
        self.tor_ips = set()
        self.malicious_hashes = set()
        self.rules = []
        self.db_callback = db_callback
        if app: self.init_app(app)

    def init_app(self, app):
        self._load_blacklist()
        self._load_tor_ips()
        self._load_malicious_hashes()
        self._load_rules()
        app.before_request(self._check_request)
        app.after_request(self._check_response)

    # --- SỬA LỖI ĐƯỜNG DẪN: Dùng os.path.join(BASE_DIR, ...) ---
    
    def _load_blacklist(self):
        try:
            file_path = os.path.join(BASE_DIR, 'blacklist.txt') # <-- SỬA
            with open(file_path, 'r', encoding='utf-8') as f:
                self.blacklisted_ips = {line.strip() for line in f if line.strip()}
        except: pass

    def _load_tor_ips(self):
        try:
            file_path = os.path.join(BASE_DIR, 'tor_ips.txt') # <-- SỬA
            with open(file_path, 'r', encoding='utf-8') as f:
                self.tor_ips = {line.strip() for line in f if line.strip()}
        except: pass

    def _load_malicious_hashes(self):
        try:
            file_path = os.path.join(BASE_DIR, 'malicious_hashes.txt') # <-- SỬA
            with open(file_path, 'r', encoding='utf-8') as f:
                self.malicious_hashes = {line.strip().lower() for line in f if line.strip()}
        except: pass

    def _load_rules(self):
        try:
            file_path = os.path.join(BASE_DIR, 'rules.json') # <-- SỬA QUAN TRỌNG NHẤT
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_rules = json.load(f)
                for rule in raw_rules:
                    try:
                        rule['compiled_pattern'] = re.compile(rule['pattern'], re.IGNORECASE)
                        self.rules.append(rule)
                    except: pass
                # In ra để debug xem đã load được chưa
                print(f"✅ [WAF LIB] Loaded {len(self.rules)} rules from {file_path}")
        except Exception as e:
            print(f"❌ [WAF LIB] Error loading rules: {e}")

    # --- CÁC HÀM LOGIC CÒN LẠI (GIỮ NGUYÊN) ---
    
    def _send_telegram_async(self, message):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, data=payload, timeout=5)
        except Exception as e:
            print(f"TeleBot Error: {e}")

    def _log_to_db(self, ip, attack_type, rule_id, description, payload):
        if self.db_callback:
            self.db_callback(ip, attack_type, rule_id, description, payload)
        
        if attack_type not in ["Reconnaissance"]: 
            icon = "⚠️"
            if "SQL" in attack_type: icon = "💉"
            elif "XSS" in attack_type: icon = "💀"
            elif "Honeypot" in attack_type: icon = "🍯"
            elif "CSRF" in attack_type: icon = "🎭"
            elif "Malicious" in attack_type: icon = "🦠"
            elif "DoS" in attack_type: icon = "🌊"
            
            msg = (
                f"{icon} *WAF ALERT DETECTED*\n"
                f"➖➖➖➖➖➖➖➖➖\n"
                f"🛑 *Type:* {attack_type}\n"
                f"🌍 *IP:* `{ip}`\n"
                f"🔍 *Rule:* {description}\n"
                f"📦 *Payload:* `{payload}`\n"
                f"🕒 *Time:* {time.strftime('%H:%M:%S')}"
            )
            threading.Thread(target=self._send_telegram_async, args=(msg,)).start()

    def _get_client_ip(self):
        fake_ip = request.headers.get('X-Fake-IP')
        return fake_ip if fake_ip else request.remote_addr

    def _inspect_uploaded_file(self, file, ip):
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
            return "Invalid Extension"
        first_bytes = file.read(10)
        file.seek(0)
        is_valid_image = False
        for magic, filetype in self.MAGIC_BYTES.items():
            if first_bytes.startswith(magic):
                is_valid_image = True
                break
        if not is_valid_image:
            return "Spoofed Extension (Magic Bytes mismatch)"
        content = file.read()
        file.seek(0)
        file_hash = hashlib.md5(content).hexdigest()
        if file_hash in self.malicious_hashes:
            return f"Malicious Hash Detected: {file_hash}"
        return None

    def _check_request(self):
        if any(request.path.startswith(p) for p in ['/waf-dashboard', '/static', '/admin', '/api']): return
        ip = self._get_client_ip()
        
        if ip in self.blacklisted_ips:
            # self._log_to_db(ip, "Blacklist", "N/A", "IP Blocked", "N/A") 
            abort(403)

        if ip in self.tor_ips:
            self._log_to_db(ip, "Tor Network", "TOR", "Tor IP Blocked", "N/A")
            abort(403)

        if request.path in ['/admin-backup', '/config.php']:
            self._log_to_db(ip, "Honeypot", "TRAP", "Honeypot Triggered", request.path)
            self.blacklisted_ips.add(ip)
            abort(403)

        country = request.headers.get('X-Country', 'VN')
        if country in self.BLOCKED_COUNTRIES:
            self._log_to_db(ip, "GeoIP", "GEO", f"Blocked Country: {country}", country)
            abort(403)

        if request.path == '/upload' and request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                threat = self._inspect_uploaded_file(file, ip)
                if threat:
                    self._log_to_db(ip, "Malicious Upload", "FILE", threat, file.filename)
                    abort(403)

        if request.method in ['POST', 'PUT', 'DELETE']:
            origin = request.headers.get('X-Origin-Fake') or request.headers.get('Origin')
            if origin:
                host = request.headers.get('Host')
                if host and host not in origin:
                     self._log_to_db(ip, "CSRF Attack", "CSRF_01", "Cross-Origin Request Blocked", f"Origin: {origin} -> Host: {host}")
                     abort(403)

        now = time.time()
        if ip not in self.ip_requests or now - self.ip_requests[ip]['start'] > self.RATE_LIMIT_PERIOD:
            self.ip_requests[ip] = {'count': 1, 'start': now}
        else:
            self.ip_requests[ip]['count'] += 1

        if self.ip_requests[ip]['count'] > self.RATE_LIMIT_COUNT:
            self._log_to_db(ip, "DoS", "RATE", "Rate limit exceeded", f"Req > {self.RATE_LIMIT_COUNT}")
            abort(429)

        self._scan_payloads(ip)

    def _check_response(self, response):
        ip = self._get_client_ip()
        if response.status_code == 404:
            now = time.time()
            if ip not in self.ip_404_counts or now - self.ip_404_counts[ip]['start'] > self.SCAN_DETECTION_PERIOD:
                self.ip_404_counts[ip] = {'count': 1, 'start': now}
            else:
                self.ip_404_counts[ip]['count'] += 1
            
            if self.ip_404_counts[ip]['count'] > self.SCAN_DETECTION_COUNT:
                if ip not in self.blacklisted_ips:
                    self._log_to_db(ip, "Reconnaissance", "SCAN", "Dir Scanning", f"404s > {self.SCAN_DETECTION_COUNT}")
                    self.blacklisted_ips.add(ip)
        return response

    def _scan_payloads(self, ip):
        for param, value in request.values.items():
            val_str = str(value)
            for rule in self.rules:
                if rule['compiled_pattern'].search(val_str):
                    self._log_to_db(ip, rule['attack_type'], rule['rule_id'], rule['description'], f"{param}={val_str}")
                    abort(403)