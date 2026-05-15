# Upstream API Contract — TD Plot

This document defines the governed platform endpoint that the TD Plot app requires.
It is the handoff artifact for the JIO platform team to implement using the governed SQL query service.

## Required Endpoint

```
GET /api/td/{uniquedataid}
```

### Parameter

| Name | Type | Description |
|---|---|---|
| `uniquedataid` | path string | Unique data identifier for the TD function |

### Success Response — 200

```json
{
  "uniquedataid": "string",
  "dataname":     "string",
  "time_unit":    "string",
  "depth_unit":   "string",
  "time_ref":     "string",
  "depth_ref":    "string",
  "td_pairs": [
    { "time": 0.0, "depth": 0.0 }
  ]
}
```

| Field | Source table | Column |
|---|---|---|
| `uniquedataid` | `wells.data` | `uniquedataid` |
| `dataname` | `wells.data` | `dataname` |
| `time_unit` | `wells.td_functions` | `time_unit` |
| `depth_unit` | `wells.td_functions` | `depth_unit` |
| `time_ref` | `wells.td_functions` | `time_ref` |
| `depth_ref` | `wells.td_functions` | `depth_ref` |
| `td_pairs[].time` | `wells.td_pairs` | `time` |
| `td_pairs[].depth` | `wells.td_pairs` | `depth` |

### Error Responses

| Status | Condition |
|---|---|
| 404 | `uniquedataid` not found in `wells.data` |
| 500 | Query error |

---

## SQL

```sql
SELECT
    d.uniquedataid,
    d.dataname,
    f.time_unit,
    f.depth_unit,
    f.time_ref,
    f.depth_ref,
    p.time,
    p.depth
FROM wells.data         d
JOIN wells.td_functions f ON f.uniquedataid = d.uniquedataid
JOIN wells.td_pairs     p ON p.uniquejobid  = d.uniquejobid
WHERE d.uniquedataid = :uniquedataid
ORDER BY p.depth ASC
```

**Parameter:** `:uniquedataid`

The response is built by reading the metadata columns from the first row and collecting
all `(time, depth)` pairs into `td_pairs`. Returns 404 when the query returns no rows.

---

## App Configuration

The TD Plot app points to this endpoint via the `TD_PLOT_DATA_SERVICE_URL` environment variable.

The app calls:

```
GET {TD_PLOT_DATA_SERVICE_URL}/api/td/{uniquedataid}
```

Set `TD_PLOT_DATA_SOURCE_MODE=external_http` in deployed environments.
Set `TD_PLOT_DATA_SOURCE_MODE=fixture` for local development (reads from `sample_data/`).

The fixture files in `sample_data/` match the exact response shape of this endpoint
and serve as the reference implementation contract.
