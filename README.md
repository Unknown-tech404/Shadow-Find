# 🔍 SHADOW FIND - Universal Link Extractor

<p align="center">
  <img src="https://raw.githubusercontent.com/unknown-tech404/Shadow-Find/main/assets/banner.png" alt="SHADOW FIND Banner" width="100%">
</p>


[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-2.1.0-red.svg)]()

> **Extract All Links & URLs from Any Website - Universal Terminal Tool**

## ✨ Features

- 🔗 Extract **all links** (internal & external)
- 🖼️ Extract **images**, **scripts**, **stylesheets**
- 📧 Extract **email addresses**
- 📞 Extract **phone numbers**
- 📄 Extract **JSON**, **XML**, **PDF**, **DOC** files
- 🚀 **Multi-threaded** scanning with layer-based crawling
- 📊 **JSON** report export with structured data
- 🎨 Beautiful **colored output** with live progress tracking
- 🔄 **Recursive crawling** with depth control
- 🧠 **Smart filtering** - Skip javascript:, mailto:, tel: links
- 💻 Works on **Linux**, **Termux**, **Windows**, **macOS**, **Cloud Shell**, **Docker**

## 📸 Screenshots

### Terminal Output - Scan in Progress
<p align="center">
  <img src="https://raw.githubusercontent.com/unknown-tech404/Shadow-Find/main/assets/terminal_scan.png" alt="SHADOW FIND Scanning" width="100%">
</p>

### Terminal Output - Results Summary
<p align="center">
  <img src="https://raw.githubusercontent.com/unknown-tech404/Shadow-Find/main/assets/terminal_results.png" alt="SHADOW FIND Results" width="100%">
</p>

## 📦 Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/unknown-tech404/Shadow-Find.git
cd Shadow-Find

# Install dependencies
pip install -r requirements.txt
```

### Direct Download
```bash
# Download the script
wget https://raw.githubusercontent.com/unknown-tech404/Shadow-Find/main/shadow_find.py

# Make it executable
chmod +x shadow_find.py
```

## 🚀 Usage

### Basic Scan
```bash
python shadow_find.py https://example.com
```

### Advanced Scan
```bash
# With custom threads and depth
python shadow_find.py https://example.com -t 20 -d 3

# Quiet mode (minimal output)
python shadow_find.py https://example.com -q

# Disable colors
python shadow_find.py https://example.com --no-color
```

### Command Line Options
```
positional arguments:
  url                     Target URL to scan

optional arguments:
  -h, --help              Show this help message and exit
  -t, --threads THREADS   Number of threads (default: 10)
  -d, --depth DEPTH       Max crawl depth (default: 2)
  -q, --quiet             Quiet mode (minimal output)
  --no-color              Disable colored output
```

## 📊 Output Example
```
📊 SCAN RESULTS SUMMARY
=======================================================================

🔗 INVENTORY COUNTS:
  ● Total Unique URLs Found: 245
  ● Internal Page Links:     189
  ● External Outbound Links: 56
  ● Scraped Images Assets:   34
  ● Script (JS) Modules:     12
  ● Stylesheet (CSS) Links:  8
  ● Interactive Form Links:  5
  ● Target Emails Found:     3
  ● Phone Links Tracked:     2
  ● Total Execution Time:    4.23s

📂 INTERNAL LINKS (ALL 189):
    1. https://example.com/
    2. https://example.com/about
    3. https://example.com/contact
    ...

📧 EMAILS DISCOVERED:
    1. info@example.com
    2. support@example.com

[+] Clean database report saved to: shadow_find_20240624_120000.json
```

## 📁 Output Files

The tool generates a JSON report with all extracted data:
- `shadow_find_YYYYMMDD_HHMMSS.json`

### JSON Structure
```json
{
  "target": "https://example.com",
  "domain": "example.com",
  "scan_date": "2024-06-24T12:00:00",
  "duration_seconds": 4.23,
  "summary": {
    "total_links": 245,
    "internal_links": 189,
    "external_links": 56,
    "images": 34,
    "scripts": 12,
    "stylesheets": 8,
    "forms": 5,
    "emails": 3,
    "phone_numbers": 2
  },
  "data_records": {
    "internal_links": [...],
    "external_links": [...],
    "images": [...],
    "scripts": [...],
    "stylesheets": [...],
    "forms": [...],
    "emails": [...],
    "phone_numbers": [...]
  }
}
```

## 🛠️ Requirements

- Python 3.6+
- requests
- beautifulsoup4
- colorama

## 🌐 Platform Support

| Platform | Status |
|----------|--------|
| Linux | ✅ Fully Supported |
| Termux | ✅ Fully Supported |
| Windows | ✅ Fully Supported |
| macOS | ✅ Fully Supported |
| Cloud Shell | ✅ Fully Supported |
| Docker | ✅ Fully Supported |

## 🔧 Development

### Building Package
```bash
python setup.py sdist bdist_wheel
```

### Running Tests
```bash
python -m pytest tests/
```

## ⚠️ Disclaimer

> This tool is for educational and legitimate security testing purposes only. Only use this tool on websites you own or have explicit permission to scan. The authors are not responsible for any misuse.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Built with Python
- Inspired by web reconnaissance and OSINT tools
- Community contributions and feedback

## 📞 Contact & Support

- GitHub: [@unknown-tech404](https://github.com/unknown-tech404)
- Issues: [Report a bug](https://github.com/unknown-tech404/Shadow-Find/issues)

---

<p align="center">
  <b>⭐ Star this repository if you found it useful! ⭐</b>
</p>

<p align="center">
  <i>Made with ❤️ for the cybersecurity community</i>
</p>
