# file: examples/record_user.py

import logging
import sys
import os
import threading
import time

# Thêm thư mục gốc của dự án vào Python Path để có thể import `tikrecording`
# (Chỉ cần thiết nếu chưa cài đặt bằng `pip install -e .`)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tikrecording import Recorder, exceptions, Converter

def main():
    # Configure logging to display messages from the library
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )

    # --- CHANGE THESE PARAMETERS ---
    TARGET_USERNAME = "funachair" # Tên người dùng bạn muốn ghi
    OUTPUT_DIRECTORY = "./videos_output" # Thư mục lưu video
    COOKIES = {}
    # -----------------------------------

    logging.info(f"Preparing to record user: '{TARGET_USERNAME}'")
    
    # 1. Khởi tạo recorder
    recorder = Recorder(username=TARGET_USERNAME, cookies=COOKIES)

    # 2. Tạo một luồng (thread) riêng để chạy tác vụ ghi hình
    # Điều này giúp luồng chính không bị "khóa" và có thể lắng nghe lệnh dừng
    record_thread = threading.Thread(target=recorder.record, args=(OUTPUT_DIRECTORY,))

    try:
        # 3. Bắt đầu luồng ghi hình
        record_thread.start()
        
        # 4. Luồng chính sẽ chờ ở đây. Nếu bạn nhấn Ctrl+C, nó sẽ được bắt lại.
        while record_thread.is_alive():
            record_thread.join(timeout=1) # Chờ 1 giây rồi kiểm tra lại

    except KeyboardInterrupt:
        logging.warning("\nPhát hiện tín hiệu dừng (Ctrl+C). Yêu cầu dừng ghi hình một cách an toàn...")
        
        # 5. Gọi phương thức stop() của recorder để nó kết thúc một cách an toàn
        recorder.stop()
        
        # Chờ luồng ghi hình xử lý xong và thoát hẳn
        record_thread.join()

    except Exception as e:
        logging.critical(f"An unexpected error occurred in main thread: {e}", exc_info=True)


if __name__ == "__main__":
    main()