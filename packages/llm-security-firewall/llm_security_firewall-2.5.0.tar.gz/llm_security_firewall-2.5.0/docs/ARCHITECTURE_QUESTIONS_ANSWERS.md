# Architecture Questions & Answers - Development Roadmap

**Date:** 2025-12-04  
**Version:** 2.4.1  
**Status:** Technical Assessment

## Executive Summary

This document provides precise answers to architectural questions that define the next concrete development steps for the LLM Security Firewall.

---

## 1. Architecture & Implementation Depth

### 1.1 Unsicherheitsklassifizierung: "escalate"/"uncertain" States

**Question:** Wird im aktuellen `RiskScorer` oder in einer Policy bereits ein expliziter **"escalate"/"uncertain"**-Zustand neben `allow`/`block` verwendet?

**Answer:** **NEIN - Binäres Entscheidungssystem**

**Current Implementation:**
- **Decision States:** Nur `ALLOW` und `BLOCK` (binär)
- **Location:** `kids_policy/firewall_engine_v2.py` - `process_request()` returns `{"status": "ALLOW"}` or `{"status": "BLOCK"}`
- **Confidence Values:** Existieren, aber führen immer zu binärer Entscheidung

**Evidence:**
```python
# kids_policy/firewall_engine_v2.py
result = {
    "status": "BLOCK",  # or "ALLOW"
    "reason": "...",
    "debug": {
        "risk_score": 0.85,
        "confidence": 0.92,  # Confidence exists but doesn't create third state
    }
}
```

**EnsembleValidator Logic:**
- `EnsembleDecision` hat `confidence: float`, aber `is_threat: bool` (binär)
- Confidence-basierte Gewichtung existiert, aber führt immer zu `ALLOW` oder `BLOCK`

**Gap Analysis:**
- **Missing:** Expliziter `UNCERTAIN` oder `ESCALATE` State
- **Impact:** Keine Möglichkeit für "human-in-the-loop" bei unsicheren Fällen
- **Opportunity:** Confidence-Werte könnten für `UNCERTAIN`-State genutzt werden (z.B. `0.4 < confidence < 0.6`)

**Recommendation:**
- Implement `DecisionState` enum: `ALLOW`, `BLOCK`, `UNCERTAIN`, `ESCALATE`
- `UNCERTAIN`: `0.4 < risk_score < 0.6` → Logging + Flagging, aber erlauben
- `ESCALATE`: `0.6 < risk_score < 0.8` → Manuelle Review erforderlich

---

### 1.2 Tool-Validierung: Inkrementelle Analyse während Streaming

**Question:** Analysiert der `ToolGuard` Code **inkrementell während des LLM-Streamings**, oder erst nach Vollständigkeit des Tool-Aufrufs?

**Answer:** **NACH Vollständigkeit - Kein Streaming**

**Current Implementation:**
- **Location:** `src/llm_firewall/detectors/tool_call_validator.py`
- **Method:** `validate_tool_call(tool_name, args)` - Validiert vollständigen Tool-Call
- **Timing:** Nach JSON-Parsing, vor Tool-Execution

**Evidence:**
```python
# src/llm_firewall/detectors/tool_call_validator.py
def validate_tool_call(
    self, tool_name: str, args: Dict[str, Any]
) -> ToolCallValidationResult:
    """
    Validates COMPLETE tool call (not incremental).
    """
    # 1. Whitelist check
    # 2. Argument validation
    # 3. Risk scoring
    # Returns: ToolCallValidationResult(allowed=True/False)
```

**ToolCallExtractor:**
- `extract_tool_calls(text)` - Extrahiert vollständige JSON-Strukturen
- Keine Streaming-API vorhanden

**Gap Analysis:**
- **Missing:** Inkrementelle Validierung während Token-Streaming
- **Impact:** Kann nicht früh blockieren, wenn gefährliche Patterns erkannt werden
- **Security Risk:** Vollständiger Tool-Call muss erst geparst werden

**Recommendation:**
- Implement `StreamingToolValidator` für Token-für-Token Analyse
- Early detection von gefährlichen Patterns (z.B. `"tool": "delete_file"` nach ersten Tokens)
- Trade-off: Komplexität vs. Sicherheit

---

### 1.3 Automatisiertes Retraining: False Negative Collection

**Question:** Gibt es bereits eine Pipeline, die **erfolgreiche Jailbreaks (False Negatives) automatisch sammelt** und zur Erstellung von Fine-Tuning-Daten für die Klassifikatoren nutzt?

**Answer:** **NEIN - Keine automatisierte Pipeline**

**Current State:**
- **Logging:** Entscheidungen werden geloggt (`logs/` directory)
- **Manual Analysis:** Scripts existieren für False Positive Analysis (`scripts/analyze_false_positives_for_risk_scorer.py`)
- **No Automation:** Keine automatische Sammlung von False Negatives

**Evidence:**
- `logs/` enthält JSONL-Dateien mit Entscheidungen
- Keine automatische Klassifizierung als "False Negative"
- Keine Retraining-Pipeline gefunden

**Gap Analysis:**
- **Missing:** Automatische False Negative Detection
- **Missing:** Fine-Tuning Data Generation Pipeline
- **Missing:** Model Retraining Automation

**Recommendation:**
- Implement `FalseNegativeCollector`:
  - Log alle `ALLOW`-Entscheidungen mit hohem Risk-Score (`>0.6`)
  - Manuelles Review-Interface für False Negative Markierung
  - Export zu Fine-Tuning Dataset (JSONL für HuggingFace)
- Retraining-Pipeline:
  - Wöchentliches Retraining mit neuen False Negatives
  - A/B Testing: Altes vs. Neues Modell

---

## 2. Resources & Prioritization

### 2.1 Zeitrahmen: Produktionsstabilität vs. Forschung

**Question:** Soll der Fokus auf der **sofortigen Verbesserung der Produktionsstabilität** (z.B. Senkung der 1,3 GB RAM-Spitze) oder auf der **Implementierung neuer Forschungsansätze** (z.B. gradientenbasierte Anomalieerkennung) liegen?

**Answer:** **Produktionsstabilität PRIORITÄT**

**Current State:**
- **Memory Usage:** 1.3GB für adversarial inputs (Target: 300MB) - **4.3x über Limit**
- **P99 Latency:** <200ms (Target erfüllt)
- **FPR:** 0.00% (Target: ≤5%, erfüllt)

**Evidence:**
```markdown
## Known Limitations
2. **Memory Usage:** Current memory usage exceeds 300MB cap for adversarial inputs (measured: ~1.3GB)
```

**Recommendation:**
- **P0 (Sofort):** Memory-Optimierung
  - Lazy Loading für ML-Modelle
  - Model Quantization (FP16 statt FP32)
  - Embedding Cache mit LRU-Eviction
  - Batch-Processing statt einzelne Requests
- **P1 (6 Wochen):** Gradientenbasierte Anomalieerkennung (Forschung)
  - Nur wenn Memory-Problem gelöst ist
  - Shadow-Mode Testing

---

### 2.2 Teamkapazität: Self-Improvement-Loop

**Question:** Stehen in den nächsten 6 Wochen **personelle Ressourcen** für ein dediziertes, experimentelles Feature (wie den automatischen Self-Improvement-Loop) zur Verfügung?

**Answer:** **UNBEKANNT - Benötigt Entscheidung**

**Assessment:**
- **Complexity:** Self-Improvement-Loop ist experimentell (hohes Risiko)
- **Time Estimate:** 4-6 Wochen für Prototyp
- **Dependencies:** False Negative Collection Pipeline (siehe 1.3)

**Recommendation:**
- **Option A:** Ja - Wenn Forschungspriorität hoch ist
  - Prototyp in 4 Wochen
  - Shadow-Mode für 2 Wochen
  - Evaluation vor Production
- **Option B:** Nein - Fokus auf Produktionsstabilität
  - Memory-Optimierung (P0)
  - FPR-Optimierung (P1)
  - Self-Improvement später (P2)

---

### 2.3 Risikotoleranz: FPR vs. ASR Trade-off

**Question:** Für die nächste Version: Ist das höchste Ziel die **weitere Reduktion der False-Positive-Rate (FPR)** bei stabiler Attack Success Rate (ASR), oder die **aggressive Senkung der ASR** auch bei moderatem FPR-Anstieg?

**Answer:** **FPR-Reduktion PRIORITÄT (basierend auf v2.4.1 Erfolg)**

**Current Metrics:**
- **FPR:** 0.00% (Validation), 5% (Production Target)
- **ASR:** 40.00% (stabil)

**Analysis:**
- v2.4.1 Hotfix zeigt: FPR-Reduktion ist möglich ohne ASR-Verschlechterung
- 17 False Positives eliminiert → 0% FPR auf Validation Dataset
- ASR bleibt stabil bei 40%

**Recommendation:**
- **Primary Goal:** FPR weiter reduzieren (Target: <2% in Production)
- **Constraint:** ASR darf nicht über 45% steigen
- **Strategy:** 
  - Weitere Whitelist-Filter für bekannte False Positive Patterns
  - Confidence-basierte Threshold-Anpassung
  - Session-basierte Kontext-Bewertung

---

## 3. Risk & Governance

### 3.1 Externe Abhängigkeiten: sentence-transformers/torch

**Question:** Wie kritisch wird die Abhängigkeit von **`sentence-transformers`/`torch`** für den Produktionseinsatz bewertet? Besteht ein starkes Ziel, diese optional zu machen oder durch kleinere ONNX-Modelle zu ersetzen?

**Answer:** **KRITISCH - Aber bereits optional implementiert**

**Current State:**
- **Dependencies:** `sentence-transformers>=2.2.0`, `torch>=2.0.0` in `requirements.txt`
- **Usage:** Embedding Detector, Perplexity Detector
- **Fallback:** System funktioniert ohne ML-Dependencies (mit reduzierter Funktionalität)

**Evidence:**
```python
# src/llm_firewall/safety/ensemble_validator.py
if embedding_detector and embedding_detector.available:
    # Use ML-based detection
else:
    # Abstain if detector unavailable
    embedding_vote = LayerVote(
        layer_name="Embedding",
        is_threat=False,
        confidence=0.0,
        reason="Embedding: unavailable",
    )
```

**ONNX Support:**
- `onnx>=1.14.0`, `onnxruntime>=1.16.0` bereits in requirements
- Layer 15 Crisis Detection nutzt ONNX
- Export-Scripts existieren: `tools/layer15/export_onnx_layer15.py`

**Gap Analysis:**
- **Current:** ML-Dependencies sind optional (Graceful Degradation)
- **Missing:** ONNX-Export für Embedding/Perplexity Detectors
- **Impact:** 1.3GB Memory hauptsächlich durch PyTorch-Modelle

**Recommendation:**
- **P0:** ONNX-Export für Embedding Detector
  - Reduziert Memory von ~1GB auf ~200MB
  - Eliminiert PyTorch-Dependency für Production
- **P1:** ONNX-Export für Perplexity Detector
  - Weitere Memory-Reduktion
- **P2:** Vollständig ONNX-basierte Pipeline
  - Keine PyTorch-Dependency mehr
  - Deployment-freundlicher

---

### 3.2 Wichtigste Bedrohung: Kritische Lücke

**Question:** Welche Angriffskategorie wird aktuell als die **kritischste Lücke** betrachtet: Ausweichende Prompt-Injections, neuartige Jailbreak-Methoden oder Missbrauch spezifischer Tools?

**Answer:** **Neuartige Jailbreak-Methoden (basierend auf ASR 40%)**

**Current Coverage:**
- **Evasive Prompt Injections:** Gut abgedeckt (Unicode-Normalization, Pattern-Matching)
- **Tool Missbrauch:** Abgedeckt (HEPHAESTUS Protocol, ToolCallValidator)
- **Novel Jailbreaks:** ASR 40% zeigt Lücke

**Evidence:**
- ASR 40% bedeutet: 40% der Redteam-Angriffe werden erlaubt
- Diese sind wahrscheinlich neuartige Jailbreaks, die nicht von statischen Patterns erfasst werden
- Tool-Missbrauch wird durch HEPHAESTUS gut blockiert

**Analysis:**
- **Evasive Injections:** Unicode-Normalization eliminiert viele Bypass-Versuche
- **Tool Abuse:** Whitelist + Argument-Validation funktioniert
- **Novel Jailbreaks:** Erfordern ML-basierte Detection (Embedding-Similarity)

**Recommendation:**
- **Focus:** Verbesserung der Embedding-basierten Jailbreak-Detection
  - Größerer Training-Datensatz für Embedding-Modelle
  - Fine-Tuning auf neuartige Jailbreak-Patterns
  - Ensemble mit mehreren Embedding-Modellen
- **Secondary:** Session-basierte Anomalie-Erkennung
  - Erkennt neuartige Patterns durch Verhaltensabweichung
  - CUSUM-basierte Drift-Detection

---

## 4. Prioritized Action Plan

### Phase 1: Production Stability (Weeks 1-4)

**P0: Memory Optimization**
1. ONNX-Export für Embedding Detector
2. Lazy Loading für ML-Modelle
3. Model Quantization (FP16)
4. Target: 1.3GB → 400MB

**P1: FPR Further Reduction**
1. Erweiterte Whitelist-Filter (ähnlich v2.4.1)
2. Confidence-basierte Threshold-Kalibrierung
3. Target: 5% → 2% FPR

### Phase 2: Adaptive Learning (Weeks 5-8)

**P1: False Negative Collection**
1. Implement `FalseNegativeCollector`
2. Manual Review Interface
3. Fine-Tuning Dataset Export

**P2: Session-Specific CUSUM**
1. Session-Baseline Calculation
2. Per-Session Drift Detection
3. Shadow-Mode Testing

### Phase 3: Advanced Features (Weeks 9-12)

**P2: Decision State Expansion**
1. Implement `UNCERTAIN` State
2. Implement `ESCALATE` State
3. Human-in-the-Loop Interface

**P3: Streaming Tool Validation**
1. Token-für-Token Analysis
2. Early Pattern Detection
3. Performance Impact Assessment

---

## 5. Decision Matrix

| Feature | Priority | Effort | Impact | Risk | Recommendation |
|---------|----------|--------|--------|------|----------------|
| Memory Optimization | P0 | 2 weeks | High | Low | **DO NOW** |
| FPR Reduction | P1 | 1 week | High | Low | **DO NOW** |
| False Negative Collection | P1 | 3 weeks | Medium | Low | **DO NEXT** |
| Session CUSUM | P2 | 4 weeks | Medium | Medium | **EVALUATE** |
| Decision States (UNCERTAIN) | P2 | 2 weeks | Low | Low | **LATER** |
| Streaming Tool Validation | P3 | 6 weeks | Medium | High | **RESEARCH** |
| Self-Improvement Loop | P3 | 6 weeks | High | High | **RESEARCH** |

---

## 6. Critical Dependencies

### External Dependencies Assessment

**sentence-transformers/torch:**
- **Current:** Optional (Graceful Degradation)
- **Target:** ONNX-only für Production
- **Timeline:** 4-6 Wochen für vollständige Migration

**ONNX Runtime:**
- **Current:** Bereits in use (Layer 15)
- **Status:** Production-ready
- **Recommendation:** Erweitern auf alle ML-Komponenten

---

## 7. Next Steps

1. **Immediate (Week 1):**
   - Memory Profiling: Identifiziere größte Memory-Consumer
   - ONNX-Export Prototype für Embedding Detector

2. **Short-term (Weeks 2-4):**
   - Memory Optimization Implementation
   - FPR Reduction (weitere Whitelist-Filter)

3. **Medium-term (Weeks 5-8):**
   - False Negative Collection Pipeline
   - Session-Specific CUSUM Prototype

4. **Long-term (Weeks 9-12):**
   - Decision State Expansion
   - Self-Improvement Loop Research

---

**Document Status:** Complete  
**Next Review:** After Phase 1 completion (Week 4)

