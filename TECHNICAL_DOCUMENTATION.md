# MovieVerse AI -- Technical Documentation

## 1. Project Overview

**Project name:** MovieVerse AI -- LLM-Based Movie Recommendation
System\
**Application type:** Python-based interactive web application\
**User interface:** Streamlit\
**Core approach:** Movie data integration, machine learning analysis,
semantic retrieval using FAISS, and Gemini-powered recommendations.

MovieVerse AI is designed to help users explore movie information and
obtain AI-assisted recommendations. The application combines information
from five external data services with a local movie retrieval system.
The retrieved and collected information is assembled into a context that
is supplied to the Gemini recommendation service.



## 2. Problem Statement

Movie information is distributed across multiple platforms, including
movie databases, ratings services, streaming-availability services, news
sources, and encyclopedic resources. Users may need to consult several
sources to understand a movie and discover related titles.

MovieVerse AI addresses this problem by bringing selected movie
information into one interface and using retrieval-augmented generation
to provide contextual recommendations.

## 3. Objectives

-   Provide a single interface for movie discovery and exploration.
-   Collect movie information from multiple external data services.
-   Prepare movie-related context from the collected information.
-   Retrieve similar movie records from a local FAISS index.
-   Combine API-derived context and retrieved movie context.
-   Send the combined context to Gemini for recommendation generation.
-   Present application features and service status through a Streamlit
    interface.
-   Support dataset analysis and machine-learning experimentation.

## 4. Technology Stack

  -----------------------------------------------------------------------
  Technology                          Role in the project
  ----------------------------------- -----------------------------------
  Python                              Main programming language

  Streamlit                           Interactive web application

  Pandas and NumPy                    Dataset handling and numerical
                                      operations

  Scikit-learn                        Machine-learning experiments and
                                      evaluation

  Matplotlib and Altair               Data visualization

  Sentence Transformers               Text embedding generation (used in
                                      the retrieval pipeline)

  FAISS CPU                           Similarity search over movie
                                      embeddings

  Gemini API (`google-genai` /        AI recommendation generation
  `google-generativeai`)              

  Hugging Face Transformers / PyTorch Supporting model ecosystem and NLP
                                      dependencies

  Requests                            HTTP communication with external
                                      services

  python-dotenv                       Loading environment variables

  SpeechRecognition / PyAudio /       Voice-related dependencies; exact
  pyttsx3                             active application usage should be
                                      verified
  -----------------------------------------------------------------------

The project dependency file also contains Streamlit-related packages,
including `streamlit-option-menu`.

## 5. Project Architecture

The inspected application has the following high-level architecture:

``` text
                         USER
                           |
                           v
                 STREAMLIT APPLICATION
                         app.py
                           |
             +-------------+-------------+
             |                           |
             v                           v
       EXTERNAL DATA APIs          LOCAL RAG RETRIEVER
             |                           |
       +-----+------+                    v
       |     |      |              FAISS INDEX
      TMDB  OMDb  WatchMode               |
       |     |      |                     v
       +-----+------+              SIMILAR MOVIES
             |                           |
       +-----+------+                    |
       |            |                    |
     News API   Wikipedia                |
       |            |                    |
       +------+-----+--------------------+
              |
              v
       MOVIE CONTEXT BUILDER
       build_movie_context()
              |
              v
       COMBINED CONTEXT
       API DATA + FAISS RESULTS
              |
              v
       GEMINI SERVICE
       generate_recommendation()
              |
              v
       RECOMMENDATION DISPLAY
```

This diagram represents the flow confirmed in the inspected `app.py`
code. The application imports service functions with guarded
`try/except` blocks and records import errors so that unavailable
modules can be reported in the interface.

## 6. External Data Sources and Services

The main application imports the following services:

  Source           Imported function   Purpose
  ---------------- ------------------- -----------------------------------------
  TMDB             `search_movie`      Search for movie information
  OMDb             `search_movie`      Retrieve movie details and ratings
  WatchMode        `search_title`      Retrieve streaming-related information
  News API         `get_movie_news`    Retrieve movie-related news
  Wikipedia        `search_movie`      Retrieve encyclopedic movie information
  TMDB Discovery   `discover_movies`   Discover movies

The application also imports `build_movie_context` from
`services.movie_context`. The inspected recommendation code passes the
requested movie title and the five API result objects to this context
builder.

Actual API response fields, quotas, authentication requirements, and
fallback behavior should be documented from the corresponding service
modules and provider documentation.

## 7. Dataset Preparation and Data Fusion

The project contains movie datasets and intermediate outputs under
folders such as `DataSet/` and `fused_data/`. A fused dataset named
`movie_fused_18_columns.csv` was previously inspected and contained
**100 rows and 18 columns**.

Other project data artifacts include cleaned, processed, fused, and
RAG-oriented CSV files, as well as a movie embedding file and FAISS
index artifacts.

The project includes data preparation and fusion scripts such as:

-   `data_fusion.py`
-   `data_fusion_18.py`
-   `phase2_dataset.py`
-   `phase3_processing.py`
-   scripts under `fusion/` and `rag/`

**Important:** The exact authoritative input dataset, complete column
definitions, cleaning rules, duplicate-handling rules, and final dataset
lineage should be confirmed from the data-processing scripts before this
section is treated as a reproducibility record.

## 8. Exploratory Data Analysis

The project includes EDA scripts and chart outputs under `eda/`,
including charts for:

-   Movie release-year distribution
-   TMDB and IMDb rating distributions
-   TMDB versus IMDb ratings
-   Vote counts and popularity
-   Genres
-   Streaming platforms and regions
-   News counts
-   Runtime distribution
-   Rating versus popularity

These are chart topics inferred from the inspected output filenames.
Their exact calculations and interpretations should be taken from the
corresponding EDA scripts and generated reports.

## 9. Machine-Learning Experiments

Previously recorded experiment outputs include classification and
regression comparisons.

### 9.1 Classification

A recorded single-evaluation result reported Random Forest with 1.00
accuracy, precision, recall, and F1-score. A separate cross-validation
summary reported:

  Metric        Random Forest mean
  ----------- --------------------
  Accuracy                  0.9289
  Precision                 0.9474
  Recall                    0.9778
  F1-score                  0.9609

### 9.2 Regression

A recorded single-evaluation comparison reported Polynomial Regression
as the best of the compared regression approaches, with an R² score of
approximately 0.9027.

A separate cross-validation summary reported:

  Metric     Polynomial Regression mean
  -------- ----------------------------
  MAE                            0.2084
  RMSE                           0.3535
  R²                             0.6753

The cross-validation R² standard deviation was approximately 0.2772,
indicating variability across folds.

**Evaluation caution:** These results are recorded project outputs, not
independently reproduced in this documentation. The dataset size, split
strategy, target definition, preprocessing performed inside or outside
cross-validation, and potential leakage must be checked before making
claims about generalization. In particular, the single-evaluation 100%
classification result should not be presented as proof of perfect
real-world performance.

## 10. Retrieval-Augmented Generation (RAG)

The project includes a retrieval pipeline using Sentence Transformers
and FAISS.

Previously executed retrieval scripts reported: - An earlier index
containing 50 movie vectors. - A fused-data retrieval run containing 100
movie documents and 100 FAISS vectors. - An embedding dimension of 384
in the inspected run.

The main application imports:

``` python
from rag.retriever import build_rag_context
```

During recommendation generation, it calls:

``` python
faiss_context, faiss_results = build_rag_context(
    recommendation_movie,
    top_k=5
)
```

The retrieved context and result objects are stored in Streamlit session
state:

``` python
st.session_state.faiss_context = faiss_context
st.session_state.faiss_results = faiss_results
```

If retrieval fails, the application displays a warning. If the retriever
is unavailable, it displays the recorded import error.

Similarity scores are retrieval-ranking signals. They should not be
described as probabilities or recommendation accuracy unless separately
calibrated and evaluated.

## 11. Gemini Integration and Context Assembly

The main application imports:

``` python
from services.gemini_service import generate_recommendation
```

It first builds API context by calling `build_movie_context()` with: -
`movie_title` - `tmdb_data` - `omdb_data` - `watchmode_data` -
`news_data` - `wikipedia_data`

It then retrieves similar movies using FAISS and combines both sources
into a single context string with two labelled sections:

-   `REQUESTED MOVIE: FIVE API DATA`
-   `SIMILAR MOVIES: FAISS RETRIEVAL`

If no FAISS context is available, the combined context includes the
message: `No similar movies were retrieved.`

The inspected code then calls Gemini with:

``` python
result = generate_recommendation(
    user_query=recommendation_movie,
    movie_context=context
)
```

This confirms that the combined API and FAISS context is passed to the
Gemini service. The exact prompt template, Gemini model identifier,
generation settings, token limits, and response parsing should be
verified in `services/gemini_service.py`.

A previous Gemini test encountered a temporary HTTP 503 service-overload
response. This indicates that the request was unavailable at that time;
it does not, by itself, establish that the API key is invalid.
Successful live generation and systematic evaluation remain to be
demonstrated.

## 12. Main Application and Modules

The main entry point is `app.py`. It: - Configures the Streamlit page. -
Sets the project root on the Python import path. - Imports API,
discovery, context, Gemini, and FAISS services. - Handles service import
errors. - Builds movie context and retrieves similar movies during
recommendations. - Displays status and recommendation information in the
interface.

Important project directories include:

  Directory        Observed contents / role
  ---------------- --------------------------------------------------
  `api/`           API integration modules
  `services/`      Application service modules
  `rag/`           Cleaning, embedding, FAISS and retrieval scripts
  `fusion/`        Movie data fusion scripts
  `eda/`           EDA scripts, charts, reports and outputs
  `DataSet/`       Movie datasets and intermediate data artifacts
  `fused_data/`    Fused dataset, RAG data and experiment outputs
  `faiss_index/`   FAISS index and movie metadata artifacts
  `assets/`        Images used by the application
  `.streamlit/`    Streamlit configuration

The exact user-facing page list and every page's behavior should be
confirmed against the complete current `app.py` before final submission.

## 13. Installation and Execution

### 13.1 Prerequisites

-   A compatible Python installation.
-   A virtual environment.
-   Internet connectivity for external API requests and Gemini calls.
-   Required API credentials configured locally.

### 13.2 Install dependencies

From the project root, activate the virtual environment and install
dependencies:

``` powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 13.3 Configure environment variables

Create or update the local `.env` file with the API credentials required
by the service modules.

**Security:** Never publish `.env`, API keys, access tokens, or private
credentials in GitHub, screenshots, reports, or shared documentation.
Use placeholder names in public examples.

### 13.4 Run the application

``` powershell
streamlit run app.py
```

Open the local address printed by Streamlit in the terminal.

## 14. Error Handling and Limitations

The inspected main application uses guarded imports and stores
import-error messages for the API, context, Gemini, and FAISS services.
It also catches exceptions during FAISS retrieval and context
construction.

Known limitations and items requiring further validation include:

-   External API availability, rate limits, and response changes can
    affect results.
-   Gemini generation depends on external service availability and valid
    local credentials.
-   FAISS retrieval quality depends on the indexed dataset, embedding
    model, and query wording.
-   A retrieved similar movie is not necessarily a good recommendation;
    relevance requires human or benchmark evaluation.
-   The dataset is relatively small in the inspected fused-data run (100
    movies).
-   Recorded machine-learning metrics require leakage and validation
    review.
-   Voice-related dependencies are present, but their complete
    integration into the main workflow has not been verified.
-   The complete application flow and every UI feature should be tested
    from a clean environment before release.

## 15. Testing and Evaluation Status

Previously executed project checks include: - Python module compilation
checks during development. - Dataset and EDA script execution. - FAISS
retrieval tests using movie queries. - External API test scripts. -
Gemini service testing, which previously encountered a 503 overload
response.

A final test report should record, for each test, the date, input,
expected behavior, actual result, and pass/fail status. Do not label a
test as passed unless its successful output has been observed.

Recommended final tests: 1. Start the app from a fresh virtual
environment. 2. Test each external API independently. 3. Test
movie-context creation with partial API availability. 4. Test FAISS
retrieval for several known queries. 5. Confirm the retrieved FAISS
context reaches Gemini. 6. Test Gemini success and failure responses. 7.
Test the main user interface and all navigation items. 8. Verify that
secrets are excluded from version control.

## 16. Future Enhancements

-   Expand and periodically refresh the movie dataset.
-   Improve metadata quality and validate inconsistent records.
-   Evaluate retrieval with a fixed query set and relevance judgements.
-   Compare recommendations with and without FAISS context.
-   Record Gemini response quality using a repeatable evaluation rubric.
-   Add robust caching, retries, and clear API status reporting where
    appropriate.
-   Improve monitoring and structured logging.
-   Add automated tests for data preparation, retrieval, service
    integrations, and UI-critical logic.
-   Document reproducible dataset versions and model configurations.

## 17. Conclusion

MovieVerse AI brings together movie information from multiple external
services, local movie retrieval using FAISS, and Gemini-based
recommendation generation in a Streamlit application. The inspected
implementation constructs a combined context containing five-source API
information and FAISS-retrieved similar movies, then passes that context
to the Gemini recommendation function.

The project also includes data-fusion, exploratory-analysis,
machine-learning, and RAG preparation artifacts. Final performance and
feature claims should be supported by reproducible tests and validated
datasets before academic submission or public release.
