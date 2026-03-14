# Contributing Guide

Thank you for your interest in contributing.

## Development Setup

1. Create virtual environment and install dependencies:

   pip install -r requirements.txt

2. Copy environment template:

   cp .env.example .env

3. Initialize local database:

   PYTHONPATH=src python scripts/init_db.py

## Before Opening a Pull Request

- Run tests:
  PYTHONPATH=src python -m pytest -q
- Run one crawler pass:
  PYTHONPATH=src python scripts/run_daily.py
- Ensure no secrets are committed.
- Add or update tests for behavior changes.

## Commit and PR Rules

- Keep commits focused and small.
- Include clear PR description: what changed, why, and how tested.
- For source-specific crawler tuning, update config/sources.yaml and explain
  reason with at least one sample URL.

## Reporting Bugs

Please include:

- Environment details (OS, Python version)
- Reproduction steps
- Expected behavior and actual behavior
- Relevant logs
