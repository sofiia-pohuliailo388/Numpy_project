# 🪐 Solar System Orbit Simulator

A pet project — an interactive solar system simulation that fetches real orbital data from NASA and visualizes planet trajectories with animation.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Data source | NASA JPL Horizons API |
| Data fetching | astroquery |
| Numerical computing | NumPy |
| Visualization | Matplotlib + Seaborn |
| Animation | Matplotlib FuncAnimation |

---

## ✨ Features

- Fetches real-time orbital data from NASA JPL Horizons
- Supports any solar system object (planets, comets, asteroids)
- Animated orbital trajectories with velocity display
- Dynamic scaling to fit all selected objects
- Tail effect showing recent trajectory

---

## ⚙️ How It Works

```
User enters object names (e.g. Earth, Mars, 1P/Halley)
            ↓
Fetches real position & velocity vectors from NASA API
            ↓
Converts AU coordinates to km
            ↓
Renders animated orbital simulation
```

---
