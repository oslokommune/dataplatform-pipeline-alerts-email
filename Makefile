 ifeq (, $(shell which pipenv))
 $(error "Pipenv not found in PATH. Install here: https://github.com/pypa/pipenv#installation")
 endif

.AWS_ROLE_NAME ?= oslokommune/iamadmin-SAML

.DEV_PROFILE := saml-origo-dev
.PROD_PROFILE := saml-dataplatform-prod

GLOBAL_PY := python3.8

get-gopass-secret = $(or $(shell gopass show $(1)), $(error gopass command failed))

.PHONY: init
init: node_modules pipenv

node_modules: package.json package-lock.json
	npm install

pipenv:
	pipenv install --dev

.PHONY: format
format: pipenv
	pipenv run format

.PHONY: format-diff
format-diff: pipenv
	pipenv run format-diff

-PHONY: lint
lint:
	pipenv run lint

.PHONY: test
test: pipenv
	pipenv run flake8
	pipenv run format-diff
	pipenv run format-check
	pipenv run test

.PHONY: deploy
deploy: node_modules login-dev
	sls deploy --stage $${STAGE:-dev} --aws-profile $(.DEV_PROFILE)

.PHONY: deploy-prod
deploy-prod: node_modules is-git-clean test login-prod
	sls deploy --stage prod --aws-profile $(.PROD_PROFILE)

ifeq ($(MAKECMDGOALS),undeploy)
ifndef STAGE
$(error STAGE is not set)
endif
ifeq ($(STAGE),dev)
$(error Please do not undeploy dev)
endif
endif
.PHONY: undeploy
undeploy: login-dev
	$(eval .DEV_ACCOUNT := $(call get-gopass-secret, dataplatform/aws/account-id-dev))
	$(eval .DEV_ROLE := 'arn:aws:iam::$(.DEV_ACCOUNT):role/$(.AWS_ROLE_NAME)')
	sls remove --stage $(STAGE) --aws-profile $(.DEV_PROFILE)

.PHONY: login-dev
login-dev:
	$(eval .DEV_ACCOUNT := $(call get-gopass-secret, dataplatform/aws/account-id-dev))
	$(eval .DEV_ROLE := 'arn:aws:iam::$(.DEV_ACCOUNT):role/$(.AWS_ROLE_NAME)')
	saml2aws login --role=$(.DEV_ROLE) --profile=$(.DEV_PROFILE)

.PHONY: login-prod
login-prod:
	$(eval .PROD_ACCOUNT := $(call get-gopass-secret, dataplatform/aws/account-id-prod))
	$(eval .PROD_ROLE := 'arn:aws:iam::$(.PROD_ACCOUNT):role/$(.AWS_ROLE_NAME)')
	saml2aws login --role=$(.PROD_ROLE) --profile=$(.PROD_PROFILE)

.PHONY: is-git-clean
is-git-clean:
	@status=$$(git fetch origin && git status -s -b) ;\
	if test "$${status}" != "## master...origin/master"; then \
		echo; \
		echo Git working directory is dirty, aborting >&2; \
		false; \
	fi