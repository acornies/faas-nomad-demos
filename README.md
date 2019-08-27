# faas-nomad-hug-workshop

## CLI requirements

- vagrant
- faas-cli
- terraform
- vegeta

## Demo steps

1) Provision local Vagrant environment

```bash
vagrant up
```

2) Use Terraform to provision Vault and Nomad jobs

```bash
# Initialize environment, download plugins
terraform init

# Run the Vault module first
terraform apply -target=module.vault

# Apply the Nomad jobs after
terraform apply -target=module.faas
```

3) Use faas-cli to deploy a function

```bash
# Authenticate with OpenFaaS gateway
faas-cli login --gateway http://localhost:8080 --password vagrant

# Deploy a function from the store
faas-cli store deploy figlet --gateway http://localhost:8080
```

4) Use `vegeta` to generate load

```bash
# Invoke figlet 50/sec for 1 minute
echo "POST http://localhost:8080/function/figlet" | vegeta -cpus 1 attack -rate=50 -duration 1m -body figlet > results.gob

# Print the results
vegeta report results.gob
```

5) Deploy a custom function using secrets

```bash
# Add the Grafana API secret
faas-cli secret create grafana-api-token --from-literal '' --gateway=http://localhost:8080

# Source repo git@github.com:acornies/faas-grafana-annotate.git

# Deploy function from stack.yml
faas-cli deploy --image acornies/grafana-annotate:0.1.2 --name grafana-annotate --env grafana_url=http://10.0.2.15:3000 --gateway=http://localhost:8080 --secret grafana-api-token
```