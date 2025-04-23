# Survey_2024
Analysis of 2024 Survey Results

GloBIAS working group 'Survey24'

Check out www.globias.org

## Installation

This package uses Pixi to manage package installation.
Please download and install Pixi from [here](https://pixi.sh/latest/#installation).


## Usage

After Installation, use Jupyter Lab to render and run the analysis of the different notebooks.
You should first change directory by using `cd` in the command line

```
cd path/to/repository/Survey_2024
```

and then executing the following command

```
pixi run jupyter lab
```

This will open Jupyter Lab in your default browser (after installing the necessary packages if not previously installed).

## Repository organization

- `data/`: data results from the survey. Feel free to add new files to this folder if needed (in case you process a table, for example), but be mindful when removing or modifying files there.

- `notebooks/`: Jupyter notebooks that process the data.

- `figures/`: Results from notebooks saved as image files.

- `scratch/`: Jupyter notebooks that are more exploratory, or not focused in answering a question.

## Tips to contribute

- Install requirements by installing Pixi as described in [Installation](#installation) and running `pixi install` from within the directory

- Notebooks can load data using `df = pd.read_csv("../data/survey2024.csv")`

- Figures can be saved by running `plt.savefig("../figures/FigureName.png", bbox_inches='tight')`

- Large bits of code, or code that can be reused should be added to `notebooks/utils.py`

- You can run `python scratch/generate_figures_readme.py ` to automatically update the file `figures/README.md` with all the images in the directory