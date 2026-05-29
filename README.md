# SmartRetail - Automated Business Intelligence for Retail Sales Data

A full-stack web application that provides automated business intelligence and analytics for retail/shop sales data. Upload your transaction files (CSV/XLS/XLSX), and get instant insights, KPIs, dashboards, and automated reports.

## 🎯 Features

- **📤 File Upload & Data Processing**: Support for CSV, Excel (XLS/XLSX) file uploads with automatic header normalization
- **🧹 Intelligent Data Cleaning**: Automatic data validation, missing value handling, and data standardization
- **📊 Advanced Analytics**: Real-time KPI calculations including revenue, profit, margins, and trends
- **💡 Automated Insights**: AI-generated business insights detecting dead stock, low-performing products, and demand spikes
- **📈 Interactive Dashboard**: Visual analytics with charts and KPIs
- **📋 Report Generation**: Export analytics to CSV and PDF formats
- **🎨 Responsive UI**: Modern, intuitive interface with dark mode support
- **⚡ Real-time Processing**: Fast ETL pipeline powered by Pandas and FastAPI

## 📋 Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** & **npm** (for frontend)
- **Git** (optional)

## 🚀 Quick Start

### 1️⃣ Setup Backend

```powershell
# Create Python virtual environment
python -m venv .venv

# Activate virtual environment (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
cd Backend
pip install -r requirements.txt
cd ..
```

### 2️⃣ Setup Frontend

```powershell
cd Frontend
npm install
cd ..
```

### 3️⃣ Start the Application

**Terminal 1 - Backend Server:**
```powershell
# Ensure virtual environment is activated
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

cd Backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend Server:**
```powershell
cd Frontend
npm run dev
```

### 4️⃣ Access the Application

- **Frontend**: http://localhost:8080
- **Backend API Docs**: http://localhost:8000/docs (Swagger UI)
- **Backend ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
data-for-shops/
├── Backend/                    # FastAPI backend server
│   ├── main.py                # Application entry point
│   ├── database.py            # SQLite database setup
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── requirements.txt        # Python dependencies
│   ├── routers/
│   │   ├── upload.py          # File upload endpoints
│   │   └── dashboard.py       # Analytics endpoints
│   ├── services/
│   │   ├── file_handler.py    # File I/O and processing
│   │   ├── data_cleaning.py   # ETL and data validation
│   │   ├── analytics.py       # KPI and metrics calculation
│   │   └── insights.py        # Insight generation logic
│   ├── utils/
│   │   └── helpers.py         # Utility functions
│   └── tests/
│       └── test_api.py        # API endpoint tests
│
├── Frontend/                   # React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx            # Main app component
│   │   ├── main.tsx           # Entry point
│   │   ├── pages/             # Page components
│   │   │   ├── Index.tsx      # Landing page
│   │   │   ├── DashboardHome.tsx
│   │   │   ├── UploadPage.tsx
│   │   │   ├── ReportsPage.tsx
│   │   │   ├── InsightsPage.tsx
│   │   │   └── SettingsPage.tsx
│   │   ├── components/        # Reusable components
│   │   │   ├── landing/       # Landing page sections
│   │   │   ├── dashboard/     # Dashboard components
│   │   │   └── ui/            # Radix UI components
│   │   ├── hooks/             # Custom React hooks
│   │   └── lib/               # Utility functions
│   ├── package.json           # NPM dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── tailwind.config.ts     # Tailwind CSS config
│   ├── tsconfig.json          # TypeScript configuration
│   └── vitest.config.ts       # Testing configuration
│
├── requirements.txt           # Root-level Python dependencies
├── smart_retail_data.csv      # Sample dataset
└── README.md                  # This file
```

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI web server
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Data Processing**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
- **File Handling**: [OpenPyXL](https://openpyxl.readthedocs.io/) for Excel support
- **Testing**: [pytest](https://pytest.org/)

### Frontend
- **Library**: [React 18](https://react.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **UI Components**: Radix UI + shadcn/ui
- **Routing**: [React Router](https://reactrouter.com/)
- **State Management**: [TanStack Query](https://tanstack.com/query/)
- **Charts**: [Recharts](https://recharts.org/)
- **Animation**: [Framer Motion](https://www.framer.com/motion/)
- **Export**: [jsPDF](https://github.com/parallax/jsPDF)
- **Testing**: [Vitest](https://vitest.dev/) + [Playwright](https://playwright.dev/)

## 📊 API Endpoints

### Health Check
- `GET /health` - Service availability check

### Upload Endpoints
- `POST /upload` - Upload and process CSV/XLS/XLSX files
  - Returns: Dataset preview (first 10 rows) + upload validation summary

### Dashboard Endpoints
- `GET /dashboard` - Get comprehensive dashboard data
  - KPIs, sales trends, top products, low-performing products, category distribution, dead stock, insights
- `GET /report` - Generate downloadable report with all analytics data

## 📈 Data Analytics Features

### Key Performance Indicators (KPIs)
- **Total Revenue**: Sum of all revenue
- **Total Profit**: Sum of all profit
- **Unique Products**: Count of distinct products
- **Average Profit Margin**: Mean profit margin across transactions

### Analytics Generated
- **Sales Trends**: Time-series revenue and profit progression
- **Top Products**: Best-selling and most profitable products
- **Low-Performing Products**: Products with negative or minimal profit
- **Category Distribution**: Sales breakdown by product category
- **Dead Stock**: Products with no sales in the last 30 days
- **Automated Insights**: Text-based alerts and recommendations

## 🧹 Data Cleaning Pipeline

The system automatically:
1. **Normalizes column headers** to standard names
2. **Validates required columns** (date, quantity, price, product_name, category, profit)
3. **Handles missing values** using median imputation for prices
4. **Coerces data types** (dates, numerics)
5. **Filters invalid rows** (negative quantities, invalid prices/dates)
6. **Calculates financial metrics** (revenue, profit margin)

## 🧪 Testing

### Backend Tests
```powershell
cd Backend
pytest
```

### Frontend Tests
```powershell
cd Frontend
npm run test        # Run once
npm run test:watch  # Watch mode
```

## 🔧 Development

### Linting Frontend
```powershell
cd Frontend
npm run lint
```

### Building Frontend
```powershell
cd Frontend
npm run build       # Production build
npm run preview     # Preview production build
```

## 📝 Sample Data

Sample datasets are provided:
- `smart_retail_data.csv` - Full dataset
- `smart_retail_data_500_rows_v2.csv` - 500-row sample

Expected CSV columns:
- `date` - Transaction date
- `quantity` - Quantity sold
- `price` - Unit price
- `product_name` - Product name
- `category` - Product category
- `profit` - Profit amount

## ⚙️ Configuration

### Backend
- API runs on `http://localhost:8000` by default
- CORS origins: `localhost:3000`, `localhost:8080`
- Database: SQLite stored in backend directory

### Frontend
- Dev server runs on `http://localhost:8080` by default
- Backend URL configured in environment variables or API client

## 📋 Current Limitations

- **No Authentication**: All users see the same dataset (single-tenant)
- **No Authorization**: No role-based access control
- **Single Dataset**: Uploads replace the entire dataset (no append mode)
- **No Real-time Updates**: Dashboard requires manual refresh
- **Dashboard/Insights Mock**: Currently static UI; backend integration in progress

## 🚀 Future Enhancements

- User authentication and authorization
- Multi-tenant support with data isolation
- Incremental dataset updates (append/merge)
- Real-time data streaming
- Advanced forecasting and predictive analytics
- Export to more formats (Excel, etc.)
- API rate limiting and request throttling
- Database migration to PostgreSQL for production

## 📚 Documentation

For more details, see:
- [SRS_Codebase_Analysis.md](SRS_Codebase_Analysis.md) - Detailed system requirements
- [start.md](start.md) - Setup guide
- FastAPI Docs: http://localhost:8000/docs (when running)

## 🤝 Contributing

1. Ensure all tests pass before committing
2. Follow existing code style and structure
3. Update this README for significant changes
4. Test both backend and frontend thoroughly

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review existing code and tests
3. Check the API documentation at `/docs` endpoint

## 📄 License

[Add your license here]

---

**Last Updated**: May 2026

