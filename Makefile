venv_script = .venv/bin/activate

requirements.txt: infrastructure/requirements.txt runtime/requirements.txt

$(venv_script): requirements.txt
	python -m venv .venv
	source $(venv_script) \
		&& pip install -r requirements.txt

venv: $(venv_script)

build: venv
	source $(venv_script) && cd infrastructure && cdk synth

deploy: venv
	source $(venv_script) && cdk bootstrap && cdk deploy

destroy: venv
	source $(venv_script) && cdk bootstrap && cdk destroy

tests:
	cd runtime/tests/dynamodb && docker-compose up --detach
	source $(venv_script) && cd runtime/tests \
		&& python -m unittest libtest \
		&& python -m unittest apptest.app_test
	cd runtime/tests/dynamodb && docker-compose down

run_local:
	cd runtime/tests/dynamodb && docker-compose up --detach
	source $(venv_script) && cd runtime/tests \
		&& python -m libtest.common
	source $(venv_script) && cd runtime \
		&& export ENDPOINT="http://localhost:4566" \
		&& chalice local
	cd runtime/tests/dynamodb && docker-compose down

