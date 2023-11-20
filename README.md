# Secret Santa App

## Overview

The Secret Santa Application is a fun and convenient way to organize a Secret Santa gift exchange. This Python-based application automates the process of matching participants and notifying them via email who they will be buying a gift for, all while respecting any specified matching constraints.

## Features
- Register participants with name and email.
- Specify constraints to prevent certain participants from being matched together.
- Automatically pair participants for the Secret Santa exchange.
- Send emails to participants with the details of their Secret Santa match.

## Getting Started

### Prerequisites
- Python 3.6 or later
- Access to an SMTP server (e.g., Gmail) for sending emails.
- `python-dotenv` package for managing environment variables.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/JeromeSolis/secret-santa
```
2. Navigate to the application directory
```bash
cd secret-santa
```
3. Install required packages:
```bash
pip install python-dotenv
```

### Setting Up
1. Rename `.env.template` to `.env`
2. Edit `.env` file with your email settings
```makefile
EMAIL_ADDRESS=your-email@example.com
EMAIL_PASSWORD=your-email-password
``` 
3. Fill in the `participants.json` file with the participants' information following the structure in `participants_template.json`.

### Usage
Run the application
```bash
python santa.py
```

## Configuration
- Participants: Update the `participants.json` file with participants' names, emails, and any match constraints.
- Email Customization: Modify the `send_emails` function in `santa.py` to customize the email content and subject.

## License
This project is licensed under the MIT License.