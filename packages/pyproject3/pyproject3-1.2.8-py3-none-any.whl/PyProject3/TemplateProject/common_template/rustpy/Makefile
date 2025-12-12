build:
	maturin develop

develop:
	maturin develop

release:
	maturin develop --release

upload:
	twine upload target/wheels/*

build_upload:
	make build
	make upload

clean:
	cargo clean