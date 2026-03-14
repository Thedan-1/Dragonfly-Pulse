# LLM API Contract

The extractor supports OpenAI-compatible chat completion API.

## Required Environment Variables

- OPENAI_API_KEY

## Optional Environment Variables

- OPENAI_MODEL (default: gpt-4o-mini)
- OPENAI_BASE_URL (default: https://api.openai.com/v1)

## HTTP Endpoint

- Method: POST
- Path: /chat/completions
- Header:
  - Authorization: Bearer <OPENAI_API_KEY>
  - Content-Type: application/json

## Request Body (Minimum)

- model: string
- messages: array

## Expected Model Output

Model should return a JSON object in message content with fields:

- competition_name
- organizer
- announcement_title
- registration_start
- registration_deadline
- competition_date
- prize
- competition_level
- source_url

If some fields do not exist in source text, return null.

## Failure Behavior

When API call fails or response JSON parsing fails, system falls back to rule-based extraction.
