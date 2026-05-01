from Alerts.logger import log_alert, log_event
from Alerts.email_alert import send_email_alert
from Database.insert import insert_event


def handle_prediction(data, prediction):
    # Save to DB
    insert_event(data, prediction)

    # Log event
    log_event(f"Prediction={prediction}, Data={data}")

    # Alert if attack
    if prediction == 1:
        message = f" Intrusion Detected! Data={data}"

        log_alert(message)

        try:
            send_email_alert(message)
        except:
            pass