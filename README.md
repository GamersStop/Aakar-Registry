# Aakar Registry (आकार) 🧱

> **The Open-Source Package Index & Specification for Swappable AI Capability Blocks**  
> *Part of the Rachana AI Architecture Ecosystem*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Specification](https://img.shields.io/badge/Spec-.aakar%20v1.0-blue.svg)](#the-aakar-package-specification)
[![Quality Gate](https://img.shields.io/badge/CI%20Gate-%E2%89%A590%25%20Compiler%20Pass-green.svg)](#quality-gating--ci-pipeline)
[![Rachana Core](https://img.shields.io/badge/Runtime-Rachana%20Core%20%E2%89%A51.0-orange.svg)](#ecosystem-architecture)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing--publishing)

---

## Overview

**Aakar Registry** (`aakar-registry`) is the open-source specification, community package index, and distribution network for modular, hot-swappable AI capability blocks. 

It establishes the universal **`.aakar`** package standard—allowing developers to extend **Rachana Core** with specialized framework, library, and language intelligence dynamically, without retraining or fine-tuning the underlying frozen base engine.

```
                              [ DEVELOPER ENVIRONMENT ]
                         (VS Code / Neovim / Cursor / CLI)
                                          │
                                          ▼
                  ┌───────────────────────────────────────────────┐
                  │          1. RACHANA CORE RUNTIME              │
                  │          (The Host Engine & Brain)            │
                  │                                               │
                  │ • Local Daemon (:11434 / :8080)               │
                  │ • SQLite State Manager (Zero History Bloat)   │
                  │ • Wasm Context Pruner (Tree-sitter AST)       │
                  │ • Dynamic LoRA Host (Frozen 3B Base Engine)   │
                  └───────────────────────┬───────────────────────┘
                                          │
                   Hot-Mounts Capability Blocks Based on Workspace
                                          │
                 ┌────────────────────────┴────────────────────────┐
                 ▼                                                 ▼
     ┌───────────────────────────────────────┐ ┌───────────────────────────────────────┐
     │          2. AAKAR REGISTRY            │ │         3. KUṬṬIMA REGISTRY           │
     │     (The Open-Source Ecosystem)       │ │     (The Paid Enterprise Platform)    │
     │                                       │ │                                       │
     │ • Free & Open-Source Community Hub    │ │ • Commercial B2B / Air-Gapped Hub     │
     │ • Public Stacks (Python, TS, SQL)     │ │ • Enterprise Stacks (PeopleSoft, SAP) │
     │ • Contributor-Driven Verification     │ │ • Private SDK Ingestion Engine        │
     │ • MIT / Apache 2.0 Licensing          │ │ • SOC 2, SLSA L3, RBAC, Air-Gap Mirror│
     └───────────────────────────────────────┘ └───────────────────────────────────────┘
```

---

## The Core Problem It Solves

Modern AI-assisted coding is caught in a false dichotomy:

1. **The Monolithic Model Trap:** Pre-training or full fine-tuning is massive, slow, and expensive. When a new framework version is released (e.g., Angular Signals, Next.js App Router, FastAPI 0.110+), developers must wait months or years for foundation model providers to update their weights.
2. **The Prompt Bloat Trap:** Developers resort to writing fragile `.cursorrules`, system prompts, and massive Markdown cheat sheets. These consume thousands of tokens per request, trigger hallucination cascades, degrade context windows, and cost significant compute.

### The Aakar Solution: Zero-Token, Hot-Mount Intelligence

Instead of stuffing raw instructions into context or modifying foundation weights, **Aakar** bundles framework knowledge into targeted, compile-checked capability blocks. When Rachana Core detects workspace triggers (e.g., `package.json` dependencies or file extensions), it mounts the relevant `.aakar` block instantly into memory.

---

## The `.aakar` Package Specification

Every `.aakar` package is an uncompressed directory or tarball composed of four fundamental structural layers:

```
fastapi.aakar/
├── aakar.json      # Layer 1: Trigger & Compatibility Manifest
├── grammar.wasm    # Layer 2: Tree-sitter AST Context Pruner (<2ms)
├── adapter.gguf    # Layer 3: Neural Delta LoRA Matrix (<50 MB)
└── verify.sh       # Layer 4: Sandboxed Local Test Harness
```

### 1. `aakar.json` (Trigger Manifest)
Specifies workspace activation rules, file extensions, import markers, and base-model compatibility. Rachana Core inspects this manifest to mount the block deterministically—**without spending a single classification token**.

```json
{
  "$schema": "https://aakar.dev/schemas/v1/manifest.json",
  "name": "fastapi-pydantic-v2",
  "version": "1.2.0",
  "description": "High-precision syntax and idiom intelligence for FastAPI & Pydantic v2",
  "author": "Community Contributors",
  "license": "MIT",
  "compatibility": {
    "engine": "rachana-core",
    "base_model": "deepseek-coder-3b-instruct",
    "min_runtime_version": "1.0.0"
  },
  "triggers": {
    "extensions": [".py"],
    "dependencies": {
      "python": ["fastapi>=0.100.0", "pydantic>=2.0.0"]
    },
    "file_markers": [
      "from fastapi import",
      "import fastapi"
    ]
  },
  "artifacts": {
    "grammar": "grammar.wasm",
    "adapter": "adapter.gguf",
    "verify": "verify.sh"
  }
}
```

### 2. `grammar.wasm` (Context Pruner)
A pre-compiled **Tree-sitter WebAssembly** binary tailored to the targeted syntax. In under **2 milliseconds**, it traverses local files and extracts:
- Interface boundaries, type definitions, and signatures
- Class contracts, function declarations, and public symbols
- Strips implementation details from distant files to prevent context window saturation while preserving 100% type awareness.

### 3. `adapter.gguf` (Neural Delta)
A compact Low-Rank Adaptation (**LoRA**) tensor file (<50 MB) trained exclusively on framework patterns, API contracts, breaking-change migration paths, and idiomatic designs.
- Runs on top of Rachana's frozen base model (e.g., 3B parameter engine).
- Zero base weight corruption or catastrophic forgetting.
- Hot-swappable in memory in milliseconds without restarting the runtime daemon.

### 4. `verify.sh` (Local Test Harness)
An isolated sandbox hook executed locally by Rachana Core to validate generated code against strict compilers, linters, and type checkers before returning suggestions to the user:
```bash
#!/usr/bin/env bash
set -euo pipefail

# Test harness executed inside an ephemeral isolated sandbox
# $1: Path to generated candidate file

mypy --strict --ignore-missing-imports "$1"
ruff check --select B,E,F,W "$1"
```

---

## Public Stacks Catalog

The community index maintains verified `.aakar` blocks across mainstream languages and modern framework ecosystems:

| Capability Block | Trigger Markers | Neural Target | AST Grammar | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`python-fastapi-v2`** | `fastapi`, `pydantic>=2` | Python idioms, async routes | Python Tree-sitter | `stable` |
| **`typescript-angular-signals`**| `@angular/core>=17` | Signals, control-flow syntax | TSX/TS Tree-sitter | `stable` |
| **`typescript-nextjs-approuter`**| `next>=14`, `app/` | Server Actions, RSC, layouts | TSX Tree-sitter | `stable` |
| **`rust-tokio-axum`** | `axum`, `tokio` | Async traits, state extractors | Rust Tree-sitter | `stable` |
| **`sql-postgres-pgvector`** | `vector`, `.sql` | Vector index ops, CTEs, PL/pgSQL | SQL Tree-sitter | `stable` |
| **`go-chi-sqlc`** | `chi`, `sqlc` | Idiomatic Go routing, type safe SQL | Go Tree-sitter | `stable` |

---

## Installation & CLI Usage

Will share the soon

---

## Building an Aakar Block

Will share soon

---

## Quality Gating & CI Pipeline

To ensure reliability, security, and developer trust, all pull requests submitted to the Aakar Registry must pass automated gating:

- **$\ge$90% First-Pass Compiler Success Rate:** Candidate code generated across standard benchmark prompts must pass `verify.sh` with no syntax, linting, or compiler errors.
- **Sub-2ms AST Pruning:** `grammar.wasm` benchmarks must parse reference file hierarchies in under 2 milliseconds.
- **Footprint Budget:** Total uncompressed package size must remain under 65 MB (`adapter.gguf` $< 50$ MB).
- **Sandboxed Execution:** `verify.sh` must execute without elevated privileges or network egress requirements.
- **Clean Licensing:** All constituent datasets, weights, and grammars must comply with open-source licenses (MIT, Apache 2.0, BSD-3-Clause).

---

## Governance & Ecosystem

Aakar Registry is built on open standards and community governance:

- **100% Free & Open Source:** Free to use, fork, inspect, and host privately.
- **Decentralized Distribution:** Works with standard Git repos, OCI artifacts, and content-addressed storage.
- **Hot-Swappable Choice:** If a community member builds a faster or more accurate block, anyone can immediately switch with zero vendor lock-in:
  ```bash
  rachana aakar swap python-fastapi-v2 https://github.com/contributor/fastapi-lightning
  ```
- **Enterprise Sister Hub:** Organizations with proprietary enterprise stacks (SAP, PeopleSoft, internal frameworks) or compliance restrictions (SOC 2, SLSA L3, air-gapped mirroring) can integrate seamlessly with **Kuṭṭima Registry**.

---

## Contributing

We welcome contributions from language experts, framework authors, and AI engineers!

1. Fork this repository.
2. Create a feature branch (`git checkout -b block/svelte-5-runes`).
3. Build and test your block using `rachana aakar test`.
4. Ensure your PR includes benchmark suites proving a $\ge 90\%$ compilation rate.
5. Open a Pull Request for automated CI gating and community review.

Please review [CONTRIBUTING.md](CONTRIBUTING.md) for detailed packaging guidelines, training recipes, and AST compilation instructions.

---

## License

This project is licensed under the [MIT License](LICENSE).
Copyright (c) 2026 Mayuresh Pandit.
Part of the **Rachana Open Intelligence Initiative**.