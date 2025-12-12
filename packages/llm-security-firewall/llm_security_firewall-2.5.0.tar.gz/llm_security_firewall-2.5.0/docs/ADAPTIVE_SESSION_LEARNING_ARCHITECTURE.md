# Adaptive Session-Learning Architecture

**Date:** 2025-12-04  
**Version:** 2.4.1+  
**Status:** Design Proposal

## Executive Summary

This document describes an adaptive, self-learning architecture for the LLM Security Firewall that uses session-based monitoring and continuous learning to improve security effectiveness while reducing false positives.

## Core Concept: Session as Learning Unit

The **Session-ID** serves as the central anchor to link all interactions, metrics, and security events of a user dialog, creating a **dynamic risk profile** that adapts over time.

## Architecture Flow

```mermaid
flowchart TD
    subgraph InputLayer["Eingabe & Session-Kontext"]
        A["Nutzeranfrage"] --> B{"Session-ID zuweisen<br>oder laden"}
        B --> C["Session-Kontext abrufen<br>Vorherige Anfragen,<br>Basis-Risikoprofil"]
    end

    subgraph AnalyseLayer["Echtzeit-Analyse & Evidenzsammeln"]
        C --> D["Statische Regeln prüfen<br>Schlüsselwörter, Prompt-Muster"]
        C --> E["CUSUM-Drift-Erkennung<br>Vergleicht aktuelle Anfrage<br>mit Session-Verlauf"]
        C --> F["LLM-basierte Klassifizierung<br>Erkennt komplexe Muster"]
    end

    subgraph EntscheidungsLayer["Evidenzfusion & Entscheidung"]
        D --> G[Dempster-Shafer Engine<br>"Fusioniert alle Evidenzen zu<br>einem Gesamtrisiko-Score"]
        E --> G
        F --> G
        G --> H{Risiko-Score<br> & Vertrauensintervall}
    end

    subgraph FeedbackLoop["Lern- & Feedback-Schleife"]
        H --> I["Aktion: Blockieren,<br>Bestätigen, Flaggen"]
        I --> J["Manuelles Feedback<br>oder automatisiertes<br>Ergebnis-Monitoring"]
        J --> K["Modelle & Thresholds<br>anpassen (Retraining)"]
        K --> C
    end
```

## Implementation Components

### 1. Session Context Enrichment & Baseline Creation

Store per Session-ID not only the history, but also **behavioral baselines**:

**Metrics to Collect:**
- Request length (character count, token count)
- Token frequency patterns
- Topic changes (semantic similarity between requests)
- Embedding cosine similarity to previous request
- Time intervals between requests
- Request complexity (nested structures, encoding patterns)

**Baseline Calculation:**
Use the first 3-5 interactions of a session to create a **"normal" profile** for that user:
- Mean and standard deviation for each metric
- Typical topic distribution
- Expected request patterns

### 2. Real-Time Anomaly Detection with Session-Specific CUSUM

Implement CUSUM not globally, but **session-specifically**:

```python
# Pseudocode for session-based CUSUM

class SessionDriftDetector:
    def __init__(self, session_id):
        self.session_id = session_id
        self.request_embeddings = []  # History of this session
        self.cusum_statistic = 0
        self.baseline_metrics = {}
        self.adaptive_threshold = 0.1  # Initial threshold
        self.alarm_threshold = 2.0  # Drift alarm level

    def update(self, current_request_embedding, current_metrics):
        # Calculate deviation from session average
        deviation = calculate_deviation(
            current_request_embedding,
            self.request_embeddings,
            current_metrics,
            self.baseline_metrics
        )
        
        # CUSUM Update: C_t = max(0, C_{t-1} + deviation - threshold)
        self.cusum_statistic = max(
            0,
            self.cusum_statistic + deviation - self.adaptive_threshold
        )
        
        self.request_embeddings.append(current_request_embedding)
        self.update_baseline(current_metrics)

        if self.cusum_statistic > self.alarm_threshold:
            return {
                "drift_detected": True,
                "session_id": self.session_id,
                "cusum_value": self.cusum_statistic
            }
        return {"drift_detected": False}

    def calculate_deviation(self, current, history, current_metrics, baseline):
        # Multi-metric deviation calculation
        embedding_dev = cosine_distance(current, mean(history))
        metric_dev = sum(
            abs(current_metrics[k] - baseline[k]["mean"]) / baseline[k]["std"]
            for k in baseline.keys()
        )
        return (embedding_dev + metric_dev) / 2
```

### 3. Dempster-Shafer Engine with Feedback Loop

**Evidence Sources:**
- `m1(Risk)` from **static rules** (e.g., known attack patterns)
- `m2(Risk)` from **CUSUM drift value** of this session
- `m3(Risk)` from **LLM-based real-time assessment** (e.g., LlamaGuard)

**Learning from Decisions:**
- If a block is **manually overridden** → mark as "False Positive" → adjust evidence weights for this session class
- If an attack was successful (**False Negative**) → **retrain** drift model with new attack data

## Practical Implementation Steps

### Phase 1: Session Database Extension

**Current State:**
- SessionMonitor tracks violations and risk accumulation
- Basic session state management exists

**Enhancements Needed:**
```sql
-- Example schema extension
ALTER TABLE sessions ADD COLUMN baseline_metrics JSONB;
ALTER TABLE sessions ADD COLUMN risk_score_timeline JSONB;
ALTER TABLE sessions ADD COLUMN false_positive_flags INTEGER DEFAULT 0;
ALTER TABLE sessions ADD COLUMN session_type VARCHAR(50); -- 'support', 'code_gen', etc.
```

### Phase 2: CUSUM Prototype

**Start with one metric** (e.g., request length) per session:
1. Collect baseline from first 3-5 requests
2. Calculate CUSUM statistic for each subsequent request
3. Log drift events (don't block yet)
4. Analyze patterns after 1-2 weeks of data

### Phase 3: Feedback Interface

**Admin Panel Features:**
- View blocked requests with context
- Mark as "Correct Block" or "False Positive"
- View session timeline and risk progression
- Export feedback data for model retraining

### Phase 4: Automatic Threshold Calibration

**Per Session-Type Thresholds:**
- "Support-Chat": Higher tolerance for question variations
- "Code-Generator": Stricter on execution patterns
- "General": Balanced approach

**Calibration Algorithm:**
```python
def calibrate_threshold(session_type, feedback_data):
    fp_rate = count_false_positives(feedback_data) / total_blocks
    if fp_rate > 0.05:  # 5% FPR target
        threshold = increase_threshold(current_threshold)
    elif fp_rate < 0.01:  # Too conservative
        threshold = decrease_threshold(current_threshold)
    return threshold
```

## Current Implementation Status

### Already Implemented

1. **Session Monitoring:**
   - `kids_policy/session_monitor.py` - Tracks violations and risk accumulation
   - Session-based risk decay
   - Violation counting

2. **CUSUM Detection:**
   - `src/llm_firewall/core/cusum_detector.py` - Global CUSUM implementation
   - Oscillation detection
   - Drift detection infrastructure

3. **Evidence Fusion:**
   - Dempster-Shafer theory implementation exists
   - Multi-evidence combination

### Missing Components

1. **Session-Specific CUSUM:**
   - Current CUSUM is global, not per-session
   - Need session-based baseline calculation

2. **Feedback Loop:**
   - No manual feedback interface
   - No automatic threshold calibration
   - No retraining pipeline

3. **Baseline Metrics:**
   - Session baseline calculation not implemented
   - Behavioral profiling incomplete

## Challenges & Considerations

### False Positives

**Problem:** Overly sensitive systems disrupt user experience.

**Solution:**
- Start with **logging only**, not automatic blocking
- Implement shadow mode: log decisions without blocking
- Gradual rollout: 1% → 10% → 100% of traffic

### Data Privacy (GDPR)

**Problem:** Session data with behavioral profiles may be personal data.

**Solution:**
- Anonymize after session end (TTL-based deletion)
- Hash session IDs with daily salt
- Store only aggregated metrics, not raw prompts
- Clear legal basis for processing

### Computational Cost

**Problem:** Real-time embedding and LLM calls are expensive.

**Solution:**
- Sample-based calculation: Calculate full metrics for 10% of requests
- Cache embeddings for similar requests
- Use lightweight models for baseline metrics
- Batch processing for non-critical paths

## Integration with Existing Architecture

### Current Flow (v2.4.1)

```
User Request → Normalization → Pattern Matching → Risk Scoring → Decision
```

### Proposed Enhanced Flow

```
User Request → Session Context Load → Baseline Comparison → 
  → [Static Rules + CUSUM Drift + LLM Classification] → 
  → Dempster-Shafer Fusion → Decision → Feedback Collection
```

### Migration Path

1. **Phase 1 (v2.5.0):** Add session baseline calculation (logging only)
2. **Phase 2 (v2.5.1):** Implement session-specific CUSUM (shadow mode)
3. **Phase 3 (v2.6.0):** Add feedback interface and threshold calibration
4. **Phase 4 (v2.7.0):** Full adaptive learning with retraining pipeline

## Benefits

1. **Context-Sensitive:** Distinguishes between "unusual new user" and "established user with sudden deviation"
2. **Reduced False Positives:** Learns from user behavior patterns
3. **Improved Detection:** Catches subtle attacks that span multiple requests
4. **Adaptive:** Adjusts to different use cases (support chat vs. code generation)

## Next Steps

1. **Design Review:** Validate architecture with security team
2. **Prototype:** Implement session baseline calculation for one metric
3. **Data Collection:** Run in shadow mode for 2-4 weeks
4. **Analysis:** Evaluate effectiveness and false positive impact
5. **Rollout:** Gradual deployment with monitoring

---

**Related Documents:**
- `ARCHITECTURE_EVOLUTION.md` - Overall architecture history
- `VALIDATION_REPORT_v2.4.1.md` - Current performance metrics
- `kids_policy/TECHNICAL_REPORT_v2.0_ENGINE_2025_11_28.md` - Engine implementation details

