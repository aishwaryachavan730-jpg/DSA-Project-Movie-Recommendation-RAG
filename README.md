# 🎬 MovieVerse AI – LLM & RAG Based Movie Recommendation System

**Intelligent movie discovery and recommendation powered by Machine Learning, Large Language Models, and Retrieval-Augmented Generation.**

MovieVerse AI is an academic Streamlit application that brings movie discovery, recommendation, movie information, news, and AI-powered question answering into one platform. It combines movie dataset processing, exploratory data analysis, machine-learning experiments, multiple external APIs, vector embeddings, FAISS retrieval, and Gemini-powered responses.

---

## 1. Project Overview

Movie information is distributed across different movie databases, rating platforms, streaming services, and entertainment news sources. Finding relevant movie information and recommendations often requires switching between multiple platforms.

MovieVerse AI aims to simplify this process through a unified movie discovery application.

The project combines:

- Movie dataset collection and preparation.
- Data cleaning and data fusion.
- Exploratory Data Analysis (EDA).
- Machine Learning experimentation.
- External movie and news API integration.
- Large Language Model integration.
- Retrieval-Augmented Generation (RAG).
- Interactive Streamlit dashboards.

**Main objective:** To develop an intelligent movie recommendation and discovery system that combines Data Science techniques with Generative AI.

## 2. Key Features

| Feature | Description |
|---|---|
| Movie Search | Search for movies and explore available movie information |
| Latest Movies | Discover recently released movies using external movie data |
| AI Movie Recommendation | Explore AI-assisted movie recommendations |
| Movie Chatbot | Ask movie-related questions and receive AI-generated responses |
| RAG-Based Retrieval | Retrieve relevant movie information using embeddings and FAISS |
| Movie News | Explore movie-related news articles |
| Movie Details | Access movie information through integrated APIs |
| Machine Learning | Perform classification, regression, and model evaluation experiments |
| EDA Dashboard | Analyze movie ratings, genres, and release-year distributions |
| API Dashboard | Explore the integrated API services |
| JSON Results | View structured movie information and API results |

## 3. APIs and Data Sources

MovieVerse AI integrates multiple external services.

| API / Source | Purpose |
|---|---|
| TMDB API | Movie search, movie information, and movie discovery |
| OMDb API | Movie details, IMDb ratings, and related information |
| WatchMode API | Streaming availability information |
| News API | Movie-related news articles |
| Wikipedia | Additional movie-related information |
| Gemini API | LLM-powered movie question answering |

API availability and returned information depend on the provider, API configuration, and network access.

## 4. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Application Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Data Visualization | Matplotlib |
| LLM Integration | Gemini |
| LLM Framework | LangChain |
| Vector Database / Search | FAISS |
| Text Embeddings | Sentence Transformers |
| External APIs | TMDB, OMDb, WatchMode, News API, Wikipedia |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |

## 5. System Workflow and Architecture

MovieVerse AI follows a modular workflow that connects movie datasets, external APIs, machine learning, and RAG-based question answering.

### Overall System Workflow

```text
             USER
               |
               v
       STREAMLIT APPLICATION
               |
      +--------+---------+
      |        |         |
      v        v         v
  Movie     Movie     AI Movie
  Search    News    Recommendation
      |        |         |
      +--------+---------+
               |
               v
       EXTERNAL DATA APIs
               |
      +--------+---------+
      |        |         |
      v        v         v
     TMDB    OMDb    WatchMode
      |        |         |
      +--------+---------+
               |
               v
        MOVIE DATASET
               |
               v
       DATA PREPROCESSING
               |
               v
          DATA FUSION
               |
         +-----+------+
         |            |
         v            v
      EDA / ML    MOVIE DOCUMENTS
         |            |
         v            v
    VISUALIZATION   CHUNKING
                      |
                      v
                  EMBEDDINGS
                      |
                      v
                  FAISS INDEX
                      |
                      v
                RELEVANT RETRIEVAL
                      |
                      v
                  GEMINI LLM
                      |
                      v
                AI-GENERATED RESPONSE
```

### RAG Workflow

The Retrieval-Augmented Generation component combines information retrieval with an LLM.

1. Prepare and process movie information.
2. Convert relevant movie records into text documents.
3. Generate vector embeddings using an embedding model.
4. Store and search vectors using FAISS.
5. Retrieve relevant movie information for a user query.
6. Provide retrieved context to the LLM.
7. Generate a contextual movie-related response.

## 6. Dataset and Data Processing

The project uses movie information collected and prepared for analysis and recommendation experiments.

### Data Processing Activities

- Dataset inspection and exploration.
- Data cleaning and quality checking.
- Handling relevant missing or inconsistent values.
- Movie information integration.
- Data fusion.
- Preparation of an 18-column fused movie dataset.
- Exporting processed datasets for analysis and application use.

### Dataset Deliverables

- Fused movie dataset in CSV format.
- Sample movie dataset.
- Excel versions of fused datasets.
- Data quality reports.
- Data fusion analysis and documentation.

## 7. Exploratory Data Analysis (EDA)

EDA is performed to understand the characteristics and distribution of movie data.

The visualizations explore:

- Movie release-year distribution.
- TMDB movie rating distribution.
- Most common movie genres.
- Top-rated movies.
- Movie trends across years.

### EDA 

**1. Movies by Year**

![Movies by Year](Movies%20by%20year.png)

**2. TMDB Movie Rating Distribution**

![TMDB Movie Rating Distribution](TMDB%20Movie%20Rating%20Distribution.png)

**3. Top 10 Movie Genres**

![Top 10 Movie Genres](Top%2010%20Movie%20Genres.png)

**4. Top 10 Rated Movies**

![Top 10 Rated Movies](Top%2010%20Rated%20Movies.png)

**5. Additional Movies by Year Analysis**

![Additional Movies by Year](Movies%20by%20year%201.png)

## 8. Machine Learning and Model Evaluation

The project includes classification and regression experiments on the prepared movie dataset.

### Classification

The classification experiment uses movie rating categories, including:

- High rating.
- Low rating.

Algorithms evaluated in the project include:

- Naive Bayes.
- Support Vector Machine (SVM).
- Random Forest.
- Other implemented classification models.

### Regression

Regression experiments explore the prediction of movie ratings using available dataset features.

Algorithms and approaches include:

- Linear Regression.
- Polynomial Regression.
- Random Forest Regression.

### Performance Metrics

| Metric | Purpose |
|---|---|
| Accuracy | Measures the proportion of correct classifications |
| Precision | Measures how many predicted positive cases are correct |
| Recall | Measures how many actual positive cases are identified |
| F1-Score | Combines precision and recall |
| MAE | Measures average absolute prediction error |
| RMSE | Measures the square root of mean squared prediction error |
| R² Score | Measures the proportion of variance explained by a regression model |

Model performance should be interpreted in relation to the dataset size, feature selection, class distribution, and evaluation methodology.

## 9. Application Screenshots

The following screenshots can be added to demonstrate the working application.

| Application Module | Screenshot |
|---|---|
| Home Page | `screenshots/home.png` |
| Movie Search | `screenshots/movie_search.png` |
| Latest Movies | `screenshots/latest_movies.png` |
| AI Recommendation | `screenshots/ai_recommendation.png` |
| Movie News | `screenshots/movie_news.png` |
| API Dashboard | `screenshots/api_dashboard.png` |
| EDA Dashboard | `screenshots/eda_dashboard.png` |
| ML Results | `screenshots/ml_results.png` |

*Add your actual application screenshots in the screenshots folder using the filenames above.*

## 10. Project Structure

```text
Movie-Recommendation-RAG/
│
├── api/
│   ├── gemini_api.py
│   ├── news_api.py
│   ├── omdb_api.py
│   ├── tmdb_api.py
│   └── watchmode_api.py
│
├── DataSet/
│   ├── MovieVerse_Fused_18_Columns.csv
│   └── sample_movies.csv
│
├── fused_data/
│   ├── EDA/
│   └── ML_Results/
│
├── rag/
│   └── rag_retrieval.py
│
├── services/
│
├── screenshots/
│
├── data_fusion.py
├── data_fusion_18.py
├── data_quality.py
├── eda_fused_18.py
├── fusion_analysis.py
├── rag_prepare.py
├── visualization.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

*This is a simplified project structure. Refer to the repository for the complete list of modules and files.*

## 11. Installation and Local Setup

### Prerequisites

- Python 3.10 or newer.
- Git.
- Visual Studio Code or another Python IDE.
- Internet connection for external API access.
- Required API credentials.

### Step 1: Clone the Repository

```bash
git clone https://github.com/aishwaryachavan730-jpg/DSA-Project-Movie-Recommendation-RAG.git
```

### Step 2: Open the Project Directory

```bash
cd DSA-Project-Movie-Recommendation-RAG
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure API Credentials

Configure the API credentials required by the project.

For Streamlit applications, secrets can be configured in:

```text
.streamlit/secrets.toml
```

Example configuration:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TMDB_API_KEY = "your_tmdb_api_key"
OMDB_API_KEY = "your_omdb_api_key"
WATCHMODE_API_KEY = "your_watchmode_api_key"
NEWS_API_KEY = "your_news_api_key"
```

Use only the credentials required by your application. Do not commit real API keys, passwords, `.env` files, or secret configuration files to GitHub.

### Step 7: Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, normally:

```text
http://localhost:8501
```

## 12. Project Outcomes

MovieVerse AI demonstrates the practical integration of:

- Python-based application development.
- Data preprocessing and data fusion.
- Exploratory Data Analysis.
- Machine Learning model experimentation.
- Performance evaluation.
- Multiple external API integrations.
- Text embeddings and vector similarity search.
- FAISS-based information retrieval.
- Large Language Model integration.
- Retrieval-Augmented Generation.
- Interactive Streamlit application development.

## 13. Limitations

- External API availability depends on service providers and network connectivity.
- API rate limits may affect movie searches and data retrieval.
- Movie information may vary across different data sources.
- Recommendation quality depends on the available dataset and implemented recommendation logic.
- Machine Learning results depend on dataset size, data quality, and feature selection.
- RAG responses may contain incomplete or inaccurate information.
- Streaming availability can vary by country and provider.
- Some features require valid API credentials.

## 14. Future Enhancements

- Personalized movie recommendations based on user preferences.
- Hybrid recommendation using content-based and collaborative filtering.
- Improved recommendation ranking and evaluation.
- Advanced conversational memory for the movie chatbot.
- More movie and streaming data integrations.
- User accounts and saved movie lists.
- Cloud deployment and improved application performance.

## 15. Academic Project Information

**Project Title:** MovieVerse AI – LLM & RAG Based Movie Recommendation System

**Project Domain:** Artificial Intelligence, Machine Learning, Data Science, and Generative AI

**Degree:** Master of Computer Applications (MCA)

**Institution:** SNDT Women's University, Mumbai, Maharashtra, India

**Project Repository:** [MovieVerse AI – GitHub](https://github.com/aishwaryachavan730-jpg/DSA-Project-Movie-Recommendation-RAG)

## 16. Security and Responsible Use

- API keys and credentials must be stored securely.
- Follow the terms and rate limits of external API providers.
- Do not expose private credentials in source code or public repositories.
- AI-generated information should be treated as informational and verified when necessary.

## 17. Developer

**MovieVerse AI – LLM & RAG Based Movie Recommendation System**

Developed as an academic MCA project.

---

⭐ If you find this project interesting, please consider starring the repository.

**GitHub Repository:**  
https://github.com/aishwaryachavan730-jpg/DSA-Project-Movie-Recommendation-RAG