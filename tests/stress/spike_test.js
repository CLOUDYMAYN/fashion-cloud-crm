import http from "k6/http"
import { check, sleep } from "k6"

export const options = {
  stages: [
    { duration: "10s", target: 100 }, // Fast ramp-up to a high point
    { duration: "1m", target: 100 }, // Stay at high point
    { duration: "10s", target: 0 }, // Quick ramp-down to 0 users
  ],
  thresholds: {
    http_req_duration: ["p(95)<2000"], // 95% of requests must complete below 2s during spike
    http_req_failed: ["rate<0.2"], // Error rate must be below 20% during spike
  },
}

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000"

export default function () {
  const response = http.get(`${BASE_URL}/`)
  check(response, {
    "status is 200": (r) => r.status === 200,
  })
  sleep(1)
}
