# GCP

## Crear un nuevo proyecto (opcional)
gcloud projects create parking-mlops

## Seleccionar el proyecto
gcloud config set project parking-ml

## Habilitar servicios requeridos
gcloud services enable storage.googleapis.com \
gcloud service bigquery.googleapis.com \
gcloud service cloudfunctions.googleapis.com \
gcloud service pubsub.googleapis.com \
gcloud service cloudbuild.googleapis.com \
gcloud service artifactregistry.googleapis.com

Algunos servicios necesitan activar el billing information entonces son mas faciles desde el dashboard 
solo se hace una vez la activacion de facturacion

## Crear el bucket donde se subirán los CSV
gsutil mb -l us-central1 gs://donostia-parking-data/

## Crear la cuenta de servicio
gcloud iam service-accounts create github-data-uploader --display-name="GitHub Data Uploader"

### Asignar permisos necesarios
gcloud projects add-iam-policy-binding parking-mlops --member="serviceAccount:github-data-uploader@parking-mlops.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding parking-mlops --member="serviceAccount:github-data-uploader@parking-mlops.iam.gserviceaccount.com" --role="roles/bigquery.dataEditor"


## Generar clave JSON local
gcloud iam service-accounts keys create github-key.json --iam-account=github-data-uploader@parking-mlops.iam.gserviceaccount.com

Luego:

Abre tu repositorio en GitHub.

Ve a Settings → Secrets → Actions → New repository secret.

Crea un secreto llamado GCP_CREDENTIALS.

Pega el contenido del archivo github-key.json.

## Crear workload identity pool
gcloud iam workload-identity-pools create "github-pool" --project="parking-mlops" --location="global" --display-name="GitHub Actions Pool"

### Obtén el ID del pool:

gcloud iam workload-identity-pools describe "github-pool"  --project="parking-mlops" --location="global" --format="value(name)"

### Provider para github

gcloud iam workload-identity-pools providers create-oidc "github-provider" --project="parking-mlops" --location="global" --workload-identity-pool="github-pool" --display-name="GitHub Provider"   --issuer-uri="https://token.actions.githubusercontent.com" --attribute-mapping="google.subject=assertion.sub"

este comando tiene un error entonces se hizo en la consola de gcp hay que agregarle una condicion que sea assertion.repository="<Nombre de usuario>/<RETO4-MLOPS>"

### dar acceso al providar a la service account

gcloud iam service-accounts add-iam-policy-binding github-data-uploader@parking-mlops.iam.gserviceaccount.com --project="parking-mlops" --role="roles/iam.workloadIdentityUser" --member="principalSet://iam.googleapis.com/projects/6182528745/locations/global/workloadIdentityPools/github-pool/attribute.repository/Hephaestus520/RETO4-MLOPS"
