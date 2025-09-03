# Celestial Coreography 
## HackUSU 2025

Celestial Choreography is a Streamlit-based application that visualizes and analyzes satellite rendezvous and proximity operations (RPO). The project was built during HackUSU 2025 at Utah State University to explore innovative ways of making complex aerospace mission planning data more accessible.

RPO is a specialized field of aerospace engineering that deals with maneuvering one satellite (the Deputy) near or around another (the Chief, often called a Resident Space Object). These operations are central to activities such as:

- Satellite servicing and refueling

- Space station docking

In-orbit inspections

Our application provides interactive 2D and 3D visualizations of relative trajectories, maneuvers, eclipse conditions, and sensor constraints. The goal is to help both technical teams and non-technical stakeholders quickly understand whether a mission plan is safe and meets its objectives

### Repository Structure

HACKUSU-2025/
├── Data/                 # CSV datasets (ignored in GitHub)
├── pages/                # Streamlit multipage app scripts
│   ├── eclipses.py
│   ├── fuel.py
│   ├── proximity.py
│   └── stability.py
├── proximity.py          # Core trajectory analysis
├── storage.py            # Data handling utilities
├── requirements.txt      # Python dependencies
├── ReadMe.md             # Project documentation
└── .gitignore


### 📊Features

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
