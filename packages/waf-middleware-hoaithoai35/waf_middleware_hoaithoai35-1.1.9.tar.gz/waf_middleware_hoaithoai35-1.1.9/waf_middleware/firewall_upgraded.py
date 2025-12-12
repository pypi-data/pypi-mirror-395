import logging
from flask import request, abort
import time

# --- HÀM THIẾT LẬP LOGGER (GIỮ NGUYÊN NHƯ TUẦN 2) ---
def setup_waf_logger():
    logger = logging.getLogger('WAF')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('waf.log', mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(file_handler)
    return logger


waf_logger = setup_waf_logger()


# --- LỚP FIREWALL ĐÃ ĐƯỢC NÂNG CẤP ---
class Firewall:
    # --- CẤU HÌNH CHO CÁC TÍNH NĂNG MỚI ---
    # Rate Limiting cơ bản (chống DoS/Brute-force)
    RATE_LIMIT_COUNT = 100  # Cho phép 100 requests
    RATE_LIMIT_PERIOD = 60  # trong vòng 60 giây

    # Rate Limiting nâng cao (phát hiện quét thư mục)
    SCAN_DETECTION_COUNT = 20 # Cho phép 20 lỗi 404
    SCAN_DETECTION_PERIOD = 60 # trong vòng 60 giây

    def __init__(self, app=None):
        # --- CÁC BIẾN ĐỂ LƯU TRỮ TRẠNG THÁI ---
        self.ip_requests = {}       # Theo dõi số request của mỗi IP
        self.ip_404_counts = {}     # Theo dõi số lỗi 404 của mỗi IP
        self.blacklisted_ips = set() # Lưu trữ các IP trong "sổ đen"

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Hàm tích hợp WAF vào ứng dụng Flask."""
        # Tải danh sách IP bị cấm từ file khi WAF khởi động
        self._load_blacklist()

        # Đăng ký các hàm kiểm tra với Flask
        app.before_request(self._check_request)
        app.after_request(self._check_response) # MỚI: Đăng ký hàm kiểm tra sau mỗi request

    def _load_blacklist(self):
        """Tải danh sách IP từ file blacklist.txt vào bộ nhớ."""
        try:
            with open('blacklist.txt', 'r') as f:
                # Đọc từng dòng, loại bỏ khoảng trắng và thêm vào một 'set' để truy vấn nhanh
                self.blacklisted_ips = {line.strip() for line in f if line.strip()}
                if self.blacklisted_ips:
                    waf_logger.info(f"Loaded {len(self.blacklisted_ips)} IP(s) from blacklist.")
        except FileNotFoundError:
            waf_logger.info("blacklist.txt not found. Starting with an empty blacklist.")
        except Exception as e:
            waf_logger.error(f"Error loading blacklist.txt: {e}")

    def _check_request(self):
        """Hàm "người gác cổng" chạy TRƯỚC mỗi request."""
        ip_address = request.remote_addr
        log_message = f"Incoming request from IP: {ip_address}, Method: {request.method}, Path: {request.full_path}"
        waf_logger.info(log_message)
        print(f"WAF is inspecting request from {ip_address}...")

        # --- QUY TẮC 1: KIỂM TRA IP BLACKLIST ---
        if ip_address in self.blacklisted_ips:
            waf_logger.warning(f"Blocked blacklisted IP: {ip_address}")
            abort(403) # Trả về lỗi 403 Forbidden (Cấm truy cập)

        # --- QUY TẮC 2: KIỂM TRA RATE LIMITING CƠ BẢN ---
        current_time = time.time()
        
        # Nếu IP chưa có trong danh sách theo dõi, hoặc đã quá thời gian theo dõi
        if ip_address not in self.ip_requests or current_time - self.ip_requests[ip_address]['start_time'] > self.RATE_LIMIT_PERIOD:
            # Reset bộ đếm cho IP này
            self.ip_requests[ip_address] = {'count': 1, 'start_time': current_time}
        else:
            # Nếu vẫn trong thời gian theo dõi, tăng số lượng request
            self.ip_requests[ip_address]['count'] += 1

        # Kiểm tra xem số lượng request có vượt ngưỡng không
        if self.ip_requests[ip_address]['count'] > self.RATE_LIMIT_COUNT:
            waf_logger.warning(f"Rate limit exceeded for IP: {ip_address}. Blocking with 429.")
            abort(429) # Trả về lỗi 429 Too Many Requests

    def _check_response(self, response):
        """Hàm chạy SAU mỗi request để kiểm tra response trả về."""
        ip_address = request.remote_addr

        # --- QUY TẮC 3: PHÁT HIỆN QUÉT THƯ MỤC (DỰA TRÊN LỖI 404) ---
        if response.status_code == 404:
            current_time = time.time()

            # Logic đếm số lỗi 404 tương tự như rate limiting
            if ip_address not in self.ip_404_counts or current_time - self.ip_404_counts[ip_address]['start_time'] > self.SCAN_DETECTION_PERIOD:
                self.ip_404_counts[ip_address] = {'count': 1, 'start_time': current_time}
            else:
                self.ip_404_counts[ip_address]['count'] += 1
            
            # Nếu số lỗi 404 vượt ngưỡng, tự động thêm IP này vào "sổ đen"
            if self.ip_404_counts[ip_address]['count'] > self.SCAN_DETECTION_COUNT:
                if ip_address not in self.blacklisted_ips:
                    waf_logger.critical(f"Directory scanning detected from IP: {ip_address}. Adding to blacklist.")
                    self.blacklisted_ips.add(ip_address)
                    # (Nâng cao) Có thể viết code để ghi IP này vào file blacklist.txt để lưu lại vĩnh viễn

        return response # Rất quan trọng: phải trả về response để client nhận được
