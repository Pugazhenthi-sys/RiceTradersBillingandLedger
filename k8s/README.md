# Open and verify the Kubernetes deployment

After a successful Jenkins build, verify from a Command Prompt that uses the same Kubernetes context:

```bat
kubectl -n rice-traders get pods,svc
kubectl -n rice-traders rollout status deployment/rice-traders-app
```

Then start a port-forward:

```bat
kubectl -n rice-traders port-forward service/rice-traders-service 6080:6080
```

Keep that Command Prompt open and browse to:

`http://localhost:6080/vnc.html`

Click **Connect** if prompted. noVNC should display the CustomTkinter desktop app running in the container.

If the page does not load, inspect the pod:

```bat
kubectl -n rice-traders get pods
kubectl -n rice-traders logs deployment/rice-traders-app
kubectl -n rice-traders describe deployment rice-traders-app
```

The app is a desktop GUI delivered through a virtual display, not a native web application. This is a lab demonstration path for Docker/Kubernetes. Do not use it as a production remote-desktop service without authentication, TLS, and security hardening.
