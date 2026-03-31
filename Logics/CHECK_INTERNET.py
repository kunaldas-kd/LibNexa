import urllib.request
import socket

def is_connected(host="http://www.google.com", timeout=5) -> bool:
    """
    Check if the internet connection is active.

    Args:
        host (str): URL to test the connection against.
        timeout (int): Time in seconds to wait for a response.

    Returns:
        bool: True if internet is connected, False otherwise.
    """
    try:
        internet = urllib.request.urlopen(host, timeout=timeout)
        # print(internet)
        if internet:
            print("✅ Internet connection is active.")
            # time.sleep(3)
            return True
    except (urllib.error.URLError, socket.timeout):
        return False

# Example usage
# if __name__ == "__main__":
#     while True:
#         is_connected()