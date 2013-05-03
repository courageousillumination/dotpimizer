clean:
	rm -f *.dot *.png *.ps *.pyc

show:
	dot -Tpdf init.dot -o init.pdf
	dot -Tpdf final.dot -o final.pdf
