command:
		cat Makefile

jupyter:
		jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser

lab:
		jupyter-lab --ip='*' --NotebookApp.token='' --NotebookApp.password='' --no-browser
