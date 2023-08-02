# Figaro: Vertex AI

## Global Variables

```py
chain = figaro_ai(
  template="Complete this sentence: Mirror mirror on the wall",
  verbose=True,
  google_project_id="acn-agbg-ai",
  google_project_location="us-central1"
)
```
|                           |           |                                                    |
| ------------------------- | --------- | -------------------------------------------------- |
| `template`                | `str`     | Jinja prompt template.                             |
| `google_project_id`       | `str`     | Google Cloud project ID.                           |
| `google_project_location` | `str`     | Google Cloud location.                             |
| `verbose`                 | `bool`    | (Optional) Enable verbose (default=`False`)        |
| `level`                   | `logging` | (Optional) Enable verbose (default=`logging.INFO`) |

## Template Usage

```j2
{% gen vertexai "result" model="text-bison" temperature=0 max_output_tokens=1024 top_k=40 top_p=0.8 %}
```

|                     |       |                                              |
| ------------------- | ----- | -------------------------------------------- |
| `max_output_tokens` | `int` | (Optional) Max tokens (default=1024)         |
| `model`             | `str` | (Optional) Model name (default=`text-bison`) |
| `temperature`       | `int` | (Optional) Temperature (default=0.2)         |
| `top_k`             | `int` | (Optional) Top K (default=40)                |
| `top_p`             | `int` | (Optional) Top P (default=0.8)               |
