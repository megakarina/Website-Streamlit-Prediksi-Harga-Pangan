## IMPORT LIBRARY
import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
import io
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sb  
import statsmodels.api as sm
import datetime
import plotly.graph_objects as go
import matplotlib.dates as mdates
from streamlit_option_menu import option_menu
from io import StringIO
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Membuat tampilan layout web menjadi wide
st.set_page_config(layout="wide")

## NAVIGATION MENU (SIDE BAR) -- START --
with st.sidebar:
    selected = option_menu(         # Membuat Nama Menu Dashboard
        menu_title="DASHBOARD",
        options=["Beranda", "Data Historis", "Hasil Prediksi",  "Tentang"], ##"Petunjuk Pengguna"
                         icons=['house-door-fill', 'calendar-event-fill', 'calendar-check-fill', 'info-square-fill'], ##'question-square-fill'
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "#66140c", "font-size": "25px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"2px", "--hover-color": "#eeeeee"},
        "nav-link-selected": {"background-color": "#ed5142"},
    }
    )
## NAVIGATION MENU (SIDE BAR) -- END --


## FITUR MENU BERANDA -- START --
if selected == "Beranda":
    st.write("<center><span style='font-size: 45px;'><b>Selamat Datang</b></span></center>", unsafe_allow_html=True)
    st.write("<center><span style='font-size: 30px;'><b>Di Sistem Hasil Prediksi Harga Bahan Pangan Pada Pasar Tradisional Kota Singkawang</b></span></center>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    # Mengubah size ukuran Tab
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 22px;
        }
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Penjelasan Website", "Tujuan dan Kegunaan Website", "Dataset Yang Digunakan"])

    with tab1:
        st.markdown("<h1 style='font-size: 22px;'>Penjelasan Website</h1>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify; font-size: 18px;">Pangan merupakan kebutuhan paling mendasar bagi sumber daya manusia. Bahan pangan yang diolah menjadi makanan adalah salah satu kebutuhan primer yang penting. Karena itulah, harga bahan pangan memiliki pengaruh yang besar dalam kehidupan manusia.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Untuk mengatasi agar tidak terjadi kenaikan harga yang ekstrim karena tidak adanya perkiraan harga dimasa depan, maka diperlukan sebuah sistem yang dapat menampilkan hasil prediksi harga yang akurat dan tepat untuk masa mendatang. Untuk mendapatkan sebuah hasil prediksi harga yang tepat dan akurat dibutuhkan penggunaan metode Least Square (Kuadrat Terkecil) yang merupakan salah satu metode peramalan yang digunakan untuk melihat trend dari data deret waktu atau time series.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Website ini merupakan hasil akhir dari tampilan perhitungan prediksi yang telah dilakukan. Website Prediksi Harga Bahan Pangan ini dilakukan dengan menggunakan metode Least Square sebagai perhitungannya. Diharapkan dengan adanya website ini, dapat membantu masyarakat dalam melihat perkiraan hasil dari prediksi harga bahan pangan pada Kota Singkawang.</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<h1 style='font-size: 22px;'>Tujuan dan Kegunaan Website</h1>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify; font-size: 18px;">Tujuan dari website ini adalah membangun suatu sistem yang dapat menampilkan hasil prediksi harga bahan pangan pada Kota Singkawang dengan menggunakan metode Least Square sebagai perhitungannya. Hasil yang ditampilkan berbentuk visualisasi tabel dan grafik, tujuannya untuk memudahkan pengguna dalam mencerna informasi yang telah disajikan tersebut.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Sedangkan kegunaan website ini yaitu memberikan gambaran kepada pengguna atau masyarakat Kota Singkawang terhadap kenaikan atau penurunan harga pangan dimasa mendatang, sehingga masyarakat dapat mempersiapkan diri ataupun mencari solusi terbaik untuk penanganannya.</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("<h1 style='font-size: 22px;'>Dataset Yang Digunakan</h1>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify; font-size: 18px;">Data yang digunakan untuk prediksi yaitu data harga pangan Kota Singkawang dengan 16 jenis komoditas pangan dari periode Januari 2018 sampai Januari 2023. 16 jenis komoditas pangan tersebut meliputi: Beras Kualitas Bawah, Beras Kualitas Medium, Beras Kualitas Super, Daging Ayam, Daging Sapi Kualitas 1, Daging Sapi Kualitas 2, Telur Ayam, Bawang Merah, Bawang Putih, Cabai Merah Besar, Cabai Rawit Hijau, Cabai Rawit Merah, Minyak Goreng Curah, Minyak Goreng Kemasan Bermerk 1, Minyak Goreng Kemasan Bermerk 2, Gula Pasir Lokal. Data diperoleh dari website Pusat Informasi Harga Pangan Strategis Nasional (PIHPS Nasional) disitus https://www.bi.go.id/hargapangan/.</div>', unsafe_allow_html=True)
## FITUR MENU BERANDA -- END --


## FITUR MENU DATA HISTORIS -- START --
if selected == "Data Historis":
    st.write("<center><span style='font-size: 45px;'><b>Data Historis Harian Harga Pangan</b></span></center>", unsafe_allow_html=True)
    st.write("")
    
    import base64
    from io import BytesIO
    
    # Tampilkan file uploader untuk mengunggah file Excel
    uploaded_file = st.file_uploader("Unggah file Excel disini.")
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":  # Cek tipe file jika Excel
            
            # Membaca data dari file Excel menggunakan library pandas
            df = pd.read_excel(uploaded_file)

            # Mendapatkan nama file yang diunggah
            file_name = uploaded_file.name
            
            # Melakukan penyimpanan DataFrame ke dalam file Excel dengan nama yang relevan.
            output_file_path = f"{file_name}.xlsx"
            df.to_excel(output_file_path, index=False)
            st.success(f"File berhasil disimpan dengan nama {output_file_path}")
            
        else:
            st.error("Terjadi kesalahan saat membaca file. Hanya mendukung file dengan format xlsx.")
            
    # Membaca daftar file dalam folder Website
    folder_path = "."  # Ganti dengan path folder Anda
    files = [file for file in os.listdir(folder_path) if file.endswith(".xlsx")]
    
    # Membuat dropdown untuk memilih file yang akan digunakan
    selected_file = st.selectbox("Pilih file data yang akan digunakan:", files)

    file_path = os.path.join(folder_path, selected_file)
    df = pd.read_excel(file_path)
    df['Year'] = pd.DatetimeIndex(df['Tanggal']).year

    st.write(f"<span style='font-size: 14px;'>File data yang digunakan: {selected_file}</span>", unsafe_allow_html=True)

    def download_excel(df):
            # Membuat objek BytesIO untuk menampung file Excel
            output = BytesIO()

            # Menulis DataFrame ke file Excel menggunakan library pandas
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)

            # Menentukan nama file
            file_name = "data_excel.xlsx"

            # Membuat link download
            b64 = base64.b64encode(output.getvalue()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Klik Untuk Unduh File Data Excel</a>'

            # Menampilkan link download
            st.markdown(href, unsafe_allow_html=True)
    
    # Tombol untuk mengunduh file Excel
    if st.button('Unduh File Data Excel'):
        download_excel(df)
        
    # Pesan info
    st.info('Harga Pangan yang ditampilkan di tabel dalam mata uang IDR atau Rupiah (Contoh: Rp 12,400)', icon="ℹ️")
        
    # Membuat dropdown untuk memilih tahun
    years = ['All'] + list(range(2017, 2024))
    selected_year = st.selectbox("Filter data berdasarkan tahun:", years)

    # Melakukan pemfilteran berdasarkan tahun yang dipilih
    filtered_df = df if selected_year == 'All' else df[df['Year'] == selected_year]

    # Menampilkan DataFrame di Streamlit
    st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Tabel Data</b></div>', unsafe_allow_html=True)
    st.write("")
    st.data_editor(filtered_df)

    # Menampilkan grafik timeseries untuk seluruh komoditas
    st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Grafik Data</b></div>', unsafe_allow_html=True)
    st.write("")
    st.line_chart(df.set_index('Tanggal'))
    
    st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Grafik Untuk Setiap Komoditas Pangan pada Dataset</b></div>', unsafe_allow_html=True)
    st.write("")
    
    a = list(df.columns)
    
    for i in a[1:]:     # 1 supaya kolom Tanggal tidak ikut
        st.markdown(f"<h1 style='font-size: 17px; text-align: center; color: #707070; padding: 20px 0;'>Grafik Data Harga Pangan {i}</h1>", unsafe_allow_html=True)
        # Menampilkan grafik data harga dari seluruh jenis komoditas pangan
        st.line_chart(df[i])
## FITUR MENU DATA HISTORIS -- END --


## FITUR MENU HASIL PREDIKSI -- START --
if selected == "Hasil Prediksi":
    st.write("<center><span style='font-size: 45px;'><b>Hasil Prediksi Harga Pangan</b></span></center>", unsafe_allow_html=True)
    st.write("")
    
    import base64
    from io import BytesIO
    
    # Tampilkan file uploader untuk mengunggah file Excel
    uploaded_file = st.file_uploader("Unggah file Excel disini.")
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":  # Cek tipe file jika Excel
            
            # Membaca data dari file Excel menggunakan library pandas
            df = pd.read_excel(uploaded_file)

            # Mendapatkan nama file yang diunggah
            file_name = os.path.splitext(uploaded_file.name)[0]

            # Melakukan penyimpanan DataFrame ke dalam file Excel dengan nama yang relevan.
            output_file_path = f"{file_name}.xlsx"
            df.to_excel(output_file_path, index=False)
            st.success(f"File berhasil disimpan dengan nama {output_file_path}")
            
        else:
            st.error("Terjadi kesalahan saat membaca file. Hanya mendukung file dengan format xlsx.")
    
    # Membaca daftar file dalam folder Website
    folder_path = "."  # Ganti dengan path folder Anda
    files = [file for file in os.listdir(folder_path) if file.endswith(".xlsx")]
    
    # Membuat dropdown untuk memilih file yang akan digunakan
    selected_file = st.selectbox("Pilih file data yang akan digunakan:", files)

    file_path = os.path.join(folder_path, selected_file)
    df = pd.read_excel(file_path)
    df['Year'] = pd.DatetimeIndex(df['Tanggal']).year

    st.write(f"<span style='font-size: 14px;'>File data yang digunakan: {selected_file}</span>", unsafe_allow_html=True)

    def download_excel(df):
            # Membuat objek BytesIO untuk menampung file Excel
            output = BytesIO()

            # Menulis DataFrame ke file Excel menggunakan library pandas
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)

            # Menentukan nama file
            file_name = "data_excel.xlsx"

            # Membuat link download
            b64 = base64.b64encode(output.getvalue()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Klik Untuk Unduh File Data Excel</a>'

            # Menampilkan link download
            st.markdown(href, unsafe_allow_html=True)
    
    # Tombol untuk mengunduh file Excel
    if st.button('Unduh File Data Excel'):
        download_excel(df)
        
    # Pesan info
    st.info('Harga Pangan yang ditampilkan di tabel dalam mata uang IDR atau Rupiah (Contoh: Rp 12,400)', icon="ℹ️")
        
    # Membuat dropdown untuk memilih tahun
    years = ['All'] + list(range(2017, 2024))
    selected_year = st.selectbox("Filter data berdasarkan tahun:", years)

    # Melakukan pemfilteran berdasarkan tahun yang dipilih
    filtered_df = df if selected_year == 'All' else df[df['Year'] == selected_year]

    # Menampilkan DataFrame di Streamlit
    st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Tabel Data</b></div>', unsafe_allow_html=True)
    st.write("")
    st.data_editor(filtered_df)

    # Menampilkan grafik timeseries untuk seluruh komoditas
    st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Grafik Data</b></div>', unsafe_allow_html=True)
    st.write("")
    st.line_chart(filtered_df.set_index('Tanggal'))
    
    a = list(df.columns)
        
    ## PERHITUNGAN PREDIKSI LEAST SQUARE -- START --
    
    st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Perhitungan Prediksi</b></div>', unsafe_allow_html=True)
    st.write("")

    # Mengubah kolom 'Tanggal' menjadi tipe data datetime
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
   
    # Membuat pilihan rentang tanggal data latih dan data uji dari st.date_input
    start_date = st.date_input("Pilih rentang tanggal awal:", value=df['Tanggal'].min().date(), min_value=df['Tanggal'].min().date(), max_value=df['Tanggal'].max().date())
    end_date = st.date_input("Pilih rentang tanggal akhir:", value=df['Tanggal'].max().date(), min_value=df['Tanggal'].min().date(), max_value=df['Tanggal'].max().date())

    # Mengonversi tipe data date menjadi datetime64[ns]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Mengfilter DataFrame berdasarkan rentang tanggal yang dipilih
    df1 = df[(df['Tanggal'] >= start_date) & (df['Tanggal'] <= end_date)]

    # Menampilkan tabel dengan data yang sudah difilter
    st.dataframe(df1)

    # Membuat pilihan untuk perbandingan data latih dan data uji dari st.slider
    train_size = st.slider('Pilih presentase data latih:', 0.1, 1.0, 0.8, 0.05)
    test_size = round(1.0 - train_size, 2)  # Menggunakan round() untuk membulatkan ke 2 digit desimal
    st.info('Persentase data uji:  ' + str(test_size))

    hitung = st.button("Memproses Perhitungan Prediksi")

    st.write("")

    if hitung:
        df = pd.read_excel(file_path, index_col='Tanggal')
        
        a = list(df.columns)
                
        # Mengunci trainsize agar tidak berubah nilai
        train_size1 = train_size
        
        new_df = pd.read_excel(file_path, index_col='Tanggal')
        
        for i in a[0:]:
            fig, ax = plt.subplots(figsize=(17, 7))
            ax.plot(df[i])
            ax.set_title('Data Harga Time Series')
            ax.set_xlabel('Tahun')
            ax.set_ylabel(f'{i}')

        ## Prediksi Future Value Yang Diketahui
        st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Perbandingan Data Aktual dan Hasil Prediksi dari Nilai Yang Diketahui</b></div>', unsafe_allow_html=True)
        st.write("")
        
        from sklearn.linear_model import LinearRegression
        import plotly.express as px
        import plotly.graph_objects as go
        import plotly.io as pio
        
        # Code dalam bentuk Streamlit
        for i in a[0:]:
            df1 = df[[f'{i}']]
            # Create lagged variable
            df1[f'Lagged_{i}'] = df1[f'{i}'].shift(1)

            # Drop missing values
            df1.dropna(inplace=True)

            # Splitting data
            train_size = int(len(df) * train_size1) # masukkan trainsize yang dikunci
            train, test = df1[:train_size], df1[train_size:]

            # Modeling
            X_train = train[f'Lagged_{i}']
            y_train = train[f'{i}']
            X_train = sm.add_constant(X_train)
            model = sm.OLS(y_train, X_train)
            model_fit = model.fit()

            # Prediction
            X_test = test[f'Lagged_{i}']
            X_test = sm.add_constant(X_test)
            predictions = model_fit.predict(X_test)
                    
            # Grafik Hidup dan Responsif
            # Create a figure
            fig = go.Figure()

            # Add the actual data trace with specified color
            fig.add_trace(go.Scatter(x=test.index, y=test[f'{i}'], name=f'{i} - Data Actual', line=dict(color='blue')))

            # Add the prediction trace with specified color
            fig.add_trace(go.Scatter(x=test.index, y=predictions, name=f'{i} - Data Hasil Prediksi', line=dict(color='red')))

            # Update the layout
            fig.update_layout(xaxis_title='Tahun', yaxis_title='Harga - 'f'{i}', width=800, height=500)
            
            # Format the y-axis tick labels to display without decimal places
            fig.update_yaxes(tickformat=".0f")

            # Display the plotly chart
            st.plotly_chart(fig)

        ## Prediksi Future Value Yang Tidak Diketahui
        st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Prediksi Nilai Masa Depan yang Tidak Diketahui</b></div>', unsafe_allow_html=True)
        st.write("")
        
        ## Prediksi Future Value Yang Diketahui
        # Code dalam bentuk Streamlit
        pred_df_result = [] # Inisialisasi list pred_df_result

        # Iterate over the columns
        for b in a[0:]:
            df1 = df[[f'{b}']]
            # Create lagged variable
            df1[f'Lagged_{b}'] = df1[f'{b}'].shift(1)
            
            # Drop missing values
            df1.dropna(inplace=True)

            # Modeling
            X_train = df1[f'Lagged_{b}']
            y_train = df1[f'{b}']
            X_train = sm.add_constant(X_train)
            model = sm.OLS(y_train, X_train)
            model_fit = model.fit()
                       
            # Prediction
            start_date = '2023-02-01'
            end_date = '2024-02-01'
            pred_index = pd.date_range(start=start_date, end=end_date, freq='D')
            pred_df = pd.DataFrame(index=pred_index, columns=['Data Hasil Prediksi'])
            pred_df.index.name = 'Tanggal'

            for i in range(len(pred_df)):
                price_needs = pred_df.iloc[i-1]['Data Hasil Prediksi'] if i > 0 else df.iloc[-1][f'{b}']
                pred_df.iloc[i]['Data Hasil Prediksi'] = model_fit.predict([1, price_needs])[0]

            pred_df.to_excel('Hasil Prediksi_' + str(f'{b}') + '.xlsx', 'sheet1') #di download hasil prediksi

            pred_df_result.append(
                {
                    'Nama Data' : f'{b}',
                    'Hasil Prediksi' : pred_df,
                }
            )
            
            # Add predictions to original dataframe
            final_result_df = pd.concat([new_df, pred_df], axis=0)

            # Grafik Hidup dan Responsif
            # Create a figure
            fig = go.Figure()

            # Add the actual data trace
            fig.add_trace(go.Scatter(x=final_result_df.index, y=final_result_df[f'{b}'], name=f'{b} - Data Actual', line=dict(color='blue')))

            # Add the prediction trace
            fig.add_trace(go.Scatter(x=final_result_df.index, y=final_result_df['Data Hasil Prediksi'], name=f'{b} - Data Hasil Prediksi', line=dict(color='red')))

            # Update the layout
            fig.update_layout(xaxis_title='Tahun', yaxis_title='Harga - 'f'{b}', width=800, height=500)

            # Menghilangkan koma di belakang angka
            fig.update_yaxes(tickformat="d")

            # Display the plotly chart
            st.plotly_chart(fig)
        
        st.markdown('<div style="text-align: justify; font-size: 22px; color: #ed5142;"><b>Hasil Prediksi Time Series dari Periode Februari 2023 sampai Januari 2024</b></div>', unsafe_allow_html=True)
        st.write("")
        
        # Code dalam bentuk Streamlit
        # Grafik Hidup dan Responsif
        for values in pred_df_result:
            # Create a figure
            fig = go.Figure()

            # Add the prediction trace
            fig.add_trace(go.Scatter(x=values['Hasil Prediksi'].index, y=values['Hasil Prediksi']['Data Hasil Prediksi'], name='Data Hasil Prediksi'))

            # Update the layout
            fig.update_layout(title=f"Hasil Prediksi Harga {values['Nama Data']} Time Series",
                            xaxis_title='Bulan',
                            yaxis_title='Harga')
            
            # Format the y-axis tick labels to display without decimal places
            fig.update_yaxes(tickformat=".0f")
    
            # Display the plotly chart
            st.plotly_chart(fig)
    ## PERHITUNGAN PREDIKSI LEAST SQUARE -- END --
## FITUR MENU HASIL PREDIKSI -- END --


## FITUR MENU TENTANG -- START --
if selected == "Tentang":
    st.write("<center><span style='font-size: 45px;'><b>Tentang Website</b></span></center>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    # Mengubah size ukuran Tab
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 19px;
        }
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Data Diri Pembuat Website", "Penjelasan Hasil Pengujian", "Hasil Pengujian Yang Didapatkan"])
    st.write("")

    with tab1:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Halo, nama saya <b>Mega Karina Anjelie</b>.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Saya merupakan seorang mahasiswa jurusan Teknik Informatika dari Universitas Tarumanagara yang sedang dalam tahap pembuatan skripsi yang berfokus pada bidang ilmu Data Science atau Data Engineering. Pada skripsi ini saya membuat sebuah sistem yang menampilkan hasil prediksi harga bahan pangan pada Kota Singkawang dengan menggunakan metode Least Square sebagai perhitungan pengujiannya.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;"><b>Kontak:</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: justify; font-size: 18px;">Email: megakarina01@gmail.com</div>', unsafe_allow_html=True)

    with tab2:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Perhitungan pada pengujian prediksi harga dilakukan dengan menggunakan metode Least Square. Selain itu pada perhitungan prediksi ini, diperlukan juga metode evaluasi untuk mengukur keakuratan suatu model prediksi. Metode evaluasi yang digunakan yaitu dengan menggunakan teknik evaluasi Mean Absolute Percentage Error (MAPE).</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">MAPE adalah persentase kesalahan rata-rata secara multak atau absolut. Pengertian MAPE adalah pengukuran statistik tentang akurasi pada prediksi. MAPE memberikan informasi seberapa besar kesalahan pada prediksi tersebut. Semakin kecil nilai presentasi kesalahan pada MAPE maka semakin akurat hasil prediksi tersebut.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;"><b>Catatan Penting:</b> Hasil prediksi tidak selalu akurat. Prediksi merupakan perkiraan dari perhitungan model matematika dan komputasi. Dengan adanya prediksi ini, diharapkan dapat membantu masyarakat dalam memperkirakan harga bahan pangan di masa mendatang.</div>', unsafe_allow_html=True)

    
    with tab3:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Prediksi yang dilakukan pada pengujian ini yaitu prediksi harga untuk 1 tahun mendatang atau selama 365 hari untuk periode Februari 2023 sampai dengan Januari 2024.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Hasil pengujian yang digunakan dalam melakukan perhitungan prediksi adalah dengan menggunakan perbandingan rasio data latih dan data uji sebanyak 80:20 atau 80% dengan pengujian dataset menggunakan tahun 2023 yaitu dari rentang periode tanggal 1 Januari 2018 sampai dengan 31 Januari 2023.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Evaluasi error menggunakan MAPE menghasilkan nilai yang rendah untuk setiap variabel jenis pangan. Hal ini menunjukan bahwa Prediksi memiliki <b>Hasil Keakuratan yang Baik</b>. Karena interpretasi nilai MAPE yang dihasilkan termasuk ke dalam kategori <b>10 – 20%</b> atau dalam artian lain tidak ada nilai MAPE yang memiliki hasil diatas 20%.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Hasil evaluasi MAPE terkecil didapatkan oleh jenis pangan Beras Kualitas Super dengan nilai MAPE yaitu 0.37%. Sedangkan hasil evaluasi MAPE terbesar didapatkan pada jenis pangan Bawang Merah dengan nilai MAPE yaitu 15.48%.</div>', unsafe_allow_html=True)
        st.write("")
        
        #x = ['Beras Kualitas Bawah', 'Beras Kualitas Medium', 'Beras Kualitas Super', 'Daging Ayam', 'Daging Sapi Kualitas 1', 'Daging Sapi Kualitas 2', 'Telur Ayam', 'Bawang Merah', 'Bawang Putih', 'Cabai Merah Besar', 'Cabai Rawit Hijau', 'Cabai Rawit Merah', 'Minyak Goreng Curah', 'Minyak Goreng Kemasan Bermerk 1', 'Minyak Goreng Kemasan Bermerk 2', 'Gula Pasir Lokal']
        x = ['Beras Kw. Bawah', 'Beras Kw. Medium', 'Beras Kw. Super', 'Daging Ayam', 'Daging Sapi Kw. 1', 'Daging Sapi Kw. 2', 'Telur Ayam', 'Bawang Merah', 'Bawang Putih', 'Cabai Merah Besar', 'Cabai Rawit Hijau', 'Cabai Rawit Merah', 'Minyak Goreng Curah', 'Minyak Goreng Kemasan 1', 'Minyak Goreng Kemasan 2', 'Gula Pasir Lokal']
        y = [1.88, 0.64, 0.37, 6.81, 2.76, 2.05, 10.03, 15.48, 8.84, 9.90, 9.99, 9.95, 11.03, 9.67, 12.87, 2.04]

        # Membuat grafik batang dengan Plotly
        fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=[ 'brown', 'maroon', 'red', 'orange', 'yellow', 'cyan', 'green', 'lime', 'blue', 'teal', 'magenta', 'pink', 'indigo', 'purple', 'gray', 'silver']))])

        # Mengatur layout responsif
        fig.update_layout(
            title="Grafik Hasil Evaluasi MAPE Dalam Persen (%)"
        )
        # Menampilkan grafik menggunakan Streamlit
        st.plotly_chart(fig)
## FITUR MENU TENTANG -- END --


## FITUR MENU PETUNJUK PENGGUNA -- START --
if selected == "Petunjuk Pengguna":
    st.write("<center><span style='font-size: 45px;'><b>Petunjuk Pengguna</b></span></center>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    # Mengubah size ukuran Tab
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 24px;
        }
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)
        
    st.info('Menu petunjuk pengguna merupakan menu bantuan untuk instruksi mengenai cara penggunaan website ini. Pada menu ini setiap fitur akan dijelaskan cara penggunaannya.', icon="ℹ️")
    st.write("")
    st.write("")

    from PIL import Image
    
    tab1, tab2, tab3, tab4 = st.tabs(["Menu Beranda", "Menu Data Historis", "Menu Hasil Prediksi", "Menu Tentang"])
    st.write("")

    with tab1:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Pada menu Beranda ini, merupakan menu tampilan awal ketika website dijalankan. Menu Beranda berisi tentang Penjelasan Wesite, Tujuan dan Kegunaan Website, serta Dataset Yang Digunakan pada perhitungan prediksi</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Terdapat slider tab seperti pada gambar di bawah ini yang dapat di klik pada bagian Menu Beranda, tujuannya adalah agar tampilan website lebih efisien dan mudah digunakan jika bisa berpindah tab untuk melihat informasi yang disajikan.</div>', unsafe_allow_html=True)

        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\TabBeranda.png')
        st.image(image, caption='Fitur Tab pada Menu Beranda')

    with tab2:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Pada menu Data Historis ini, merupakan menu yang berisi tentang tampilan tabel serta grafik pada data yang dipilih. Terdapat fitur untuk mengunggah file data dalam format Excel dari dokumen pengguna, yang dimana ketika data tersebut diunggah, data akan tersimpan secara otomatis pada website.</div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\\WebSkripsi\\img\\UnggahFile.png')
        st.image(image, caption='Berhasil unggah file data Excel dan tersimpan ke dalam website')
        
        st.write("")
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Terdapat fitur selectbox untuk memilih file data yang ingin ditampilkan pada tabel dan grafik dari data yang telah diunggah sebelumnya ke dalam website.</div>', unsafe_allow_html=True)
        st.write("")

        image = Image.open('C:\WebSkripsi\img\PilihData.png')
        st.image(image, caption='Memilih file data yang ingin ditampilkan pada fitur selectbox')
        
        st.write("")
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Terdapat fitur button untuk mengunduh file data dalam format excel yang dipilih sebelumnya dari dalam website.</div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\DownloadData.png')
        st.image(image, caption='Tombol (Button) untuk mengunduh file data yang telah dipilih')
        
        st.write("")
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Selain itu, terdapat fitur selectbox untuk memilih pada tahun berapa data yang ingin ditampilkan pada file data yang telah dipilih sebelumnya. Hal ini bertujuan agar pengguna dapat melihat historis data pada tahun-tahun tertentu.</div>', unsafe_allow_html=True)
        st.write("")

        image = Image.open('C:\WebSkripsi\img\PilihTahun.png')
        st.image(image, caption='Memilih tahun berapa yang ingin ditampilkan pada data')
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Setelah memilih file data dan tahun, data tersebut akan langsung ditampilan ke dalam Tabel dan Grafik Data. Pada Tabel Data terdapat fitur yang dapat mengurutkan nilai baris yang ada pada kolom, baik dari yang terkecil ke terbesar begitupun sebaliknya. </div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\TabelData.png')
        st.image(image, caption='Tabel Data Historis')
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Selanjutnya untuk Grafik Data yang ditampilkan dibuat responsif dan iteraktif agar dapat memudahkan pengguna untuk melihat dan memahami grafik yang disajikan.</div>', unsafe_allow_html=True)      
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\GrafikData.png')
        st.image(image, caption='Grafik Data Historis')
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Selain itu, ditampilkan juga Grafik Data untuk setiap Komoditas Pangan yang ada pada kolom data. Grafik ini bertujuan agar pengguna dapat lebih mudah untuk melihat dan memahami grafik yang disajikan untuk setiap jenis komoditas yang ada pada data.</div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\GrafikKomoditas.png')
        st.image(image, caption='Grafik Data setiap jenis Komoditas')
    
    with tab3:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Pada menu Hasil Prediksi ini, merupakan menu yang berisi tentang tampilan tabel serta grafik pada data yang dipilih pada Data Historis. Pada menu ini juga pengguna dapat langsung melakukan prediksi harga. Terdapat fitur input tanggal, untuk memilih dari rentang tanggal berapa sampai dengan berapa perhitungan prediksi ingin dilakukan.</div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\RangeTanggal.png')
        st.image(image, caption='Input tanggal untuk rentang waktu pengujian pada data')

        st.markdown('<div style="text-align: justify; font-size: 18px;">Selain itu juga terdapat fitur untuk memilih berapa perbandingan rasio data latih dan data uji yang ingin dilakukan pada perhitungan prediksi.</div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\SliderRasio.png')
        st.image(image, caption='Pilih rasio perbandingan data latih dan data uji')
        
        st.markdown('<div style="text-align: justify; font-size: 18px;">Jika telah selesai memilih rentang tanggal dan rasio perbandingan data latih dan data uji, terdapat tombol / button untuk dapat memproses perhitungan prediksi pada website. Button ini dapat di klik agar hasil dari perhitungan prediksi dapat ditampilkan.</div>', unsafe_allow_html=True)
        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\ButtonProses.png')
        st.image(image, caption='Klik tombol atau button untuk dapat memproses perhitungan prediksi')
        
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Setelah tombol atau button di klik maka hasil perhitungan prediksi akan ditampilkan dalam bentuk grafik. Hasil tersebut dapat dilihat pada Menu Hasil Prediksi. </div>', unsafe_allow_html=True)

        
    with tab4:
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Pada menu Tentang ini, merupakan menu yang berisi tentang Data Diri Pembuat Website, Penjelasan Hasil Pengujian, serta Hasil Pengujian yang Didapatkan.</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div style="text-align: justify; font-size: 18px;">Terdapat slider tab seperti pada gambar di bawah ini yang dapat di klik pada bagian Menu Tentang, tujuannya adalah agar tampilan website lebih efisien dan mudah digunakan jika bisa berpindah tab untuk melihat informasi yang disajikan.</div>', unsafe_allow_html=True)

        st.write("")
        
        image = Image.open('C:\WebSkripsi\img\TabTentang.png')
        st.image(image, caption='Fitur Tab pada Menu Tentang')
## FITUR MENU PETUNJUK PENGGUNA -- END --
