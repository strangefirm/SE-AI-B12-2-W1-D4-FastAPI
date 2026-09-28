"""Simple calculator API built with FastAPI, with a small web page at '/'."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Simple Calculator", description="Add, subtract, multiply and divide two numbers.")


def result_of(a: float, b: float, operation: str, result: float) -> dict:
    return {"a": a, "b": b, "operation": operation, "result": result}


@app.get("/add")
def add(a: float, b: float):
    return result_of(a, b, "add", a + b)


@app.get("/subtract")
def subtract(a: float, b: float):
    return result_of(a, b, "subtract", a - b)


@app.get("/multiply")
def multiply(a: float, b: float):
    return result_of(a, b, "multiply", a * b)


@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return result_of(a, b, "divide", a / b)


PAGE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Simple Calculator</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f2f4f7; display: flex;
           justify-content: center; padding-top: 60px; }
    .card { background: #fff; padding: 28px; border-radius: 12px; width: 320px;
            box-shadow: 0 4px 16px rgba(0,0,0,.1); }
    h2 { margin-top: 0; text-align: center; }
    input, select, button { width: 100%; padding: 10px; margin: 8px 0; font-size: 16px;
                            box-sizing: border-box; border: 1px solid #ccc; border-radius: 6px; }
    button { background: #146b55; color: #fff; border: none; cursor: pointer; }
    button:hover { background: #0f5443; }
    #result { margin-top: 14px; text-align: center; font-size: 20px; font-weight: bold; }
    .error { color: #c0392b; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Calculator</h2>
    <input id="a" type="number" step="any" placeholder="First number">
    <select id="op">
      <option value="add">+ Add</option>
      <option value="subtract">- Subtract</option>
      <option value="multiply">&times; Multiply</option>
      <option value="divide">&divide; Divide</option>
    </select>
    <input id="b" type="number" step="any" placeholder="Second number">
    <button onclick="calculate()">Calculate</button>
    <div id="result"></div>
  </div>

  <script>
    async function calculate() {
      const a = document.getElementById("a").value;
      const b = document.getElementById("b").value;
      const op = document.getElementById("op").value;
      const out = document.getElementById("result");
      if (a === "" || b === "") { out.className = "error"; out.textContent = "Enter both numbers"; return; }
      const response = await fetch(`/${op}?a=${a}&b=${b}`);
      const data = await response.json();
      if (response.ok) { out.className = ""; out.textContent = "Result: " + data.result; }
      else { out.className = "error"; out.textContent = data.detail; }
    }
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE