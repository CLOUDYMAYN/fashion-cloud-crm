import http from "k6/http"
import { check, sleep } from "k6"
import { Rate } from "k6/metrics"

// Custom metrics
export const errorRate = new Rate("errors")

// Test configuration
export const options = {
  stages: [
    { duration: "2m", target: 10 }, // Ramp up to 10 users
    { duration: "5m", target: 10 }, // Stay at 10 users
    { duration: "2m", target: 20 }, // Ramp up to 20 users
    { duration: "5m", target: 20 }, // Stay at 20 users
    { duration: "2m", target: 0 }, // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% of requests must complete below 500ms
    http_req_failed: ["rate<0.1"], // Error rate must be below 10%
    errors: ["rate<0.1"],
  },
}

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000"

export default function () {
  // Test home page
  const homeResponse = http.get(`${BASE_URL}/`)
  check(homeResponse, {
    "home page status is 200": (r) => r.status === 200,
    "home page loads in <500ms": (r) => r.timings.duration < 500,
  }) || errorRate.add(1)

  sleep(1)

  // Test product catalog
  const catalogResponse = http.get(`${BASE_URL}/catalog/`)
  check(catalogResponse, {
    "catalog status is 200": (r) => r.status === 200,
    "catalog loads in <1000ms": (r) => r.timings.duration < 1000,
  }) || errorRate.add(1)

  sleep(1)

  // Test login page
  const loginResponse = http.get(`${BASE_URL}/login/`)
  check(loginResponse, {
    "login page status is 200": (r) => r.status === 200,
  }) || errorRate.add(1)

  sleep(2)
}

export function handleSummary(data) {
  return {
    "load_test_results.json": JSON.stringify(data, null, 2),
  }
}
