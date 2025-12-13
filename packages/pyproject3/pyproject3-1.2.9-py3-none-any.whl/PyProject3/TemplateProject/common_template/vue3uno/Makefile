install:
	cnpm install

dev:
	npm run dev

build:
	npm run build

preview:
	npm run preview

clean:
	rm -rf dist

ls_pyproject_vue3uno:
# 列出vue3项目代码
	ls -l ../py-project/PyProject3/TemplateProject/common_template/vue3uno

rsync:
# 1. 同步代码到py-project项目
	rsync -av --exclude='node_modules' --exclude='dist' --exclude='.git' --exclude='tmp/__pycache__' --exclude='tmp' . ../py-project/PyProject3/TemplateProject/common_template/vue3uno

git_push_py_project:
	cd ../py-project/ && \
	git add . && \
	git commit -m "update vue3uno" && \
	git push

publish_to_pyproject:
# 1. 同步代码到py-project项目
# 2. 更新版本号
# 3. 构建并上传到pypi
	make rsync && \
	cd ../py-project/ && \
	/Users/jiangbin/venvs/py38_xingyun/bin/python scripts/update_version.py && \
	make clean && \
	make build_upload && \
	cd -