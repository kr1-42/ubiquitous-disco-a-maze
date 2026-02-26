NAME=a_maze_ing.py
FIG=configs/config.txt

run:
	python3 $(NAME) $(FIG)

debug:
	python3 -m pdb $(NAME) $(FIG)


lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
