AI Trading Bot — LLM Agent with Sentiment Analysis

A production-style, agentic AI trading bot that combines LLM reasoning, sentiment analysis, market indicators, and broker APIs to make and (optionally) execute trading decisions.


This repo is designed as a portfolio / research project showing full-stack AI/ML engineering: ingestion, models, agents (tool orchestration), backtesting, execution, monitoring, and a small UI


Table of Contents

1. Project Overview
2. Features
3. Architecture
4. Repo Structure
5. Quickstart (Dev / Paper Trading)
6. Configuration & Environment Variables
7. Detailed Components

Ingestion

LLM Layer & Prompts

Decision Agent (Tooling)

Prediction Models / Backtesting

Execution

Dashboard & Monitoring

8. Example Prompts & Response Schema

9. Risk Management & Safety

10. Deployment Suggestions

11. Testing & Evaluation

12. Contributing

13. License

14. Acknowledgements

![Extract Metrics Screenshot](https://raw.githubusercontent.com/fsaavedra0003/LangChain-PDF-Chatbot-OpenAI/main/Screenshots/extract_metrics.png)


1 The Reddit Ingestion Script for AI Trading Bot
-------------------------------------------
- Fetches posts from relevant subreddits
- Filters by keywords/tickers
- Saves results to JSON for sentiment analysis
