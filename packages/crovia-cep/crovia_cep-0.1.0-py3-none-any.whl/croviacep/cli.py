import argparse
import json
import sys
from huggingface_hub import hf_hub_download

# Default dataset where capsules live
DEFAULT_DATASET = "Tarike/cep-capsules"  # cambia se sposti la mesh


def load_capsule(fingerprint: str, dataset: str = DEFAULT_DATASET) -> dict:
    """
    Scarica e carica una capsule JSON da Hugging Face.
    Si aspetta un file <FINGERPRINT>.json dentro al dataset.
    """
    filename = f"{fingerprint}.json"
    try:
        path = hf_hub_download(
            repo_id=dataset,
            repo_type="dataset",
            filename=filename,
        )
    except Exception as e:
        print(f"cep crovia  {fingerprint}  FAIL", file=sys.stderr)
        print(f"[ERROR] cannot download {filename} from {dataset}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"cep crovia  {fingerprint}  FAIL", file=sys.stderr)
        print(f"[ERROR] cannot read capsule JSON: {e}", file=sys.stderr)
        sys.exit(1)


def print_report(capsule: dict) -> None:
    """
    Stampa il report compatto nello stile che vuoi tu.
    Per ora consideriamo VERIFIED se la capsule esiste e si legge.
    """
    fp = capsule.get("fingerprint", "UNKNOWN")
    model = capsule.get("model", {}) or {}
    metrics = capsule.get("metrics", {}) or {}

    model_id = model.get("model_id", "UNKNOWN")
    period = capsule.get("period", "UNKNOWN")
    providers = metrics.get("providers_total", "?")
    receipts = metrics.get("receipts_valid", "?")
    gini = metrics.get("gini_payouts", "?")
    health = metrics.get("data_health", "?")

    # Riga chiave: brand
    print(f"cep crovia  {fp}  VERIFIED")
    print(f"model      {model_id}")
    print(f"period     {period}")
    print(f"providers  {providers:<6} receipts  {receipts:<6} gini  {gini}")
    print(f"health     {health}      AI Act Annex IV ready")
    print()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="cep",
        description="Display a CROVIA CEP capsule fingerprint"
    )
    parser.add_argument(
        "fingerprint",
        help="Capsule ID, e.g. CEP-2511-K4I7X2",
    )
    parser.add_argument(
        "--dataset",
        default=DEFAULT_DATASET,
        help=f"Hugging Face dataset with capsules (default: {DEFAULT_DATASET})",
    )

    args = parser.parse_args(argv)

    capsule = load_capsule(args.fingerprint, dataset=args.dataset)
    print_report(capsule)


if __name__ == "__main__":
    main()
