TEST_HTML=js-ipuz-player/test.html

all: $(TEST_HTML)

%.ipuz: %.xd
	./xd2ipuz.py $< > $@

js-ipuz-player/%.html: %.ipuz
	js-ipuz-player/generate-html.py $< > $@

clean:
	rm $(TEST_HTML) *.ipuz

.PRECIOUS: .ipuz
