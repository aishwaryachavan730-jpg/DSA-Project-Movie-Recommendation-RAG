# 🎬 MovieVerse AI – LLM & RAG Based Movie Recommendation System

An intelligent movie recommendation and discovery application powered by Machine Learning, Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG).

MovieVerse AI helps users discover movies, explore movie information, view recommendations, and interact with an AI-powered movie assistant.

---

## 📌 1. Project Overview

MovieVerse AI is a Python-based movie recommendation application that combines movie datasets, Machine Learning, external movie APIs, and AI-powered question answering.

The system integrates movie information from multiple sources and uses a FAISS-based retrieval system with an LLM to provide relevant movie-related responses.

**Main objective:** To develop an intelligent and interactive movie discovery platform that combines traditional recommendation techniques with modern Generative AI and RAG technology.

## ✨ 2. Key Features

- **Movie Search:** Search for movie information.
- **Latest Movies:** Explore recently released movies.
- **AI Movie Recommendation:** Get movie recommendations.
- **AI Movie Chatbot:** Ask movie-related questions using an LLM.
- **RAG-Based Retrieval:** Retrieve relevant movie information using FAISS.
- **Movie News:** Explore movie-related news.
- **Movie Details:** Access movie information through external APIs.
- **Machine Learning:** Analyze movie datasets and evaluate ML algorithms.
- **Data Visualization:** Explore movie trends, ratings, and genres.
- **API Dashboard:** Monitor integrated API functionality.

## 🧰 3. Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / Interface | Streamlit |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Data Visualization | Matplotlib |
| Generative AI | Gemini |
| LLM Framework | LangChain |
| Vector Search | FAISS |
| Embeddings | Sentence Transformers |
| External APIs | TMDB, OMDb, WatchMode, News API, Wikipedia |
| Development Tool | Visual Studio Code |
| Version Control | Git and GitHub |

## 🔌 4. External APIs

MovieVerse AI integrates multiple external data services:

1. **TMDB API** – Movie search and movie information.
2. **OMDb API** – Movie details and IMDb ratings.
3. **WatchMode API** – Streaming availability information.
4. **News API** – Movie-related news articles.
5. **Wikipedia** – Additional movie-related information.
6. **Gemini API** – AI-powered movie question answering.

## 🤖 5. Machine Learning and AI

### Machine Learning

The project includes movie dataset processing, feature analysis, classification, regression, and model evaluation.

The analysis explores:
- Movie ratings.
- Movie genres.
- Movie release years.
- Rating-based classification.
- Regression-based rating prediction.
- Model performance metrics.

### Retrieval-Augmented Generation (RAG)

The RAG workflow combines information retrieval with AI-generated responses.

**Workflow:**

1. Load and prepare movie information.
2. Convert movie information into text documents.
3. Generate vector embeddings.
4. Store and search embeddings using FAISS.
5. Retrieve relevant movie information.
6. Pass retrieved context to the LLM.
7. Generate a contextual response.

## 📊 6. Dataset and EDA Visualizations

The project includes a fused movie dataset containing 18 columns.

Data preparation and exploratory analysis help understand movie ratings, genres, and release-year distributions.

### Movies by Year

![Movies by Year](Movies%20by%20year.png)

### TMDB Movie Rating Distribution

![TMDB Movie Rating Distribution](TMDB%20Movie%20Rating%20Distribution.png)

### Top 10 Movie Genres

![Top 10 Movie Genres](Top%2010%20Movie%20Genres.png)

### Top 10 Rated Movies

![Top 10 Rated Movies](Top%2010%20Rated%20Movies.png)

### Additional Movies by Year Visualization

![Movies by Year Additional](Movies%20by%20year%201.png)

## 🏗️ 7. Project Architecture

The application follows a modular architecture:

- **User Interface:** Streamlit application.
- **API Integration:** Separate modules for external API services.
- **Data Processing:** Dataset cleaning, fusion, and preparation.
- **Machine Learning:** Model training and evaluation.
- **RAG System:** Document preparation, embeddings, and FAISS retrieval.
- **LLM Integration:** Gemini-powered AI responses.

### Simplified Workflow

User → Streamlit Interface → Movie Search / Recommendation → APIs and Dataset → RAG Retrieval → Gemini → AI Response

## 📁 8. Project Structure

```text
Movie-Recommendation-RAG/
│
├── app.py
│
├── api/
│   ├── gemini_api.py
│   ├── news_api.py
│   ├── omdb_api.py
│   ├── tmdb_api.py
│   └── watchmode_api.py
│
├── rag/
│   └── rag_retrieval.py
│
├── DataSet/
│   ├── MovieVerse_Fused_18_Columns.csv
│   └── sample_movies.csv
│
├── fused_data/
│   └── ML_Results/
│
├── services/
│
├── data_fusion.py
├── data_fusion_18.py
├── data_quality.py
├── eda_fused_18.py
├── fusion_analysis.py
├── rag_prepare.py
├── visualization.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

*Note: This is a simplified overview. Some folders and files may contain additional modules.*

## ⚙️ 9. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/aishwaryachavan730-jpg/DSA-Project-Movie-Recommendation-RAG.git
```

### Step 2: Open the project folder

```bash
cd DSA-Project-Movie-Recommendation-RAG
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure API credentials

Configure the required API credentials using Streamlit secrets or environment variables, according to the API modules.

Do not upload API keys, passwords, `.env` files, or secret configuration files to GitHub.

### Step 7: Run the application

```bash
streamlit run app.py
```

## 📈 10. Project Outcomes

MovieVerse AI demonstrates the integration of:

- Data preprocessing and data fusion.
- Exploratory Data Analysis.
- Machine Learning experimentation.
- External API integration.
- Vector embeddings and similarity search.
- Retrieval-Augmented Generation.
- Large Language Model integration.
- Interactive application development.

## 🔐 11. Security Notes

- API credentials must remain private.
- Use Streamlit secrets or environment variables.
- Never commit `.env` or secret configuration files.
- Follow the usage limits and terms of each external API.

## 🚀 12. Future Enhancements

- Personalized recommendations based on user preferences.
- Improved recommendation ranking.
- More advanced hybrid recommendation techniques.
- Enhanced movie filtering and search.
- Improved conversational memory.
- Additional movie information sources.
- Deployment to a cloud hosting platform.

## 👩‍💻 13. Developer

**Project:** MovieVerse AI – LLM & RAG Based Movie Recommendation System

**Repository:** [MovieVerse AI on GitHub](https://github.com/aishwaryachavan730-jpg/DSA-Project-Movie-Recommendation-RAG)

---

⭐ If you find this project interesting, consider giving the repository a star!