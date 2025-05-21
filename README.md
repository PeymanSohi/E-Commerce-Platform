# 🛒 Scalable E-commerce Platform (Microservices + Docker)

This project implements a scalable e-commerce backend using microservices architecture and Docker. Each service is independently deployable, uses MySQL for data persistence, and communicates over REST. It includes centralized logging (ELK), monitoring (Prometheus + Grafana), and an API Gateway for routing.

---

## 📦 Microservices Overview

| Service                | Description                              | Port |
| ---------------------- | ---------------------------------------- | ---- |
| `user-service`         | User registration, login, JWT auth       | 8000 |
| `product-service`      | Product catalog and inventory            | 5001 |
| `cart-service`         | Shopping cart management                 | 5002 |
| `order-service`        | Order processing, triggers payment       | 5003 |
| `payment-service`      | Mock payment processing                  | 5004 |
| `notification-service` | Sends mock emails/SMS                    | 5005 |
| `api-gateway`          | NGINX reverse proxy for external routing | 8080 |

---

## 🚀 How to Run the Project

```bash
docker-compose -f docker-compose.yml up --build
docker-compose -f logging/docker-compose-elk.yml up -d
docker-compose -f monitoring/docker-compose-monitoring.yml up -d
```

---

## 🧪 API Test Commands via API Gateway (`localhost:8080`)

### 🧍 User Service

**Register a user**

```bash
curl -X POST http://localhost:8080/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "pass123"}'
```

**Login a user**

```bash
curl -X POST http://localhost:8080/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "pass123"}'
```

---

### 📦 Product Service

**Add product**

```bash
curl -X POST http://localhost:8080/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 15", "category": "electronics", "price": 999.99, "stock": 10}'
```

**List all products**

```bash
curl http://localhost:8080/products/
```

---

### 🛒 Cart Service

**Add item to cart**

```bash
curl -X POST http://localhost:8080/cart/john \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

**Get cart for user**

```bash
curl http://localhost:8080/cart/john
```

---

### 📦 Order Service

**Place an order**

```bash
curl -X POST http://localhost:8080/orders/ \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "john",
        "products": [
          { "product_id": 1, "price": 999.99, "quantity": 2 }
        ]
      }'
```

**List user orders**

```bash
curl http://localhost:8080/orders/john
```

---

### 💳 Payment Service

**Simulate payment**

```bash
curl -X POST http://localhost:8080/pay \
  -H "Content-Type: application/json" \
  -d '{"user_id": "john", "order_id": "1", "amount": 1999.98}'
```

---

### 📬 Notification Service

**Send mock email**

```bash
curl -X POST http://localhost:8080/notify \
  -H "Content-Type: application/json" \
  -d '{"type": "email", "to": "john@example.com", "message": "Order confirmed!"}'
```

---

### ❤️ Health Check Endpoints

```bash
curl http://localhost:8080/users/health
curl http://localhost:8080/products/health
curl http://localhost:8080/cart/health
curl http://localhost:8080/orders/health
curl http://localhost:8080/pay/health
curl http://localhost:8080/notify/health
```

---

## 📊 Monitoring

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)
  *Default login: `admin / admin`*

---

## 📚 Logging

* Kibana: [http://localhost:5601](http://localhost:5601)
  *Index pattern: `ecommerce-logs*`*

---
