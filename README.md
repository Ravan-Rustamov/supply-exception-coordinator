# Supply Exception Coordinator

Multi-agent AI for mid-market manufacturing supply chain exceptions.

## Quick Start

```bash
docker-compose up -d
curl -X POST http://localhost:8002/emails \
  -H "Content-Type: application/json" \
  -d '{"from_addr":"supplier@acme.com","subject":"Delayed","body":"..."}'
open http://localhost:8003
```

## Architecture

| Component | Role |
|-----------|------|
| **mock-erp** | Fake ERP simulation |
| **mock-inbox** | Email receiver |
| **case-api** | UI + approvals |
| **worker** | Agent orchestrator |
| **postgres** | Append-only ledger |
| **redis** | Queue + locks |

## License

MIT + Commercial Restrictions (see LICENSE)

## ARCHIVED — 2026-09-30
Stopped and removed from k8s-master (10.10.100.50). Replaced by the `dq-ai` project (AI Automated Cleaning).
DB dump: /root/cleanup/backup/sec-db-2026-09-30.sql.gz (kept by Ravan Rustamov, not in git).
