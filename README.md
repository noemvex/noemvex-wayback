# NOEMVEX CHRONOS v4.0
![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-grey) ![Focus](https://img.shields.io/badge/Focus-OSINT%20%26%20Takeover-yellow) ![Type](https://img.shields.io/badge/Edition-Chronos-cyan)

> **"Master the Time, Reveal the Shadows."**
> The Ultimate Offensive OSINT Weapon. Engineered for High-Entropy Secret Detection, Cloud Asset Hijacking, and automated Nuclei weaponization by manipulating historical internet archives.
> ⚠️ **Disclaimer:** This tool is for educational purposes and authorized security testing only.

---
## About
**NOEMVEX CHRONOS** transcends traditional OSINT parsers. Standard tools merely dump thousands of dead URLs. The Chronos Engine bends time by ingesting years of historical target data and applying Mathematical Shannon Entropy to pinpoint hardcoded AWS/API secrets forgotten in query parameters. Furthermore, it actively probes discovered S3/Azure cloud links for "Zombie" status (Subdomain Takeover vulnerability) and automatically generates weaponized Nuclei templates for immediate CI/CD integration.

## Capabilities
* **Shannon Entropy Analysis:** Calculates mathematical randomness (>4.5 score) to detect hidden JWTs, Stripe tokens, and API keys hidden in historical URLs.
* **Zombie Asset Hijacking:** Actively probes dead Cloud buckets (AWS S3, Azure Blob) found in archives to verify if they are vulnerable to immediate Subdomain Takeover.
* **Auto-Weaponization (Nuclei):** Dynamically generates a `nuclei_noemvex_<domain>.yaml` template containing all discovered sensitive paths, ready to be fed into your vulnerability scanner.
* **Noise Reduction:** Bypasses useless MIME types (images, CSS) to focus purely on configuration files, databases, and source code.

---
## Usage

### 1. Requirements
Ensure you have Python 3.x installed. The tool utilizes the requests library.

    pip3 install requests

### 2. Execution
Run the tool against a target domain. ROOT privileges are recommended for optimal socket performance.

Syntax:
    sudo python3 noemvex_chronos.py -d <target_domain>

Example:
    sudo python3 noemvex_chronos.py -d tesla.com

---
## Output Preview

    ███╗   ██╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗
    ████╗  ██║██╔═══██╗██╔════╝████╗ ████║██║   ██║██╔════╝╚██╗██╔╝
    ██╔██╗ ██║██║   ██║█████╗  ██╔████╔██║██║   ██║█████╗   ╚███╔╝ 
    ██║╚██╗██║██║   ██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝██╔══╝   ██╔██╗ 
    ██║ ╚████║╚██████╔╝███████╗██║ ╚═╝ ██║ ╚████╔╝ ███████╗██╗  ██╗
    ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                   [ CHRONOS v4.0 ]

    [15:42:01] [INFO] Initiating CHRONOS Scan for: tesla.com
    [15:42:04] [SUCCESS] Ingested 14250 historical data points.
    [15:42:04] [INFO] Engaging Entropy Math & Zombie Asset Hunter...
        >> [ZOMBIE] HIJACKABLE S3 BUCKET: https://tesla-assets-old.s3.amazonaws.com
        >> [ENTROPY 4.82] POTENTIAL SECRET: https://tesla.com/api/v1/auth?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    [15:42:08] [SUCCESS] Weaponized Nuclei Template generated: nuclei_noemvex_tesla.com.yaml
    [15:42:08] [SUCCESS] Chronos Report saved to: chronos_report.txt

---
## ⚠️ Compliance & Ghost Mode
**Regulatory Context:** Identifying forgotten/zombie cloud infrastructure is a critical component of ISO 27001 asset management and prevents massive GDPR data breaches via Subdomain Takeovers.

**Ghost Mode:** All commits to this repository are GPG signed and metadata is strictly managed. Outputs (Nuclei templates, reports) must be strictly ignored.

---
### Developer
**Emre 'noemvex' Sahin**
*Red Team Specialist & Security Architect*
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/emresahin-sec) [![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/noemvex)