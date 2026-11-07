# Software Requirements Specification (SRS) & Non-Functional Requirements (NFRs)

## 1. System Overview
The Agentic Cityscape Multi-Agent System is an autonomous, token-optimized artificial intelligence orchestration platform featuring 4-tier model routing, persistent memory, and a minimalist animated desktop UI.

---

## 2. Non-Functional Requirements (NFRs) & Latency SLAs

### 2.1 Latency Service Level Agreements (SLAs)
To maintain real-time responsiveness and prevent user-perceived lag, subtask execution must adhere to the following tier-specific maximum round-trip latencies:

| Tier | Provider / Runtime | Target Latency | P95 SLA Ceiling | Primary Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | **Local Ollama** (`:11434`) | `< 25 ms` | **`<= 50 ms`** | Raw telemetry ingestion, syntactic parsing, JSON formatting |
| **Tier 1** | **Local Colibri MoE** (`:8080`) | `< 120 ms` | **`<= 200 ms`** | Quantitative risk modeling, scenario stress-testing |
| **Tier 2** | **FreeLLMAPI Cloud** (`:8000`) | `< 350 ms` | **`<= 500 ms`** | Cloud heuristics, Map-Reduce fan-out, ReAct thought loops |
| **Tier 3** | **Paid Frontier API** | `< 900 ms` | **`<= 1200 ms`** | Regulatory audit sign-off, final executive synthesis |

### 2.2 Dynamic Hardware Scaling & Dual-Mode Power Governor (Universal Profile)

The orchestrator dynamically profiles the host machine's physical hardware and power supply state, scaling concurrency, context limits, and memory ceilings:

| Hardware Profile Tier | Typical Hardware Specs | Concurrency (AC Perf) | RAM Allocation Cap | Local MoE Cache | Context Window |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **ULTRA_LIGHT** | $\le$ 2–4 Cores, $\le$ 6 GB RAM | 2 Worker Threads | 2.0 GB | 1.2 GB | 2048 tokens |
| **ENTRY_LAPTOP** (Dell Inspiron Profile) | 4 Cores, 8–16 GB RAM | 4 Worker Threads | 4.5 GB | 3.5 GB | 4096 tokens |
| **BALANCED_WORKSTATION** | 6–8 Cores, 16–32 GB RAM | 8 Worker Threads | 12.0 GB | 8.0 GB | 8192 tokens |
| **HIGH_END_DESKTOP** | 8–16 Cores, 32–64 GB RAM | 16 Worker Threads | 24.0 GB | 16.0 GB | 16384 tokens |
| **SERVER_ENTERPRISE** | 16+ Cores, $\ge$ 64 GB RAM / Multi-GPU | 32 Worker Threads | 48.0 GB | 32.0 GB | 32768 tokens |

#### Dual-Mode Power Management (AC Performance vs. Battery Saver)
* **⚡ AC Mains Mode (High-Performance Mode)**:
  - **Full Concurrency**: Runs at 100% of maximum worker thread capacity for the detected hardware tier.
  - **Local Model Acceleration**: Keeps Tier 0 (Ollama) and Tier 1 (Colibri MoE) active on local CPU/NVMe/GPU hardware for zero latency, zero cloud dependency, and $0.00 token cost.
  - **Standard Compression**: Standard 2.0x prompt compression ratio (`target_ratio: 0.50`).
* **🔋 Battery Saver Mode (Low TDP / Preservation Mode)**:
  - **Stepped-Down Concurrency**: Throttles worker pool to 1–2 low-power threads (or 3 threads on large workstations) to eliminate fan noise and thermal throttling.
  - **Zero-Cost Cloud Offloading**: Automatically intercepts local compute-heavy subtasks (Ollama dense generation and Colibri disk streaming) and redirects them to zero-cost cloud relays (Tier 2 FreeLLMAPI), dropping host CPU/GPU utilization to $<5\%$ and extending battery life.
  - **Aggressive Token Compression**: Automatically increases compression target to 2.86x (`target_ratio: 0.35`) to minimize network transmission energy.
  - **Dynamic Thermal Tripwire**: If CPU package temp exceeds 85.0°C, concurrency immediately steps down to 2 threads until cooling below 75.0°C.

---

## 3. Quantitative Acceptance Criteria (Definition of Done)

A software build or scheduled optimization run is defined as **DONE** and production-ready only when it satisfies all of the following verifiable criteria:

1. **Zero-Cost Offload Threshold**:
   * Minimum **70.0%** of all generated subtasks in a workflow must be resolved on Tier 0, Tier 1, or Tier 2 at $0.00 billable API cost.
2. **Error-Free Cascading Escalation**:
   * **100%** of network timeouts, connection drops, or malformed schema outputs must recover via the cascading escalation protocol (`Tier 0 -> Tier 1 -> Tier 2 -> Tier 3`) without terminating the active DAG or throwing unhandled exceptions.
3. **Persistent Memory Horizon Adherence**:
   * **100%** of facts saved by the background memory pass must satisfy the **1-month horizon test** (*"Would this statement still be true and worth reading in a conversation a month from now?"*).
   * All saved facts must be tagged `- [stated]` with valid YAML frontmatter and SHA-256 version tokens.
4. **Token Prompt Economy**:
   * Microsoft LLMLingua clause density compression must maintain a prompt compression ratio of **>= 2.0x**.
   * The 4-layer prompt frame must maintain a KV-cache hit rate of **>= 50.0%**.
5. **UI Accessibility & Visual Polish (Taste-Skill Standard)**:
   * The animated cityscape dashboard must maintain WCAG AA contrast ratios (minimum 4.5:1 for body text, 3:1 for large display text).
   * Display headlines must not wrap past 2 lines on desktop viewports.
   * Zero uncalibrated multi-color AI purple gradient slop.

---

## 4. Cybersecurity Standards & Compliance SLAs (2025/2026 Baseline)

To satisfy modern enterprise cyber defense benchmarks, all runtime subsystems and daily updates must continuously enforce:

1. **NIST SP 800-218 (Secure Software Development Framework - SSDF)**:
   - **Automated SBOM Generation**: CycloneDX v1.5 compliant Software Bill of Materials generated on every release with SHA-256 and SHA-384 component hashes.
   - **Provenance & Integrity**: All code modifications cryptographically hashed and verified before runtime loading.
   - **Least Privilege Execution**: All filesystem reads/writes strictly confined within `%LocalAppData%\JanusCore\agent_sandbox\`.

2. **OWASP Top 10 for LLM Applications (2025/2026 Enhanced Defense)**:
   - **LLM01 / Injection Guard**: Multi-layered regex and AST inspection neutralizing direct prompt overrides, indirect injections, and ASCII smuggling.
   - **LLM02 / PII & Secret Redactor**: Automatic redaction of sensitive credentials, emails, SSNs, credit cards, and API keys prior to model dispatch.
   - **LLM05 / SSRF & Protocol Defense**: Strict blocking of cloud metadata endpoints (`169.254.169.254`), private RFC1918 subnets, and non-HTTP protocol schemes.
   - **LLM06 / Excessive Agency Limiter**: Risk-Tiered Sandbox Governor enforcing explicit human approval for destructive operations, external network calls, and host modifications.
   - **LLM10 / Denial of Wallet & Resource Protection**: Sliding-window token accounting and 4.5 GB memory ceilings preventing unbounded consumption.

3. **CISA Secure by Design Guidelines**:
   - Zero default external network access.
   - Hardware-bound DPAPI and authenticated AES-GCM encryption for all stored secrets.
   - Ephemeral session tokens and constant-time HMAC validation.

---

## 5. Command & Search Workbench & Frontend Design Standards (taste-skill aligned)

To ensure enterprise-grade user interaction and eliminate generic AI aesthetic slop:

1. **Interactive Prompt & File Execution Deck**:
   - **Multi-File Context Ingestion**: Drag-and-drop dropzone supporting `.py`, `.md`, `.csv`, `.json`, `.txt`, `.pdf`, `.yaml`, and `.log` with live size calculation, file preview modals, and Cross-Agent Taint Guard sanitization.
   - **Intelligent Prompt Matrix**: Monospaced multi-line command input with real-time token count estimation and quick-action command presets (Deep Search, Autonomous Command, Risk Simulation, Security Audit, Council Consensus).
   - **Routing Engine Selection**: Interactive mode dropdown supporting Auto 4-Tier, Local Edge Only ($0.00), Speculative Fast DAG (-35% Latency), and Battery Saver Low-TDP.

2. **Frontend UI/UX Quality & Anti-Slop Discipline**:
   - **Calibrated Aesthetic Dimensions**: Design Variance 7/10, Motion Intensity 5/10, Visual Density 6/10.
   - **Color Discipline**: Single electric sky blue accent (`#38bdf8` / `#0ea5e9`) anchored by deep zinc/slate backdrops (`#090d16`, `#0f172a`), with functional emerald (`#10b981`) and amber (`#f59e0b`) status indicators.
   - **Tactile Interactions**: Micro-interactions with snappy 180ms cubic-bezier easing and `translateY(-1px)` hover states.
   - **Zero-Trust Session Authentication**: Automatic injection of hardware-bound session bearer tokens for all frontend API calls.

---

## 6. Autonomous Self-Healing & Continuous Error Correction

To guarantee rock-solid runtime execution across automated daily updates:

1. **Multi-Layer Static & Syntax Error Proofing**:
   - **AST Validation**: Python Abstract Syntax Tree parsing (`ast.parse`) checking for syntax errors, unhandled exception branches, and invalid imports before committing any file.
   - **JavaScript & Frontend Linting**: Automated syntax checks (`node -c`) and HTML tag balancing on all UI dashboard components to prevent escaped characters, broken event listeners, or unclosed elements.
   - **Type & Schema Conformance**: Automated validation of API payload schemas, REST routing paths, and header authorizations.

2. **Automated Error Correction & Self-Repair Loops**:
   - **Autonomous Fault Isolation**: When unit tests, syntax checks, or endpoint health checks detect a defect, the system automatically isolates the offending lines, generates a targeted AST patch, and re-executes tests until 100% green.
   - **Numerical & Logic Hallucination Bounds (OWASP LLM09)**: Quantitative outputs (such as VaR figures, Solvency II ratios, token counts) must satisfy strict mathematical sanity bounds before persisting to memory or UI telemetry.

3. **Atomic Rollback & Regression Defense**:
   - If an automated daily patch fails any validation, unit test, or security check after self-repair attempts, an automatic rollback is immediately executed to preserve the last known stable state.
