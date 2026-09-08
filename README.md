# agile-game-final
# Aadu Puli Aatam - v1.0.0-alpha

Welcome to the initial release of **Aadu Puli Aatam** (The Goat and Tiger Game)! This version establishes the fundamental core mechanics, board layout matrix, and turn-based structure for local two-player gameplay.

## 🐅 Features in v1.0.0
* **Asymmetric Board Matrix:** Generates the traditional vertex-and-line intersection chart (apex triangle and expansion grid).
* **Initial Setup:** 
  * 3 Tiger pieces pre-positioned at the apex and inner vertex points.
  * 15 Goat pieces initialized in the reserve pool (off-board).
* **Core Turn Mechanics:**
  * **Phase 1 (Placement):** Goat player places one goat per turn onto any vacant vertex. Goats cannot move or slide until all 15 are deployed. 
  * **Phase 2 (Movement & Capture):** Tigers can move to adjacent connected nodes or capture a goat by jumping over it into an empty space.
* **Win/Loss Detection (Basic):**
  * Tigers win immediately if they capture **5 goats**.
  * Goats win if all tigers are completely immobilized (no legal moves left).

## 🕹️ Controls (CLI / MVP)
* Input node coordinates using alphanumeric notation (e.g., `PLACE G -> A3` or `MOVE T1 -> B2`).
  # Aadu Puli Aatam - v1.0.0-stable

The final production release of **Aadu Puli Aatam** brings a complete, polished experience with intelligent AI opponents, optimized rules enforcement, match history logging, and cross-platform support.

## 🚀 What's New in the Final Release
* **Intelligent AI Opponents:** 
  * Play against the computer with adjustable difficulty levels (*Easy, Medium, Hard*) using Minimax algorithm with Alpha-Beta pruning.
* **Enhanced Rule Enforcement:**
  * Strict validation ensuring tigers cannot leap over other tigers.
  * Prevention of illegal goat movements during the placement phase.
* **Draw Condition Handler:**
  * Automatic stalemate detection (e.g., if neither side wins after 30 consecutive turns without progress, a draw can be claimed).
* **UI & Audio Overhaul:**
  * Traditional South Indian aesthetic theme with responsive touch/click controls.
  * Smooth transition animations for jumping captures and movement paths.
  * Ambient sound effects for goat placements and tiger hunts.

## 📋 Complete Rule Summary Reference
1. **The Board:** Consists of specific intersecting points forming a large triangle with trapezoidal sub-grids. All movements must strictly follow drawn lines.
2. **Goats (Aadu):** 
   * Move first by dropping pieces onto the board one by one.
   * Once deployed, they slide one step at a time along connected paths.
   * **Objective:** Encircle and trap the tigers so they have zero legal moves.
3. **Tigers (Puli):**
   * Can move right from turn one, sliding or jumping over adjacent goats to capture them.
   * **Objective:** Hunt down and eliminate 5 goats.

## 🛠️ Installation & Running
1. Clone the repository:
   ```bash
   git clone [https://github.com/username/aadu-puli-aatam.git](https://github.com/username/aadu-puli-aatam.git)
