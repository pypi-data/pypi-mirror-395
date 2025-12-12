# Inline SVG Extension for Markdown

A Python-Markdown extension that enables **inline embedding of local SVG 
files** directly into rendered HTML. Unlike standard Markdown image 
syntax—which outputs `<img>` tags. This extension inserts the **actual SVG 
markup**, enabling:

 - full CSS styling of embedded SVGs  
 - consistent scaling behaviour  
 - figure + caption support  
 - improved control over accessibility and semantics

## Features

### Inline SVG injection

Embed SVG files using a syntax similar to normal images:

```markdown
![caption](path/to/image.svg)
```

or without caption:

```markdown
!(path/to/image.svg)
```

### Automatic `<figure>` + `<figcaption>` wrapping

If a caption is provided, the output becomes:

```html
<figure>
    <svg> ... </svg>
    <figcaption>Your caption</figcaption>
</figure>
```

Without a caption, only the SVG element is inserted.

### Safe placeholder handling

The extension first inserts placeholder tokens, preventing Python-Markdown from 
escaping the SVG. Placeholders are later replaced with the final SVG markup in 
the postprocessor phase.

### Internal caching

SVG files are parsed once and stored in a global cache for the lifetime of the 
process, improving performance.

## Installation

```bash
pip install markdown isvg
```

Use the extension:

```python
import markdown
from isvg import InlineSVGExtension

md = markdown.Markdown(extensions=[InlineSVGExtension(root="assets/svg")])
html = md.convert("![Logo](logo.svg)")
```

## Usage

### Basic Inline SVG

```markdown
!(diagram.svg)
```

### Inline SVG with Caption

```markdown
![Data Flow](images/flow.svg)
```

### Example HTML Output

```html
<figure>
  <svg xmlns="http://www.w3.org/2000/svg" ...> ... </svg>
  <figcaption>Data Flow</figcaption>
</figure>
```

## Configuration

### `root` (default: `"./"`)

Defines the base directory from which SVG paths are resolved.

```python
InlineSVGExtension(root="/var/www/assets/svg")
```

A Markdown reference such as:

```markdown
![icon](ui/menu.svg)
```

resolves to:

```text
/var/www/assets/svg/ui/menu.svg
```

## How it Works

 1. **Regex detection**
    Matches `![caption](file.svg)` or `!(file.svg)`.
 2. **Path resolution**
    Relative paths are resolved using the configured root.
 3. **SVG parsing & caching**
    Files are parsed with `xml.etree.ElementTree`.
    Parsed SVGs are cached globally in `_CACHE`.
 4. **Placeholder insertion**
    A placeholder token like `\x02/path/to/file.svg\x03` is inserted instead of 
    the SVG.
 5. **Postprocessing**
    Placeholders are replaced with raw SVG markup in the final HTML output.

## Error Handling

The extension silently ignores:

 * Non-SVG files
 * Remote URLs (`http://`, `https://`, `//`)
 * Missing paths
 * Invalid or malformed SVGs

In such cases, the original Markdown text is left unchanged.

## Security Considerations

Inlining SVGs introduces risks if files are not trusted. SVGs can contain:

 - JavaScript
 - External resource references
 - Embedded HTML
 - CSS injections

If processing user-provided content, sanitize SVGs beforehand using tools 
such as: external SVG sanitizers or whitelist-based filtering.

## Known Limitations

 - A global cache is used, which persists for the lifetime of the process.
 - Relative links inside SVGs are not rewritten.
 - Captions are treated as plain text; no Markdown is rendered inside captions.
 - Interactions with other Markdown extensions may affect final output order.

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3).
You may redistribute and/or modify it under the terms of the GPLv3.
