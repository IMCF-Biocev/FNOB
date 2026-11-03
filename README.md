# FNOB 2026 – FLOPA Hands-on Session

Welcome to the hands-on session on **FLOPA** for the course **FNOB – FLIM Not Only for Biologists**!

This repository contains the instructions and materials needed to install and run FLOPA, a Python-based software environment for FLIM data analysis.

## Demo datasets

The demo datasets used during the practical session are available on Zenodo: **[Download demo datasets from Zenodo](https://doi.org/10.5281/zenodo.23809808)**

Download the datasets before starting the practical session. Extract the downloaded archive and keep the data in an easily accessible folder.

## Software installation

There are two ways to set up the environment:

- **Option A (recommended):** Install using [`uv`](https://docs.astral.sh/uv/).
- **Option B:** Install using Conda.

Choose one of these approaches.

---

### Option A: Installation using uv (recommended)

#### Step 1. Install uv

  - Follow the official installation instructions for your operating system: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)
  - After installation:
    - **Windows:** Close the PowerShell window used for installation and open a new Command Prompt (CMD).
    - **Linux/macOS:** Open a new terminal window.
  - Check that `uv` is installed correctly by running:
    ```bash
    uv
    ```
  - You should see the uv command-line help.

#### Step 2. Download the repository

  - Download the course repository from GitHub:
    1. Open the GitHub repository.
    2. Click **Code → Download ZIP**.
    3. Extract the downloaded ZIP archive to a folder of your choice.
  - *Alternatively, if you have Git installed, you can clone the repository.*

#### Step 3. Open the repository folder in a terminal

  - Navigate to the folder containing the downloaded repository. 
  - For example:
    ```bash
    cd C:\Users\oa2user\Desktop\Courses\FNOB2026
    ```
  - **Important:** Make sure that you are located in the repository folder containing the `pyproject.toml` file.

#### Step 4. Create the environment and install dependencies

  - Run:
    ```bash
    uv sync --locked
    ```

#### Step 5. Start napari

  - Once the installation is complete, launch napari:
    ```bash
    uv run napari
    ```
  - **That's it!** You are ready to start the practical session.

---
---

### Option B: Installation using Conda

If you prefer using Conda, follow these instructions.

#### Step 1. Install Conda distribution (e.g. Miniforge)

  - Download and install Miniforge for your operating system: [https://github.com/conda-forge/miniforge](https://github.com/conda-forge/miniforge)
  
#### Step 2. Open a terminal

  - **Windows:** Open the Miniforge Prompt from the Start menu.
  - **Linux/macOS:** Open a terminal where Conda is available.

#### Step 3. Download the repository

  - Download the course repository from GitHub:
    1. Open the GitHub repository.
    2. Click **Code → Download ZIP**.
    3. Extract the ZIP archive to a folder of your choice.
    - *Alternatively, clone the repository using Git.*

#### Step 4. Navigate to the repository folder

  - Use `cd` to navigate to the extracted repository folder.
  - For example:
    ```bash
    cd C:\Users\oa2user\Desktop\Courses\FNOB2026
    ```
  - Make sure you are in the folder containing the `environment.yml` file.

#### Step 5. Create and activate the Conda environment

  - Create the environment using the provided configuration file:
    ```bash
    conda env create -f environment.yml
    ```

  - Activate the environment:
    ```bash
    conda activate flopa-demo
    ```

#### Step 6. Start napari

  - Launch napari:
    ```bash
    napari
    ```
  - **That's it!** You are ready to start the practical session.

---

## Useful links

- **Demo datasets:** [Zenodo – FNOB 2026](https://doi.org/10.5281/zenodo.23809808)
- **uv installation:** [Official documentation](https://docs.astral.sh/uv/getting-started/installation/)
- **Miniforge installation:** [GitHub – Miniforge](https://github.com/conda-forge/miniforge)
- **napari documentation:** [https://napari.org/](https://napari.org/)
- **napari-flopa repository:** [GitHub repository](https://github.com/cockovaz/napari-flopa)
