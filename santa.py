import argparse
import random
import json
import os
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
    with open(filename, 'r') as file:
        data = json.load(file)
        return data['participants']

# Function to create matches
def create_matches(participants):
    names = [p['name'] for p in participants]
    constraints = {p['name']: p['constraint'] for p in participants}
    givers = list(names)
    receivers = list(names)
    matches = {}

    while givers:
        giver = random.choice(givers)
        possible_receivers = [r for r in receivers if r != giver and r != constraints.get(giver, '')]

        if not possible_receivers:
            # No valid match, restart the process
            return create_matches(participants)

        receiver = random.choice(possible_receivers)
        matches[giver] = receiver
        givers.remove(giver)
        receivers.remove(receiver)

    return matches

# Function to send emails
def send_emails(matches, participants):
    participants_dict = {p['name']: p['email'] for p in participants}

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

    for giver, receiver in matches.items():
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = participants_dict[giver]
        message["Subject"] = "Ton Père Noël secret !"

        body = (
            f"Bonjour {giver},\n\n"
                "Joyeux Noël ! Nous sommes ravis de t'annoncer que tu es le Père Noël secret de "
                f"{receiver} cette année ! C'est le moment parfait pour partager la joie et l'esprit de Noël.\n\n"
                "N'oublie pas de choisir un cadeau spécial qui rendra son Noël inoubliable. 🎄🎁\n\n"
                "Meilleurs vœux,\n"
                "J"
        )
        message.attach(MIMEText(body, "plain"))
        server.sendmail(sender_email, participants_dict[giver], message.as_string())

    server.quit()

# 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Secret Santa for a specified JSON file.")
    parser.add_argument("json_file", help="Name of the JSON file with participant data")
    args = parser.parse_args()
    return args.json_file

# Main function to run the Secret Santa app
def run_secret_santa_for_group(group_file):
    participants = load_participants(group_file)
    matches = create_matches(participants)
    send_emails(matches, participants)

# Run the app
def main():
    json_file = parse_arguments()
    run_secret_santa_for_group(json_file)

if __name__ == "__main__":
    main()