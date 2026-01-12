
---

# Local Business Search — Technical Overview

## 1. Purpose

This project is a **backend-oriented Django application** designed to study and apply best practices in:

* External API integration
* Data normalization and validation
* Backend-driven rendering
* Defensive programming
* Clean separation of concerns

The frontend exists strictly as a **presentation layer**.

---

## 2. Core Responsibilities

The backend is responsible for:

* Managing all API communication
* Authenticating external requests via Bearer Token
* Validating and normalizing third-party data
* Ensuring data consistency before rendering
* Preventing client-side logic errors

No critical logic is delegated to the frontend.

---

## 3. Architecture

### Request Flow

```
Client Request
   ↓
Django View (IndexView)
   ↓
Service Layer (utils.py)
   ↓
External API (Yelp Fusion)
   ↓
Normalization & Validation
   ↓
Template Rendering
```

### Architectural Decisions

* Views are thin and orchestration-focused
* External integrations are isolated in a service layer
* Templates receive only prevalidated data
* All coordinates are normalized server-side

---

## 4. Backend Implementation Details

### 4.1 View Logic (`IndexView`)

Responsibilities:

* Resolve search parameters
* Determine fallback location via GeoIP
* Trigger API call
* Normalize API response
* Prepare rendering context

Key properties:

* No HTTP logic in templates
* No external calls inside templates
* All failures handled gracefully

---

### 4.2 External API Integration (`yelp_search`)

* Uses `requests`
* Authenticated via `Authorization: Bearer <API_KEY>`
* Parameters validated before dispatch
* Raw JSON response returned to service layer

```python
headers = {
    "Authorization": f"Bearer {settings.YELP_API_KEY}"
}
```

---

### 4.3 Data Normalization Strategy

Yelp API may return inconsistent numeric formats.

Normalization rules:

* Convert latitude/longitude to `float`
* Replace commas with dots if necessary
* Invalidate coordinates on conversion failure

```python
coords["latitude"] = float(str(lat).replace(",", "."))
coords["longitude"] = float(str(lon).replace(",", "."))
```

This guarantees safe map rendering.

---

## 5. Geolocation (GeoIP)

* Uses `GeoIP2`
* One-shot attempt per request
* Failure-safe fallback

GeoIP errors **never block** application execution.

---

## 6. Frontend Interaction Model

### Role of the Frontend

* Render validated data
* Initialize map once
* Display markers
* Provide optional hover interactions

### What the Frontend Does *Not* Do

* No data validation
* No API calls
* No error handling logic
* No business logic

---

## 7. Map Handling (Leaflet)

### Stability Measures

* Single initialization guard
* No re-render on DOM events
* Only valid coordinates generate markers

```javascript
if (map) return;
```

---

## 8. Error Handling Philosophy

The application explicitly handles:

* Missing or invalid API keys
* Empty API responses
* Network errors
* Invalid coordinates
* GeoIP resolution failures

No unhandled exceptions propagate to the user.

---

## 9. Configuration Management

### Environment Variables

All secrets are externalized.

```env
YELP_API_KEY=********
```

Validation is enforced at startup.

---

## 10. Known Technical Limitations

* No caching layer
* No request throttling
* No pagination
* No automated tests
* GeoIP provides approximate location only

These were conscious trade-offs for educational focus.

---

## 11. Potential Technical Extensions

* Redis-based caching
* DRF API exposure
* Async HTTP requests
* Unit and integration testing
* Structured logging
* Pagination and filtering

---

## 12. Design Philosophy

* Backend-first
* Deterministic data flow
* Fail-safe integrations
* Minimal frontend responsibility
* Explicit over implicit behavior

---

## 13. Author Notes

This project was developed as a **technical study**, prioritizing:

* Code clarity
* Architectural discipline
* Error resilience
* Backend correctness

UI/UX complexity was intentionally deprioritized.

---