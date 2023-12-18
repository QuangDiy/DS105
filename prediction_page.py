import streamlit as st
import pickle
from crawler_data import search_image, search_image_base
import os
import sklearn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
import threading



example_data = {
    'laptop_name': 'Laptop Acer Aspire 3 A315 59 314F',
    'laptop_cpu': 'Intel Core i3 Alder Lake - 1215U',
    'laptop_ram_type': 'DDR4',
    'laptop_ram': 8,
    'laptop_hard_drive': 'SSD',
    'laptop_hard_drive_size': 256,
    'laptop_graphic_name': 'Intel UHD Graphics',
    'laptop_warranty_location': 'Chính Hãng',
    'laptop_warranty_time': 7.5,
    'laptop_year': 2022,
    'laptop_price_new': 13.49,
    'laptop_resolution': 'Full HD',
    'laptop_os': 'Windows 11 Home SL',
}


def prediction_page():
    st.title(":rainbow[Laptop Price Predictor] 💻")

    label_encoders = pickle.load(open('pkl\label_encoders.pkl', "rb"))

    left_column, right_column = st.columns(2)

    with left_column:
        st.header('Thông tin cơ bản')
        laptop_name = left_column.text_input('Tên Laptop 💻', example_data['laptop_name'])
        laptop_cpu = left_column.text_input('CPU Laptop', example_data['laptop_cpu'])
        laptop_ram_type = left_column.selectbox("Loại RAM", ["DDR4", "DDR3", 'LPDDR4', 'LPDDR4X', 'DDR3L', 'DDR5', 'Apple', 'LPDDR5'], index = 0)
        laptop_ram = left_column.selectbox("RAM (GB)", [4, 8, 16, 32], index=1)
        laptop_hard_drive = left_column.selectbox("Ổ cứng 💽", ['SSD', "HDD", 'eMMC'], index=0)
        laptop_hard_drive_size = left_column.selectbox("Dung lượng (GB) 💽", [128, 256, 512, 1024, 2048], index=1)
        laptop_graphic_name = left_column.text_input('Tên Card đồ họa', example_data['laptop_graphic_name'])

    with right_column:
        st.header('Thông tin khác')
        laptop_os = right_column.selectbox('Hệ điều hành', ['Windows 10 Home SL', 'Windows 10 Home Standard', 'Windows 10 Pro', 'Windows 11 Home SL', 'Windows 11 Pro', 'macOS'], index=3)
        laptop_resolution = right_column.selectbox("Độ phân giải", ['Full HD', '2.2K', '2K', 'WQXGA', 'HD', 'QHD+', 'QHD', '2.8K', '4K/UHD', 'WQHD', 'Full HD+', '4K/UHD+','WUXGA', 'Retina', 'Liquid Retina'], index=0)
        laptop_year = right_column.text_input("Năm sản xuất", example_data['laptop_year'])
        laptop_warranty_time = right_column.text_input("Thời gian bảo hành (Tháng)", example_data['laptop_warranty_time'])
        laptop_warranty_location = right_column.selectbox("Địa điểm bảo hành", ['Chính Hãng', 'Cửa Hàng'], index=0)
        laptop_price_new = right_column.text_input("Giá mua mới (Triệu đồng)", example_data['laptop_price_new'])
        model_name = right_column.selectbox("Mô Hình Dự Đoán", ['RandomForest', 'Lasso', 'Ridge', 'ElasticNet', 'LinearRegression'], index=4)
    
    # Load model
    model_path = f"pkl\{model_name}.pkl"
    pipe = pickle.load(open(model_path, "rb")) 

    # extract data
    if laptop_name and laptop_cpu and laptop_graphic_name:
        laptop_brand = laptop_name.split(' ')[1]
        laptop_type = 'gaming' if 'gaming' in laptop_name.lower() else 'general'
        laptop_cpu_brand = laptop_cpu.split(' ')[0]
        laptop_graphic = "Card tích hợp" if any(x in laptop_graphic_name.lower() for x in ["intel", "amd"]) else "Card rời"

        # Encode categorical features
        encoded_laptop_name = label_encoders['Name'].transform([laptop_name])[0]
        encoded_laptop_brand = label_encoders['Laptop Brand'].transform([laptop_brand])[0]
        encoded_laptop_type = label_encoders['Laptop Type'].transform([laptop_type])[0]
        encoded_laptop_cpu = label_encoders['CPU'].transform([laptop_cpu])[0]
        encoded_laptop_cpu_brand = label_encoders['CPU Brand'].transform([laptop_cpu_brand])[0]
        encoded_laptop_ram_type = label_encoders['Ram Type'].transform([laptop_ram_type])[0]
        encoded_laptop_hard_drive = label_encoders['Hard Drive'].transform([laptop_hard_drive])[0]
        encoded_laptop_resolution = label_encoders['Resolution'].transform([laptop_resolution])[0]
        encoded_laptop_os = label_encoders['OS'].transform([laptop_os])[0]
        encoded_laptop_graphic = label_encoders['Graphic'].transform([laptop_graphic])[0]
        encoded_laptop_warranty_location = label_encoders['Warranty Location'].transform([laptop_warranty_location])[0]
        encoded_laptop_graphic_name = label_encoders['Graphic Name'].transform([laptop_graphic_name])[0]


    if st.button("Predict"):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        if laptop_name and laptop_cpu and laptop_graphic_name:
            input_data = [  encoded_laptop_name, encoded_laptop_type, encoded_laptop_brand, encoded_laptop_cpu, encoded_laptop_cpu_brand, encoded_laptop_ram_type,
                            encoded_laptop_hard_drive, encoded_laptop_resolution, encoded_laptop_os, encoded_laptop_graphic, encoded_laptop_graphic_name, laptop_price_new,
                            laptop_ram, laptop_hard_drive_size, laptop_warranty_time, laptop_year, encoded_laptop_warranty_location]
            input_data = [input_data]
            predicted_price = pipe.predict(input_data)
            col1, col2, col3, col4 = st.columns(4)

            img_src = search_image_base(laptop_name, driver)
            result = search_image(laptop_name, float(laptop_warranty_time), driver)
            driver.quit()


            with col2:
                container = st.container(border=True)

                if img_src is not None:
                    with container:
                        st.markdown(
                            f"<h5 style='text-align: center;'>Mô Hình {model_name} Dự Đoán</h5>",
                            unsafe_allow_html=True
                        )
                        st.image(img_src, use_column_width=True, output_format='PNG')
                        st.markdown(
                            f"<h6 style='text-align: center;'>{laptop_name}</h6>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<p style='text-align: center;'><strong>Giá:</strong> {'{:,.0f}₫'.format(predicted_price[0] * 1000000).replace(',', '.')}</p>",
                            unsafe_allow_html=True
                        )
                else:
                    with container:
                        st.markdown(
                            f"<h5 style='text-align: center;'>Mô Hình {model_name} Dự Đoán</h5>",
                            unsafe_allow_html=True
                        )
                        st.image('data/R.png', use_column_width=True, output_format='PNG')
                        st.markdown(
                            f"<h6 style='text-align: center;'>{laptop_name}</h6>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<p style='text-align: center;'><strong>Giá:</strong> {'{:,.0f}₫'.format(predicted_price[0] * 1000000).replace(',', '.')}</p>",
                            unsafe_allow_html=True
                        )


            with col3:
                container = st.container(border=True)

                if result is not None:
                    with container:
                        st.markdown(
                            f"<h5 style='text-align: center;'>Thông Tin Sản Phẩm Cũ Từ TheGioiDiDong</h5>",
                            unsafe_allow_html=True
                        )
                        st.image(result[1], use_column_width=True, output_format='PNG')
                        st.markdown(
                            f"<h6 style='text-align: center;'><a href='{result[0]}'>{laptop_name}</a></h6>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<p style='text-align: center;'><strong>Giá:</strong> {result[2]}</p>",
                            unsafe_allow_html=True
                        )
                else:
                    with container:
                        st.markdown(
                            f"<h5 style='text-align: center;'>Không Tìm Thấy Sản Phẩm Cũ Từ TheGioiDiDong</h5>",
                            unsafe_allow_html=True
                        )
                        st.image('data/R.png', use_column_width=True, output_format='PNG')
                        st.markdown(
                            f"<h6 style='text-align: center;'>{laptop_name}</a></h6>",
                            unsafe_allow_html=True
                        )

