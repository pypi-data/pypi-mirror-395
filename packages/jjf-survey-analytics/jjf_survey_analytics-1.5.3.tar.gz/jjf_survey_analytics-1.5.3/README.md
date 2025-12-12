# 📊 JJF Survey Analytics Platform

A comprehensive survey data management and analytics platform that reads data directly from Google Sheets into memory and provides powerful analytics dashboards with real-time data processing capabilities.

## 🎯 Project Intent

This platform is designed to:
- **Load** survey data directly from multiple Google Sheets sources
- **Process** data in-memory for fast access and analysis
- **Analyze** survey responses with statistical insights and visualizations
- **Monitor** response activity and respondent patterns
- **Refresh** automatically when the application restarts
- **Provide** a beautiful, responsive web interface for data exploration

## ✨ Key Features

- 📊 **Survey Analytics Dashboard** - Comprehensive statistics and visualizations
- ⚡ **In-Memory Processing** - Fast data access with no database overhead
- 📈 **Response Activity Monitoring** - Track who responded and when
- 🏥 **Health Check System** - Monitor API connectivity and system health
- 🔐 **Authentication** - Secure access with password protection
- 📱 **Responsive Design** - Beautiful Tailwind CSS interface for all devices
- 🚀 **Production Ready** - Deployable to Railway as lightweight application
- 🔒 **Single Source of Truth** - Google Sheets as authoritative data source, in-memory processing

### 🚀 Performance Features

- **TTL-Based Report Caching** (v1.2.6)
  - Configurable cache TTL via `REPORT_CACHE_TTL` environment variable
  - Default: 300 seconds (5 minutes)
  - 2,400x performance improvement: 120 seconds → 50ms (cached)
  - Automatic cache invalidation on data changes or TTL expiration

### 🔐 Data Integrity

- **Calculation Checksums** (v1.2.3)
  - SHA-256 checksums for all dimension calculations
  - Verifies calculation consistency across API responses
  - Enables audit trail and debugging

### 📊 JSON API Endpoints (v1.2.4)

- `GET /api/reports/organizations` - List all organizations with metadata
- `GET /api/reports/organization/<name>/json` - Full report with checksums
- `GET /api/reports/organization/<name>/verification` - Verification data only
- `GET /api/docs` - Interactive API documentation with examples
- CORS enabled for cross-origin requests

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for Google Sheets access)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Application
```bash
python app.py
```

### 5. Open in Browser
Navigate to: **http://localhost:8080**

**Authentication:**
- **Local Development:** No password required (disabled by default)
- **Production:** Set `REQUIRE_AUTH=true` and `APP_PASSWORD=your-password`

## 📁 Project Structure

```
jjf-survey-analytics/
├── app.py                          # Main Flask web application
├── railway_app.py                  # Railway-specific deployment app
├── survey_analytics.py             # Survey analytics engine
├── survey_normalizer.py            # Data normalization service
├── auto_sync_service.py            # Background auto-sync service
├── improved_extractor.py           # Google Sheets data extractor
├── healthcheck.py                  # Health check entry point
│
├── healthcheck/                    # Health check system
│   ├── api_validators.py          # API key validation
│   ├── dependency_checker.py      # External dependency checks
│   ├── e2e_tests.py               # End-to-end tests
│   ├── monitoring.py              # Continuous monitoring
│   └── config_validator.py        # Configuration validation
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── dashboard.html             # Main dashboard
│   ├── survey_analytics.html      # Survey analytics dashboard
│   ├── survey_dashboard.html      # Survey overview
│   ├── survey_responses.html      # Response activity monitor
│   ├── sync_dashboard.html        # Auto-sync management
│   ├── health_dashboard.html      # Health check dashboard
│   ├── spreadsheets.html          # Spreadsheets listing
│   ├── spreadsheet_detail.html    # Individual spreadsheet view
│   ├── jobs.html                  # Extraction jobs history
│   ├── login.html                 # Authentication page
│   └── error.html                 # Error page
│
├── hybrid_surveyor/                # Advanced CLI tool (optional)
│   ├── src/                       # Source code
│   ├── tests/                     # Test suite
│   └── docs/                      # Additional documentation
│
├── docs/                           # Project documentation
│   ├── PROGRESS.md                # Development progress
│   └── work-logs/                 # Work session logs
│
├── tests/                          # Test suite
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
│
├── surveyor_data_improved.db       # Raw spreadsheet data (SQLite)
├── survey_normalized.db            # Normalized survey data (SQLite)
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project configuration
├── Makefile                        # Development commands
├── Procfile                        # Railway deployment config
├── railway.toml                    # Railway configuration
└── README.md                       # This file
```

## 🎯 Core Features

### 📊 **Survey Analytics Dashboard** (`/surveys`)
- **Overview Statistics** - Total surveys, responses, respondents, response rates
- **Survey Breakdown** - Performance by survey type and name
- **Completion Statistics** - Visual completion rates with progress bars
- **Respondent Analysis** - Browser, device, and response frequency patterns
- **Beautiful Visualizations** - Color-coded charts and progress indicators

### 📈 **Detailed Analytics** (`/surveys/analytics`)
- **Question-Level Analysis** - Response rates and answer distributions
- **Statistical Insights** - Numeric averages, boolean counts, unique answers
- **Time Series Charts** - Response trends over time
- **Survey Filtering** - Focus on specific surveys
- **Export Capabilities** - CSV download and API access

### ⏰ **Response Activity Monitor** (`/surveys/responses`)
- **Timeline View** - When and who responded with detailed logs
- **Technology Analysis** - Browser and device usage patterns
- **Response Patterns** - Frequency analysis and daily activity
- **Real-time Updates** - Auto-refresh for live monitoring
- **Responsive Design** - Works on all devices

### 🔄 **Auto-Sync Management** (`/sync`)
- **Intelligent Change Detection** - Automatically finds new/updated data
- **Service Management** - Start/stop/configure sync service
- **Real-time Monitoring** - Live status and performance metrics
- **Manual Triggers** - Force immediate sync when needed
- **Activity Logging** - Detailed sync history and troubleshooting

### 🏥 **Health Check System** (`/health/dashboard`)
- **API Key Validation** - Verify Google Sheets API access
- **Dependency Monitoring** - Check external service availability
- **End-to-End Tests** - Validate complete data flow
- **Configuration Validation** - Ensure proper setup
- **Continuous Monitoring** - Background health checks

### 📋 **Spreadsheets Management** (`/spreadsheets`)
- **Grid View** - All imported spreadsheets
- **Search and Filter** - By title and type
- **Type Categorization** - Color-coded badges (Survey, Assessment, Inventory)
- **Row Count** - Last sync information
- **Direct Links** - To Google Sheets sources

### ⚙️ **Job Monitoring** (`/jobs`)
- **Extraction Job History** - Detailed progress tracking
- **Success/Failure Rates** - Error reporting
- **Real-time Status Updates** - For running jobs
- **Job Duration** - Performance metrics

## 🎨 **User Interface**

### **Design System**
- **Tailwind CSS** for modern, responsive design
- **Font Awesome icons** for visual clarity
- **Color-coded categories**:
  - 🔵 **Survey** - Blue theme
  - 🟢 **Assessment** - Green theme  
  - 🟣 **Inventory** - Purple theme
- **Mobile-first** responsive design

### **Interactive Features**
- **Hover effects** and smooth transitions
- **Copy-to-clipboard** functionality
- **Modal dialogs** for detailed views
- **Auto-refresh** for live data updates

## 🗄️ **Database Architecture**

### **Raw Data Database** (`surveyor_data_improved.db`)
1. **`spreadsheets`** - Metadata about each Google Sheet
2. **`raw_data`** - Actual spreadsheet data stored as JSON
3. **`extraction_jobs`** - Job tracking and history

### **Normalized Survey Database** (`survey_normalized.db`)
1. **`surveys`** - Survey metadata and configuration
2. **`survey_questions`** - Normalized question definitions
3. **`survey_responses`** - Individual response records
4. **`survey_answers`** - Detailed answer data with type parsing
5. **`respondents`** - Unique respondent tracking
6. **`sync_tracking`** - Auto-sync history and status
7. **`normalization_jobs`** - Process tracking and auditing

### **Key Features**
- **Relational Structure** - Proper foreign key relationships
- **Type Safety** - Automatic type detection and parsing
- **JSON Storage** - Flexible data structure for raw data
- **SHA256 Hashing** - Deduplication and change detection
- **Optimized Indexes** - Fast queries on all search fields
- **Data Integrity** - Foreign key constraints throughout

## 🏗️ **Architecture**

### **MVC Pattern** (v1.2.2+)

The application follows a Model-View-Controller architecture for clean separation of concerns:

- **Model** (`src/analytics/report_generator.py`): All calculation logic and dimension scoring
- **View** (`templates/`): Pure presentation layer with no business logic
- **Controller** (`app.py`): Request handling, caching, and routing

### **Calculation Checksums** (v1.2.3)

All dimension calculations include SHA-256 checksums for verification:
- Ensures calculation consistency across requests
- Enables result verification via API endpoints
- Provides audit trail for debugging and compliance
- Validates formula: `adjusted_score = max(0, min(5, base_score + total_modifier))`

### **Caching Strategy** (v1.2.6)

Multi-criteria cache validation ensures optimal performance while maintaining data freshness:

1. **Cache exists** for organization
2. **Response count matches** current data
3. **Cache age within TTL** (configurable, default 5 minutes)

**Cache invalidation triggers:**
- New survey responses added
- Admin edits applied to reports
- TTL expiration (configurable via `REPORT_CACHE_TTL`)

**Performance impact:**
- First request: ~120 seconds (with AI analysis)
- Cached requests: ~50ms (2,400x improvement)
- Cost reduction: Minimizes API calls for repeated report views

## 📈 **Supported Google Sheets**

The system currently supports **6 JJF Technology Assessment spreadsheets**:

| **Type** | **Count** | **Description** |
|----------|-----------|-----------------|
| **Survey** | 2 | Survey questions and response collection |
| **Assessment** | 3 | Technology maturity assessments (CEO, Staff, Tech Lead) |
| **Inventory** | 1 | Software systems inventory |

## 🛠️ **Development Setup**

### **Requirements**
- **Python 3.8+** (Python 3.13 recommended)
- **pip** - Python package manager
- **SQLite3** - Database (built into Python)
- **Internet connection** - For Google Sheets access

### **Installation**

#### Option 1: Quick Install
```bash
# Install all dependencies
pip install -r requirements.txt
```

#### Option 2: Development Setup with Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

#### Option 3: Using Make
```bash
# Set up development environment
make setup

# Activate virtual environment
source venv/bin/activate

# Install dependencies
make install
```

### **Initial Data Setup**

```bash
# 1. Extract data from Google Sheets
python improved_extractor.py

# 2. Normalize survey data
python survey_normalizer.py --auto

# 3. (Optional) Initialize health checks
python healthcheck.py
```

### **Running the Application**

```bash
# Start the web server
python app.py

# Access at http://localhost:8080
# No password required for local development
```

### **Environment Variables**

Create a `.env` file in the project root:

```bash
# Application Configuration
PORT=8080
SECRET_KEY=your-secret-key-here

# Authentication (disabled by default for local development)
REQUIRE_AUTH=false  # Set to 'true' for production
APP_PASSWORD=survey2025!  # Only used when REQUIRE_AUTH=true

# Cache Configuration (v1.2.6+)
REPORT_CACHE_TTL=300  # Cache TTL in seconds (default: 300 = 5 minutes)

# Database (for Railway deployment)
DATABASE_URL=postgresql://...  # Optional, uses SQLite if not set

# Logging
LOG_LEVEL=INFO

# Auto-Sync Configuration
AUTO_SYNC_INTERVAL=300  # seconds
```

**Environment Variable Reference:**

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Web server port | `8080` | No |
| `SECRET_KEY` | Flask session secret | Auto-generated | No |
| `REQUIRE_AUTH` | Enable password protection | `false` | No |
| `APP_PASSWORD` | Login password | `survey2025!` | No |
| `REPORT_CACHE_TTL` | Report cache TTL (seconds) | `300` | No |
| `DATABASE_URL` | PostgreSQL URL (Railway) | SQLite fallback | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `AUTO_SYNC_INTERVAL` | Auto-sync interval (seconds) | `300` | No |

### **Version Management**

The project includes a comprehensive Make-based version management system:

```bash
# Display current version information
make version

# Bump patch version (1.0.0 → 1.0.1) - bug fixes
make version-patch

# Bump minor version (1.0.0 → 1.1.0) - new features
make version-minor

# Bump major version (1.0.0 → 2.0.0) - breaking changes
make version-major

# Update build metadata only (no version bump)
make version-build
```

**Features:**
- Semantic versioning (major.minor.patch)
- Automatic git metadata extraction (commit hash, branch name)
- Build date and build number tracking
- Version displayed at application startup

**Workflow:**
1. Make changes to the codebase
2. Run `make version-patch` (or minor/major as appropriate)
3. Review changes: `git diff version.py`
4. Commit: `git add version.py && git commit -m "chore: bump version"`
5. Push: `git push origin main`

## 📊 **API Endpoints**

### **Web Routes**
- `GET /` - Main dashboard
- `GET /login` - Authentication page
- `GET /logout` - Logout
- `GET /spreadsheets` - Spreadsheets listing
- `GET /spreadsheet/<id>` - Individual spreadsheet view
- `GET /jobs` - Extraction jobs history
- `GET /surveys` - Survey analytics dashboard
- `GET /surveys/analytics` - Detailed question analysis
- `GET /surveys/responses` - Response activity monitor
- `GET /sync` - Auto-sync management dashboard
- `GET /health/dashboard` - Health check dashboard
- `GET /health/test` - Run health checks

### **API Routes**

#### Core API
- `GET /api/stats` - Dashboard statistics (JSON)
- `GET /api/spreadsheet/<id>/data` - Spreadsheet data (JSON)
- `GET /api/sync/status` - Auto-sync service status
- `POST /api/sync/start` - Start auto-sync service
- `POST /api/sync/stop` - Stop auto-sync service
- `POST /api/sync/force` - Force immediate sync
- `GET /api/survey/search` - Search survey responses
- `GET /api/survey/<id>/export` - Export survey data (CSV)
- `GET /health/status` - Health check status (JSON)
- `POST /health/check` - Run specific health checks

#### JSON Report API (v1.2.4+)
- `GET /api/reports/organizations` - List all organizations with metadata
- `GET /api/reports/organization/<name>/json` - Full organization report with checksums
- `GET /api/reports/organization/<name>/verification` - Verification data only (lightweight)
- `GET /api/docs` - Interactive API documentation with usage examples
- **Features:** CORS enabled, calculation checksums included, cache metadata exposed

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Database not found**
   ```bash
   # Run the extractor first
   python improved_extractor.py

   # Then normalize the data
   python survey_normalizer.py --auto
   ```

2. **Port already in use**
   ```bash
   # Change port via environment variable
   export PORT=8080

   # Or kill existing process
   lsof -ti:5001 | xargs kill -9  # Mac/Linux
   ```

3. **Google Sheets access denied**
   - Check if sheets are publicly accessible
   - Verify URLs are correct in the extractor
   - Check internet connection
   - Review API key configuration

4. **Authentication issues**
   ```bash
   # Disable authentication for testing
   export REQUIRE_AUTH=false

   # Or set custom password
   export APP_PASSWORD=your-password
   ```

5. **Auto-sync not working**
   - Check sync dashboard at `/sync`
   - Verify sync service is started
   - Review logs for errors
   - Ensure source data has changed

6. **Health checks failing**
   ```bash
   # Run health checks manually
   python healthcheck.py

   # Check specific components
   python healthcheck.py --api-only
   python healthcheck.py --deps-only
   ```

### **Debug Mode**
The web application runs in debug mode by default in development:
- **Auto-reload** on code changes
- **Detailed error messages** in browser
- **Interactive debugger** for exceptions
- **Verbose logging** to console

To disable debug mode (production):
```bash
export RAILWAY_ENVIRONMENT=production
```

## 📝 **Data Flow**

```
┌─────────────────────┐
│  Google Sheets      │
│  (Source Data)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  improved_extractor │
│  (Data Extraction)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  surveyor_data_     │
│  improved.db        │
│  (Raw Data)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  survey_normalizer  │
│  (Normalization)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  survey_normalized  │
│  .db (Relational)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Flask Application  │
│  (Web Interface)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  User Browser       │
│  (Dashboards)       │
└─────────────────────┘
```

## 🚀 **Deployment**

### **Local Development**
```bash
# Start the application
python app.py

# Access at http://localhost:8080
# No password required
```

### **Railway Deployment**

1. **Connect Repository**
   - Link your GitHub repository to Railway
   - Railway will auto-detect the Python project

2. **Configure Environment Variables**
   ```bash
   APP_PASSWORD=your-secure-password
   SECRET_KEY=your-secret-key
   REQUIRE_AUTH=true
   ```

3. **Deploy**
   - Railway will automatically build and deploy
   - Health checks at `/health/status`
   - PostgreSQL database automatically provisioned

4. **Access**
   - Your app will be available at `https://your-app.railway.app`

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed deployment instructions.

## 📚 **Additional Documentation**

- [FINAL_IMPLEMENTATION_SUMMARY.md](FINAL_IMPLEMENTATION_SUMMARY.md) - Complete feature overview
- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Railway deployment guide
- [AUTHENTICATION_CONFIG.md](AUTHENTICATION_CONFIG.md) - Authentication setup
- [AUTO_SYNC_IMPLEMENTATION.md](AUTO_SYNC_IMPLEMENTATION.md) - Auto-sync details
- [HEALTHCHECK_README.md](HEALTHCHECK_README.md) - Health check system
- [hybrid_surveyor/README.md](hybrid_surveyor/README.md) - Advanced CLI tool

## 🧪 **Testing**

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test suite
python -m pytest tests/unit -v
python -m pytest tests/integration -v

# Run health checks
python healthcheck.py
```

## 🎯 **Use Cases**

### **Survey Analysis**
- Analyze response patterns across multiple surveys
- Track completion rates and respondent engagement
- Identify trends in survey responses over time
- Export data for external analysis

### **Data Management**
- Centralized view of all survey data
- Automatic synchronization with Google Sheets
- Historical tracking of data changes
- Audit trail for all operations

### **Monitoring**
- Real-time health checks of system components
- API key validation and dependency monitoring
- Response activity tracking
- System performance metrics

## 🏆 **Current Status**

### **Production Ready Features**
- ✅ **22 survey responses** processed across 5 surveys
- ✅ **240 questions** normalized with proper typing
- ✅ **585 answers** analyzed with statistical insights
- ✅ **13 unique respondents** tracked
- ✅ **Auto-sync service** with intelligent change detection
- ✅ **Health check system** with comprehensive monitoring
- ✅ **Authentication** with password protection
- ✅ **Railway deployment** ready with PostgreSQL support
- ✅ **Responsive design** for all devices
- ✅ **REST API** for programmatic access

### **Supported Survey Types**
| **Type** | **Count** | **Description** |
|----------|-----------|-----------------|
| **Survey** | 2 | Survey questions and response collection |
| **Assessment** | 3 | Technology maturity assessments (CEO, Staff, Tech Lead) |
| **Inventory** | 1 | Software systems inventory |

---

## 🌐 **Access Points**

**Local Development:**
- **Main Application:** http://localhost:8080
- **Survey Analytics:** http://localhost:8080/surveys
- **Auto-Sync Dashboard:** http://localhost:8080/sync
- **Health Dashboard:** http://localhost:8080/health/dashboard

**Authentication:**
- **Local:** No password required (disabled by default)
- **Production:** Set `REQUIRE_AUTH=true` and configure `APP_PASSWORD`

---

## 📞 **Support**

For issues, questions, or contributions:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [additional documentation](#-additional-documentation)
3. Run health checks: `python healthcheck.py`
4. Check application logs for detailed error messages

---

**Built with ❤️ using Flask, SQLite, and Tailwind CSS**
