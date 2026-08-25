# PitchVision

**PitchVision** is a computer vision and sports analytics framework designed to extract automated spatial data from soccer match footage, evaluate player decision-making, and calculate custom advanced metrics like **Expected Pass Completion (xPC)** and **Decision Quality Scores (DQS)**.

## 1. The Computer Vision Pipeline (Data Ingest)

To feed the decision engine, the CV pipeline extracts specific frame-by-frame states whenever a player receives the ball:

* **Player & Ball Tracking:** Uses YOLO for detection and ByteTrack to maintain consistent tracking IDs across frames.
* **Pitch Mapping (Homography):** Maps 2D camera pixel coordinates to a standardized top-down coordinate space ($X, Y$) so distances and angles are calculated in real-world meters instead of pixels.
* **Event Segmentation (The "Freeze Frame"):** Programmatically detects key moments—specifically, **Frame $T_0$ (Ball Receipt)**—marking the exact moment a player locks down possession and must make a choice.

## 2. The Decision Matrix (The Options Generation)

At the exact moment of ball receipt ($T_0$), the system evaluates the spatial state of the pitch:

### 1. The Ball Carrier's Choices

* **Pass:** Scans all teammate locations and calculates passing lanes while checking for defender body-blocking and occlusion.
* **Shoot:** Evaluates distance to goal, angle to goal, and the visual blocking shadow of the goalkeeper and defenders when within shooting range.
* **Dribble/Hold:** Calculates the open space radius (Voronoi cell area) around the ball carrier alongside the closing speed of nearby pressuring defenders.

### 2. Classifying Difficulty (Pass Difficulty Rating)

* Differentiates routine actions (e.g., a short 5-yard square ball between center-backs) from complex execution (e.g., a whipped cross-field switch or a threaded ball through a multi-defender seam).
* Feeds features into a **Pass Difficulty Rating (PDR)** based on distance, defender proximity along the vector line, and passing angle.

## 3. Expected Value & Outcome Tracking (The xPC & Impact Model)

Every decision is linked to a probabilistic outcome, mirroring the concept of Expected Goals (xG):

* **Expected Pass Completion (xPC):** A logistic regression model trained on CV features (defender distance, pass length, pressure) that outputs a baseline completion percentage (e.g., a threaded ball evaluated at **14% xPC**).
* **Decision Quality Score (DQS):** Evaluates all available options at the moment of receipt and scores the player's actual choice.
* *Example:* Choosing a low-percentage 2% xPC dribble into a defensive trap when an open teammate with an 85% xPC pass is available negatively impacts the **Decision Efficiency** score.

* **Downstream Possession Impact (The Chain Reaction):** Tracks the possession window 5 to 10 seconds downstream to measure whether a decision contributed to a high-xG attacking sequence or resulted in an opponent counter-attack.

## 4. Implementation Road Map (TDD Style)

Built iteratively following a test-driven development cycle:

1. **Step 1 (The Baseline):** Write scripts to parse clip coordinates, map 2D top-down locations, and verify accuracy using unit tests on known coordinate data.
2. **Step 2 (The Geometry):** Implement vector-math functions to calculate passing lanes and detect defender bounding box intersections.
3. **Step 3 (The Difficulty Buckets):** Categorize passes into simple bins (Easy, Medium, High Difficulty) and calculate custom success rates.
4. **Step 4 (The Decision Engine):** Build core logic comparing player choices against optimal passing and shooting options within each frame.