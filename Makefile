clean:
	rm -f *.dot *.png *.pyc *.pdf

show:
	dot -Tpdf init.dot -o init.pdf
	for F in `ls | grep "dot$$" | grep mid | sed s/\.dot//`; do dot -Tpdf $$F.dot -o $$F.pdf; done
	dot -Tpdf final.dot -o final.pdf
