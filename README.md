#My ETL Project
1. Clone the repository:
```bash
git clone https://github.com/aguiarpaulo/data_quality_one_billion_rows.git

cd data_quality_one_billion_rows
```
2. Configure the correct Python version with pyenv:
```bash
pyenv install 3.11.3
pyenv local 3.11.3
```
3. Install project dependencies:
```bash
poetry install
```
4. Activate the virtual environment:
```bash
poetry shell
```
5. Run tests to ensure everything is working as expected:
```bash
poetry run pytest -v
```
6. Run the command to view project documentation:
```bash
mkdocs serve
```
7. Run the pipeline run command to perform ETL:
```bash
poetry run python app/etl.py
```
8. read duckdb file:
```bash
poetry run python app/read_duckdb.py
```
9. Check in the data/output folder if the file was generated correctly.
```
Contact:
Paulo Aguiar - aguiarlapaulo@gmail.com