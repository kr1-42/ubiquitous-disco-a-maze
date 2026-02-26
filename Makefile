# Makefile per a_maze_ing.py
# @author: chrilomb, ...?

#@param NAME: nome del main script da eseguire
NAME=a_maze_ing.py
#@param FIG: path del file base di configurazione da passare al main script
FIG=config.txt

#@description: esegue il main script con il file di configurazione specificato
	# se viene messo un file di configurazione $(FIG)
	# nella root della repo lo esegue
	# altrimenti esegue con il file di configurazione di default
run:
	@echo "Running $(NAME) with configuration file: $(FIG)"
	@if [ -f $(FIG) ]; then \
		python3 $(NAME) $(FIG); \
	else \
		python3 $(NAME) configs/$(FIG); \
	fi

#@description: esegue il main script con il file di configurazione specificato in modalità debug
	# se viene messo un file di configurazione $(FIG)
	# nella root della repo lo esegue
	# altrimenti esegue con il file di configurazione di default
debug:
	if [ -f $(FIG) ]; then \
		python3 -m pdb $(NAME) $(FIG); \
	else \
		python3 -m pdb $(NAME) configs/$(FIG); \
	fi

#@description: esegue i test con 10 esempi di configurazione
NUMBERS=0 1 2 3 4 5 6 7 8 9
test:
		$(foreach num, $(NUMBERS), python3 $(NAME) configs/config$(num).txt;)

#@description: esegue la norma di codice con flake8 e mypy 
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

#@description: esegue la norma di codice con flake8 e mypy in modalità strict
lint-strict:
	flake8 .
	mypy . --strict

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf src/__pycache__ src/.mypy_cache src/.pytest_cache

