
build:
    python setup.py bdist_wheel

clean:
    rm -rf build dist *.egg-info

install:
    python setup.py install


upload:
    twine upload dist/*

build_upload:
    make build
    make upload
    