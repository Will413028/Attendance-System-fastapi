# Attendance-System-fastapi

## Demo Link

https://attendance-system-frontend-5raarijksa-de.a.run.app/


## Features
- ### Database: using MySQL
- ### Authentication: using jsonwebtoken
- ### Testing: unit tests using pytest
- ### CI/CD: using GitHub Action and GCP


## API Endpoints
List of available routes:

**Auth routes**:\
`POST /login` - login

**User routes**:\
`GET /users` - get all users\
`PUT /users/:id` - update user

**Attendance routes**:\
`GET /attendances` - get all attendance\
`POST /attendances` - create an attendance\
`PUT /attendances/:id` - update attendance\
`GET /attendanceQRcode` - get attendance QRcode

**Holiday routes**:\
`POST /holidays` - create holiday\
`GET /holidays` - get all holiday


## How to run:

Run server

```
uvicorn main:app --reload
```

Docker build
```
sudo docker build -t <image_name>:<tag> .
```

Docker run

```
docker run --name test -p 8000:8000 test
```
Run test
```
python -m pytest
```

Auto generate migration
```
alembic revision --autogenerate -m "migration message"
```

Do migration
```
alembic upgrade head
```

docker compose
```
sudo docker-compose up -d --build 
```



### Use GitHub Actions Workflow for Google cloud run tutorial
1. create a new project on the Google Cloud Platform.

2. Take a note of the Project ID, in this example fastapi-test-143023.

3. If you don't have gcloud, follow the officai doc to install, https://cloud.google.com/sdk/docs/install

4. Set temporary variables in terminal session
```
export GITHUB_REPO=<YOUR_GITHUB_REPO> (e.g. user/project check your github repo)
export PROJECT_ID=<YOUR_PROJECT_ID> (from your google cloud plateform)
export SERVICE_ACCOUNT=<NAME_OF_SERVICE_ACCOUNT> (use your own)
export WORKLOAD_IDENTITY_POOL=<WORKLOAD_IDENTITY_POOL_NAME> (use your own)
export WORKLOAD_IDENTITY_PROVIDER=<WORKLOAD_IDENTITY_PROVIDER> (use your own)
```
5. using the gcloud command, set the project
```
gcloud config set project $PROJECT_ID
```

6. Enable the APIs for Artifact Registry, IAM Credential, Container Registry and Cloud Run:
```
gcloud services enable \
   artifactregistry.googleapis.com \
   iamcredentials.googleapis.com \
   containerregistry.googleapis.com \
   run.googleapis.com
```

7. Create a Service Account that will be used by GitHub Actions:
```
gcloud iam service-accounts create $SERVICE_ACCOUNT \
   --display-name="GitHub Actions Service Account"
```

8. Bind the Service Account to the Roles in the Services it must interact:
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
   --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
   --role="roles/run.developer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
   --role="roles/storage.admin"
```

9. Create a Workload Identity Pool for GitHub:
```
gcloud iam workload-identity-pools create $WORKLOAD_IDENTITY_POOL \
   --location="global" \
   --display-name="GitHub Workload Identity Pool"
```

10. Create a Workload Identity Provider for GitHub:
```
gcloud iam workload-identity-pools providers create-oidc $WORKLOAD_IDENTITY_PROVIDER \
   --location="global" \
   --workload-identity-pool=$WORKLOAD_IDENTITY_POOL \
   --display-name="GitHub provider" \
   --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
   --issuer-uri="https://token.actions.githubusercontent.com"
```

11. Retrieve the Workload Identity Pool ID:
```
WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools \
   describe $WORKLOAD_IDENTITY_POOL \
   --location="global" \
   --format="value(name)")
```

12. Allow authentications from the Workload Identity Provider originating from your repository:

```
gcloud iam service-accounts add-iam-policy-binding \
   $SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
   --role="roles/iam.workloadIdentityUser" \
   --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}"
```

13. Finally, extract the Workload Identity Provider resource name:
```
WORKLOAD_IDENTITY_PROVIDER_LOCATION=$(gcloud iam workload-identity-pools providers \
   describe $WORKLOAD_IDENTITY_PROVIDER \
   --location="global" \
   --workload-identity-pool=$WORKLOAD_IDENTITY_POOL \
   --format="value(name)")
```

14. Create a GitHub Actions Workflow, example in .github/workflows

15. check the some variables, and add them to github action secrets
```
echo $WORKLOAD_IDENTITY_PROVIDER_LOCATION

echo $SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

```