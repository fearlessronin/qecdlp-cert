test:
	python -m pytest -q

layout:
	find . -maxdepth 3 -type f | sort

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find paper -type f \( -name "*.aux" -o -name "*.bbl" -o -name "*.blg" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.synctex.gz" \) -delete
