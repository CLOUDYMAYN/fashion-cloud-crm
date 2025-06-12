#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔥 Starting stress testing...${NC}"

# Check if k6 is installed
command -v k6 >/dev/null 2>&1 || { 
    echo -e "${RED}❌ k6 is required but not installed.${NC}" >&2
    echo -e "${YELLOW}Install k6: https://k6.io/docs/getting-started/installation/${NC}"
    exit 1
}

# Set target URL
TARGET_URL=${1:-http://localhost:8000}
echo -e "${YELLOW}🎯 Target URL: ${TARGET_URL}${NC}"

# Create results directory
mkdir -p test_results

# Run load test
echo -e "${YELLOW}📊 Running load test...${NC}"
k6 run --env BASE_URL=${TARGET_URL} tests/stress/load_test.js --out json=test_results/load_test.json

# Run spike test
echo -e "${YELLOW}⚡ Running spike test...${NC}"
k6 run --env BASE_URL=${TARGET_URL} tests/stress/spike_test.js --out json=test_results/spike_test.json

# Generate HTML report
echo -e "${YELLOW}📋 Generating HTML report...${NC}"
cat > test_results/report.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>CRM Shop Stress Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        .test-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .success { color: green; }
        .warning { color: orange; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 CRM Shop Stress Test Report</h1>
        <p>Target: ${TARGET_URL}</p>
        <p>Date: $(date)</p>
    </div>
    
    <div class="test-section">
        <h2>📊 Load Test Results</h2>
        <p>Check test_results/load_test.json for detailed metrics</p>
    </div>
    
    <div class="test-section">
        <h2>⚡ Spike Test Results</h2>
        <p>Check test_results/spike_test.json for detailed metrics</p>
    </div>
    
    <div class="test-section">
        <h2>📈 Recommendations</h2>
        <ul>
            <li>Monitor response times under load</li>
            <li>Check error rates during spike tests</li>
            <li>Verify database performance</li>
            <li>Monitor memory and CPU usage</li>
        </ul>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}✅ Stress testing completed!${NC}"
echo -e "${GREEN}📋 Report generated: test_results/report.html${NC}"
