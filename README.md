# dataplatform-pipeline-alerts-email
Sends alerts about failing pipelines as an email.


## Requirements
This project uses [Pipenv](https://github.com/pypa/pipenv) and
the [Serverless Framework](https://www.serverless.com/) to run, test,
and deploy the application.
It also requires [gopass](https://github.com/gopasspw/gopass) to be configured
with the secrets for dataplatform.  

See how to configure gopass for Team Dataplatform
[here](https://github.oslo.kommune.no/origo-dataplatform/dataplatform-gopass-secrets)

## Development
There are various GNU Make commands to make this easier  

##### Format using black
`make format`
##### Show format diff using black
`make format-diff`  
##### Lint using flake8
`make lint`
##### Test
`make test`  
##### Deploy to dev
`make deploy`  
##### Deploy to prod
`make deploy-prod`  