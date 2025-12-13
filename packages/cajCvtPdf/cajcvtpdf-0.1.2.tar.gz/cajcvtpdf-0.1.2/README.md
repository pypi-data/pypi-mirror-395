# cajCvtPdf

A thin Python wrapper that ships the original `caj2pdf.exe` binary so it can be installed from PyPI and invoked as `caj2pdf`.

## Usage

```bash
caj2pdf convert input.caj -o output.pdf -m MUTOOL
```

The command simply delegates to the bundled `caj2pdf.exe` located under `cajCvtPdf/bin`.
