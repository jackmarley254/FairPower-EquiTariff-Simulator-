# FairPower EquiTariff Simulator – Setup Guide

🔹 Prerequisites

- Install Anaconda (Python 3.10 recommended).
- Install VS Code with the Python and Jupyter extensions.
- Git installed for version control.

🔹 Environment Setup

Clone the repository:

```bash
git clone https://github.com/jackmarley254/FairPower-EquiTariff-Simulator.git
cd FairPower-EquiTariff-Simulator
```

Create the Conda environment from the recipe card (`environment.yml`):

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate equitariff
```

Verify installation:

```bash
python --version
```

Should show Python 3.10.x.

🔹 Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open Swagger UI for API testing:

http://127.0.0.1:8000/docs

🔹 Testing

Run unit tests with:

```bash
pytest
```

