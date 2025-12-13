# 🎥 Demo

This guide walks you through setting up **HESTIA** as a microservice that:

- Logs structured events in **JSON format**.
- Process logs with **Fluent Bit**. 
- Streams logs to **Elasticsearch** for centralized storage.
- Visualizes logs in **Kibana & Grafana**.
- Runs inside **Docker & Kubernetes**.


## 🎬 A Glance on HESTIA

=== "Kibana"

    ![Kibana Screenshot](assets/screenshots/kibana.png){ width=800 }

=== "Grafana"

    ![Grafana Screenshot](assets/screenshots/grafana.png){ width=800 }


## ⚡️ Prerequisites

Before starting, ensure you have:

- **Docker** and **Docker Compose** installed ([Installation Guide](prerequisites.md)).
- A terminal to run commands.
- Basic familiarity with web browsers to access Kibana and Grafana.

---

## 🚀 Running the Microservices

All microservices are managed in the `services/` directory. Follow these steps to get them up and running:

### 1. Run the Setup Script

Navigate to the Services Directory

```bash
cd services

```

Make sure that permissions are set correctly for The `setup_microservices.sh` script. 

```bash
chmod +x setup_microservices.sh

```

THis script configures the network, creates directories, and starts the services.

```bash
./setup_microservices.sh

```

!!! tip
    If you encounter subnet conflicts, the script will suggest alternative subnets (e.g., 172.19.0.0/16). Edit setup_microservices.sh to change `SUBNET` if needed.


### 2. Verify Services 

Check that all services are running:

```bash
docker ps -a

```

You should see:

- log-generator
- fluentbit
- es01 and es02 (Elasticsearch nodes)
- kibana
- grafana

--- 

## 📊 Exploring Logs in Kibana

### 1. Access Kibana

Open your browser and go to:

```bash
http://localhost:5601

```

### 2. Verify the Index Pattern

Navigate to Menu **(☰) > Management > Stack Management > Index Management**.

Indices are listed in the following pattern:

```bash
hestia-logs-yyyy.mm.dd

```

### 3. View Logs

Navigate to Menu **(☰) > Management > Analytics > Discover**, and create a Data View with the following attributes:


|attribute |value |
|------ | ------|
|**Name** | `hestia-logs`|
|**Index pattern** | `hestia-logs-*`|
|**Timestamp field** |`@timestamp`|

---

## 🎨 Logging Dashboard in Grafana

### 1. Access Grafana

Open your browser and go to:

```bash
http://localhost:3000

```

### 2. Login to Grafana

The default login information is set as _admin/admin (username/password)_. On the first login, Grafan redirects you to setting a new password. 


### 3. View HESTIA Dashboard

Navigate to Menu **(☰) > Dashboards > Hestia Logger**.

---

!!! note

    **Kibana and Grafana** may take a few minutes to start. Please be patient! ⏳



Thank you for exploring our demo!🙌 We hope this example has given you a clear understanding of how to utilize **HESTIA** and integrate its features into your projects. Whether you're just getting started or diving deeper, our goal is to make your experience as seamless and productive as possible. ✌️