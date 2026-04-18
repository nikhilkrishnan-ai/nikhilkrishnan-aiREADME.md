# Forensic Audit of GNSS Data Integrity & AI Reliability

## Section 1: Project Objective

**Goal:** To identify, analyze, and mitigate military-grade GPS spoofing anomalies using structured data auditing and IBM-certified prompt engineering frameworks.

**Context:** Evaluation of AI navigation reliability during regional electronic warfare (**Operation Epic Fury**) in the UAE.

---

## Section 2: Technical Methodology

### Data Extraction
- Utilized Visual Studio Code to isolate single-day telemetry logs (April 7, 2026) from a multi-gigabyte JSON dataset.

### Verification Scripting
Developed a custom analysis script to detect kinematic impossibilities, specifically focusing on:

1. **Temporal Inconsistency** — Identifying "Zero-Time Jumps" (multiple coordinates for the same timestamp)
2. **Velocity Spikes** — Flagging movements exceeding human physical limits (recorded 47.5 km/h max velocity)
3. **Spatial Displacement** — Auditing the 333km total distance recorded during a 2.5-hour power-off window

---

## Section 3: Key Findings (April 7 Case Study)

### Ground Truth
- Verified physical presence in **Mohamed Bin Zayed City, Abu Dhabi** (verified via Gainz Gym check-in at 6:40 PM)

### Anomaly Detection

| Entry | Finding | Detail |
|-------|---------|--------|
| Entry 5 | **Critical Anomaly** | Single GPS fix at 14:56 placing device ~145km from base (53.06°E vs base 54.53°E) |
| Entry 6 | **24 position jumps** | Distinct jumps exceeding 100 meters during 18:00–20:00 window |
| Entry 8 | **4.8km "Missing Travel" jump** | Massive displacement during period with no movement trail |

### Root Cause
- **High probability of GPS spoofing / signal generator interference** rather than device hardware failure
- Confirmed by 6-hour blackout (08:00–14:00) consistent with active jamming
- Second 3-hour blackout (15:00–18:00) following anomalous fix

---

## Section 4: Mitigation & Resolution

### AI-Assisted Troubleshooting
- Collaborated with AI tools to deploy a real-time mitigation strategy

### Technical Fix
- Successfully performed a **manual AGPS Reset and Cache Clear** using GNSS diagnostic tools
- This purged the corrupted coordinate data and forced a re-lock on valid satellite constellations

---

## Project Structure
- `Timelineapril7.json` — Raw GPS coordinates and timestamps (April 7, 2026)
- `analyze_gps_spoofing.py` — Custom kinematic anomaly detection script
- `analyze_gps_jumps.py` — Position jump analysis script
- `analyze_gps_dataflow.py` — Apache Beam (Dataflow) pipeline for GeoSense By NK
- `requirements.txt` — Project dependencies (`apache-beam[gcp]`)
- `GEOSENSE_ML_STRATEGY.md` — Cloud integration and ML advanced feature engineering strategy
- `visualize_timeline.html` — Interactive map visualization
- `April_7_Analysis.json` — Structured forensic analysis output
- `April_7_Forensic_Analysis.json` — Clean forensic report (web-tool compatible)
- `spoofing_report.json` — Detailed anomaly log
- `dataflow_anomalies_output-00000-of-00001.jsonl` — Anomalies detected via Dataflow pipeline
- `IBMSkillsNetwork_AI0117EN_Certificate.pdf` — IBM Skills Network certification
- `Screenshot_15_JumpMap.jpg` — Jump-map visual evidence
- `NK jump_highlight.jpg` — Visual validation of the 50m+ physical anomaly
- `1000430245_GymBaseline.jpg` — Ground-truth baseline visual evidence
- `NK_Project_Summary_Final.pdf` — Final project summary

---

## Defense Implications
- GPS spoofing common in active conflict zones (Operation Epic Fury, UAE)
- Civilian navigation systems unreliable during military-grade jamming
- **Countermeasures:** INS (Inertial Navigation Systems), DGPS, AGPS Reset
- Multi-constellation receivers (GPS, GLONASS, Galileo) provide redundancy
- Single-point GPS fixes must be flagged as unreliable during blackout windows
