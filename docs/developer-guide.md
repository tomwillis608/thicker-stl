# Developer Guide - Managing Requirements in the Virtual Environment


This guide explains how to manage and update both production and development dependencies in the virtual environment using Nox and `pip-tools`.


#### 1. **Setting Up the Virtual Environment**

To begin working with the project, you need to set up a virtual environment manually.

1. **Create the virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

---

#### 2. **Managing Dependencies**

The project uses two primary files to manage dependencies:

- **`requirements.in`**: Contains production dependencies.
- **`requirements-dev.in`**: Contains both production and development dependencies.

##### **To Install Dependencies**:
1. After activating the virtual environment, you can install all necessary dependencies by running the Nox `install_dependencies` session:
   ```bash
   nox -s install_dependencies
   ```
   This will install dependencies from the `requirements-dev.txt` file, which includes both production and development dependencies.

##### **To Update or Add Dependencies**:

1. To add a new dependency to the production environment:
   - Add the dependency to the `requirements.in` file.
   
2. To add a new development dependency:
   - Add the dependency to the `requirements-dev.in` file (make sure to include `-r requirements.in` to inherit the production dependencies).

3. After updating the `.in` files, regenerate the `requirements.txt` and `requirements-dev.txt` files by running the Nox `generate_requirements` session:
   ```bash
   nox -s generate_requirements
   ```

This will regenerate both the `requirements.txt` and `requirements-dev.txt` files, ensuring they reflect the changes made in the `.in` files.

---

#### 3. **Rebuilding the Virtual Environment**:
If you need to rebuild the virtual environment (e.g., to ensure it's up to date or fix issues), you can follow these steps:

1. Deactivate the current environment:
   ```bash
   deactivate
   ```

2. Delete the old virtual environment:
   ```bash
   rm -rf venv  # On macOS/Linux
   rmdir /s /q venv  # On Windows
   ```

3. Recreate the virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   nox -s install_dependencies
   ```

---

#### 4. **Summary of Nox Commands**:
- **Generate requirements files**:
  ```bash
  nox -s generate_requirements
  ```
- **Install dependencies**:
  ```bash
  nox -s install_dependencies
  ```
