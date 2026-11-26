# Build the manuscript

From the repository root, run the following with an existing TeX distribution.

    cd paper
    latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex

The CI workflow checks references and layout. The LaTeX file contains a self-contained bibliography, also provided as a BibTeX file. Different TeX engines and distributions can produce different PDF bytes.
