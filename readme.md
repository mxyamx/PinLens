# PinLens 📌

A high-performance visual metadata ingestion and validation pipeline designed to power large-scale discovery platforms.

`PinLens` combines multimodal AI vision extraction (GPT-4o Vision) with **strict deterministic guardrails** and an asynchronous caching layer (Redis) to ensure data safety, quality, and low latency.

---

## 🚀 Architecture & Key Features

- **High-Performance Async API:** Built with `FastAPI` and `Uvicorn` to handle real-time ingestion workloads seamlessly.
- **Deterministic Guardrails:** Automatically filters out low-confidence metadata (< 0.70) and audits safety flags before content indexing.
- **Smart Caching (Redis):** Prevents redundant AI model invocations by caching and instantly retrieving validated results.
- **Observability & Telemetry:** Integrates `Prometheus` to monitor real-time ingestion throughput, validation failures, and latency histograms.

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+, Pydantic v2
- **Web Framework:** FastAPI, Uvicorn
- **Database & Cache:** PostgreSQL, Redis (Asyncio)
- **AI & Multimodal:** OpenAI API / Vision Models
- **Testing & DevOps:** Pytest, Docker & Docker Compose, Prometheus

---

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mxyamx/pinlens.git](https://github.com/mxyamx/pinlens.git)
   cd pinlens