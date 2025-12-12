docs_serve:
	uv run --group docs mkdocs serve --strict

docs_build:
	uv run --group docs mkdocs build --strict

docs: docs_build
	rm -rf public/ && \
	mkdir -p public/ && \
	cp -r build/mkdocs/* public/
