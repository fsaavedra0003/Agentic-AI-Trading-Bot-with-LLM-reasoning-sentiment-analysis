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



![Architecture Overview](https://github.com/fsaavedra0003/Agentic-AI-Trading-Bot-with-LLM-reasoning-sentiment-analysis/blob/master/pictures/Architecture_overview.png?raw=true)



Project Overview
This project demonstrates an autonomous trading agent that:

ingests news, tweets, Reddit and earnings reports,

uses an LLM to produce sentiment, structured insights and high-level reasoning,

calls tool endpoints (technical indicators, risk calculator, position manager),

decides actions (BUY / SELL / HOLD + position sizing + stop/take rules),

optionally executes trades via a broker API (paper mode strongly recommended),

includes backtesting and a small Streamlit dashboard for visualisation.

Goal: be a clear, well-documented, modular reference implementation suitable for GitHub demonstration and extension.

----

Features
Multi-source ingestion (Twitter, Reddit, News API, earnings PDFs)

LLM-based sentiment, summarization, and reasoning (easy to swap model/provider)

Agent orchestration (LangChain-like tool pattern included)

Hybrid decision logic: LLM reasoning + configurable rules + ML models

Backtesting engine and paper-trading support (Alpaca / Binance adapter)

Streamlit dashboard with sentiment & trade logs

CI checks, unit tests, and deployment Dockerfile examples

Designed with security and risk controls (max position size, circuit breakers)