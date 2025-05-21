# 🛒 E-commerce Microservices Platform

A scalable and containerized e-commerce backend built using **microservices architecture** and **Docker**, featuring core services such as user authentication, product catalog, shopping cart, order management, payment processing, and notifications. It also includes support infrastructure such as API Gateway, service discovery (Consul), centralized logging (ELK stack), and monitoring (Prometheus + Grafana).

---

## 📦 Microservices Overview

| Service              | Description                                              | Port |
|----------------------|----------------------------------------------------------|------|
| `user-service`       | User registration, login, and JWT-based authentication   | 5000 |
| `product-service`    | Product catalog, categories, and inventory management    | 5001 |
| `cart-service`       | User shopping cart operations (add, remove, update)      | 5002 |
| `order-service`      | Order placement and tracking                             | 5003 |
| `payment-service`    | Payment simulation with order linking                    | 5004 |
| `notification-service` | Email/SMS notification handling                        | 5005 |
| `api-gateway`        | Reverse proxy for routing traffic to microservices       | 80   |

---

## 🚀 Getting Started

### ✅ Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)
- (Optional) [GitHub CLI](https://cli.github.com/) if using GitHub Actions

---

### 🏗️ Run the Application

From the root of the project:

```bash
docker-compose up --build
````

Access services through the API Gateway at:

* `http://localhost/users/`
* `http://localhost/products/`
* `http://localhost/cart/`
* `http://localhost/orders/`
* `http://localhost/payments/`
* `http://localhost/notifications/`

---

## 🔧 Infrastructure Components

### 🌐 API Gateway (NGINX)

* Central routing entry for all microservices.
* Configurable in `api-gateway/nginx.conf`.

---

### 🔍 Service Discovery (Consul)

Start Consul:

```bash
docker-compose -f service-discovery/docker-compose-consul.yml up
```

Visit [http://localhost:8500](http://localhost:8500) to view services and health checks.

---

### 📜 Centralized Logging (ELK Stack)

Start logging stack:

```bash
docker-compose -f logging/docker-compose-elk.yml up
```

* Kibana: [http://localhost:5601](http://localhost:5601)
* Elasticsearch: [http://localhost:9200](http://localhost:9200)

Logs are collected via Logstash on port 5000.

---

### 📊 Monitoring (Prometheus + Grafana)

Start monitoring stack:

```bash
docker-compose -f monitoring/docker-compose-monitoring.yml up
```

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000) (login: `admin` / `admin`)

---

## 🔁 CI/CD

This project includes GitHub Actions for automated CI/CD.

Path: `.github/workflows/deploy.yml`

To enable:

1. Push the code to a GitHub repo.
2. Set DockerHub credentials in repo secrets: `DOCKER_USER`, `DOCKER_PASS`.

---

## 🧪 Example Usage

```bash
# Register a user
curl -X POST http://localhost/users/register -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "1234"}'

# Add a product
curl -X POST http://localhost/products -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'
```
---

## 🙏 Acknowledgments

* [Docker](https://www.docker.com/)
* [NGINX](https://www.nginx.com/)
* [Consul](https://www.consul.io/)
* [Elastic Stack](https://www.elastic.co/what-is/elk-stack)
* [Prometheus](https://prometheus.io/)
* [Grafana](https://grafana.com/)

```

