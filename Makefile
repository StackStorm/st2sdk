.PHONY: compile
compile:
	@echo "======================= compile ========================"
	@echo "------- Compile all .py files (syntax check test) ------"
	@if python -c 'import compileall,re; compileall.compile_dir(".", rx=re.compile(r"/virtualenv|.tox"), quiet=True)' | grep .; then exit 1; else exit 0; fi
	find . -name \*.pyc -type f -not -path "./build/*" -print0 | xargs -0 -I {} rm {}
