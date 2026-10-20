# ME 273 F1 Project: Plan, Constraints, and Goals

Authors: Lucas Boockholdt, Braden Jensen (Sept 2026)

This file is the reference for what the project is, what the program should do, and how we work on it. Check it before starting new work.

## 1. Two Goals

### A. Project goal
Use Formula 1 telemetry from OpenF1 (https://openf1.org, API at api.openf1.org, data from 2023 onward) to analyze drivers. Two candidate directions (pick one, or do both if time allows):

1. **Driving-style classification (primary candidate):** Use each driver's telemetry to sort them into racing styles, then see which styles correlate with better finishing results. Team-level styles can be grouped too.
2. **Overtake prediction (alternative):** Predict the likelihood of a successful overtake from features such as track position, battery state, and gap to the car ahead.

### B. Personal learning goal (equally important)
Lucas wants to teach himself Python through this project. This is a MATLAB class, but the project requires Python, so the Python used should resemble what a sophomore-level college course covers and map onto MATLAB concepts where possible:

- Functions (defining, arguments, return values)
- Matrix math and linear algebra (NumPy)
- Data types: lists, arrays, vectors, matrices; indexing and slicing elements
- Elementwise (vectorized) operations and built-in math functions
- Plotting and visualization (Matplotlib)
- `for` loops, `while` loops, `if/elif/else`
- Possibly some classes (e.g., a `Driver` class holding a driver's data and style metrics)

## 2. Constraints and Working Rules

- **Language:** Python (data pulling and computation). The final deliverable may be Python or MATLAB, per the proposal.
- **Keep the code simple and readable.** Prefer plain NumPy arrays, loops, and functions over clever one-liners, advanced libraries, or heavy abstractions. If a concise idiom is used, explain it.
- **Teach as we go.** When introducing a new Python concept, briefly explain it and note the MATLAB equivalent (e.g., 0-based vs 1-based indexing, `a[1:3]` vs `a(2:3)`, `np.dot` vs `*`, `.T` vs `'`).
- **Use the basics deliberately.** Where reasonable, show both the explicit loop version and the vectorized version so the underlying idea is clear.
- **Data scale:** Datasets have thousands of rows and many columns. Cache pulled data locally (e.g., CSV/NPY files) so we do not re-hit the API each run. Respect OpenF1 rate limits.
- **Libraries (expected):** `numpy`, `matplotlib`, `requests` (API), and possibly `pandas` for tabular loading. Introduce `pandas` only after the NumPy basics are comfortable, and keep it minimal.
- **Project structure:** keep the folder organized (data, code, plots) and comment code in plain language.
- **Short, concise, organized code:** each file has one job and stays short. Functions do one thing. No copy-pasted blocks; if code repeats, make it a function.
- **Notebook + modules split:** the real logic lives in `.py` module files (the "final product"). A notebook (`test.ipynb` or a main notebook) is the front end: it imports the modules, runs them, and shows plots and results. Use the notebook for experimenting and learning, then move working code into modules.

Planned layout (grow it as needed, do not create files before they have a purpose):

```
ME 273 F1 Project/
  PROJECT_PLAN.md
  main.ipynb        # runs the pipeline, shows plots
  data/             # cached API pulls (CSV/NPY)
  f1/
    fetch.py        # OpenF1 API calls + caching
    metrics.py      # style metrics per driver
    classify.py     # style classification / grouping
    plots.py        # all plotting functions
    driver.py       # Driver class (later)
```

## 3. Data Available (OpenF1)

- Car telemetry: speed, throttle, brake status, engine RPM, gear, DRS
- Location: track x/y/z coordinates
- Timing: lap times, sector times, race positions, intervals/gaps
- Pit stops, tire stints
- Weather, race control messages, team radio
- Championship standings

## 4. What the Program Should Do

1. **Fetch and store** telemetry and timing data for selected race sessions via the OpenF1 API.
2. **Clean and organize** it per driver and per lap (arrays/matrices of time series).
3. **Compute style metrics** per driver, for example:
   - Average and maximum throttle, fraction of lap at full throttle
   - Braking frequency, braking duration, brake point consistency
   - Gear shift behavior and RPM distribution
   - Speed through corners (using x/y track position)
   - Lap-time consistency (standard deviation)
   - Tire/pit strategy tendencies
4. **Classify styles** (start simple: threshold rules with `if` statements, then try grouping such as k-means or a hand-written clustering) and group drivers and teams.
5. **Relate style to results** using finishing positions or points (correlation, comparison per style group).
6. **Plot** results so drivers can be compared easily: speed/throttle/brake traces, driver-vs-driver overlays, track maps colored by speed, bar and scatter plots of style metrics vs. placement.
7. *(If doing the overtake option)* build features (gap, position, battery) and estimate overtake success probability, starting from a simple rule-based or logistic model.

## 5. Suggested Learning Progression

1. Python basics: variables, types, printing, `if`, `for`, `while`, functions.
2. NumPy: arrays, vectors, matrices, indexing/slicing, elementwise ops, matrix multiplication, `mean/std/max`.
3. Matplotlib: line plots, subplots, labels, legends, scatter plots, bar charts.
4. Pulling data from the API with `requests`, parsing JSON, saving to file.
5. Computing per-lap and per-driver metrics with loops, then vectorizing.
6. Classes: a `Driver` class storing data and metrics.
7. Style classification and comparison plots.
8. Results analysis and write-up.

## 6. Expected Deliverables

- A Python (or MATLAB) program that takes F1 telemetry and reports each driver's racing style and how styles relate to placings (or predicts takeover likelihood).
- Plots that make it easy to compare drivers.
- Clear, commented code that reflects sophomore-level programming concepts.

## 7. Decisions Made

- **Direction:** driving-style classification (overtake prediction is dropped for now).
- **Per-driver metrics:** compute and display the style metrics for every driver.
- **Success analysis:** evaluate each driver's success relative to course conditions (track layout, weather, tires, etc.), not just raw finishing position.
- **Stretch goal:** predict the next race's results reasonably well from style + track/conditions.
- **Starting scope:** one race first, then scale up.
- **Future ideas:** visualize each course layout (from x/y location data), show which styles suit which tracks, and predict finishing order from that.
- **Language:** Python only. No MATLAB integration (it is possible, via MATLAB's Python interface or by exchanging CSV/.mat files, but it adds complexity that does not help the learning goal).

## 8. Starting Scope (updated)

- **Season:** 2025, all races, so every race has data to compare. Build it season-agnostic (season is a variable) so 2026 can be added later.
- **Drivers:** the top 5 in the 2025 championship standings (pull from the OpenF1 standings data rather than hard-coding).
- **Order of work:** get one 2025 race working end to end for the 5 drivers first, then loop over the full season.
- **Caution:** a full season of telemetry is large (thousands of rows per lap per driver per race). Cache each race to `data/` once, and only pull the 5 drivers' data.

## 9. Remaining Open Questions

- Which single 2025 race to use for the first end-to-end test? (Suggest the season opener, or any race with a normal dry result.)
