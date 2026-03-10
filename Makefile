.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log paper/paper.out paper/paper.toc

# ----------------------------
# Task 2: Dependency graph Qs
# ----------------------------
# 1) If I edit code/preprocess.py:
#    Rebuild: output/figures/figure_5_2.png and output/figures/figure_5_3.png,
#             then paper/paper.pdf.
#    Skip:    output/tables/did_table.tex.
#
# 2) If I edit code/did_analysis.py:
#    Rebuild: output/tables/did_table.tex,
#             then paper/paper.pdf.
#    Skip:    output/figures/figure_5_2.png and output/figures/figure_5_3.png.
#
# 3) If I edit paper/paper.tex:
#    Rebuild: paper/paper.pdf only.
#    Skip:    output/figures/figure_5_2.png,
#             output/figures/figure_5_3.png,
#             output/tables/did_table.tex.