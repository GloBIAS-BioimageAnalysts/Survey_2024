import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas
    #import pygwalker #only when running locally, but fun!
    return mo, pandas


@app.cell
def _(pandas):
    #Uncomment lines 2 and 3 to run on GH Actions in WASM; uncomment line 4 to run locally
    import pyodide #only need for running remotely; 
    df = pandas.read_csv(pyodide.http.open_url("https://raw.githubusercontent.com/GloBIAS-BioimageAnalysts/Survey_2024/refs/heads/main/data/survey2024_headersandcommascleaned_recleaned.csv"))
    # df = pandas.read_csv("data/survey2024_headersandcommascleaned_recleaned.csv")
    df.drop(columns=["Timestamp"],inplace=True)
    return (df,)


@app.cell
def _(mo):
    mo.md("""# Welcome to the data exploration page for the GloBIAS 2024 Survey""")
    return


@app.cell
def _(mo):
    mo.md(
        """
    Please read our preprint on [arXiv](https://arxiv.org/abs/2507.06407) to learn more about GloBIAS!

    Want to play with the data yourself? Try it below!
    """
    )
    return


@app.cell
def _(mo):
    mo.md("""## Explore or transform the dataframe itself in Marimo's dataframe explorer""")
    return


@app.cell
def _(df, mo):
    dataframe= mo.ui.dataframe(df)
    dataframe
    return


@app.cell
def _():
    #'''mo.md(
    #    """
    ## Explore, transform, or graph the data in Pygwalker
    #
    #(If you're having trouble, check your aggregation and stacking settings, and try making sure "row count" is in your axes!)
    #"""
    #)''' #doesn't work in wasm
    return


@app.cell
def _():
    #pygwalker.walk(df)
    return


if __name__ == "__main__":
    app.run()
