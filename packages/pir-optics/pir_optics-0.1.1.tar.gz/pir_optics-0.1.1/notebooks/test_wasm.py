import marimo as mo

app = mo.App()

@app.cell
def _():
    import marimo as mo
    return mo

@app.cell
def _(mo):
    return mo.md("Hello from WASM")
