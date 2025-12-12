# Gondolin

**Gondolin** is a security framework for AI Agents. It acts as a "Safe Proxy" layer between your LLM and your sensitive tools (like Jira, Stripe, or AWS).

## The Concept

Instead of giving your Agent raw access to a library, you wrap it in Gondolin. 
Gondolin applies **Policy-as-Code** (YAML + Decorators) to ensure the Agent never executes dangerous actions.