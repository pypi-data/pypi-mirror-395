all: build publish

run:
	uv run exe-analyzer

build:
	uv build

publish:
	uv publish

test:
	npx @modelcontextprotocol/inspector uv run python main.py