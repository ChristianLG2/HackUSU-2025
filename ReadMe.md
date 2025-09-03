# Celestial Coreography 
## HackUSU 2025

Celestial Choreography is a Streamlit-based application that visualizes and analyzes satellite rendezvous and proximity operations (RPO). The project was built during HackUSU 2025 at Utah State University to explore innovative ways of making complex aerospace mission planning data more accessible.

RPO is a specialized field of aerospace engineering that deals with maneuvering one satellite (the Deputy) near or around another (the Chief, often called a Resident Space Object). These operations are central to activities such as:

- Satellite servicing and refueling

- Space station docking

In-orbit inspections

Our application provides interactive 2D and 3D visualizations of relative trajectories, maneuvers, eclipse conditions, and sensor constraints. The goal is to help both technical teams and non-technical stakeholders quickly understand whether a mission plan is safe and meets its objectives

### Repository Structure

| File/Folder        | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `Data/`            | Raw CSV datasets used for mission planning (**ignored** via `.gitignore`).  |
| `pages/`           | Streamlit multipage app scripts.                                            |
| `pages/eclipses.py`| Eclipse conditions views/plots.                                             |
| `pages/fuel.py`    | Fuel/ΔV usage calculations and visuals.                                     |
| `pages/proximity.py`| Relative motion & safety (KOZ/range-rate) views.                           |
| `pages/stability.py`| Mission segment & stability diagnostics.                                   |
| `proximity.py`     | Core trajectory & proximity operations analysis.                            |
| `storage.py`       | Data loading/parsing utilities for CSV inputs.                              |
| `requirements.txt` | Python dependencies to run the app.                                         |
| `ReadMe.md`        | Project overview and documentation.                                         |
| `.gitignore`       | Ignore rules (all `*.csv` and the entire `Data/` folder).                   |


### Features

Trajectory Visualization: Relative motion of Deputy vs Chief in LVLH and ECI frames.

Maneuver Analysis: Delta-V planning and visualization of maneuver branches.

Ground Contact Windows: Displays when communication with ground stations is possible.

Payload Events: Visualizes data collection and onboard storage capacity.

Condition Overlays: Highlights eclipse phases, sun/moon angle limits, and safety zones.

### HackUSU 2025

This project was developed as part of HackUSU 2025 at Utah State University.
Our team’s objective was to merge aerospace engineering concepts with data visualization and analytics to produce a tool that is both technically accurate and easy to understand.

### Team

- Christian Lira González
- Oscar A. Ramos 
- Patrick O'Neill
