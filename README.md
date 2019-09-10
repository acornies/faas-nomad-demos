# faas-nomad-demos

## CLI requirements

- vagrant
- faas-cli
- terraform
- vegeta

## Demo steps

Provision local Vagrant environment

```bash
vagrant up
```

Use Terraform to provision Vault and Nomad jobs

```bash
# Initialize environment, download plugins
cd terraform
terraform init

# Run the Vault module first
terraform apply -target=module.vault

# Apply the Nomad jobs after
terraform apply -target=module.faas
```

OpenFaaS and supporting components should be avialable:

- OpenFaaS gateway: http://localhost:8080
- Consul: http://localhost:8500
- Vault: http://localhost:8200
- Nomad: http://localhost:4646
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (import dashboard id: 3434)

Use faas-cli to deploy a function

```bash
# Authenticate with OpenFaaS gateway
faas-cli login --gateway http://localhost:8080 --password vagrant

# Deploy a function from the store
faas-cli store deploy figlet
```

Use `vegeta` to generate load

```bash
cd ../
# Invoke figlet 50/sec for 1 minute
echo "POST http://localhost:8080/function/figlet" | vegeta -cpus 1 attack -rate=50 -duration 1m -body figlet > results.gob

# Print the results
vegeta report results.gob
```

Deploy a custom function using secrets

```bash
# Add the Grafana API secret
faas-cli secret create grafana-api-token --from-literal '' --gateway=http://localhost:8080

# Source repo git@github.com:acornies/faas-grafana-annotate.git

# Deploy function from stack.yml
faas-cli deploy --image acornies/grafana-annotate:0.1.2 --name grafana-annotate --env grafana_url=http://10.0.2.15:3000 --gateway=http://localhost:8080 --secret grafana-api-token
```

## HashiConf 19 additions

```bash
# Add stripe webhook payload secret
faas-cli secret create stripe-webhook-secret --from-literal ''

# Apply the Kafka modules
terraform apply -target=module.kafka
terraform apply -target=module.faas_kafka_connector

# Login to Vagrant VM to create a kafka console consumer
vagrant ssh

# Find kafka broker container
docker ps | grep kafka-brokers
docker exec -it ${name} bash

# Launch console consumer
kafka-console-consumer --bootstrap-server 10.0.2.15:29092 --topic stripe-webhook-charge-dispute-created
```

Launch a function tied to our Kafka topic:

```bash
# Launch a function from store with special topic annotation
faas-cli store deploy cows --annotation topic=stripe-webhook-charge-dispute-created
```
