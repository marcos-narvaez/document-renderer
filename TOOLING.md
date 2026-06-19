# Document Renderer Tooling

Read this file before using or describing the local infrastructure tools in this
repository.

## Document Renderer

Use `document-renderer` for formal PDF reports.

Workflow:

1. Write the report as clean Markdown in the relevant project folder.
2. Save standalone JPEG, PNG, or PDF images beside the Markdown file and
   reference them with standard Markdown image syntax.
3. Run:

   ```bash
   document-renderer "/path/to/report.md"
   ```

4. Confirm that the PDF was generated beside the Markdown source.
5. Return the Markdown and PDF paths.

Behavior:

- A successful build keeps the PDF and deletes the intermediate `.tex`.
- Use `--keep-tex` only when LaTeX source is explicitly needed.
- Use `--no-compile` only when `.tex` output without a PDF is explicitly needed.
- Use `-o` only when a different output directory is explicitly requested.
- If compilation fails, the renderer retains the `.tex` file for debugging.
- Quote paths because filenames may contain spaces, apostrophes, or em dashes.

Do not generate raw LaTeX unless explicitly requested or the renderer cannot
support the document.
