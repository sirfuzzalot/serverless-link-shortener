# Serverless Link Shortener

This service takes URLs and provides a shortened version in return. The
shortened URL can then be exchanged for the original URL.

## Setting Up The Development Environment

Once you've cloned the project run these command in the project root.

bash

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r dev.requirements.txt
```

pwsh

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r dev.requirements.txt
```

## Starting the Development Server

From within your virtual environment

```bash
uvicorn src.link_shortener.main:app --reload
```

Uvicorn will output the URL for your local service. You can add `/docs`
to the URL to get the Swagger UI docs.

To test locally against Amazon DynamoDB (after deploying once) you can update
the environment using a `.env` file. See `example.env`.

## Deploying Your Code

You will need [Node.js](https://nodejs.org/en/download/) installed. Run
these commands from the project root.

```
npm install
```

### Development Deploy

The **deploy** command will output the URL for your service.

bash

```bash
STAGE=[your stage name. ex: prod] REGION=[your AWS region. ex: us-west-2] npm run deploy
```

pwsh

```powershell
$ENV:STAGE="[your stage name. ex: prod]"; $ENV:REGION="[your AWS region. ex: us-west-2]"; npm run deploy
```

### Production Deploy

bash

```bash
DOMAIN_NAME=[your domain] STAGE=[your stage name. ex: prod] REGION=[your AWS region. ex: us-west-2] npm run deploy
```

pwsh

```powershell
$ENV:DOMAIN_NAME="[your domain]"; $ENV:STAGE="[your stage name. ex: prod]"; $ENV:REGION="[your AWS region. ex: us-west-2]"; npm run deploy
```

## Resources

- [FastAPI](https://fastapi.tiangolo.com/)
- [Mangum](https://mangum.io/)
- [Amazon DynamoDB Docs](https://docs.aws.amazon.com/dynamodb/index.html)
- [Boto3 DynamoDB Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
- [CloudFormation DynamoDB Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DynamoDB.html)
- [Serverless](https://www.serverless.com/framework/docs)
- [serverless-python-requirements](https://github.com/serverless/serverless-python-requirements)
- [serverless-api-gateway-throttling](https://github.com/DianaIonita/serverless-api-gateway-throttling)
- [serverless-plugin-log-retention](https://github.com/ArtificerEntertainment/serverless-plugin-log-retention)
- [serverless-domain-manager](https://github.com/amplify-education/serverless-domain-manager)
