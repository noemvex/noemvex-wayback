#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOEMVEX CHRONOS v4.0
Author: Emre 'noemvex' Sahin
Description: The Ultimate Offensive OSINT Weapon. Features Mathematical Entropy Analysis, 
             Zombie Asset Hijacking (Takeover Check), and Auto-Nuclei Template Generation.
"""

import os
import sys
import requests
import argparse
import re
import math
import time
# SSL uyarılarını gizlemek için (God Mode gürültü sevmez)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from datetime import datetime
from urllib.parse import urlparse, parse_qs

class UI:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    GREY = '\033[90m'
    END = '\033[0m'

    @staticmethod
    def banner():
        # Raw string (r"") 
        ascii_art = [
            r"███╗   ██╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗",
            r"████╗  ██║██╔═══██╗██╔════╝████╗ ████║██║   ██║██╔════╝╚██╗██╔╝",
            r"██╔██╗ ██║██║   ██║█████╗  ██╔████╔██║██║   ██║█████╗   ╚███╔╝ ",
            r"██║╚██╗██║██║   ██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝██╔══╝   ██╔██╗ ",
            r"██║ ╚████║╚██████╔╝███████╗██║ ╚═╝ ██║ ╚████╔╝ ███████╗██╗  ██╗",
            r"╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝"
        ]
        
        print(f"{UI.GREEN}{UI.BOLD}")
        for line in ascii_art:
            print(line)
        print(f"               {UI.PURPLE}[ CHRONOS v4.0 ]{UI.END}\n")

    @staticmethod
    def log(message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": UI.BLUE, "SUCCESS": UI.GREEN, "WARN": UI.YELLOW, 
            "CRITICAL": UI.RED, "ZOMBIE": UI.RED + UI.BOLD, "ENTROPY": UI.CYAN
        }
        print(f"{UI.GREY}[{timestamp}]{UI.END} {colors.get(level, UI.BLUE)}[{level}]{UI.END} {message}")

# --- MATHEMATICAL ENGINE ---
class EntropyEngine:
    @staticmethod
    def calculate(string):
        """Calculates Shannon Entropy to detect high-randomness strings (Secrets/Keys)"""
        if not string: return 0
        entropy = 0
        for x in set(string):
            p_x = float(string.count(x)) / len(string)
            entropy += - p_x * math.log(p_x, 2)
        return entropy

# --- CORE GOD MODE ENGINE ---
class ChronosEngine:
    def __init__(self, domain, output_file=None):
        self.domain = domain
        self.output_file = output_file
        self.clean_domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
        
        # Core Findings
        self.findings = []
        self.zombies = [] # Hijackable assets
        self.high_entropy_urls = []
        
        # Regex Patterns (Legacy + Cloud)
        self.cloud_patterns = {
            "S3": re.compile(r"s3\.amazonaws\.com|[a-z0-9.-]+\.s3-[a-z0-9-]+\.amazonaws\.com", re.IGNORECASE),
            "Azure": re.compile(r"blob\.core\.windows\.net", re.IGNORECASE)
        }
        self.secrets_regex = re.compile(r"(api|secret|token|auth|password|key|jenkins|access)", re.IGNORECASE)
        
        # Ignore List
        self.blacklisted_mimes = ["text/html", "application/xhtml+xml", "image/jpeg", "image/png"]

    def check_root(self):
        if hasattr(os, 'geteuid') and os.geteuid() != 0:
            UI.log("Running without ROOT. Socket restrictions may apply.", "WARN")

    def fetch_cdx(self):
        # Optimized One-Shot Query
        api_url = (f"http://web.archive.org/cdx/search/cdx?url=*.{self.clean_domain}/*"
                   f"&output=json&fl=original,mimetype,timestamp&collapse=urlkey")
        UI.log(f"Initiating CHRONOS Scan for: {UI.BOLD}{self.clean_domain}{UI.END}")
        try:
            resp = requests.get(api_url, timeout=60)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if len(data) > 0: data.pop(0)
                    UI.log(f"Ingested {len(data)} historical data points.", "SUCCESS")
                    return data
                except ValueError:
                    UI.log("Archive.org returned non-JSON data. Server might be busy.", "CRITICAL")
                    return []
            return []
        except Exception as e:
            UI.log(f"Fetch failed: {e}", "CRITICAL")
            return []

    def check_zombie_hijack(self, provider, url):
        """Active Check: Is this cloud asset dead and available for takeover?"""
        try:
            # SENIOR FIX: verify=False to catch buckets with expired/bad SSL
            r = requests.head(url, timeout=4, verify=False, allow_redirects=True)
            
            # AWS S3 404 often means "NoSuchBucket" -> Takeover Possible
            if provider == "S3" and r.status_code == 404:
                return True
            # Azure 404 often means "ContainerNotFound"
            if provider == "Azure" and r.status_code == 404:
                return True
        except:
            pass
        return False

    def analyze(self, data):
        UI.log("Engaging Entropy Math & Zombie Asset Hunter...", "INFO")
        
        for item in data:
            url, mime, timestamp = item[0], item[1], item[2]
            
            # 1. ZOMBIE ASSET HIJACKING (Active)
            for provider, regex in self.cloud_patterns.items():
                if regex.search(url):
                    # Found a cloud link, now check if it's dead (ZOMBIE)
                    if self.check_zombie_hijack(provider, url):
                        self.zombies.append({"type": provider, "url": url})
                        print(f"    {UI.RED}{UI.BOLD}>> [ZOMBIE] HIJACKABLE {provider} BUCKET: {url}{UI.END}")
                    else:
                        # Just a finding
                        self.findings.append({"type": "Cloud", "url": url, "date": timestamp})

            # 2. SHANNON ENTROPY ANALYSIS (Mathematical Secret Detection)
            # Check query parameters for high entropy (e.g., id=Ab3$9zLp...)
            if "?" in url:
                try:
                    query = urlparse(url).query
                    for val in parse_qs(query).values():
                        val_str = val[0]
                        # Only check meaningful strings (>12 chars) to reduce noise
                        if len(val_str) > 12:
                            score = EntropyEngine.calculate(val_str)
                            if score > 4.5: # Threshold for high randomness
                                self.high_entropy_urls.append({"url": url, "score": score})
                                print(f"    {UI.CYAN}>> [ENTROPY {score:.2f}] POTENTIAL SECRET: {url}{UI.END}")
                except: pass

            # 3. LEGACY REGEX
            if self.secrets_regex.search(url) and mime not in self.blacklisted_mimes:
                 self.findings.append({"type": "Secret_Pattern", "url": url, "date": timestamp})

    def generate_nuclei_template(self):
        """Generates a weaponized Nuclei template for discovered paths"""
        if not self.findings and not self.high_entropy_urls: return

        template_name = f"nuclei_noemvex_{self.clean_domain}.yaml"
        
        # Extract unique paths
        paths = set()
        for i in self.findings: paths.add(urlparse(i['url']).path)
        for i in self.high_entropy_urls: paths.add(urlparse(i['url']).path)
        
        if not paths: return

        try:
            with open(template_name, 'w') as f:
                f.write(f"id: noemvex-chronos-{self.clean_domain}\n")
                f.write("info:\n")
                f.write(f"  name: Noemvex Generated Scan for {self.clean_domain}\n")
                f.write("  author: noemvex\n")
                f.write("  severity: medium\n")
                f.write("requests:\n")
                f.write("  - method: GET\n")
                f.write("    path:\n")
                for p in list(paths)[:50]: # Limit to top 50 to avoid huge files
                    if p: # Ensure path is not empty
                        f.write(f"      - \"{{{{BaseURL}}}}{p}\"\n")
                f.write("\n    matchers:\n")
                f.write("      - type: status\n")
                f.write("        status:\n")
                f.write("          - 200\n")
            
            UI.log(f"Weaponized Nuclei Template generated: {UI.BOLD}{template_name}{UI.END}", "SUCCESS")
        except Exception as e:
            UI.log(f"Nuclei generation error: {e}", "WARN")

    def save_report(self):
        fname = self.output_file if self.output_file else f"chronos_report.txt"
        try:
            with open(fname, 'w') as f:
                f.write("NOEMVEX CHRONOS v4.0 [REPORT]\n" + "="*50 + "\n")
                
                if self.zombies:
                    f.write(f"\n[!!!] ZOMBIE ASSETS (HIJACKABLE) ({len(self.zombies)})\n")
                    for z in self.zombies: f.write(f"[VULNERABLE] {z['type']}: {z['url']}\n")
                
                if self.high_entropy_urls:
                    f.write(f"\n[+] HIGH ENTROPY SECRETS ({len(self.high_entropy_urls)})\n")
                    for e in self.high_entropy_urls: f.write(f"[Score: {e['score']:.2f}] {e['url']}\n")

                f.write(f"\n[+] GENERAL FINDINGS ({len(self.findings)})\n")
                for i in self.findings: f.write(f"[{i['type']}] {i['url']}\n")

            UI.log(f"Chronos Report saved to: {fname}", "SUCCESS")
        except Exception as e:
            UI.log(f"Report save failed: {e}", "CRITICAL")

    def run(self):
        UI.banner()
        self.check_root()
        data = self.fetch_cdx()
        if data:
            self.analyze(data)
            self.generate_nuclei_template()
            self.save_report()
        print(f"\n{UI.CYAN}{UI.BOLD}[√] CHRONOS OPERATION COMPLETED.{UI.END}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NOEMVEX CHRONOS EDITION")
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-o', '--output', help='Output filename')
    
    if len(sys.argv) == 1: parser.print_help(); sys.exit(1)
    
    args = parser.parse_args()
    engine = ChronosEngine(args.domain, args.output)
    engine.run()
