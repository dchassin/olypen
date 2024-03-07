import marimo

__generated_with = "0.3.1"
app = marimo.App()


@app.cell
def __(mo, op):
    table = mo.ui.dropdown(options=op.directory,label="Table:")
    table
    return table,


@app.cell
def __(mo, op, table):
    mo.ui.table(op[table.value] if table.value else None,page_size=12)

    return


@app.cell
def __():
    import marimo as mo
    import olypen
    op = olypen.Olypen()
    return mo, olypen, op


if __name__ == "__main__":
    app.run()
