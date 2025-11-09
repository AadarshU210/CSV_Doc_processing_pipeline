# CSV File Processing Pipeline

A FastAPI-based asynchronous CSV file processing system that allows users to upload CSV files, process them in the background, and retrieve statistical insights.

## Features

- ✅ Upload multiple CSV files simultaneously
- ✅ Asynchronous background processing with concurrent execution
- ✅ Real-time status tracking for each file
- ✅ Extract insights: total rows, most frequent values, numerical averages
- ✅ CSV file validation
- ✅ PostgreSQL database for storing results
- ✅ RESTful API with automatic documentation

## Tech Stack

- **FastAPI** - Modern async web framework
- **PostgreSQL** - Database for storing file metadata and results
- **SQLAlchemy** (Async) - ORM for database operations
- **Pandas** - CSV processing and data analysis

## Installation

1. **Clone the repository**
   git clone https://github.com/AadarshU210/CSV_Doc_processing_pipeline.git
   cd csv-processing-pipeline


2. **Create virtual environment**


3. **Install dependencies**

4. **Setup PostgreSQL**

   update the db_url

5. **Start the server**
   uvicorn main:app --reload


6. **Access the API**
- Server: `http://127.0.0.1:8000`
- Interactive API docs: `http://127.0.0.1:8000/docs`
- Alternative docs: `http://127.0.0.1:8000/redoc`

## API Endpoints

### 1. Upload CSV Files
POST /upload
Content-Type: multipart/form-data

### 2. Check Processing Status
GET /status/{file_id}

### 3. Get Processing Results
GET /results/{file_id}

## How It Works

1. **Upload**: User uploads CSV files via `/upload` endpoint
2. **Validation**: System validates files are CSV format
3. **Storage**: Files are saved to `uploads/` directory and metadata stored in database
4. **Processing**: Background tasks process files concurrently using asyncio
5. **Status Updates**: Database tracks processing status for each file
6. **Results**: Extracted insights are stored and available via `/results` endpoint

## Key Features Explained

### Concurrent Processing
- Uses `asyncio.gather()` for concurrent file processing
- Each file gets its own database connection to avoid bottlenecks
- Significantly faster than sequential processing

### Status Tracking
- **pending**: File uploaded, waiting to process
- **in-progress**: Currently being processed
- **completed**: Processing finished successfully
- **failed**: Error occurred during processing

### Data Insights Extracted
- Total number of rows
- Most frequently occurring value in each column
- Average of all numerical columns

## License

MIT License

## Author

Aadi210

