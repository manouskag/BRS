import streamlit as st
import pickle
import pandas as pd

# Load files
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
books = pickle.load(open('book.pkl', 'rb'))  # Book details DataFrame

# Function to recommend books
def recommend(book_name):
    if book_name not in pt.index:
        return []
    
    index = pt.index.get_loc(book_name)
    similar_books = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []
    for i in similar_books:
        title = pt.index[i[0]]
        similarity_score = i[1]
        
        book_info = books[books['Book-Title'] == title].drop_duplicates('Book-Title')
        
        if not book_info.empty:
            author = book_info.iloc[0]['Book-Author']
            image = book_info.iloc[0]['Image-URL-M']
        else:
            author = "Unknown"
            image = ""

        recommendations.append({
            'title': title,
            'author': author,
            'image': image,
            'similarity': similarity_score
        })

    return recommendations

# Streamlit UI
st.title("Book Recommender System")

book_list = pt.index.tolist()

user_input = st.text_input("Enter a book name:")

if st.button("Recommend"):
    if user_input.strip() == "":
        st.warning("Please enter a book name.")
    else:
        # Find the best matching book title
        matches = [title for title in book_list if user_input.lower() in title.lower()]
        
        if matches:
            selected_book = matches[0]  # Take the first matching title
            st.success(f"Recommendations for: '{selected_book}'")

            recommendations = recommend(selected_book)

            if recommendations:
                for rec in recommendations:
                    if rec['image']:
                        st.image(rec['image'], width=150)
                    st.write(f"**{rec['title']}** by {rec['author']}")
                    st.write(f"Similarity Score: {rec['similarity']:.2f}")
                    st.markdown("---")
            else:
                st.warning("No recommendations found for this book.")
        else:
            st.error("No matching book found. Please check the spelling or try a different name.")
