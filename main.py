import argparse
import webbrowser
import time
import threading
from ui.gradio_app import launch

def open_browser(url, delay=2):
    """Opens browser after a delay to give the server time to start"""
    time.sleep(delay)
    webbrowser.open(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860,
                        help="Port number for the server")
    parser.add_argument("--no-browser", action="store_true",
                        help="Don't open browser automatically")
    args = parser.parse_args()

    # Local server URL
    url = f"http://localhost:{args.port}"

    # Start browser in separate thread if not disabled
    if not args.no_browser:
        browser_thread = threading.Thread(target=open_browser, args=(url,))
        browser_thread.daemon = True
        browser_thread.start()

    print(f"🚀 Starting AI Assistant interface on {url}")
    launch(server_port=args.port, server_name="0.0.0.0")