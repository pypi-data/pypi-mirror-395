# crovia-cep

A minimal CLI to verify CROVIA CEP Capsules (`crovia_cep_capsule.v1`).

## Install (dev / local)

From the source tree:

```bash
pip install -e .

Usage
cep CEP-2511-K4I7X2


Expected output:

cep crovia  CEP-2511-K4I7X2  VERIFIED
model      crovia-llm-demo
period     2025-11
providers  4      receipts  200    gini  0.16
health     A      AI Act Annex IV ready


Capsules dataset:
https://huggingface.co/datasets/Crovia/cep-capsules

