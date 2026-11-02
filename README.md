# lambda-cicd-basic

The smallest possible CI/CD-deployed AWS Lambda. Pushing to `main` makes
GitHub Actions run `sam build` + `sam deploy`, which creates (or updates) the
Lambda function and its execution role through CloudFormation. Nothing is
created by hand in AWS.

```
src/app.py                    the Lambda handler
template.yaml                 SAM template: one function
.github/workflows/deploy.yml  build + deploy on push to main
```

## One-time setup (the only manual AWS step)

GitHub needs a role it can assume via OIDC. Create it once:

1. IAM -> Identity providers -> add `token.actions.githubusercontent.com`
   (audience `sts.amazonaws.com`) if your account doesn't have it yet.
2. Create an IAM role with this trust policy (replace `<ACCOUNT_ID>`):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"},
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
      "StringLike":   {"token.actions.githubusercontent.com:sub": "repo:RRavala/lambda-cicd-basic:ref:refs/heads/main"}
    }
  }]
}
```

3. Give the role permission to deploy the stack (broad enough for a learning
   account; tighten later): `AWSCloudFormationFullAccess`, `AWSLambda_FullAccess`,
   `IAMFullAccess`, and `AmazonS3FullAccess` (SAM's artifact bucket).
4. In the GitHub repo: Settings -> Secrets and variables -> Actions -> new
   secret `AWS_DEPLOY_ROLE_ARN` = the role's ARN.

(You can reuse the role from `lambda-cicd-demo` by adding this repo's `sub`
line to its trust policy.)

## Deploy

```bash
git init -b main
git add . && git commit -m "Initial commit"
git remote add origin git@github.com:RRavala/lambda-cicd-basic.git
git push -u origin main      # triggers the deploy
```

Watch the run in the Actions tab; then check the `lambda-cicd-basic` stack in
CloudFormation and invoke the function from the Lambda console.

Region and stack name are set at the top of `deploy.yml`.
