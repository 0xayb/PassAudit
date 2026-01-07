# 🛡 PassAudit - Password Strength and Breach Detection Tool

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)
![CLI](https://img.shields.io/badge/Interface-CLI-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**PassAudit** is a professional command line tool designed to evaluate password strength using modern security metrics. It combines realistic attack modeling with entropy estimation and breach dictionary checks, while also offering secure password generation features.

The tool is suitable for:
* Cybersecurity students
* Blue team learning and awareness
* Developers validating password policies
* Personal password hygiene

---

## 📋 Table of Contents

- [✨ Key Features](#-key-features)
- [🚀 Installation](#-installation)
- [🎮 Usage](#-usage)
- [📈 Example Output](#-example-output)
- [🔐 Security Notes](#-security-notes)
- [📜 License](#-license)

---

## ✨ Key Features

### 🔍 Password Analysis
* Strength estimation using **zxcvbn**
* Detection against large compromised password dictionaries
* Entropy calculation and character set analysis
* Pattern detection such as dates, sequences, and dictionary words
* Human readable security recommendations

### 🔑 Password Generation
* Strong passphrase generation using the **EFF Large Wordlist**
* Mixed character passwords with symbols, numbers, and casing
* Alphanumeric and PIN generation
* Cryptographically secure randomness

### 📊 Reporting
* Rich terminal output with colorized results
* Export reports in **JSON** or **CSV** format
* Batch password analysis from files
* Optional **HTML** report generation

### 🖥️ User Experience
* Clean and intuitive CLI powered by **Typer**
* Secure password input using hidden prompts
* Fast feedback with structured output via **Rich**

---

## 🚀 Installation

### Prerequisites
* Python **3.10 or higher**
* pip

### Setup

```bash
# Clone the repository
git clone https://github.com/0xayb/PassAudit.git
cd PassAudit

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make the script executable (optional, Unix/Linux)
chmod +x main.py
```

### Verify Installation

```bash
python3 main.py info
```

If you see the PassAudit information screen, the installation is successful!

---

## 🎮 Usage

### Check Password Strength (Interactive)

```bash
python main.py check
# Enter password when prompted (input is hidden)
```

### Check Password Strength (CLI)

```bash
# Check a specific password
python3 main.py check --password "MyP@ssw0rd123" --show

# Export report
python3 main.py check --password "MyPassword" --export report.json

# With additional dictionary
python3 main.py check -p "test123" --dict custom_passwords.txt
```

### Generate Strong Passwords

```bash
# Generate 1 passphrase (default)
python main.py generate

# Generate 5 passphrases with high entropy
python main.py generate --count 5 --entropy 60

# Generate mixed character passwords
python main.py generate --style mixed --count 3

# Generate alphanumeric passwords
python main.py generate --style alphanumeric --count 5
```

Available styles:
- `passphrase` - Word-based passwords (e.g., "Correct-Horse-Battery-Staple42")
- `mixed` - Random mix of letters, numbers, and symbols
- `alphanumeric` - Letters and numbers only
- `pin` - Numeric only


### Batch Analysis

```bash
# Create a test file
echo -e "password123\nadmin\nqwerty\nMyP@ssw0rd!" > passwords.txt

# Analyze passwords from file
python3 main.py batch passwords.txt

# Custom output file
python3 main.py batch passwords.txt --output results.csv
```

### Get Information

```bash
python main.py info
```

---

## 📈 Example Output

### Password Check Example

```
Password: ********
Length: 8 characters
Strength: Weak (1/4)
Entropy: 37.6 bits
SHA-256 Hash: a665a45920422f...

⚠ WARNING: This is a commonly used password!
It appears in known password breach databases and should not be used.

Security Recommendations:
  1. ⚠️ This password has been exposed in data breaches
  2. Use at least 12 characters for better security
  3. Add uppercase letters, special characters for better security

Suggested Strong Password:
  Ceramic-Snowman-Tropical-Bagel89
  Strength: 4/4
```

### Password Generation Example

```
Generating 3 strong password(s):

┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ #  ┃ Password                   ┃ Length ┃ Entropy  ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ Bamboo-Acrobat-Olive32     │ 23     │ 61.2 bits│
│ 2  │ Gadget-Flamingo-Metric77   │ 25     │ 64.5 bits│
│ 3  │ Plumber-Cosmic-Anchor91    │ 24     │ 62.3 bits│
└────┴────────────────────────────┴────────┴──────────┘
```

---

## 🔐 Security Notes

* Passwords are never stored or logged
* Dictionary checks use SHA-256 hashes only
* Secure random number generator is used
* This tool is not a password manager

---

## 📜 License

This project is licensed under the **MIT License**.
