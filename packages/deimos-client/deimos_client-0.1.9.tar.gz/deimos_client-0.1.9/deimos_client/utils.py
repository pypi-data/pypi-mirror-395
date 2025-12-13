import functools
import os
import time

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2

def encode_image(image, encode_type='.png'):
    if encode_type == '.jpg':
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        is_success, im_buf_arr = cv2.imencode(encode_type, image, img_param)
    elif encode_type == '.webp':
        img_param = [int(cv2.IMWRITE_WEBP_QUALITY), 80]
        is_success, im_buf_arr = cv2.imencode(encode_type, image, img_param)
    else:
        is_success, im_buf_arr = cv2.imencode(encode_type, image)
    return im_buf_arr.tobytes()

def get_job_type(routing_key):
        return '.'.join(routing_key.split('.')[:2])

def retry_on_connect_error(max_retries=5, delay=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (OSError, ConnectionError, ConnectionResetError) as e:
                    last_exception = e
                    print(f"[send_metric/status] Connection Wise Error, retrying {attempt+1}/{max_retries}: {e}")
                    time.sleep(delay)
            # 最后一次还是失败，抛出异常
            raise last_exception
        return wrapper
    return decorator
