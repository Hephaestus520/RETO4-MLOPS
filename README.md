# GCP

## Crear un nuevo proyecto (opcional)
gcloud projects create donostia-parking-mlops

## Seleccionar el proyecto
gcloud config set project donostia-parking-ml

## Habilitar servicios requeridos
gcloud services enable storage.googleapis.com 
gcloud service bigquery.googleapis.com 
gcloud service cloudfunctions.googleapis.com 
gcloud service pubsub.googleapis.com 
gcloud service cloudbuild.googleapis.com 
gcloud service artifactregistry.googleapis.com

Algunos servicios necesitan activar el billing information entonces son mas faciles desde el dashboard 
solo se hace una vez la activacion de facturacion

## Crear el bucket donde se subirán los CSV
gsutil mb -l us-central1 gs://donostia-parking-data/
