# GitHub and DVC Foundations Practice

## Objective

By the end of this assignment, you will be able to:

- Set up and manage a GitHub repository.
- Utilize Git for version control of your codebase.
- Implement DVC for data versioning and management.
- Collaborate effectively using branches and pull requests.
- Understand the integration between GitHub and DVC in a data-centric project.

## Prerequisites

- Basic understanding of Git and GitHub
- Familiarity with command-line interfaces
- Python installed
- An active GitHub account
- Basic DVC knowledge (helpful but not required)

## Tools and Resources

- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [DVC](https://dvc.org/)
- [Visual Studio Code](https://code.visualstudio.com/) or another code editor

---

## Assignment Structure

### Part 1: Setting Up the GitHub Repository

1. **Create a new GitHub repository** called `github-dvc-practice`.
2. Clone the repo:
   ```bash
   git clone https://github.com/tmatin100/github-dvc-practice.git
   ```

### Part 2: Git Fundamentals

3. Create a Python script `analysis.py`:
   ```python
   def greet(name):
       return f"Hello, {name}!"

   if __name__ == "__main__":
       user_name = input("Enter your name: ")
       print(greet(user_name))
   ```

4. Commit and push:
   ```bash
   git add analysis.py
   git commit -m "Add analysis script"
   git push origin main
   ```

5. Create and merge a branch:
   ```bash
   git checkout -b feature/greeting
   ```

   Modify `analysis.py`:
   ```python
   def farewell(name):
       return f"Goodbye, {name}!"

   print(farewell(user_name))
   ```

   Then:
   ```bash
   git add analysis.py
   git commit -m "Add farewell function"
   git push origin feature/greeting
   ```

   Create and merge a Pull Request on GitHub.

---

### Part 3: Introducing DVC for Data Management

6. Install DVC:
   ```bash
   pip install dvc
   ```

7. Initialize DVC:
   ```bash
   dvc init
   ```

8. Add remote storage (local):
   ```bash
   mkdir ../dvc-remote
   dvc remote add -d myremote ../dvc-remote
   git add .dvc/config .dvc/.gitignore
   git commit -m "Configure DVC remote storage"
   git push origin main
   ```

9. Track a dataset:
   Create `data/sample_data.csv` with:
   ```csv
   id,value
   1,10
   2,20
   3,30
   ```

   Then:
   ```bash
   dvc add data/sample_data.csv
   git add data/sample_data.csv.dvc .dvc/.gitignore
   git commit -m "Track sample dataset with DVC"
   git push origin main
   dvc push
   ```

10. Update the dataset:
    ```csv
    id,value
    1,10
    2,20
    3,30
    4,40
    ```

    Then:
    ```bash
    dvc add data/sample_data.csv
    git add data/sample_data.csv.dvc
    git commit -m "Update sample dataset with new entry"
    git push origin main
    dvc push
    ```

---

### Part 4: Collaboration with Git and DVC

11. Simulate a collaborator:
    ```bash
    git clone https://github.com/tmatin100/github-dvc-practice.git collaborator
    cd collaborator
    git pull origin main
    dvc pull
    ```

    Modify `analysis.py`:
    ```python
    import pandas as pd

    def sum_values():
        df = pd.read_csv('data/sample_data.csv')
        return df['value'].sum()

    print(f"Sum of values: {sum_values()}")
    ```

    Install pandas:
    ```bash
    pip install pandas
    ```

    Commit and push:
    ```bash
    git add analysis.py
    git commit -m "Add sum_values function to analysis script"
    git push origin main
    ```

12. Pull changes in the original repo:
    ```bash
    git pull origin main
    dvc pull
    python analysis.py
    ```

---

## License

This project is for educational purposes only.
