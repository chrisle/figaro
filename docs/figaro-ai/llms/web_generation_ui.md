# Figaro: Web Generation UI

## Global Variables

```py
chain = figaro_ai(
  template="Complete this sentence: Mirror mirror on the wall",
  verbose=True,
  web_generation_ui_url="http://localhost:5000",
)
```
|                         |           |                                                    |
| ----------------------- | --------- | -------------------------------------------------- |
| `template`              | `str`     | Jinja prompt template.                             |
| `web_generation_ui_url` | `str`     | Web Generation UI base URL                         |
| `verbose`               | `bool`    | (Optional) Enable verbose (default=`False`)        |
| `level`                 | `logging` | (Optional) Enable verbose (default=`logging.INFO`) |

## Template Usage

```j2
{% gen webgenui "result" temperature=0 %}
```

|                            |             |                                                                                 |
| -------------------------- | ----------- | ------------------------------------------------------------------------------- |
| `add_bos_token`            | `bool`      | (Optional) (default=`True`)                                                     |
| `ban_eos_token`            | `bool`      | (Optional) (default=`False`)                                                    |
| `do_sample`                | `bool`      | (Optional) (default=`True`)                                                     |
| `early_stopping`           | `bool`      | (Optional) (default=`False`)                                                    |
| `epsilon_cutoff`           | `int`       | (Optional) In units of 1e-4 (default=`0`)                                       |
| `eta_cutoff`               | `int`       | (Optional) In units of 1e-4 (default=`0`)                                       |
| `length_penalty`           | `int`       | (Optional) (default=`1`)                                                        |
| `max_new_tokens`           | `int`       | (Optional) Max new tokens (default=`2048`)                                      |
| `min_length`               | `int`       | (Optional) (default=`0`)                                                        |
| `mirostat_eta`             | `int`       | (Optional) (default=`0.1`)                                                      |
| `mirostat_mode`            | `int`       | (Optional) (default=`0`)                                                        |
| `mirostat_tau`             | `int`       | (Optional) (default=`5`)                                                        |
| `no_repeat_ngram_size`     | `int`       | (Optional) (default=`0`)                                                        |
| `num_beams`                | `int`       | (Optional) (default=`1`)                                                        |
| `penalty_alpha`            | `int`       | (Optional) (default=`0`)                                                        |
| `preset`                   | `str`       | (Optional) Use preset. If used, all other options are ignored. (default=`None`) |
| `repetition_penalty_range` | `int`       | (Optional) (default=`0`)                                                        |
| `repetition_penalty`       | `int`       | (Optional) (default=`1.18`)                                                     |
| `seed`                     | `int`       | (Optional) (default=`-1`)                                                       |
| `skip_special_tokens`      | `bool`      | (Optional) (default=`True`)                                                     |
| `stopping_strings`         | `list[str]` | (Optional) (default=`[])`                                                       |
| `temperature`              | `int`       | (Optional) (default=`0.7`)                                                      |
| `tfs`                      | `int`       | (Optional) (default=`1`)                                                        |
| `top_a`                    | `int`       | (Optional) (default=`0`)                                                        |
| `top_k`                    | `int`       | (Optional) (default=`40`)                                                       |
| `top_p`                    | `int`       | (Optional) (default=`0.1`)                                                      |
| `truncation_length`        | `int`       | (Optional) (default=`2048`)                                                     |
| `typical_p`                | `int`       | (Optional) (default=`1`)                                                        |
