import marimo as mo

app = mo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    return mo.md("# Hello from WASM", "If you see this, WASM is working ✅")

if __name__ == "__main__":
    app.run()
