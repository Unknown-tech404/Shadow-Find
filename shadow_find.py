#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║                       SHADOW FIND - UNIVERSAL LINK EXTRACTOR                      ║
║                     Extract All Links & URLs from Any Website                     ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import re
import time
import json
import argparse
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin, urlunparse

# ============================================================================
# COLORS
# ============================================================================

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    @staticmethod
    def disable():
        Colors.RED = Colors.GREEN = Colors.YELLOW = Colors.BLUE = ''
        Colors.MAGENTA = Colors.CYAN = Colors.WHITE = Colors.BOLD = ''
        Colors.DIM = Colors.RESET = ''

# ============================================================================
# HTTP REQUEST HANDLING LAYER
# ============================================================================

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error

# Disable SSL insecure site warning triggers gracefully
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass

# ============================================================================
# SHADOW FIND CORE
# ============================================================================

class ShadowFind:
    def __init__(self):
        self.target_url = None
        self.domain = None
        self.visited_urls = set()
        self.all_links = set()
        self.internal_links = set()
        self.external_links = set()
        self.images = set()
        self.scripts = set()
        self.stylesheets = set()
        self.forms = set()
        self.emails = set()
        self.admin_panels = set()  # Replaced phone_numbers with admin_panels
        self.jsons = set()
        self.xmls = set()
        self.pdfs = set()
        self.docs = set()
        self.start_time = None
        self.end_time = None
        self.threads = 10
        self.max_depth = 2
        self.lock = threading.Lock()
        self.quiet = False
    
    def banner(self):
        banner = f"""{Colors.RED}{Colors.BOLD}
    ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗ ███████╗██╗███╗   ██╗██████╗ 
    ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║ ██╔════╝██║████╗  ██║██╔══██╗
    ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║ █████╗  ██║██╔██╗ ██║██║  ██║
    ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║ ██╔══╝  ██║██║╚██╗██║██║  ██║
    ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝ ██║     ██║██║ ╚████║██████╔╝
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝  ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ 
                                                                                     
                    {Colors.GREEN}UNIVERSAL LINK EXTRACTOR - v2.2{Colors.RESET}{Colors.RED}                           
              {Colors.YELLOW}Extract All Links & URLs from Any Website{Colors.RESET}{Colors.RED} 
                    {Colors.CYAN}Author:{Colors.RESET} {Colors.WHITE}Unknown-tech404{Colors.RESET}                            
"""
        print(banner)
    
    def get_page_content(self, url):
        """Fetch raw data, abstracting fallback mechanisms securely"""
        if HAS_REQUESTS:
            try:
                response = requests.get(
                    url, 
                    timeout=10, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                    verify=False
                )
                if response.status_code == 200:
                    return response.text
            except Exception:
                pass
        else:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    return response.read().decode('utf-8', errors='ignore')
            except Exception:
                pass
        return None
    
    def normalize_url(self, url):
        if not url:
            return None
        try:
            parsed = urlparse(url)
            normalized = urlunparse((
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path.rstrip('/') or '/',
                parsed.params,
                parsed.query,
                ''  # Erases target sub-element fragment hash addresses (#tags)
            ))
            return normalized
        except Exception:
            return url
    
    def is_internal_link(self, link):
        if not link:
            return False
        try:
            parsed = urlparse(link)
            if not parsed.netloc:
                return True
            return parsed.netloc == self.domain
        except Exception:
            return False

    def check_admin_panel(self, url):
        """Checks if a URL matches common administrative portal structures"""
        admin_keywords = [
            '/admin', '/login', '/wp-admin', '/wp-login', '/administrator', 
            '/backend', '/cpanel', '/dashboard', '/controlpanel', '/manage', 
            '/signin', '/auth', '/webmaster', '/portal'
        ]
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        if any(keyword in path for keyword in admin_keywords):
            self.admin_panels.add(url)

    def extract_links_from_page(self, url, depth):
        """Scrapes web assets and schedules found internal pointers to current thread-pool layer"""
        with self.lock:
            if url in self.visited_urls:
                return []
            self.visited_urls.add(url)
        
        if not self.quiet:
            with self.lock:
                sys.stdout.write(f"\r{Colors.YELLOW}[*] Crawling ({len(self.visited_urls)}): {Colors.WHITE}{url[:50]:<50} {Colors.CYAN}[Found Total: {len(self.all_links)}]{Colors.RESET}")
                sys.stdout.flush()

        content = self.get_page_content(url)
        if not content:
            return []
        
        discovered_internals = []

        # Scrape and balance core attributes using optimized regex matrices
        link_patterns = [
            r'href\s*=\s*["\']([^"\']+)["\']',
            r'src\s*=\s*["\']([^"\']+)["\']',
            r'action\s*=\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in link_patterns:
            for match in re.findall(pattern, content, re.IGNORECASE):
                href_str = match.strip()
                if not href_str or href_str.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue
                    
                full_url = urljoin(url, href_str)
                normalized = self.normalize_url(full_url)
                if normalized:
                    with self.lock:
                        if normalized not in self.all_links:
                            self.all_links.add(normalized)
                            if self.is_internal_link(normalized):
                                self.internal_links.add(normalized)
                                discovered_internals.append(normalized)
                            else:
                                self.external_links.add(normalized)

                            # Run target through administrative portal evaluation logic
                            self.check_admin_panel(normalized)

                            # Categorization sorting metrics engines
                            lowered = normalized.lower()
                            if lowered.endswith('.json'): self.jsons.add(normalized)
                            elif lowered.endswith('.xml'): self.xmls.add(normalized)
                            elif lowered.endswith('.pdf'): self.pdfs.add(normalized)
                            elif lowered.endswith(('.doc', '.docx')): self.docs.add(normalized)
        
        # Identity Profile Scrapers (Emails)
        for email in re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content):
            self.emails.add(email)
        
        # Scrape Asset Objects explicitly via structural regex filters
        for match in re.findall(r'src\s*=\s*["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg|webp))["\']', content, re.IGNORECASE):
            self.images.add(urljoin(url, match))
        for match in re.findall(r'src\s*=\s*["\']([^"\']+\.js)["\']', content, re.IGNORECASE):
            self.scripts.add(urljoin(url, match))
        for match in re.findall(r'href\s*=\s*["\']([^"\']+\.css)["\']', content, re.IGNORECASE):
            self.stylesheets.add(urljoin(url, match))
        for match in re.findall(r'action\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE):
            self.forms.add(urljoin(url, match))
            
        return discovered_internals
    
    def scan(self, url, threads=10, max_depth=2, quiet=False):
        """Controlled level-based multithreaded architecture execution layer"""
        self.threads = threads
        self.max_depth = max_depth
        self.quiet = quiet
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.target_url = url
        self.domain = urlparse(url).netloc
        self.start_time = datetime.now()
        
        print(f"\n{Colors.CYAN}[*] Target: {Colors.WHITE}{url}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Domain: {Colors.WHITE}{self.domain}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Threads: {Colors.WHITE}{threads}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Max Depth: {Colors.WHITE}{max_depth}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Started: {Colors.WHITE}{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
        print(f"{Colors.GREEN}[+] Launching Scraper Engine...{Colors.RESET}\n")
        
        # Layering queue matrix map initialization block
        current_layer_queue = [url]
        
        for current_depth in range(max_depth + 1):
            if not current_layer_queue:
                break
                
            next_layer_queue = []
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = {executor.submit(self.extract_links_from_page, target, current_depth): target for target in current_layer_queue}
                for future in futures:
                    try:
                        results = future.result()
                        if results:
                            next_layer_queue.extend(results)
                    except Exception:
                        pass
            
            # Rebalance array tracks keeping out existing visited sets links
            current_layer_queue = list(set(next_layer_queue) - self.visited_urls)
        
        if not self.quiet:
            sys.stdout.write("\r" + " " * 85 + "\r")  # Clean rolling banner footprints smoothly
            sys.stdout.flush()
            
        self.end_time = datetime.now()
        self.display_results()
    
    def display_results(self):
        elapsed = (self.end_time - self.start_time).total_seconds()
        
        print(f"\n{Colors.GREEN}{'='*75}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}📊 SCAN RESULTS SUMMARY{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*75}{Colors.RESET}\n")
        
        print(f"{Colors.BOLD}{Colors.YELLOW}🔗 INVENTORY COUNTS:{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Total Unique URLs Found: {Colors.WHITE}{len(self.all_links)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Internal Page Links:     {Colors.WHITE}{len(self.internal_links)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} External Outbound Links: {Colors.WHITE}{len(self.external_links)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Scraped Images Assets:   {Colors.WHITE}{len(self.images)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Script (JS) Modules:     {Colors.WHITE}{len(self.scripts)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Stylesheet (CSS) Links:  {Colors.WHITE}{len(self.stylesheets)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Interactive Form Links:  {Colors.WHITE}{len(self.forms)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Target Emails Found:     {Colors.WHITE}{len(self.emails)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Admin Panels Tracked:    {Colors.WHITE}{len(self.admin_panels)}{Colors.RESET}")
        print(f"  {Colors.GREEN}●{Colors.RESET} Total Execution Time:    {Colors.WHITE}{elapsed:.2f}s{Colors.RESET}\n")
        
        # Display explicit panel sections cleanly
        self._render_section("INTERNAL LINKS", self.internal_links, Colors.CYAN)
        self._render_section("EXTERNAL LINKS", self.external_links, Colors.MAGENTA)
        self._render_section("IMAGES FOUND", self.images, Colors.CYAN)
        self._render_section("SCRIPTS FOUND", self.scripts, Colors.GREEN)
        self._render_section("STYLESHEETS FOUND", self.stylesheets, Colors.BLUE)
        self._render_section("EMAILS DISCOVERED", self.emails, Colors.BLUE)
        self._render_section("ADMIN PANELS / PAGE LINKS", self.admin_panels, Colors.RED)
        
        print(f"{Colors.GREEN}{'='*75}{Colors.RESET}")
        print(f"{Colors.GREEN}[✓] Scan Routine execution finished successfully.{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*75}{Colors.RESET}\n")
        
        self.save_results()

    def _render_section(self, title, dataset, item_color):
        if dataset:
            print(f"{Colors.BOLD}{Colors.YELLOW}📂 {title} (ALL {len(dataset)}):{Colors.RESET}")
            for idx, entry in enumerate(sorted(list(dataset)), 1):
                print(f"  {item_color}{idx:3d}.{Colors.RESET} {entry}")
            print()
    
    def save_results(self):
        try:
            filename = f"shadow_find_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            results = {
                'target': self.target_url,
                'domain': self.domain,
                'scan_date': self.start_time.isoformat(),
                'duration_seconds': (self.end_time - self.start_time).total_seconds(),
                'summary': {
                    'total_links': len(self.all_links),
                    'internal_links': len(self.internal_links),
                    'external_links': len(self.external_links),
                    'images': len(self.images),
                    'scripts': len(self.scripts),
                    'stylesheets': len(self.stylesheets),
                    'forms': len(self.forms),
                    'emails': len(self.emails),
                    'admin_panels': len(self.admin_panels)
                },
                'data_records': {
                    'internal_links': sorted(list(self.internal_links)),
                    'external_links': sorted(list(self.external_links)),
                    'images': sorted(list(self.images)),
                    'scripts': sorted(list(self.scripts)),
                    'stylesheets': sorted(list(self.stylesheets)),
                    'forms': sorted(list(self.forms)),
                    'emails': sorted(list(self.emails)),
                    'admin_panels': sorted(list(self.admin_panels))
                }
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"{Colors.GREEN}[+] Clean database report saved to: {Colors.WHITE}{filename}{Colors.RESET}\n")
        except Exception as e:
            if not self.quiet:
                print(f"{Colors.RED}[!] Failed writing session JSON log structure: {e}{Colors.RESET}")

# ============================================================================
# MAIN ENTRYPOINT PARSER
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='SHADOW FIND - Universal Link Extractor Runtime Platform')
    parser.add_argument('url', help='Target endpoint domain network interface to scan')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Max thread-pool size limits context (default: 10)')
    parser.add_argument('-d', '--depth', type=int, default=2, help='Crawling link structure depth layer threshold (default: 2)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Activate quiet mode to suppress trace tracking streams')
    parser.add_argument('--no-color', action='store_true', help='Strip terminal visual layout color adjustments')
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
        
    try:
        finder = ShadowFind()
        finder.banner()
        finder.scan(args.url, args.threads, args.depth, args.quiet)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Process execution terminated by user.{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] System platform error breakdown: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == '__main__':
    main()
