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


## Crear workload identity pool
gcloud iam workload-identity-pools create "github-pool" --project="parking-mlops" --location="global" --display-name="GitHub Actions Pool"

### Obtén el ID del pool:

gcloud iam workload-identity-pools describe "github-pool"  --project="parking-mlops" --location="global" --format="value(name)"

### Provider para github

gcloud iam workload-identity-pools providers create-oidc "github-provider" --project="parking-mlops" --location="global" --workload-identity-pool="github-pool" --display-name="GitHub Provider"   --issuer-uri="https://token.actions.githubusercontent.com" --attribute-mapping="google.subject=assertion.sub"

este comando tiene un error entonces se hizo en la consola de gcp hay que agregarle una condicion que sea assertion.repository="<Nombre de usuario>/<RETO4-MLOPS>"

### dar acceso al providar a la service account

gcloud iam service-accounts add-iam-policy-binding github-data-uploader@parking-mlops.iam.gserviceaccount.com --project="parking-mlops" --role="roles/iam.workloadIdentityUser" --member="principalSet://iam.googleapis.com/projects/6182528745/locations/global/workloadIdentityPools/github-pool/attribute.repository/Hephaestus520/RETO4-MLOPS"


### Crear cloud function

antes se debe haber creado un data set en bigquery llamado donostia_dataset
para ejecutare este comando se debe estar en la carpeta src del repositorio

gcloud projects add-iam-policy-binding parking-mlops --member="serviceAccount:service-6182528745@gs-project-accounts.iam.gserviceaccount.com" --role="roles/pubsub.publisher"

gcloud functions deploy load_to_bigquery --runtime python311 --trigger-event google.storage.object.finalize --trigger-resource donostia-parking-data --region us-central1 --entry-point load_to_bigquery


## Modelo y predicciones en bigquery

CREATE OR REPLACE MODEL `donostia_dataset.parking_forecast`
OPTIONS(
  model_type = 'linear_reg',
  input_label_cols = ['libres']
) AS
SELECT
  nombre,
  EXTRACT(HOUR FROM timestamp) AS hora,
  EXTRACT(DAYOFWEEK FROM timestamp) AS dia_semana,
  libres
FROM
  `donostia_dataset.parking_data`;

este fue el codigo para iniciar el modelo en una sentencia SQL en bigquery 

### Este es un ejemplo de una consulta para una preddiccion 

SELECT
  nombre,
  hora,
  dia_semana,
  predicted_libres
FROM
  ML.PREDICT(MODEL `donostia_dataset.parking_forecast`,
    (
      SELECT
        nombre,
        EXTRACT(HOUR FROM timestamp) AS hora,
        EXTRACT(DAYOFWEEK FROM timestamp) AS dia_semana
      FROM
        `donostia_dataset.parking_data`
      WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
    )
  );

### Creacion de tabla de predicciones en bigquery

CREATE OR REPLACE TABLE `donostia_dataset.parking_predictions` AS
SELECT
  nombre,
  hora,
  dia_semana,
  predicted_libres,
  CURRENT_TIMESTAMP() AS generated_at
FROM
  ML.PREDICT(MODEL `donostia_dataset.parking_forecast`,
    (
      SELECT
        nombre,
        EXTRACT(HOUR FROM timestamp) AS hora,
        EXTRACT(DAYOFWEEK FROM timestamp) AS dia_semana
      FROM
        `donostia_dataset.parking_data`
      WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
    )
  );
