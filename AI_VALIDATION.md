# AI Collaboration & Validation Philosophy — PinLens

## Overview
PinLens leverages multimodal AI (GPT-4o Vision) to extract visual tags and categories from user pins. However, non-deterministic AI outputs cannot be trusted blindly in large-scale production infrastructure. 

This engine enforces **deterministic engineering guardrails** to audit, sanitize, and validate AI output before it touches production databases or vector indexes.

## Deterministic Guardrail Rules
1. **Confidence Floor Enforcement:** Any AI output with a confidence score lower than `0.70` is automatically rejected with HTTP 422, preventing low-quality discovery metadata from cluttering the feed.
2. **Safety Auditing:** Safety flags returned by vision models are verified independently before flagging content as safe (`is_safe: bool`).
3. **Data Normalization:** Raw AI tag outputs are sanitized, lowercased, and deduplicated deterministically.

## AI Tooling Used During Development
- **Cursor / GitHub Copilot:** Used to accelerate boilerplate generation for Pydantic data schemas and FastAPI endpoints.
- **Manual Engineering Validation:** All AI-suggested code was refactored for asynchronous efficiency (`asyncio`), schema correctness, and strict type checking.