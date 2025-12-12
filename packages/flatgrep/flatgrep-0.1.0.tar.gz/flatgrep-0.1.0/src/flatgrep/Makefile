APP_NAME = flatgrep
ENTRY = main.py

.PHONY: build run clean install reinstall

# Gera o binário usando PyInstaller
build:
	pyinstaller --onefile --name $(APP_NAME) $(ENTRY)

# Executa o binário já compilado
run: build
	./dist/$(APP_NAME)

# Remove arquivos de build/ e dist/
clean:
	rm -rf build dist *.spec __pycache__ */__pycache__

# Move o binário para ~/.local/bin (precisa estar no PATH)
install: build
	mkdir -p ~/.local/bin
	cp dist/$(APP_NAME) ~/.local/bin/

# Limpa e recompila do zero
reinstall: clean build install

