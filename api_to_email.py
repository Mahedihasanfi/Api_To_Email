import sys
import requests
import smtplib, ssl
from email.message import EmailMessage

def main():
    validate_arguments(3, sys.argv)
    recipient_email = sys.argv[1]
    validate_recipient_email(recipient_email)
    api = sys.argv[2]
    validate_api(api)

    # Fetch information from the Weather API
    if api == "weather":
        url = f"https://api.open-meteo.com/v1/forecast?latitude=60.262&longitude=25.07&current_weather=true"
        response = requests.get(url)
        data=response.json()
        def weather_api():
            while True:
                weather_info=[]
                for key, value in data["current_weather"].items():
                    weather_info.append(f"'{key}': {value}")
                return '\n'.join(weather_info)

    # Fetch information from the Movie API
    elif api == "movie":
        url = "https://online-movie-database.p.rapidapi.com/auto-complete?q=gun"
        headers = {
            "X-RapidAPI-Key": "046fad8b16msh90155f603dd4c97p19396bjsn9f4c32a4d9f0",
            "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"}
        response = requests.get(url, headers=headers)
        data=response.json()
        def movie_api():
            while True:
                movie_info = []
                for item in data["d"]:
                    movie_info.append(item["l"])
                return '\n'.join(movie_info)

    # Formatting the retrieved information into a message
    message = f"API:{api}\n"
    if api == "weather":
        message += f"Weather Information:\n{weather_api()}"
    elif api == "movie":
        message += f"Movie related with word Gun:\n{movie_api()}"

    # For SSL port and Email info
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "YOUR GMAIL"
    receiver_email = recipient_email
    password = "YOUR PASSWORD"

    # Email subject and body text
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "API Information from Python learner!"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Sending Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
            print("Email sent successfully")
        except:
            print("Email didn't send successfully")

# Validating command line arguments
def validate_arguments(length, arg):
    if len(arg) != length:
        print("Please provide two command-line arguments: an email address and an API.")
        sys.exit(1)
    return True

# Validating recipient email
def validate_recipient_email(recipient):
    if "@" not in recipient or "." not in recipient:
        print("Invalid email address format.")
        sys.exit(1)

# Validating API
def validate_api(Api):
    apis = ["weather", "movie"]
    if Api not in apis:
        print("Invalid API argument.")
        sys.exit(1)

# Main function calling
if __name__ == "__main__":
    main()
