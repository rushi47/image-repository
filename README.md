**Image Repository for Shopify Challenge**

**How to test this repo -**

- Repo expects Kubernetes(minikube) & Helm installed on the System.
- Clone repo from : 
```
https://github.com/rushi47/image-repository
```
- Once cloned, install the app using Helm -
```
helm install -n shopify -f image-kube-charts/test-values.yaml shopify image-kube-charts --create-namespace
```
 _image-kube-chars_ : Dir contains chart to install app on Kubernetes.

( Docker image for respective code, is already pushed on docker hub. So no need to build it 😄.)
  And this should create :
  - Deployment
  - ReplicaSet
  - Ingress Controller
  - Service Object
  - HPA - As of now deployment will scale on minimum _60% CPU_ utilisation. (Ideally it should be on request rate)
  - PDB 

- **[A]** [optional] If nginx-ingress controller is installed - app is exposed on : _**shopify-test.com**_
- **[B]** Else create tunnel to service object : for minikube - 
```
minikube service --url shopify -n shopify
```

Using above steps, app should be exposed smoothly on the URL from step **A** or **B** 😃.
[In case kube is not installed, we can run from docker directly, I will mention the steps for the same at end of this README]

- Because of the time constraints I didnt get chance to create front end but we can test the app using _**curl**_

- App is configured with basic auth for now (I got to know about the challenge late :( ) 

- To test bulk upload feature :
```
curl -v --user "shopify:shopify@123" -X POST -F files=@'file_name1.jpg' -F files=@'file_name2.jpg' localhost:55028/bulk_upload
```

- Above endpoint lets you upload, multiple files

- As its our image repo, Only file allowed are with Extension :
```
['png', 'jpg', 'jpeg', 'gif']
```

- App is deployed on Kubernetes, _**the volume is shared between all the pods**_. Avoiding problem dedup and consistency.

- App also support bulk delete feature and can be tested from:
```
curl -v --user "shopify:shopify@123" -H "Content-Type: application/json" -X POST -d '{"name": "working", "file_names":["test3.jpg", "test2.jpg"]}' localhost:55028/bulk_delete
```

- Dont worry, I got you covered, you can retrieve the list of files uploaded 😉 :
```
curl -v --user "shopify:shopify@123" localhost:55028/read_files
```


---
**Testing Repo without Kubernetes:**
- As image is available on docker hub it should be as simple as :
```
docker run -d -p 4747:4747 rushib47/shopify-task:v1
```


Existing architecture of app, already have components decoupled and is Kubernetes ready. For instance to modify auth, only thing which we need to modify is auth file.
Considering **_shopify runs of one the largest Kubernetes cluster_** in industry, this app also takes in assumption that front end and back end will be decoupled.
And it will also be run on kubernetes on different node, just by segregating using labels like app=backend or app=frontend. Achieving High Availability out of the box 
and also giving room to scale without any efforts.

TO DO:
As I just got 2-3 days to implement the project but in Ideal scenario, I would like to add components such as:
- Upload Cache - As it gives advantage, to quickly serve the uploaded files, if they are requested from other end.
- Download Cache - To cache the downloads, if files are uploaded recently, from download cache files can also looked up in upload cache, saving round trips.
- Replicators - To replicate the files uploaded, to external storage like s3, google bucket to achieve SLOs.
- Monitoring - Create metrics for important function, to monitor performance and detect issues.
