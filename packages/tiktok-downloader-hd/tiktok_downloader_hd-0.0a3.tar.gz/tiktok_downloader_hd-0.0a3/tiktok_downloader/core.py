import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp

class TikTokDownloader:
    """
    A Selenium-based downloader for TikTok videos using SnapTik.
    """
    def __init__(self, download_dir="downloads", cookies_path=None, headless=False):
        self.download_dir = os.path.abspath(download_dir)
        self.cookies_path = os.path.abspath(cookies_path) if cookies_path else None
        self.headless = headless
        
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            
        self.driver = self._init_driver()
        if self.cookies_path:
            self._inject_cookies()

    def _init_driver(self):
        print("[*] Initializing Chrome driver...")
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
            
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        # Hide automation flags
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        return webdriver.Chrome(options=options)

    def _inject_cookies(self):
        if not os.path.exists(self.cookies_path):
            print("[!] Cookies file not found.")
            return

        try:
            self.driver.get("https://snaptik.app/404")
            time.sleep(0.3)
            
            with open(self.cookies_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or not line.strip(): continue
                    parts = line.strip().split('\t')
                    if len(parts) >= 7 and "snaptik" in parts[0]:
                        try:
                            cookie = {
                                'name': parts[5], 
                                'value': parts[6], 
                                'domain': parts[0], 
                                'path': parts[2], 
                                'expiry': int(parts[4])
                            }
                            self.driver.add_cookie(cookie)
                        except: pass
            print("[+] Cookies injected successfully.")
            time.sleep(0.3)
        except Exception as e:
            print(f"[!] Failed to inject cookies: {e}")

    def _inject_ad_killer(self):
        script = """
            window.killerParams = { active: true };
            const observer = new MutationObserver((mutations) => {
                if (!window.killerParams.active) return;
                const consentButtons = ["//button[contains(., 'Consent')]", "//button[contains(., 'AGREE')]", "//button[contains(., 'Allow')]"];
                consentButtons.forEach(xpath => {
                    try {
                        let btn = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (btn) { btn.click(); btn.remove(); }
                    } catch (e) {}
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        """
        self.driver.execute_script(script)

    def _wait_for_file(self, pre_files, timeout=60):
        start = time.time()
        while time.time() - start < timeout:
            current_files = set(os.listdir(self.download_dir))
            new_files = current_files - pre_files
            for f in new_files:
                if not f.endswith('.crdownload') and not f.endswith('.tmp'):
                    return os.path.join(self.download_dir, f)
            time.sleep(0.3)
        return None

    def _process_video(self, url):
        try:
            self.driver.get("https://snaptik.app")
            time.sleep(0.3)
            self._inject_ad_killer()

            # Input
            try:
                inp = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "url")))
                inp.clear()
                time.sleep(0.1)
                inp.send_keys(url)
                time.sleep(0.3)
            except: return False, "Input not found"

            # Click Go
            try:
                self.driver.execute_script("document.querySelector('.btn-go').click()")
            except:
                inp.send_keys(Keys.RETURN)
            
            # Wait for results
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'token=') or contains(@href, 'dl.php')]"))
                )
            except: return False, "Results timeout"
            
            time.sleep(0.3)

            # Spatial Click (Offset Strategy)
            buttons = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'token=') or contains(@href, 'dl.php')]")
            if not buttons: return False, "Buttons missing"

            base_btn = buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", base_btn)
            time.sleep(0.3)
            
            rect = self.driver.execute_script("return arguments[0].getBoundingClientRect();", base_btn)
            target_x = rect['left'] + (rect['width'] / 2)
            target_y = rect['bottom'] + 45
            
            self.driver.execute_script(f"var el = document.elementFromPoint({target_x}, {target_y}); if(el) el.click();")
            
            time.sleep(0.3)
            
            # Close popup ads
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(0.1)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            
            return True, "Clicked"

        except Exception as e:
            return False, str(e)

    def download(self, video_url, filename_prefix="vid", retries=3):
        """
        Download a single video.
        """
        final_path = os.path.join(self.download_dir, f"{filename_prefix}.mp4")
        if os.path.exists(final_path) and os.path.getsize(final_path) > 1024*1024:
            print(f"[-] {filename_prefix}: Already exists.")
            return True

        print(f"[*] {filename_prefix}: Processing...")
        pre_files = set(os.listdir(self.download_dir))

        for attempt in range(1, retries + 1):
            success, msg = self._process_video(video_url)
            if success:
                new_file = self._wait_for_file(pre_files)
                if new_file:
                    time.sleep(0.3)
                    if os.path.exists(final_path): os.remove(final_path)
                    try:
                        shutil.move(new_file, final_path)
                        print(f"[+] {filename_prefix}: Downloaded ({os.path.getsize(final_path)/1024/1024:.2f} MB)")
                        return True
                    except: return True
            
            print(f"[!] {filename_prefix}: Retry {attempt}/{retries}...")
            time.sleep(0.3)
        
        return False

    def get_user_videos(self, user_url, limit=10):
        print(f"[*] Fetching links from {user_url}...")
        ydl_opts = {
            'extract_flat': True,
            'dump_single_json': True,
            'quiet': True,
            'playlistend': limit,
            'cookiefile': self.cookies_path,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                res = ydl.extract_info(user_url, download=False)
                return [e['url'] for e in res.get('entries', []) if e.get('url')]
        except Exception as e:
            print(f"[!] Error fetching links: {e}")
            return []

    def close(self):
        if self.driver:
            self.driver.quit()