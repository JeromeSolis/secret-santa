import argparse
import random
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()
sender_email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

# Load participant data
def load_participants(filename):
    filepath = os.path.join('data', 'participants', filename)
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data['participants']

# Load email template
def load_email_template(filename):
    filepath = os.path.join('data', 'email_templates', filename)
    with open(filepath, 'r') as file:
        return json.load(file)

# Function to create matches
def create_matches(participants):
    names = [p['name'] for p in participants]
    constraints = {p['name']: p.get('constraint', []) for p in participants}
    givers = list(names)
    receivers = list(names)
    matches = {}

    while givers:
        giver = random.choice(givers)
        possible_receivers = [r for r in receivers if r != giver and r not in constraints[giver]]

        if not possible_receivers:
            # No valid match, restart the process
            return create_matches(participants)

        receiver = random.choice(possible_receivers)
        matches[giver] = receiver
        givers.remove(giver)
        receivers.remove(receiver)

    return matches

def save_matches_to_log(matches, participant_file, log_dir="logs"):
    # Ensure the logs directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Extract base name of participant file
    base_name = os.path.splitext(os.path.basename(participant_file))[0]

    # Create a log file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{log_dir}/{base_name}_matches_{timestamp}.json"

    # Write matching results to the log file
    with open(log_filename, "w") as file:
        json.dump(matches, file, indent=4)

    print(f"Matches saved to {log_filename}")

# Function to send emails
def send_emails(matches, participants, email_template):
    participants_dict = {p['name']: p['email'] for p in participants}

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

    for giver, receiver in matches.items():
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = participants_dict[giver]
        message["Subject"] = email_template["subject"]

        body = email_template["body"].format(giver=giver, receiver=receiver)
        message.attach(MIMEText(body, "plain"))
        server.sendmail(sender_email, participants_dict[giver], message.as_string())

    server.quit()

# Parse input arguments (group filename)
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Secret Santa for a specified JSON file.")
    parser.add_argument("json_file", help="Name of the JSON file with participant data")
    parser.add_argument("--template", default="email_default.json", help="Email template JSON file (optional)")
    args = parser.parse_args()
    return args.json_file, args.template

# Main function to run the Secret Santa app
def run_secret_santa_for_group(group_file, template_file):
    participants = load_participants(group_file)
    email_template = load_email_template(template_file)
    matches = create_matches(participants)
    send_emails(matches, participants, email_template)
    save_matches_to_log(matches, group_file)

# Run the app
def main():
    # Usage: python script.py group1.json --template group1_email.json
    # The script will look for 'participants/group1.json' and 'email_templates/group1_email.json'
    json_file, template_file = parse_arguments()
    run_secret_santa_for_group(json_file, template_file)

if __name__ == "__main__":
    main()