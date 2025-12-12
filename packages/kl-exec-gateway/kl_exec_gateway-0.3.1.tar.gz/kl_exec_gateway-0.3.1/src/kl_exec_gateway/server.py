# src/kl_exec_gateway/server.py

from __future__ import annotations

import os
import signal
import sys
import webbrowser
from pathlib import Path
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from kl_kernel_logic import Kernel

from .chat_session import GatewayChatSession
from .config_loader import load_config
from .events import EventStore
from .kernel_integration import build_gateway_kernel
from .logging_config import setup_logging
from .models import GatewayTrace
from .providers import OpenAIChatClient
from .trace_store import TraceStore


class ChatRequest(BaseModel):
    message: str


class PolicySummary(BaseModel):
    allowed: bool
    code: str | None = None
    reason: str | None = None
    rule_id: str | None = None


class StepInfo(BaseModel):
    step_id: str
    step_type: str
    duration_ms: float | None = None
    metadata: dict = {}


class TraceSummary(BaseModel):
    trace_id: str
    created_at: str
    user_message: str
    effective_chat_response: str
    policy: PolicySummary
    steps: list[StepInfo] = []
    total_duration_ms: float | None = None


class ChatResponse(BaseModel):
    reply: str
    trace: TraceSummary


class StatusResponse(BaseModel):
    configured: bool


class StatsResponse(BaseModel):
    version: str
    total_requests: int
    allowed_count: int
    denied_count: int
    avg_duration_ms: float


class ConfigureRequest(BaseModel):
    api_key: str


app = FastAPI(title="KL Exec Gateway", version="0.3.0")

# Process local singletons
_kernel: Optional[Kernel] = None
_event_store: Optional[EventStore] = None
_trace_store: Optional[TraceStore] = None
_session: Optional[GatewayChatSession] = None
_api_key: Optional[str] = None  # takes precedence over ENV
_config_loaded: bool = False


def _effective_api_key() -> Optional[str]:
    if _api_key:
        return _api_key
    return os.environ.get("OPENAI_API_KEY")


def _ensure_config_loaded() -> None:
    """Load configuration and setup logging once."""
    global _config_loaded

    if _config_loaded:
        return

    # Load config
    config = load_config(Path("pipeline.config.json"))

    # Setup logging
    if config.logging.enabled:
        setup_logging(
            log_dir=config.logging.log_dir,
            max_bytes=config.logging.max_bytes,
            backup_count=config.logging.backup_count,
            log_level=config.logging.level,
        )

    _config_loaded = True


def _ensure_session() -> GatewayChatSession:
    global _kernel, _event_store, _trace_store, _session

    if _session is not None:
        return _session

    # Ensure config is loaded
    _ensure_config_loaded()

    api_key = _effective_api_key()
    if not api_key:
        # No key configured - UI should show setup bar
        raise RuntimeError("API_KEY_MISSING")

    # Load config for pipeline settings
    config = load_config(Path("pipeline.config.json"))

    _kernel = build_gateway_kernel()
    _event_store = EventStore()

    # Optional trace persistence
    if config.trace_persistence.enabled:
        _trace_store = TraceStore(db_path=config.trace_persistence.db_path)

    model_client = OpenAIChatClient(model="gpt-4.1-mini", api_key=api_key)

    # Check which transforms are enabled
    enable_sanitization = config.is_step_enabled("sanitize")
    enable_formatting = config.is_step_enabled("format")

    _session = GatewayChatSession(
        kernel=_kernel,
        model_client=model_client,
        event_store=_event_store,
        trace_store=_trace_store,
        enable_sanitization=enable_sanitization,
        enable_formatting=enable_formatting,
    )
    return _session


def _get_event_store() -> Optional[EventStore]:
    """
    Returns the event store if a session exists, otherwise None.
    
    This allows /api/events to return empty list before API key is configured.
    """
    global _event_store
    return _event_store


def _trace_to_summary(trace: GatewayTrace) -> TraceSummary:
    # Convert step traces to step info
    steps = []
    total_duration = 0.0
    
    for step_trace in getattr(trace, 'step_traces', []):
        step_info = StepInfo(
            step_id=step_trace.step_id,
            step_type=step_trace.step_type,
            metadata=step_trace.metadata,
        )
        steps.append(step_info)
    
    return TraceSummary(
        trace_id=trace.trace_id,
        created_at=trace.created_at.isoformat(),
        user_message=trace.user_message.content,
        effective_chat_response=trace.effective_chat_response,
        policy=PolicySummary(
            allowed=trace.policy_decision.allowed,
            code=trace.policy_decision.code,
            reason=trace.policy_decision.reason,
            rule_id=trace.policy_decision.rule_id,
        ),
        steps=steps,
        total_duration_ms=total_duration if total_duration > 0 else None,
    )


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>KL Exec Gateway</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        html, body {
            height: 100%;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1e1f22;
            color: #e6e8eb;
        }
        
        /* Top Bar */
        .top-bar {
            background: #2a2c31;
            padding: 12px 24px;
            font-size: 13px;
            border-bottom: 1px solid #3f4248;
            font-weight: 500;
            letter-spacing: 0.3px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .top-bar-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .top-bar-title {
            color: #e6e8eb;
        }
        .top-bar-version {
            color: #a5a7ab;
            font-size: 11px;
            background: #33353a;
            padding: 3px 8px;
            border-radius: 4px;
        }
        .top-bar-right {
            display: flex;
            align-items: center;
            gap: 20px;
            font-size: 12px;
            color: #a5a7ab;
        }
        .stat-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .stat-label {
            color: #a5a7ab;
        }
        .stat-value {
            color: #e6e8eb;
            font-weight: 600;
        }
        .stat-value.green {
            color: #4caf50;
        }
        .stat-value.red {
            color: #e53935;
        }
        
        /* Setup Bar */
        .setup-bar {
            display: none;
            padding: 10px 24px;
            background: #33353a;
            border-bottom: 1px solid #3f4248;
            align-items: center;
            gap: 12px;
            font-size: 13px;
        }
        .setup-bar input {
            flex: 1;
            max-width: 400px;
            padding: 8px 12px;
            background: #2a2c31;
            border: 1px solid #3f4248;
            border-radius: 6px;
            color: #e6e8eb;
            font-size: 13px;
        }
        .setup-bar input:focus {
            outline: none;
            border-color: #4aa3ff;
        }
        .setup-bar button {
            padding: 8px 16px;
            background: #4aa3ff;
            border: none;
            border-radius: 6px;
            color: #fff;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
        }
        .setup-bar button:hover {
            background: #3b8fdb;
        }
        .setup-bar span {
            color: #a5a7ab;
        }
        #api-key-status {
            color: #4caf50;
        }
        
        /* Main Container */
        .container {
            display: flex;
            height: calc(100vh - 50px);
        }
        
        /* Left: Chat Panel */
        .chat-panel {
            flex: 62%;
            display: flex;
            flex-direction: column;
            background: #1e1f22;
        }
        .chat-log {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
        }
        .chat-input-wrapper {
            padding: 16px 24px;
            background: #2a2c31;
            border-top: 1px solid #3f4248;
        }
        .chat-form {
            display: flex;
            gap: 12px;
        }
        .chat-form input {
            flex: 1;
            padding: 12px 16px;
            background: #33353a;
            border: 1px solid #3f4248;
            border-radius: 8px;
            color: #e6e8eb;
            font-size: 14px;
        }
        .chat-form input:focus {
            outline: none;
            border-color: #4aa3ff;
        }
        .chat-form input::placeholder {
            color: #6b6d72;
        }
        .chat-form button {
            padding: 12px 24px;
            background: #4aa3ff;
            border: none;
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
        }
        .chat-form button:hover {
            background: #3b8fdb;
        }
        
        /* Chat Messages */
        .message-user {
            margin: 14px 0;
            background: #33353a;
            padding: 14px 18px;
            border-radius: 12px;
            max-width: 75%;
            border-left: 3px solid #4aa3ff;
        }
        .message-ai {
            margin: 14px 0;
            background: #2a2c31;
            padding: 14px 18px;
            border-radius: 12px;
            max-width: 75%;
            border-left: 3px solid #9fa2a7;
        }
        .message-ai.denied {
            border-left: 3px solid #e53935;
            background: #2d2628;
        }
        .message-prefix {
            font-size: 11px;
            color: #a5a7ab;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .message-content {
            color: #e6e8eb;
            line-height: 1.6;
        }
        .message-system {
            margin: 14px 0;
            padding: 12px 16px;
            background: #2d2a29;
            border-left: 3px solid #f59e0b;
            border-radius: 8px;
            color: #f59e0b;
            font-size: 13px;
        }
        
        /* Right: Insight Panel */
        .insight-panel {
            flex: 38%;
            background: #2a2c31;
            border-left: 1px solid #3f4248;
            display: flex;
            flex-direction: column;
        }
        
        /* Pipeline Visualization */
        .pipeline-viz {
            background: #1e1f22;
            border-bottom: 1px solid #3f4248;
            padding: 20px 24px;
        }
        .pipeline-label {
            font-size: 10px;
            color: #a5a7ab;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            font-weight: 600;
            margin-bottom: 12px;
        }
        .pipeline-steps {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .pipeline-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            flex: 1;
        }
        .step-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #2a2c31;
            border: 2px solid #3f4248;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            transition: all 0.3s ease;
        }
        .step-icon.active {
            background: #4aa3ff;
            border-color: #4aa3ff;
            box-shadow: 0 0 12px rgba(74, 163, 255, 0.4);
            animation: pulse 0.6s ease;
        }
        .step-icon.success {
            background: #4caf50;
            border-color: #4caf50;
        }
        .step-icon.denied {
            background: #e53935;
            border-color: #e53935;
        }
        .step-icon.skipped {
            background: #2a2c31;
            border-color: #3f4248;
            opacity: 0.4;
        }
        .step-name {
            font-size: 9px;
            color: #a5a7ab;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .step-arrow {
            color: #3f4248;
            font-size: 14px;
            margin: 0 -4px;
            transition: opacity 0.3s ease;
        }
        .step-arrow.dimmed {
            opacity: 0.2;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .events-log {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
        }
        
        /* Audit Cards */
        .audit-card {
            background: #33353a;
            border: 1px solid #3f4248;
            padding: 18px 20px;
            border-radius: 10px;
            margin-bottom: 18px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        .audit-card.allowed {
            border-left: 3px solid #4caf50;
        }
        .audit-card.denied {
            border-left: 3px solid #e53935;
        }
        
        /* Card Header */
        .card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
        }
        .card-icon {
            font-size: 16px;
        }
        .card-status {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }
        .status-allowed {
            background: rgba(76, 175, 80, 0.15);
            color: #4caf50;
        }
        .status-denied {
            background: rgba(229, 57, 53, 0.15);
            color: #e53935;
        }
        .card-time {
            margin-left: auto;
            font-size: 11px;
            color: #a5a7ab;
            font-family: 'SF Mono', Consolas, 'Courier New', monospace;
        }
        
        /* Card Content */
        .card-meta {
            font-size: 11px;
            color: #a5a7ab;
            margin-bottom: 12px;
        }
        .card-section {
            margin: 10px 0;
        }
        .preview-label {
            font-size: 10px;
            color: #a5a7ab;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .card-steps {
            display: flex;
            gap: 8px;
            margin: 10px 0;
            flex-wrap: wrap;
        }
        .mini-step {
            background: #2a2c31;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
            border-left: 2px solid #3f4248;
        }
        .mini-step.llm {
            border-left-color: #4aa3ff;
        }
        .mini-step.policy {
            border-left-color: #4caf50;
        }
        .mini-step.policy.denied {
            border-left-color: #e53935;
        }
        .mini-step.transform {
            border-left-color: #9c27b0;
        }
        .mini-step-icon {
            font-size: 12px;
        }
        .mini-step-name {
            color: #a5a7ab;
        }
        .card-prompt, .card-response {
            font-size: 13px;
            padding: 10px 14px;
            background: #2a2c31;
            border-radius: 6px;
            border-left: 2px solid #3f4248;
            color: #d1d3d6;
            line-height: 1.5;
            word-wrap: break-word;
        }
        .card-response.denied {
            color: #e53935;
            background: #2d2628;
            border-left: 2px solid #e53935;
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #2a2c31;
        }
        ::-webkit-scrollbar-thumb {
            background: #3f4248;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #4a4c52;
        }
    </style>
</head>
<body>
<div class="top-bar">
    <div class="top-bar-left">
        <span class="top-bar-title">KL Exec Gateway</span>
        <span class="top-bar-version" id="version">v0.3.0</span>
    </div>
    <div class="top-bar-right" id="stats-bar">
        <div class="stat-item">
            <span class="stat-label">Requests:</span>
            <span class="stat-value" id="stat-total">0</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Allowed:</span>
            <span class="stat-value green" id="stat-allowed">0</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Denied:</span>
            <span class="stat-value red" id="stat-denied">0</span>
        </div>
    </div>
</div>
<div id="setup-bar" class="setup-bar">
    <span>OPENAI_API_KEY for this session:</span>
    <input id="api-key-input" type="password" placeholder="sk-..." />
    <button id="api-key-save">Save</button>
    <span id="api-key-status"></span>
</div>
<div class="container">
    <div class="chat-panel">
        <div id="chat-log" class="chat-log"></div>
        <div class="chat-input-wrapper">
            <form id="chat-form" class="chat-form">
                <input id="chat-input" type="text" autocomplete="off" placeholder="Type a message..." />
                <button type="submit">Send</button>
            </form>
        </div>
    </div>
    <div class="insight-panel">
        <div class="pipeline-viz">
            <div class="pipeline-label">Pipeline Execution</div>
            <div class="pipeline-steps" id="pipeline-viz">
                <div class="pipeline-step">
                    <div class="step-icon" id="step-llm">🤖</div>
                    <div class="step-name">LLM</div>
                </div>
                <div class="step-arrow" id="arrow-1">→</div>
                <div class="pipeline-step">
                    <div class="step-icon" id="step-policy">🛡️</div>
                    <div class="step-name">Policy</div>
                </div>
                <div class="step-arrow" id="arrow-2">→</div>
                <div class="pipeline-step">
                    <div class="step-icon" id="step-sanitize">🧼</div>
                    <div class="step-name">Sanitize</div>
                </div>
                <div class="step-arrow" id="arrow-3">→</div>
                <div class="pipeline-step">
                    <div class="step-icon" id="step-format">📝</div>
                    <div class="step-name">Format</div>
                </div>
                <div class="step-arrow" id="arrow-4">→</div>
                <div class="pipeline-step">
                    <div class="step-icon" id="step-final">✓</div>
                    <div class="step-name">Done</div>
                </div>
            </div>
        </div>
        <div class="events-log" id="events-log"></div>
    </div>
</div>

<script>
    const setupBar = document.getElementById("setup-bar");
    const apiKeyInput = document.getElementById("api-key-input");
    const apiKeySave = document.getElementById("api-key-save");
    const apiKeyStatus = document.getElementById("api-key-status");

    const chatLog = document.getElementById("chat-log");
    const eventsLog = document.getElementById("events-log");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");

    function appendChat(role, text, denied = false) {
        const div = document.createElement("div");
        
        if (role === "user") {
            div.className = "message-user";
            const prefix = document.createElement("div");
            prefix.className = "message-prefix";
            prefix.textContent = "You";
            const content = document.createElement("div");
            content.className = "message-content";
            content.textContent = text;
            div.appendChild(prefix);
            div.appendChild(content);
        } else if (role === "ai") {
            div.className = "message-ai" + (denied ? " denied" : "");
            const prefix = document.createElement("div");
            prefix.className = "message-prefix";
            prefix.textContent = "Assistant";
            const content = document.createElement("div");
            content.className = "message-content";
            content.textContent = text;
            div.appendChild(prefix);
            div.appendChild(content);
        } else {
            div.className = "message-system";
            div.textContent = text;
        }
        
        chatLog.appendChild(div);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    // Pipeline Animation - based on REAL execution trace
    function animatePipeline(steps, policyAllowed) {
        const stepMapping = {
            'llm': 'step-llm',
            'llm_call': 'step-llm',
            'policy': 'step-policy',
            'policy_check': 'step-policy',
            'sanitize': 'step-sanitize',
            'sanitize_pii': 'step-sanitize',
            'format': 'step-format',
            'format_markdown': 'step-format',
            'finalize': 'step-final'
        };
        
        const allStepIds = ['step-llm', 'step-policy', 'step-sanitize', 'step-format', 'step-final'];
        
        // Reset all to default
        allStepIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.className = 'step-icon';
            }
        });
        
        // Reset arrows
        for (let i = 1; i <= 4; i++) {
            const arrow = document.getElementById('arrow-' + i);
            if (arrow) {
                arrow.className = 'step-arrow';
            }
        }
        
        // Track which UI steps were executed
        const executedSteps = new Set();
        
        // Animate based on actual executed steps
        let delay = 0;
        let policyDenied = false;
        
        steps.forEach((step, idx) => {
            const uiStepId = stepMapping[step.step_type] || stepMapping[step.step_id];
            if (!uiStepId) return;
            
            executedSteps.add(uiStepId);
            
            // Check if this is a denied policy step
            const isDenied = (step.step_type === 'policy' || step.step_type === 'policy_check') && !policyAllowed;
            if (isDenied) policyDenied = true;
            
            setTimeout(() => {
                const el = document.getElementById(uiStepId);
                if (el) {
                    el.classList.add('active');
                    setTimeout(() => {
                        el.classList.remove('active');
                        if (isDenied) {
                            el.classList.add('denied');
                        } else {
                            el.classList.add('success');
                        }
                    }, 400);
                }
            }, delay);
            delay += 500;
        });
        
        // Mark skipped steps (those not in executedSteps)
        setTimeout(() => {
            allStepIds.forEach(id => {
                if (!executedSteps.has(id)) {
                    const el = document.getElementById(id);
                    if (el && !el.classList.contains('success') && !el.classList.contains('denied')) {
                        el.classList.add('skipped');
                    }
                }
            });
            
            // Dim arrows after denied/skipped steps
            const stepSequence = ['step-llm', 'step-policy', 'step-sanitize', 'step-format', 'step-final'];
            stepSequence.forEach((stepId, idx) => {
                const step = document.getElementById(stepId);
                const arrow = document.getElementById('arrow-' + (idx + 1));
                if (arrow && step && (step.classList.contains('skipped') || step.classList.contains('denied'))) {
                    arrow.classList.add('dimmed');
                }
            });
            
            // Final step status
            const finalEl = document.getElementById('step-final');
            if (finalEl && !executedSteps.has('step-final')) {
                if (policyDenied) {
                    finalEl.classList.add('denied');
                } else if (policyAllowed) {
                    finalEl.classList.add('active');
                    setTimeout(() => {
                        finalEl.classList.remove('active');
                        finalEl.classList.add('success');
                    }, 400);
                }
            }
        }, delay);
    }

    async function sendMessage(message) {
        appendChat("user", message);
        
        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });
            if (!res.ok) {
                const data = await res.json().catch(() => null);
                const detail = data && data.detail ? data.detail : res.statusText;
                if (res.status === 400 && detail === "API key not configured") {
                    appendChat("system", "API key missing. Please paste your key in the bar above.");
                    setupBar.style.display = "flex";
                } else {
                    appendChat("system", "Error: " + detail);
                }
                return;
            }
            const data = await res.json();
            const denied = data.trace && data.trace.policy && !data.trace.policy.allowed;
            const policyAllowed = data.trace && data.trace.policy ? data.trace.policy.allowed : true;
            const steps = data.trace && data.trace.steps ? data.trace.steps : [];
            
            // Animate pipeline based on ACTUAL executed steps
            animatePipeline(steps, policyAllowed);
            
            appendChat("ai", data.reply, denied);
            
            // Update stats after message
            pollStats();
        } catch (err) {
            appendChat("system", "Network error: " + err);
        }
    }

    chatForm.addEventListener("submit", function (ev) {
        ev.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;
        chatInput.value = "";
        sendMessage(msg);
    });

    function getIcon(allowed) {
        return allowed ? "✓" : "✕";
    }

    function formatTime(isoString) {
        const d = new Date(isoString);
        return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    function truncate(text, maxLen = 120) {
        if (text.length <= maxLen) return text;
        return text.substring(0, maxLen) + "...";
    }

    function renderEvents(events) {
        eventsLog.innerHTML = "";
        for (const ev of events) {
            const card = document.createElement("div");
            card.className = "audit-card " + (ev.policy.allowed ? "allowed" : "denied");
            
            // Header: Icon + Status + Time
            const header = document.createElement("div");
            header.className = "card-header";
            
            const icon = document.createElement("span");
            icon.className = "card-icon";
            icon.textContent = getIcon(ev.policy.allowed);
            
            const status = document.createElement("span");
            status.className = "card-status " + (ev.policy.allowed ? "status-allowed" : "status-denied");
            status.textContent = ev.policy.allowed ? "ALLOWED" : "DENIED";
            
            const time = document.createElement("span");
            time.className = "card-time";
            time.textContent = formatTime(ev.created_at);
            
            header.appendChild(icon);
            header.appendChild(status);
            header.appendChild(time);
            
            // Meta: Rule info
            const meta = document.createElement("div");
            meta.className = "card-meta";
            meta.textContent = "rule: " + (ev.policy.rule_id || "n/a") + " · code: " + (ev.policy.code || "n/a");
            
            // Steps section
            const stepsDiv = document.createElement("div");
            stepsDiv.className = "card-steps";
            if (ev.steps && ev.steps.length > 0) {
                ev.steps.forEach(step => {
                    const miniStep = document.createElement("div");
                    miniStep.className = "mini-step " + step.step_type;
                    if (step.step_type === 'policy' && !ev.policy.allowed) {
                        miniStep.classList.add('denied');
                    }
                    
                    const icon = document.createElement("span");
                    icon.className = "mini-step-icon";
                    icon.textContent = getStepIcon(step.step_type);
                    
                    const name = document.createElement("span");
                    name.className = "mini-step-name";
                    name.textContent = step.step_id;
                    
                    miniStep.appendChild(icon);
                    miniStep.appendChild(name);
                    stepsDiv.appendChild(miniStep);
                });
            }
            
            // Prompt section
            const promptSection = document.createElement("div");
            promptSection.className = "card-section";
            const promptLabel = document.createElement("div");
            promptLabel.className = "preview-label";
            promptLabel.textContent = "Prompt";
            const promptText = document.createElement("div");
            promptText.className = "card-prompt";
            promptText.textContent = truncate(ev.user_message, 100);
            promptSection.appendChild(promptLabel);
            promptSection.appendChild(promptText);
            
            // Response section
            const responseSection = document.createElement("div");
            responseSection.className = "card-section";
            const responseLabel = document.createElement("div");
            responseLabel.className = "preview-label";
            responseLabel.textContent = "Response";
            const responseText = document.createElement("div");
            responseText.className = "card-response" + (ev.policy.allowed ? "" : " denied");
            responseText.textContent = truncate(ev.effective_chat_response, 150);
            responseSection.appendChild(responseLabel);
            responseSection.appendChild(responseText);
            
            // Reason (if denied)
            if (!ev.policy.allowed && ev.policy.reason) {
                const reasonDiv = document.createElement("div");
                reasonDiv.className = "card-meta";
                reasonDiv.textContent = "reason: " + ev.policy.reason;
                reasonDiv.style.marginTop = "8px";
                responseSection.appendChild(reasonDiv);
            }
            
            card.appendChild(header);
            card.appendChild(meta);
            if (stepsDiv.children.length > 0) {
                card.appendChild(stepsDiv);
            }
            card.appendChild(promptSection);
            card.appendChild(responseSection);
            
            eventsLog.appendChild(card);
        }
        eventsLog.scrollTop = 0;
    }
    
    function getStepIcon(stepType) {
        const icons = {
            'llm': '🤖',
            'llm_call': '🤖',
            'policy': '🛡️',
            'policy_check': '🛡️',
            'sanitize': '🧼',
            'sanitize_pii': '🧼',
            'format': '📝',
            'format_markdown': '📝',
            'finalize': '✓'
        };
        return icons[stepType] || '•';
    }

    async function pollEvents() {
        try {
            const res = await fetch("/api/events");
            if (!res.ok) return;
            const data = await res.json();
            renderEvents(data);
        } catch (err) {
            // silent in UI
        }
    }
    
    async function pollStats() {
        try {
            const res = await fetch("/api/stats");
            if (!res.ok) return;
            const data = await res.json();
            
            document.getElementById("stat-total").textContent = data.total_requests;
            document.getElementById("stat-allowed").textContent = data.allowed_count;
            document.getElementById("stat-denied").textContent = data.denied_count;
        } catch (err) {
            // silent
        }
    }

    async function checkStatus() {
        try {
            const res = await fetch("/api/status");
            if (!res.ok) return;
            const data = await res.json();
            if (data.configured) {
                setupBar.style.display = "none";
            } else {
                setupBar.style.display = "flex";
            }
        } catch (err) {
            // ignore
        }
    }

    apiKeySave.addEventListener("click", async function () {
        const key = apiKeyInput.value.trim();
        if (!key) {
            apiKeyStatus.textContent = "Please paste a key.";
            return;
        }
        apiKeyStatus.textContent = "";
        try {
            const res = await fetch("/api/configure", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: key }),
            });
            if (!res.ok) {
                const data = await res.json().catch(() => null);
                const detail = data && data.detail ? data.detail : res.statusText;
                apiKeyStatus.textContent = "Error: " + detail;
                return;
            }
            apiKeyInput.value = "";
            apiKeyStatus.textContent = "✓ Saved";
            setTimeout(() => setupBar.style.display = "none", 1500);
        } catch (err) {
            apiKeyStatus.textContent = "Network error: " + err;
        }
    });

    // Poll every 3 seconds to reduce noise
    setInterval(pollEvents, 3000);
    setInterval(pollStats, 3000);
    pollEvents();
    pollStats();
    checkStatus();
</script>
</body>
</html>
    """


@app.get("/api/status", response_model=StatusResponse)
async def api_status() -> StatusResponse:
    configured = _effective_api_key() is not None
    return StatusResponse(configured=configured)


@app.post("/api/configure", response_model=StatusResponse)
async def api_configure(req: ConfigureRequest) -> StatusResponse:
    global _api_key, _session, _event_store, _trace_store, _kernel
    api_key = (req.api_key or "").strip()
    if not api_key:
        raise HTTPException(status_code=400, detail="Empty API key")

    # Keep in process only, do not persist.
    _api_key = api_key

    # Reset current session so the next chat uses the new key.
    _session = None
    _event_store = None
    _trace_store = None
    _kernel = None

    return StatusResponse(configured=True)


@app.post("/api/chat", response_model=ChatResponse)
async def api_chat(req: ChatRequest) -> ChatResponse:
    try:
        session = _ensure_session()
    except RuntimeError as exc:
        if str(exc) == "API_KEY_MISSING":
            raise HTTPException(status_code=400, detail="API key not configured")
        raise HTTPException(status_code=500, detail=str(exc))

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    reply, trace = session.send(req.message)
    summary = _trace_to_summary(trace)
    return ChatResponse(reply=reply, trace=summary)


@app.get("/api/events", response_model=List[TraceSummary])
async def api_events(limit: int = 50) -> List[TraceSummary]:
    """
    Returns recent events. Returns empty list if no session exists yet.
    """
    store = _get_event_store()
    if store is None:
        return []
    traces = list(store.list_recent(limit=limit))
    return [_trace_to_summary(t) for t in traces]


@app.get("/api/stats", response_model=StatsResponse)
async def api_stats() -> StatsResponse:
    """
    Returns aggregate statistics for the current session.
    """
    store = _get_event_store()
    if store is None:
        return StatsResponse(
            version="0.3.0",
            total_requests=0,
            allowed_count=0,
            denied_count=0,
            avg_duration_ms=0.0,
        )
    
    traces = list(store.list_recent(limit=1000))
    total = len(traces)
    allowed = sum(1 for t in traces if t.policy_decision.allowed)
    denied = total - allowed
    
    # Calculate average duration (placeholder, we don't have duration yet)
    avg_duration = 0.0
    
    return StatsResponse(
        version="0.3.0",
        total_requests=total,
        allowed_count=allowed,
        denied_count=denied,
        avg_duration_ms=avg_duration,
    )


def main() -> None:
    """
    Start the web server for the 60/40 UI.

    Entry points:
        kl-gateway-web
        kl-gateway-web --key "sk-..."
        python -m kl_exec_gateway.server

    Configuration is loaded from pipeline.config.json in the current directory.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="KL Exec Gateway Web UI")
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="OpenAI API key (alternative to OPENAI_API_KEY env variable)"
    )
    args = parser.parse_args()
    
    # If --key provided, set it globally
    if args.key:
        global _api_key
        _api_key = args.key
    
    # Ensure config and logging are initialized before starting server
    _ensure_config_loaded()

    url = "http://127.0.0.1:8787"
    print(f"[KL Exec Gateway] Starting server at {url}")
    print("[KL Exec Gateway] Configuration loaded from pipeline.config.json")
    if args.key:
        print("[KL Exec Gateway] API key provided via --key argument")
    print("[KL Exec Gateway] Press Ctrl+C to stop")

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig: int, frame) -> None:
        print("\n[KL Exec Gateway] Shutting down gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        webbrowser.open(url)
    except Exception:
        # If opening a browser fails, the server is still usable.
        pass

    try:
        uvicorn.run(
            "kl_exec_gateway.server:app",
            host="127.0.0.1",
            port=8787,
            reload=False,
            log_level="warning",  # Reduce noise, only warnings and errors
        )
    except KeyboardInterrupt:
        print("\n[KL Exec Gateway] Server stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
