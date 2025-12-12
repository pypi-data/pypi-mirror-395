# KL Exec Gateway

**A small execution layer that lets you see and govern what an LLM actually does.**

Most LLM calls are a black box:
you send a prompt, something happens in between, and a result appears.

You don't see the steps, the decisions, or the filters.

**KL Exec Gateway makes the entire process visible.**

It runs each request through a deterministic pipeline:

```
LLM → Policy → Sanitization → Formatting → Trace
```

Every step recorded.  
Local. Reproducible. Inspectable.

---

## Try it in 10 seconds

```bash
pip install kl-exec-gateway
kl-gateway-web
# On first launch, the Browser will prompt you to enter your OpenAI API key.
```

Opens automatically at **http://localhost:8787**

**You immediately see:**

- Live pipeline execution with animation
- what you sent to the model
- what the model returned
- which rules were applied
- what was removed or transformed
- the final output
- the full step-by-step trace

![KL Exec Gateway Pipeline](screenshots/pipeline-example-allow-deny.png)

**Alternative: CLI mode**

```bash
kl-gateway --key "sk-..."
```

Interactive terminal chat with full trace logging.

---

## Examples

### 1. Allowed

A normal request flows through the entire pipeline:

```
hello
```

Result:

```
LLM → policy → sanitize → format → done
```

### 2. Denied after LLM (length limit)

```
tell me a love story
```

This usually produces a long answer that exceeds the default 500-character length policy:

```
LLM → policy (DENY_LENGTH) → done
```

### 3. Denied before LLM (forbidden pattern)

If a request contains a forbidden pattern (configured in the policy engine), it is blocked before the model is even called:

```
my secret code
```

Result:

```
policy (DENY_PATTERN) → done
```

The LLM step is skipped entirely.

---

## Use cases

- enforce policies on LLM output
- remove or mask sensitive data
- analyse model behaviour
- build safe internal tools
- reproduce responses
- explain decisions to auditors or teams

Simple building blocks. All deterministic (except the LLM call).

---

## Configuration

Default limits: 500 characters, basic pattern blocking.

To adjust:

- Edit `policy.config.json` (policy limits)
- Edit `pipeline.config.json` (pipeline steps, logging, trace)
- Use templates: `configs/production.config.json`, `configs/compliance-gdpr.config.json`

---

## Documentation

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** – how the pipeline works
- **[docs/USAGE.md](docs/USAGE.md)** – examples and recipes
- **[docs/THEORY_ALIGNMENT.md](docs/THEORY_ALIGNMENT.md)** – how it maps to KL Execution Theory

---

## About the KL Execution Model

This project demonstrates how deterministic execution, policy evaluation and step-level traces can be composed into a practical LLM gateway.

It uses **[KL Kernel Logic](https://github.com/lukaspfisterch/kl-kernel-logic)** as its underlying execution substrate.

For details on how the gateway maps to the execution axioms, see **[docs/THEORY_ALIGNMENT.md](docs/THEORY_ALIGNMENT.md)**.

---

## License

[MIT](LICENSE)
