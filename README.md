# Survey_2024
Analysis of 2024 Survey Results

GloBIAS working group 'Survey24'

Check out www.globias.org

## Repository organization

- `data/`: data results from the survey. Feel free to add new files to this folder if needed (in case you process a table, for example), but be mindful when removing or modifying files there.

- `notebooks/`: Jupyter notebooks that process the data.

- `figures/`: Results from notebooks saved as image files.

- `scratch/`: Juopyter notebooks that are more exploratory, or not focused in answering a question.

## Tips to contribute

- Install requirements by running `pip install -r requirements.txt`

- Notebooks can load data using `df = pd.read_csv("../data/survey2024.csv")`

- Figures can be saved by running `plt.savefig("../figures/FigureName.png", bbox_inches='tight')`

- Large bits of code, or code that can be reused should be added to `notebooks/utils.py`