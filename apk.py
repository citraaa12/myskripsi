import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from numpy import array
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
import subprocess
subprocess.run(['pip', 'install', 'imbalanced-learn'])
from imblearn.over_sampling import RandomOverSampler
from math import sqrt
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import joblib
import re
import time
import seaborn as sns
import os
os.system('pip install nltk')
from nltk.stem import PorterStemmer


st.set_page_config(
    page_title="Analisis Sentimen Pembangunan Ibukota Nusantara",
    page_icon="https://raw.githubusercontent.com/citraaa12/myskripsi/main/ikn.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

st.write(
    """<h1 style="font-size: 40px;">Analisis Sentimen Pembangunan Ibukota Nusantara</h1>""",
    unsafe_allow_html=True,
)

with st.container():
    with st.sidebar:
        selected = option_menu(
            st.write(
                """<h2 style = "text-align: center;"><img src="https://raw.githubusercontent.com/dinia28/skripsi/main/home.png" width="130" height="130"><br></h2>""",
                unsafe_allow_html=True,
            ),
            [
                "Home",
                "Data",
                "Preprocessing",
                "Word2Vec",
                "Hasil Klasifikasi",
                "Implementasi",

            ],
            icons=[
                "house",
                "person",
                "gear",
                "bar-chart",
                "arrow-down-square",
                "file-earmark-font",
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#87CEEB"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "white",
                },
                "nav-link-selected": {"background-color": "#005980"},
            },
        )

    if selected == "Home":
        st.write(
            """<h3 style = "text-align: center;">
        <img src="https://raw.githubusercontent.com/citraaa12/myskripsi/main/ikn.png" width="500" height="300">
        </h3>""",
            unsafe_allow_html=True,
        )

        st.subheader("""Deskripsi Aplikasi""")
        st.write(
            """
        ANALISIS SENTIMEN PEMBANGUNAN IBUKOTA NUSANTARA MENGGUNAKAN METODE LONG SHORT TERM-MEMORY (LSTM) DAN WORD2VEC
        """
        )

    elif selected == "Data":

        st.subheader("""Deskripsi Data""")
        st.write(
            """
        Data yang digunakan dalam aplikasi ini yaitu data dari hasil crawling komentar pada video youtube
        """
        )
        
        st.subheader("Dataset")
        # Membaca file CSV dari URL
        df = pd.read_csv(
            "https://raw.githubusercontent.com/citraaa12/myskripsi/main/dataset.csv"
        )
        st.dataframe(df, width=600)
        
        st.subheader("Label")
        # Menampilkan frekuensi dari masing-masing label
        label_counts = df['label'].value_counts()
        st.write(label_counts)
        
    elif selected == "Preprocessing":
        # Cleansing
        st.subheader("Preprocessing")
    
        import pandas as pd
import streamlit as st
import string
import re

# Fungsi untuk membersihkan teks
def clean_text(text):
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    # Menghapus tanda baca
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Menghapus angka
    text = re.sub(r'\d+', '', text)
    # Menghapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Streamlit app
if selected == "Data":

    st.subheader("""Deskripsi Data""")
    st.write(
        """
        Data yang digunakan dalam aplikasi ini yaitu data dari hasil crawling komentar pada video youtube
        """
    )
    
    st.subheader("Dataset")
    # Membaca file CSV dari URL
    df = pd.read_csv(
        "https://raw.githubusercontent.com/citraaa12/myskripsi/main/dataset.csv"
    )
    st.dataframe(df, width=600)
    
    st.subheader("Label")
    # Menampilkan frekuensi dari masing-masing label
    label_counts = df['label'].value_counts()
    st.write(label_counts)
    
    st.subheader("Data Cleaning")
    st.write("Proses cleaning data meliputi penghapusan nilai kosong, tanda baca, angka, dan spasi berlebih.")
    
    # Menangani nilai kosong
    df.dropna(inplace=True)
    st.write("Data setelah menghapus nilai kosong:")
    st.dataframe(df, width=600)
    
    # Cleaning kolom teks (ganti 'komentar' dengan nama kolom teks Anda)
    if 'komentar' in df.columns:
        df['cleaned_komentar'] = df['komentar'].apply(clean_text)
        st.write("Data setelah membersihkan teks:")
        st.dataframe(df[['komentar', 'cleaned_komentar']], width=600)
    else:
        st.error("Kolom 'komentar' tidak ditemukan dalam dataset. Pastikan nama kolom sesuai.")

    st.write("Proses cleaning selesai!")
        
    # Menambahkan proses case folding
    df['CaseFolding'] = df['Cleaning'].str.lower()
    st.write("Hasil Case Folding :")
    st.dataframe(df[['komentar', 'Cleaning', 'CaseFolding']])
        
    # Membaca file slang words
    slangword_normalisasi = pd.read_csv("combined_slang_words.csv")
        
    # Membuat kamus slang words untuk normalisasi
    kata_normalisasi_dict = {row[0]: row[1] for _, row in slangword_normalisasi.iterrows()}
        
        # Fungsi untuk normalisasi kata slang
    def normalisasi_kata(document):
            return ' '.join([kata_normalisasi_dict.get(term, term) for term in document.split()])
        
        # Menerapkan fungsi normalisasi slang words
        df['CaseFolding'] = df['CaseFolding'].fillna('').astype(str)
        df['slangword'] = df['CaseFolding'].apply(normalisasi_kata)
        
        # Tampilkan hasil akhir setelah normalisasi slang words
        st.write("Hasil Normalisasi Slang Words:")
        st.dataframe(df[['Ulasan', 'Cleaning', 'CaseFolding', 'slangword']])

        # Tokenizing
    def tokenizer(text):
            if isinstance(text, str):
                return text.split()  # Tokenisasi sederhana dengan split
                return []
        
        # Menerapkan tokenizing pada kolom 'slangword'
        df['Tokenizing'] = df['slangword'].apply(tokenizer)
        
        # Tampilkan hasil akhir setelah tokenizing
        st.write("Hasil Tokenizing:")
        st.dataframe(df[['Ulasan', 'Cleaning', 'CaseFolding', 'slangword', 'Tokenizing']])
        
        # Stopword removal
        sw = pd.read_csv("combined_stop_words.csv", header=None)[0].tolist()
        
        # Gabungkan stopword default dengan stopword tambahan
        corpus = sw
        
        # Fungsi stopword removal
    def stopword_removal(words):
            return [word for word in words if word not in corpus]
        
        # Menerapkan stopword removal pada kolom 'Tokenizing'
        df['Stopword_Removal'] = df['Tokenizing'].apply(stopword_removal)
        
        # Menampilkan hasil di Streamlit
        st.write("Data setelah stopword removal:")
        st.dataframe(df[['Ulasan', 'Cleaning', 'CaseFolding', 'slangword', 'Tokenizing', 'Stopword_Removal']])

        # Inisialisasi Porter Stemmer
        stemmer = PorterStemmer()
        
        # Fungsi stemming
    def stemText(words):
            return [stemmer.stem(word) for word in words]
        
        # Menerapkan stemming pada kolom 'Stopword_Removal'
        df['Stemming'] = df['Stopword_Removal'].apply(stemText)
        
        # Menggabungkan hasil stemming menjadi satu kalimat
        df['Full_Text_Stemmed'] = df['Stemming'].apply(lambda x: ' '.join(x))
        
        # Menampilkan hasil akhir di Streamlit
        st.write("Data setelah Stemming:")
        st.dataframe(df[['Ulasan', 'Cleaning', 'CaseFolding', 'slangword', 'Tokenizing', 'Stopword_Removal', 'Stemming', 'Full_Text_Stemmed']])

elif selected == "TF-IDF":
        # Load the dataset from 'hasil_preprocessing.xlsx'
        df = pd.read_excel("hasil_preprocessing.xlsx")
        # Assume 'Full_Text_Stemmed' is the column with the processed text for TF-IDF
        # Create a new DataFrame for TF-IDF
        df_tfidf = df[['Full_Text_Stemmed', 'Label']]  
        # Initialize the TfidfVectorizer
        vectorizer = TfidfVectorizer()
        # Transform the 'Full_Text_Stemmed' column into a TF-IDF matrix
        tfidf_matrix = vectorizer.fit_transform(df_tfidf['Full_Text_Stemmed'].values.astype('U')) 
        # Get feature names (the words corresponding to the TF-IDF values)
        feature_names = vectorizer.get_feature_names_out()
        # Convert the TF-IDF matrix into a DataFrame
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names) 
        # Add the 'Label' column to the DataFrame
        tfidf_df['Label'] = df_tfidf['Label']
        # Display the TF-IDF result
        st.subheader("TF-IDF Results")
        st.dataframe(tfidf_df)
        # Optionally, you can save the vectorizer for future use (for example, to use in predictions)
        # import joblib
        # joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    
elif selected == "Information Gain":
        import requests
        from io import BytesIO
        st.subheader("Information Gain")
        st.write("Proses Information Gain")  # Debugging tambahan
        url = "https://raw.githubusercontent.com/dinia28/skripsi/main/hasil_ig.xlsx"
        response = requests.get(url)
        if response.status_code == 200:
            data = BytesIO(response.content)
            df = pd.read_excel(data)
            st.dataframe(df, width=600)
        else:
            st.error("Gagal mengambil file. Periksa URL atau koneksi internet.")
    
    elif selected == "Model WKNN":
        # Fungsi untuk memuat model dan menampilkan hasil rinci
        def load_and_display_model_details(percentage):
            model_filename = f"best_knn_model_{percentage}percent.pkl"
            results_filename = "training_results_with_rankings.xlsx"
            
            if not os.path.exists(model_filename):
                st.warning(f"Model untuk persentase {percentage}% tidak ditemukan.")
                return
        
            # Muat model
            best_model = joblib.load(model_filename)
            st.write(f"Model untuk {percentage}% dimuat.")
        
            # Muat hasil pelatihan dari file Excel
            if os.path.exists(results_filename):
                results = pd.read_excel(results_filename)
        
                # Filter hasil berdasarkan persentase fitur
                specific_results = results[results['Percentage'] == percentage]
                if specific_results.empty:
                    st.warning("Data hasil pelatihan tidak ditemukan untuk persentase ini.")
                    return
        
                # Menampilkan rincian hasil untuk setiap kombinasi parameter
                st.subheader("Detail Hasil untuk Kombinasi Parameter:")
                for index, row in specific_results.iterrows():
                    params = row['Best Parameters']
                    accuracy = row['Accuracy']
                    elapsed_time = row['Elapsed Time (s)']
                    st.write(f"Params: {params} | Accuracy: {accuracy:.4f} | Time: {elapsed_time:.2f} seconds")
                
                
                # Tampilkan informasi terbaik
                best_accuracy = specific_results['Accuracy'].max()
                best_params = specific_results.loc[specific_results['Accuracy'].idxmax(), 'Best Parameters']
                best_elapsed_time = specific_results.loc[specific_results['Accuracy'].idxmax(), 'Elapsed Time (s)']
                
                st.write(f"Model disimpan sebagai: {model_filename}")
                st.write(f"Best Params for {percentage}% features: {best_params}")
                st.write(f"Best Accuracy on Test Data: {best_accuracy:.4f}")
                st.write(f"Total Elapsed Time for Best Model: {best_elapsed_time:.2f} seconds")
            else:
                st.warning("File hasil pelatihan tidak ditemukan.")
        
        # Pilihan persentase yang dapat dipilih pengguna
        percentage_options = [95, 90, 85, 80, 75, 70, 65]
        selected_percentage = st.selectbox("Pilih Persentase Model:", percentage_options)
        
        # Memanggil fungsi untuk menampilkan detail model
        load_and_display_model_details(selected_percentage)
            
st.markdown("---")  # Menambahkan garis pemisah
st.write("Syamsyiya Tuddiniyah-200441100016 (Sistem Informasi)")
