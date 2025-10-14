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
