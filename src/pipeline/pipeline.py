from src.capture.sniffer import start_sniffing
from src.features.extractor import extract_features
from src.detection.predictor import final_decision


MODEL_KEY = "Set-1"


def process_packet(packet):
    try:
        features = extract_features(packet)
        result = final_decision(features, MODEL_KEY)

        print(f"[{result}] {packet.summary()}")

    except Exception as e:
        print("Error:", e)


def start_pipeline():
    print("Starting IDS Pipeline...")
    try:
        start_sniffing(process_packet, iface=None)
    except Exception as exc:
        print(f"Pipeline could not start: {exc}")
        raise


if __name__ == "__main__":
    start_pipeline()
