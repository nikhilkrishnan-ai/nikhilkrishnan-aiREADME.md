# GeoSense By NK: Hybrid Cloud Integration & Machine Learning Strategy

The introduction of the `analyze_gps_dataflow.py` Apache Beam pipeline marks the transition of this project from static forensic analysis to a scalable, hybrid cloud-native anomaly detection system leveraging both **Google Cloud** and **IBM Cloud**.

## 1. Google Cloud & Distributed Processing

The addition of the `apache-beam[gcp]` dependency in `requirements.txt` is crucial. It enables future seamless integration with Google Cloud services (such as Cloud Dataflow) and provides distributed processing capabilities for massive telemetry datasets.

The core of the pipeline leverages Beam's `DoFn` functions to:
*   **Extract Consecutive GPS Pairs:** Efficiently processes `Timelineapril7.json` by focusing on sequential GPS points, which is fundamental for analyzing movement.
*   **Calculate Haversine Distance and Real-time Velocity:** By computing these metrics for each consecutive jump, we establish quantitative measures of movement. The Haversine formula is particularly important here as it accurately calculates distances on a sphere, making it suitable for geographical coordinates.

## 2. Visual Validation & Physical Anomalies

**Visual Validation of Pipeline:** `NK jump_highlight.jpg`

The pipeline intelligently filters and flags points that represent a physical anomaly, specifically identifying jumps exceeding 50 meters. This threshold serves as an initial heuristic for potential spoofing events.

## 3. Prime Example for Feature Engineering

The detected anomalies serve as an excellent foundation for advanced anomaly detection:

*   **Distance and Velocity:** The extreme length of the jump implies an impossible velocity, which can be calculated and flagged as a feature for ML models.
*   **Trajectory Inconsistency:** The straight line over water without any discernible path on land is highly unnatural and acts as a strong indicator of spoofing when analyzed in context with surrounding points.
*   **Environmental Context:** The fact that the jump occurs over a large body of water (the Arabian Gulf, in UAE) provides another layer of contextual anomaly detection. Devices typically don't jump across vast stretches of water unless on a boat or aircraft—if there is land-based travel, this is a red flag.

## 4. Enhancing Anomaly Detection Strategies

Moving forward, the extracted features will power advanced detection strategies:

*   **Statistical Analysis:** These jumps would undoubtedly register as significant outliers in any statistical analysis of distance between points or velocity distribution.
*   **Machine Learning Training (IBM Watsonx & Vertex AI):** To create a labeled dataset for supervised learning, these specific jumps provide perfect examples of "spoofed" or "anomalous" events. The features extracted (e.g., extremely high velocity, straight-line path over water) will contribute to training a robust model. This allows for a **Hybrid Cloud approach**, utilizing **IBM Watsonx.ai** for prompt engineering and model training (building upon our IBM Skills Network certification) alongside Google Cloud's Vertex AI.
*   **Contextual Rules (Geofencing):** We can define rules such as: *"If a device's GPS jumps more than X distance and lands in a large body of water from a land-based origin, flag as highly suspicious."*

## 5. Demonstration and Visualization

These visual artifacts and Dataflow outputs are excellent for demonstrating the project's capabilities. Building a visualization layer using Google Maps Platform APIs on Cloud Run will allow users to highlight such jumps interactively. Imagine clicking on a red anomalous line in a custom web app and seeing the associated data (timestamp, calculated speed, and anomaly score from the ML model).
