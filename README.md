# 🤖 AI Trading Bot — LLM Agent with Sentiment Analysis

A **production-style, agentic AI trading bot** that combines **LLM reasoning, sentiment analysis, market indicators, and broker APIs** to make and (optionally) execute trading decisions.

This repository is designed as a **portfolio / research project** demonstrating full-stack AI/ML engineering:

- Data ingestion (news, Reddit, Twitter/X, earnings PDFs) 
- LLM reasoning & tool orchestration  
- Hybrid decision logic (LLM + ML + rules)
- Backtesting & paper trading  
- Execution & monitoring with a Streamlit dashboard 

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features) 
3. [Architecture](#architecture)
4. [Repo Structure](#repo-structure)
5. [Quickstart](#quickstart)       
6. [Configuration & Environment Variables](#configuration--environment-variables) 
7. [Detailed Components](#detailed-components)  
   - Ingestion  
   - LLM Layer & Prompts  
   - Decision Agent (Tooling)  
   - Prediction Models / Backtesting  
   - Execution  
   - Dashboard & Monitoring  
8. [Example Prompts & Response Schema](#example-prompts--response-schema)  
9. [Risk Management & Safety](#risk-management--safety)  
10. [Deployment Suggestions](#deployment-suggestions)  
11. [Testing & Evaluation](#testing--evaluation)  
12. [Contributing](#contributing)  
13. [License](#license)  
14. [Acknowledgements](#acknowledgements)  

---

## 🏗️ Architecture

![Architecture Overview](https://github.com/fsaavedra0003/Agentic-AI-Trading-Bot-with-LLM-reasoning-sentiment-analysis/blob/master/pictures/Architecture_overview.png?raw=true)

**Pipeline Overview:**

- Multi-source ingestion: Twitter/X, Reddit, News API, earnings PDFs  
- LLM reasoning: sentiment, structured insights, and decision-making 
- Decision agent: orchestrates tools, indicators, and ML models  
- Broker API: executes trades (paper trading recommended)  
- Backtesting & monitoring via Streamlit dashboard  

---

## 📘 Project Overview

This project demonstrates an **autonomous trading agent** that:
- Ingests **news, tweets, Reddit posts, and earnings reports**  
- Uses an **LLM** for sentiment, summarization, and structured reasoning
- Invokes **tools** for technical indicators, risk calculation, and position sizing   
- Makes decisions: `BUY` / `SELL` / `HOLD` + stop-loss/take-profit rules  
- Optionally executes trades via broker API (paper trading strongly recommended)  
- Includes **backtesting** and a **dashboard** for visualization  

**Goal:** Provide a **clear, modular, and documented** reference for portfolio demonstration and extension.

---

## 🚀 Features

- **Multi-source ingestion:** Twitter, Reddit, News API, earnings PDFs  
- **LLM-based analysis:** Sentiment, summarization, reasoning (swap providers easily)
- **Agent orchestration:** LangChain-style tool pattern  
- **Hybrid decision logic:** LLM reasoning + configurable rules + ML models  
- **Trading support:** Backtesting + paper-trading (Alpaca / Binance adapters) 
- **Dashboard:** Streamlit visualization for sentiment & trade logs  
- **DevOps ready:** CI checks, unit tests, Dockerfile examples 
- **Risk controls:** max position size, configurable limits, circuit breakers  

---

## 📂 Repo Structure

Agentic-AI-Trading-Bot/
│
├─ ingestion/ # Twitter, Reddit, News, PDFs ingestion
├─ sentiment/ # LLM-based sentiment & reasoning modules
├─ models/ # ML models, feature engineering, backtesting
├─ agents/ # Agent orchestration & tool invocation
├─ execution/ # Broker adapters (paper/real trading)
├─ dashboard/ # Streamlit UI
├─ config/ # Env variables, settings, credentials
├─ tests/ # Unit tests
├─ main.py # Entry point (ingestion → analysis → decision)
├─ requirements.txt # Python dependencies











