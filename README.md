# Python Markdown Extension: csv2md

See: https://pypi.org/project/mdtable/

## Settings

| Setting | Default | Description |
| --- | --- | --- |
| base_path | `'.'` | Base path from where relative paths are calculated. |
| padding | `1` | Padding to use in raw formatted markdown table. |
| delimiter | `','` | Delimiter character in CSV file. |
| quotechar | `'"'` | Quote character in CSV file. |
| escapechar | `''` | Escape character in CSV file. |

## Example Input

```
[caption](./path/to/my/file.csv)
```

## Example Output (markdown)

```
|Code              |Prompt                           |Type     |Required|
|------------------|---------------------------------|---------|--------|
|question_type     |Question Type                    |select   |Yes     |
|                  |facet                            |         |No      |
|                  |value                            |         |No      |
|                  |hybrid                           |         |No      |
|facet_field       |Facet Field                      |text     |No      |
|keyword           |Keyword (over heading)           |text     |No      |
|short_description |Short Description (under heading)|memo     |No      |
|long_description  |Long Description (in popup)      |memo     |No      |
|load_answer_images|Load Answer Images               |checkbox |No      |
|disable_when_true |Disable When True                |multitext|No      |
```
