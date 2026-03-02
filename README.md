# WP-Agents

An intelligent agent framework with multi-tiered memory management and semantic understanding capabilities.

## Overview

WP-Agents is a sophisticated Python-based system designed to manage conversational memory, extract structured information from interactions, and provide contextual understanding through semantic analysis. The system combines short-term message handling with long-term memory archiving and summarization.

## Key Components

- **Memory Management**: Multi-layered memory system with short-term caches and long-term archives
- **Summarization**: Automatic extraction of bookings, reservations, requests, tasks, and facts from conversations
- **User Context**: Per-user state management and message tracking
- **Message Processing**: Semantic analysis and matching of conversation elements

## Project Structure

```
src/
├── memory/          # Core memory management system
├── user/            # User state and context management
└── utils/           # Utilities for data handling and tokens
```

## TODO 

- [ ] MCP compatibility: Add the ability for agents to execute tasks
- [ ] Context management: Supply agents with contextual information to do their tasks 