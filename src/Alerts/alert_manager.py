from alerts.logger import log_alert, log_event
from alerts.email_alert import send_email_alert


def handle_prediction(data, prediction):
    """
    data: input features
    prediction: 0 (normal) / 1 (attack)
    """

    # Log every event
    log_event(f"Prediction={prediction}, Data={data}")

    # Trigger alert only if attack
    if prediction == 1:
        message = f" Intrusion Detected! Data={data}"

        log_alert(message)

        # Optional email
        try:
            send_email_alert(message)
        except:
            pass