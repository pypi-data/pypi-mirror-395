# PyJSX Language Support

![](example.png)

This plugin provides basic language support for [PyJSX](https://github.com/tomasr8/pyjsx).

This includes:
- __Syntax highlighting__
- __Ability to toggle comments__ (`Ctrl + /` by default)

## Extension Settings

There are currenly no settings available.

## Release Notes

### 0.0.1

* Initial release

## Technical details

The TextMate grammar is a combination of the official
[Python](https://github.com/microsoft/vscode/tree/main/extensions/python) and
[JS](https://github.com/microsoft/vscode/tree/main/extensions/javascript)
grammars.

I use the Python grammar with just a few modifications. The JSX grammar is added by extending the `expression` rule:

```json
"expression": {
    "comment": "All valid Python expressions",
    "patterns": [
        {
            "include": "#jsx"
        },
        ... more patterns
    ]
},
```

The JSX grammar is defined as an [embedded grammar](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide#embedded-languages). 

