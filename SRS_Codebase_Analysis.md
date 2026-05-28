# 1. INTRODUCTION

### 1.1 Purpose

- This system provides automated business intelligence for retail/shop sales data.
- It accepts uploaded CSV/XLS/XLSX transaction files, cleans and standardizes data, computes analytics, and exposes dashboard/report APIs.
- It includes a web UI for dataset upload and report download (CSV/PDF), with dashboard and insights views.

### 1.2 Scope

- In scope (implemented):
- Single-dataset file upload and replacement in backend storage.
- Data cleaning and validation pipeline.
- KPI and aggregated analytics generation.
- Insight text generation from computed analytics.
- Dashboard and report REST endpoints.
- Frontend pages for landing, dashboard navigation, upload, reports, insights, and settings UI.
- Out of scope (not implemented in code):
- User authentication and authorization.
- Multi-tenant or role-based data isolation.
- Incremental dataset append/merge workflows (current behavior replaces all prior records).
- Real-time streaming updates.

### 1.3 Intended Users

- Small shop owners or store managers who upload sales data and review business insights.
- Business operators who need KPI summaries, low-performing product alerts, and dead-stock visibility.
- Technical users (developers/testers) who run and validate FastAPI and React/Vite modules.

### 1.4 Definitions

- ETL: Extract, Transform, Load process for uploaded retail files.
- KPI: Key Performance Indicator (total revenue, total profit, unique products, average profit margin).
- Dead Stock: Product with no sale after a threshold period (default logic: 30 days relative to latest dataset date).
- Low Performing Product: Product with low or negative profitability based on aggregated sales/profit sorting.
- Profit Margin: profit / revenue, set to 0 when revenue is 0.
- Dataset Preview: First N rows (currently 10) returned after upload.

---

# 2. OVERALL DESCRIPTION

### 2.1 Product Perspective

- The system is a standalone web application with separate frontend and backend applications.
- Architecture:
- Frontend: React + TypeScript SPA (Vite), routed with React Router.
- Backend: FastAPI service exposing REST APIs.
- Data store: SQLite database file in backend.
- Processing engine: Pandas/Numpy data transformations.
- Interaction model:
- Frontend uploads data and requests reports via HTTP.
- Backend validates, cleans, computes analytics, stores dataset, and returns JSON payloads.

### 2.2 Product Functions

- Health endpoint for service availability.
- File upload endpoint supporting CSV/XLS/XLSX.
- Header normalization and required-column enforcement.
- Data cleaning:
- String normalization and missing-value handling.
- Numeric/date coercion.
- Median-based imputation for missing prices.
- Invalid-row filtering with warning summary.
- Financial metric enrichment:
- Revenue, profit, and profit margin calculation.
- Dashboard analytics generation:
- KPIs, sales trend, top products, low-performing products, category distribution, dead stock.
- Insight generation:
- Dead stock warnings, top-profit-category trend, loss alerts, demand spike signal.
- Report generation endpoint with aggregate payload and timestamp.
- Frontend report export to CSV and PDF.
- Frontend dashboard navigation and responsive layout with dark-mode class toggle.

### 2.3 User Classes

- Business user (non-technical):
- Uploads files, views summaries, downloads reports.
- Analyst user (semi-technical):
- Interprets charts, trends, low-performance lists, and insight statements.
- Developer/test user (technical):
- Runs local servers/tests and validates APIs.

### 2.4 Operating Environment

- Backend stack:
- Python, FastAPI, Uvicorn.
- Pandas, Numpy, OpenPyXL, python-multipart.
- SQLite local database file.
- Frontend stack:
- React 18, TypeScript, Vite.
- React Router, Tailwind CSS, Radix UI/shadcn-style components.
- Recharts for charts, Framer Motion for UI animation, jsPDF for PDF export.
- Test stack:
- Backend: pytest + FastAPI TestClient.
- Frontend: Vitest (+ jsdom), Playwright config present.
- Deployment/runtime assumptions in code:
- Frontend defaults backend base URL to http://localhost:8000.
- Vite dev server configured on port 8080.

### 2.5 Constraints

- Input schema constraints:
- Required business columns must be present after normalization.
- Missing required columns trigger upload failure (400).
- Data validity constraints:
- Rows with invalid date, non-positive quantity, invalid/missing prices are dropped.
- Storage constraint:
- Upload replaces entire existing transaction table (no append mode).
- CORS constraint:
- Allowed origins are explicitly local hostnames/ports only.
- Feature completeness constraints:
- Frontend dashboard and insights pages are currently static/mock and not bound to backend dashboard API.
- Settings page is UI-only placeholder.
- No auth/security middleware beyond basic CORS and request validation.

### 2.6 Assumptions

- Users provide tabular sales files with recognizable column headers.
- Backend service is reachable from frontend host.
- Single shared dataset semantics are acceptable for current use case.
- Local SQLite persistence is acceptable for current scale.
- Browser supports modern JavaScript APIs (fetch, blob download, etc.).

---

# 3. EXTERNAL INTERFACE REQUIREMENTS

### 3.1 User Interface

- Implemented pages:
- Landing page: /
- Dashboard home: /dashboard
- Upload page: /dashboard/upload
- Reports page: /dashboard/reports
- Insights page: /dashboard/insights
- Settings page: /dashboard/settings
- Not Found page: *

- Landing UI components:
- Navbar
- HeroSection
- FeaturesSection
- HowItWorks
- CTASection
- Footer

- Dashboard shell/component:
- DashboardLayout (sidebar, topbar, outlet container)

- Navigation utility:
- NavLink wrapper component

- UI component primitives under src/components/ui:
- accordion
- alert-dialog
- alert
- aspect-ratio
- avatar
- badge
- breadcrumb
- button
- calendar
- card
- carousel
- chart
- checkbox
- collapsible
- command
- context-menu
- dialog
- drawer
- dropdown-menu
- form
- hover-card
- input-otp
- input
- label
- menubar
- navigation-menu
- pagination
- popover
- progress
- radio-group
- resizable
- scroll-area
- select
- separator
- sheet
- sidebar
- skeleton
- slider
- sonner
- switch
- table
- tabs
- textarea
- toast
- toaster
- toggle-group
- toggle
- tooltip
- use-toast

- Observed UI behavior:
- Responsive sidebar behavior on dashboard layout.
- Drag-and-drop upload plus click-to-select.
- Upload preview table with cleaning summary and warnings.
- Report cards with CSV/PDF download actions.
- Dark-mode class toggle in layout (session-only, no persistence logic).

### 3.2 Hardware Interfaces

- No specialized hardware integrations are implemented.
- Supported interaction is standard browser-based input:
- Keyboard, mouse, touch.
- File selection and drag/drop from local filesystem.

### 3.3 Software Interfaces

- Frontend to backend API interfaces:
- POST /upload (multipart/form-data, file field).
- GET /report (JSON).
- Backend also provides GET /dashboard and GET /health.

- Backend libraries/interfaces:
- FastAPI routing and pydantic schemas.
- Pandas/Numpy processing APIs.
- SQLite connection via sqlite3.

- Frontend libraries/interfaces:
- React Router for navigation.
- Native fetch for HTTP.
- Recharts for chart widgets.
- jsPDF + Blob API for file exports.
- Tailwind CSS + Radix UI/shadcn component layer.

### 3.4 Communication Interfaces

- Protocol and data format:
- HTTP/REST over local network.
- JSON responses for analytics/report payloads.
- multipart/form-data for uploads.

- Frontend API base URL:
- Uses VITE_API_BASE_URL when defined.
- Falls back to http://localhost:8000.

- Error communication:
- Backend returns HTTP 400 for validation/input issues and HTTP 500 for generic upload failures.
- Frontend surfaces backend detail message where available.

---

# 4. SYSTEM FEATURES

## File Upload

- Description
- Accepts a retail dataset file and initiates the ETL pipeline.
- Input
- File in .csv, .xls, or .xlsx format.
- Processing
- Validates extension and non-empty content.
- Saves temporary file under backend tmp_uploads with generated unique name.
- Reads file into DataFrame.
- Standardizes column headers to strict schema.
- Sends data into cleaning and analytics enrichment pipeline.
- Replaces prior SQLite dataset with cleaned/enriched records.
- Removes temporary file in finally block.
- Output
- JSON response with preview rows, total/cleaned/dropped row counts, and warnings list.
- HTTP 400 for validation errors, HTTP 500 for unexpected failures.

## Data Cleaning

- Description
- Cleans incoming records and enforces structural validity before analytics.
- Input
- Standardized tabular dataset with fields: date, product_name, category, cost_price, selling_price, quantity.
- Processing
- Normalizes text fields and trims whitespace.
- Drops rows with missing critical fields (product_name/date).
- Parses date and numeric values.
- Fills missing category with Uncategorized.
- Imputes missing prices with product median, then category median, then global median.
- Sets missing quantity to 0, then drops invalid rows (bad date, quantity <= 0, invalid prices).
- Sorts by date and resets index.
- Builds cleaning summary warnings.
- Output
- Cleaned DataFrame and summary metadata (input_rows, cleaned_rows, dropped_rows, warnings).

## Analytics Engine

- Description
- Computes financial metrics and aggregate analytics used by dashboard/report endpoints.
- Input
- Cleaned transaction DataFrame.
- Processing
- Adds revenue, profit, and profit_margin columns.
- Computes KPIs.
- Builds sales trend grouped by date.
- Builds top products and low-performing products views.
- Computes category distribution.
- Detects dead stock based on inactivity threshold.
- Builds broader product performance list for reports.
- Output
- Structured analytics payload dictionaries consumed by dashboard/report responses.

## Dashboard

- Description
- Exposes consolidated analytics and generated insight strings.
- Input
- Request to backend /dashboard.
- Processing
- Loads transactions from SQLite.
- If dataset is empty, returns default zero structures and guidance message.
- If dataset exists, computes dashboard payload and appends generated insights.
- Output
- JSON dashboard response containing:
- kpis
- sales_trend
- top_products
- low_performing_products
- category_distribution
- dead_stock
- insights
- Note
- Frontend DashboardHome page currently renders static mock data and does not consume this endpoint.

## Insights Generation

- Description
- Produces textual advisory messages from computed analytics.
- Input
- Raw DataFrame and precomputed dashboard sections.
- Processing
- Adds warnings for top dead-stock products.
- Adds trend statement for most profitable category.
- Adds alerts for low-performing products with negative profit.
- Adds demand spike message using 90th percentile quantity heuristic.
- Falls back to informational message if no issues/anomalies detected.
- Output
- Ordered list of insight strings (WARNING/TREND/ALERT/SPIKE/INFO style messages).

## Reports

- Description
- Produces aggregated reporting dataset and enables user download in browser.
- Input
- Request to backend /report.
- Processing
- Builds report payload with generated timestamp, row count, KPIs, aggregated groups, dead stock, low-performing products.
- Frontend Reports page fetches payload and maps data into downloadable CSV and PDF files.
- Output
- Backend JSON report response.
- Frontend-generated files:
- CSV report files by report type.
- PDF report files by report type.

---

# 5. NON-FUNCTIONAL REQUIREMENTS

- Performance
- In-memory Pandas processing with local SQLite storage is suitable for small-to-medium datasets.
- Preview response limited to first 10 rows reduces payload size.
- No background worker/queue; uploads are processed in request path.

- Security
- Input validation includes file-type constraints, required-column checks, and structural row validation.
- CORS configured for local development origins.
- Missing: authentication, authorization, CSRF strategy, rate limiting, and advanced upload security scanning.

- Usability
- Upload workflow supports drag-drop and file picker.
- Clear upload status (uploading/success/error) and warning display.
- Dashboard navigation is responsive with mobile sidebar.
- Missing: fully functional settings actions and dynamic dashboard binding.

- Reliability
- Backend has deterministic cleaning and explicit exceptions for invalid inputs.
- Temporary files are cleaned in finally block.
- Automated backend tests cover key upload/report scenarios and expected error handling.
- Frontend automated tests exist but are minimal (example test only).

- Scalability
- Current architecture scales vertically only to a limited extent:
- SQLite single-file storage.
- Full-table replacement on each upload.
- In-process analytics, no caching layer, no distributed workers.
- Suitable baseline for prototype/small deployment; not yet optimized for large multi-user workloads.

---

# 6. PROJECT STRUCTURE

- Top-level context:
- Root contains sample retail CSV files and two application folders: Backend and Frontend.

- Backend folder responsibilities:
- main.py: FastAPI app init, lifespan DB init, CORS, router registration.
- database.py: SQLite connection, table creation, replace/fetch/clear operations.
- models.py: Table/column constants and data record dataclass.
- schemas.py: Pydantic response contracts for upload/dashboard/report.
- routers/upload.py: Upload endpoint orchestration (file save/read/clean/enrich/store).
- routers/dashboard.py: Dashboard/report endpoints.
- services/data_cleaning.py: ETL cleaning rules and warning generation.
- services/analytics.py: KPI and aggregation computations.
- services/insights.py: Insight text generation logic.
- services/file_handler.py: Upload file IO and preview creation.
- utils/helpers.py: Column normalization and DataFrame-to-JSON-safe conversion helpers.
- tests/test_api.py: End-to-end API behavior tests (upload/dashboard/report and negative cases).
- requirements.txt: Backend dependency specification.

- Frontend folder responsibilities:
- src/main.tsx: React entrypoint.
- src/App.tsx: Router tree and providers.
- src/pages/*: Route-level screens (landing/dashboard/upload/reports/insights/settings/not-found).
- src/components/dashboard/DashboardLayout.tsx: Shared dashboard shell.
- src/components/landing/*: Marketing/landing sections.
- src/components/ui/*: Reusable UI primitives (Radix/shadcn pattern).
- src/hooks/*: UI utility hooks.
- src/lib/utils.ts: Classname utility function.
- vite/tailwind/tsconfig/eslint files: Build, style, type, and lint configuration.
- vitest/playwright configs: Test framework setup.

- Important implementation note:
- The frontend framework is React + Vite (not Next.js).

---

# 7. APPENDIX

- Glossary of terms
- ETL: Process of importing and transforming raw sales files.
- KPI: Key metric for business performance (revenue/profit/etc.).
- Dead Stock: Product unsold beyond configured inactivity window.
- Low Performing Product: Product with low or negative profit/revenue outcome.
- Category Distribution: Aggregated revenue/profit/quantity by category.
- Sales Trend: Time-series aggregate of revenue/profit/quantity by date.
- Profit Margin: Ratio of profit to revenue.
- API: Application Programming Interface used by frontend to request backend data.

- Future scope based on current extensibility
- Connect frontend dashboard and insights pages to backend /dashboard for real-time data rendering.
- Implement authentication and authorization for protected operations.
- Add multi-user dataset isolation and role-aware access.
- Add append/merge upload mode in addition to full replace mode.
- Persist UI preferences (theme/settings) and implement settings actions.
- Expand test coverage:
- Frontend component/integration tests.
- End-to-end Playwright scenarios.
- Introduce production-grade observability, retries/timeouts, and stricter security controls.
- Consider migrating from SQLite to managed DB for higher concurrency and scale.
