import streamlit as st
import pandas as pd
import faiss
from image_to_text import image_caption
from chatbot import chatbot

from sentence_transformers import SentenceTransformer
from streamlit_option_menu import option_menu
from voice import listen, speak

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="🎬 AI Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#0E1117;
    color:white;
}

div.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------

@st.cache_resource
def load_model():

    model = SentenceTransformer("all-MiniLM-L6-v2")

    index = faiss.read_index("faiss_index/movie_index.faiss")

    movies = pd.read_csv("faiss_index/movie_metadata.csv")

    return model,index,movies


model,index,movies = load_model()

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

if "favorites" not in st.session_state:
    st.session_state.favorites=[]

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

with st.sidebar:

    selected = option_menu(

        "🎬 Movie AI",

        [
            "Home",
            "Movie Search",
            "Popular",
            "Favorites",
            "Image Search",
            "Movie Chatbot",
            "About"
        ],

        icons=[
            "house",
            "search",
            "fire",
            "heart",
            "image",
            "robot",
            "info-circle"
        ],

        default_index=0
    )
# ----------------------------------------------------
# HOME
# ----------------------------------------------------

if selected=="Home":

    st.title("🎬 AI Movie Recommendation System")

    try:
        st.image("assets/banner.jpg",use_container_width=True)
    except:
        st.info("Add banner.jpg inside assets folder.")

    st.markdown("""
### Welcome 👋

This project uses

✅ Artificial Intelligence

✅ FAISS Vector Database

✅ Sentence Transformers

✅ Retrieval Augmented Generation (RAG)

✅ Semantic Search

Search movies using AI and discover similar movies instantly.
""")

# ----------------------------------------------------
# MOVIE SEARCH
# ----------------------------------------------------

elif selected=="Movie Search":

    st.title("🔍 AI Movie Search")

    col1,col2=st.columns([5,1])

    with col1:

        query=st.text_input(
            "Movie Name",
            placeholder="Example : Avengers"
        )

    with col2:

        st.write("")
        st.write("")

        if st.button("🎤"):

            query=listen()

            st.success("You said : "+query)

    if st.button("🎬 Recommend"):

        if query.strip()=="":

            st.warning("Please enter movie name.")

        else:

            embedding=model.encode([query])

            D,I=index.search(embedding,5)

            st.success("Top Recommended Movies")

            for idx in I[0]:

                if idx>=len(movies):
                    continue

                movie=movies.iloc[idx]

                title=movie["title"]

                genres=movie["genres"]

                rating=movie["vote_average"]

                overview=movie["overview"]

                st.markdown("---")

                st.subheader("🎬 "+title)

                try:
                    stars="⭐"*max(1,int(float(rating)//2))
                except:
                    stars="⭐⭐⭐"

                st.write(stars)

                st.write("⭐ Rating :",rating)

                st.write("🎭 Genre")

                genre_list=str(genres).split("|")

                cols=st.columns(len(genre_list))

                for i,g in enumerate(genre_list):

                    cols[i].success(g)

                st.write("📝 Overview")

                st.write(overview)

                c1,c2=st.columns(2)

                with c1:

                    if st.button(
                        "❤️ Favorite",
                        key="fav"+str(idx)
                    ):

                        if title not in st.session_state.favorites:

                            st.session_state.favorites.append(title)

                            st.success("Added!")

                with c2:

                    if st.button(
                        "🔊 Read Overview",
                        key="voice"+str(idx)
                    ):

                        speak(overview)

# ----------------------------------------------------
# POPULAR
# ----------------------------------------------------

elif selected=="Popular":

    st.title("🔥 Popular Movies")

    top=movies.sort_values(
        by="vote_average",
        ascending=False
    ).head(10)

    for _,movie in top.iterrows():

        st.markdown("---")

        st.subheader(movie["title"])

        st.write("⭐",movie["vote_average"])

        st.write("🎭",movie["genres"])

# ----------------------------------------------------
# FAVORITES
# ----------------------------------------------------

elif selected=="Favorites":

    st.title("❤️ Favorite Movies")

    if len(st.session_state.favorites)==0:

        st.info("No Favorite Movies")

    else:

        for movie in st.session_state.favorites:

            st.success(movie)

# ----------------------------------------------------
# IMAGE SEARCH
# ----------------------------------------------------
# ----------------------------------------------------
# IMAGE SEARCH
# ----------------------------------------------------

elif selected == "Image Search":

    st.title("🖼️ Image To Text")

    st.write("Upload any movie poster or image and AI will describe it.")

    uploaded = st.file_uploader(
        "Choose an Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded is not None:

        st.image(uploaded, caption="Uploaded Image", width=350)

        if st.button("Generate Caption"):

            with st.spinner("Generating Caption..."):

                caption = image_caption(uploaded)

            st.success("Caption Generated Successfully")

            st.write("### AI Caption")

            st.info(caption)

            # ----------------------------------------------------
# MOVIE CHATBOT
# ----------------------------------------------------

elif selected == "Movie Chatbot":

    st.title("🤖 AI Movie Chatbot")

    question = st.text_input(
        "Ask about movies",
        placeholder="Example: Suggest horror movies"
    )

    if st.button("Ask AI"):

        result = chatbot(question)

        if len(result) == 0:

            st.warning("No movies found.")

        else:

            st.success(f"{len(result)} Movies Found")

            for _, movie in result.iterrows():

                st.markdown("---")

                st.subheader(movie["title"])

                st.write("⭐ Rating :", movie["vote_average"])

                st.write("🎭 Genre :", movie["genres"])

                st.write(movie["overview"])
# ----------------------------------------------------
# ABOUT
# ----------------------------------------------------

elif selected == "About":

    st.title("About Project")

    st.write("### Technologies Used")

    st.write("✅ Python")
    st.write("✅ Streamlit")
    st.write("✅ FAISS")
    st.write("✅ Sentence Transformers")
    st.write("✅ Retrieval Augmented Generation (RAG)")
    st.write("✅ Artificial Intelligence")
    st.write("✅ Speech Recognition")
    st.write("✅ Text To Speech")
    st.write("✅ Image To Text")
    st.write("✅ AI Movie Chatbot")