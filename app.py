import streamlit as st

from models import (
    recommend_content,
    recommend_collaborative,
    hybrid_recommend,
    get_popular_movies
)



st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)



st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

[data-testid="stSidebar"]{
    background-color:#0f172a;
}

.main-title{
    text-align:center;
    font-size:3.2rem;
    font-weight:800;
    color:white;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:1.1rem;
    margin-bottom:20px;
}

.movie-card{
    background:#1f2937;
    padding:18px;
    border-radius:12px;
    margin-bottom:12px;
    border-left:5px solid #38bdf8;
    color:white;
    font-size:18px;
}

.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)



st.markdown(
    """
    <div class="main-title">
         Movie Recommendation System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
        Content-Based Filtering • Collaborative Filtering • Hybrid Recommendation Engine
    </div>
    """,
    unsafe_allow_html=True
)



col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Movies",
        value="9,742"
    )

with col2:
    st.metric(
        label="Users",
        value="610"
    )

with col3:
    st.metric(
        label="Ratings",
        value="100,836"
    )

st.divider()



with st.sidebar:

    st.title(" Recommendation Settings")

    model = st.selectbox(
        "Choose Model",
        [
            "Popular Movies",
            "Content-Based Filtering",
            "Collaborative Filtering",
            "Hybrid Recommender"
        ]
    )

    if model != "Popular Movies":

        movie_name = st.text_input(
            "Movie Name"
        )

    else:

        movie_name = ""

    recommend_btn = st.button(
        " Recommend",
        use_container_width=True
    )

    st.divider()

    st.markdown("###  About")

    st.write("""
    This project demonstrates:

    - KNN
    - Cosine Similarity
    - Content-Based Filtering
    - Collaborative Filtering
    - Hybrid Recommendation Systems
    """)

    st.divider()

    st.write("Built by Asavare Trivedi")



if recommend_btn:

    try:

        if model == "Popular Movies":

            recommendations = get_popular_movies()

        elif model == "Content-Based Filtering":

            recommendations = recommend_content(
                movie_name
            )

        elif model == "Collaborative Filtering":

            recommendations = recommend_collaborative(
                movie_name
            )

        else:

            recommendations = hybrid_recommend(
                movie_name
            )

        st.success("Recommendations Generated Successfully!")

        st.subheader(" Recommended Movies")

        for i, movie in enumerate(
            recommendations,
            start=1
        ):

            st.markdown(
                f"""
                <div class="movie-card">
                    <strong>{i}.</strong> {movie}
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception:

        st.error(
            "Movie not found. Please try another movie."
        )



st.divider()

st.markdown(
    """
    <div class="footer">
        Built  using Python, Pandas, Scikit-Learn and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)