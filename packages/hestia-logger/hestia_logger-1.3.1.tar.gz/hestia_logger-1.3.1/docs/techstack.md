# 💻 Tech Stack

When designing a logging and monitoring stack, we needed a **robust, scalable, and efficient** system that can **process, store, visualize, and analyze logs** effectively. Below is the reasoning behind our choices:

---

## **🛢️ Fluent Bit**

🔸 Purpose: **The Lightweight Log Forwarder**

- **Lightweight and Fast**: Minimal resource usage, perfect for Docker containers.
- **Efficient Log Forwarding**: Collects JSON logs from HESTIA Logger (e.g., via `log-generator`) and forwards them to Elasticsearch.
- **Built-in Processing**: Parses structured logs with filtering and transformation capabilities.
- **Seamless Elasticsearch Integration**: Native output plugin ensures smooth ingestion.

**Alternatives Considered:**

- **Logstash**: Powerful for complex transformations but resource-heavy.
- **Filebeat**: Great for log shipping but lacks parsing flexibility.

**🏅 Why Fluent Bit Won?**

- **Low memory footprint** for containerized environments.
- **Native JSON parsing** aligns with HESTIA’s log format.
- **Balanced performance and functionality** for our needs.
- **Direct Elasticsearch support** simplifies the pipeline.

---

## **🔍 Elasticsearch**

🔸 Purpose: **The Log Storage & Search Engine**

- **Distributed Architecture**: Runs as a two-node cluster (`es01`, `es02`) for redundancy and scale.
- **Full-Text Search**: Enables quick log retrieval with powerful queries.
- **Real-Time Indexing**: Logs are searchable almost instantly after ingestion.
- **Scalable Storage**: Handles growing log volumes effortlessly.

**Alternatives Considered:**

- **MongoDB**: General-purpose database, not optimized for log search.
- **Loki**: Lightweight and cost-effective but weaker full-text search.

**🏅 Why Elasticsearch Won?**

- **Built for log storage and querying at scale.**
- **Near real-time search** enhances observability.
- **Pairs seamlessly with Fluent Bit and Kibana.**

---

## **📊 Kibana**

🔸 Purpose: **The Log Visualization Tool**

- **Powerful UI**: Search and explore HESTIA logs in Elasticsearch via `port 5601`.
- **Discover & Dashboards**: Simplifies log analysis with filters and visualizations.
- **Real-Time Monitoring**: Tracks log trends as they happen.

**Alternatives Considered:**

- **Grafana**: Strong dashboards but weaker log search.
- **Graylog**: Feature-rich but overkill for our setup.

**🏅 Why Kibana Won?**

- **Ideal for interactive log exploration.**
- **Native Elasticsearch integration** via Docker Compose.
- **Quick dashboards** for HESTIA log trends.**
  
---

## **🎨 Grafana**

🔸 Purpose: **Advanced Monitoring & Dashboards**

- **Custom Dashboards**: Visualizes HESTIA logs (e.g., “HESTIA Logging Overview”) via `port 3000`.
- **Multiple Data Sources**: Integrates Elasticsearch with potential for metrics (e.g., Prometheus).
- **Rich Visualizations**: Time-series, heatmaps, and alerts for log insights.
- **Advanced Alerting**: Proactive monitoring of log patterns.

**Alternatives Considered:**

- **Kibana Alone**: Limited dashboard flexibility.
- **Loki with Grafana**: Simpler but misses full-text search.

**🏅 Why Grafana Won?**

- **Flexible dashboards** for log analytics.
- **Future-proof** with multi-source support.
- **Enhanced alerting** beyond Kibana’s capabilities.**


---

## Summary

✔ **Fluent Bit**: Collects and forwards HESTIA logs.  
✔ **Elasticsearch**: Stores and indexes logs in a cluster.  
✔ **Kibana**: Enables log search and basic visualization.  
✔ **Grafana**: Provides advanced monitoring dashboards.  

**🎯 Together, these tools power HESTIA Logger’s observability pipeline.**