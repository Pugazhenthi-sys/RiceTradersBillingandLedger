# Jenkins setup (Windows + Docker Desktop Kubernetes)

## 1. Prepare the project

Extract the ZIP and double-click `PREPARE-PROJECT.bat`.
It clones/updates the source at `D:\RiceTradersCICD` and copies the Docker/Kubernetes files there.

## 2. Create Docker Hub repository

Create a Docker Hub repository named `rice-traders-app` (or your preferred name).
Your repository value must be `YOUR_DOCKERHUB_USERNAME/rice-traders-app`.

## 3. Add Jenkins credential

In Jenkins:
1. Manage Jenkins → Credentials → System → Global credentials → Add Credentials.
2. Kind: Username with password.
3. Username: your Docker Hub username.
4. Password: Docker Hub access token (recommended), not your account password.
5. ID: `dockerhub-creds`.
6. Save.

## 4. Make sure Jenkins can run the tools

On the Windows machine that runs the Jenkins agent, verify in a Command Prompt running as that same Windows user:

```bat
docker --version
kubectl version --client
kubectl config current-context
kubectl get nodes
```

Expected Kubernetes context: `docker-desktop`; node should be `Ready`.

Jenkins runs as a Windows service under a different account in many installations. In that case, it may not see your Docker Desktop engine or your user's kubeconfig. The easiest local-lab setup is to configure a Jenkins agent that runs interactively under the same Windows account that starts Docker Desktop, and run the job on that agent. Do not assume that a successful command in your personal CMD also works inside Jenkins.

Required tools on the Jenkins agent:
- Git
- Python 3.12+ (for source syntax validation)
- Docker CLI connected to Docker Desktop
- kubectl configured for the Docker Desktop Kubernetes cluster

The `bat` steps in the Jenkinsfile are intended for a Windows agent.

## 5. Create the Pipeline job

1. Jenkins Dashboard → New Item.
2. Name: `RiceTradersCICD`.
3. Select **Pipeline** → OK.
4. Under Pipeline, choose **Pipeline script from SCM**.
5. SCM: Git.
6. Repository URL: `https://github.com/Pugazhenthi-sys/RiceTradersBillingandLedger.git`
7. Branch: `*/main` (if the repository uses another default branch, use that branch).
8. Script Path: `Jenkinsfile`.
9. Save.

If your GitHub repository is private, configure a separate GitHub credential for checkout and select it in the job.

## 6. Set DOCKERHUB_REPO for the job

The Jenkinsfile needs the full image name. Configure it as a global environment variable for the agent/Jenkins, or add this environment variable in the pipeline job's configuration if your Jenkins setup supports job-level environment variables:

`DOCKERHUB_REPO=YOUR_DOCKERHUB_USERNAME/rice-traders-app`

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username. Do not include `https://` or `docker.io/`.

## 7. Build

Open `RiceTradersCICD` → **Build Now** → Console Output.

The pipeline:
1. Checks out source.
2. Checks Python syntax.
3. Builds the image.
4. Pushes a versioned and `latest` image to Docker Hub.
5. Applies Kubernetes resources and waits for rollout.

## 8. Important note about GUI

The original app uses CustomTkinter. Kubernetes containers do not normally have a desktop display. This package starts a virtual X display and noVNC so the GUI can be viewed through a browser. It does not turn the desktop app into a native web app.

## Troubleshooting

- `docker` not found: install Docker CLI on the Jenkins agent or fix PATH.
- Docker daemon unavailable: start Docker Desktop and verify the agent runs as the right Windows user.
- `kubectl` context missing: configure the agent user's kubeconfig for Docker Desktop Kubernetes.
- `docker push denied`: check `dockerhub-creds`, repository name, and Docker Hub access token.
- Pod `ImagePullBackOff`: verify image name and that the Docker Hub repository is public or Kubernetes has image-pull credentials.
- Build fails at Python validation because Python is not on PATH: install Python on the Jenkins agent.
- Git checkout fails: check repository URL, branch, and GitHub credentials if private.
