import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="温州市PM2.5时空可视化分析",
    page_icon="🌍",
    layout="wide"
)

def fetch_realtime_data():
    try:
        url = "https://www.air-level.com/air/wenzhou/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = []
        stations = ['鹿城站', '龙湾站', '瓯海站', '瑞安站', '乐清站', '永嘉站', '洞头站', '平阳站', '苍南站', '泰顺站']
        coords = {
            '鹿城站': (120.65, 28.01),
            '龙湾站': (120.75, 27.95),
            '瓯海站': (120.60, 27.98),
            '瑞安站': (120.62, 27.80),
            '乐清站': (120.95, 28.15),
            '永嘉站': (120.80, 28.25),
            '洞头站': (121.10, 27.85),
            '平阳站': (120.50, 27.65),
            '苍南站': (120.35, 27.50),
            '泰顺站': (119.75, 27.68)
        }
        
        for station in stations:
            pm25 = np.random.randint(20, 80)
            pm10 = pm25 + np.random.randint(15, 30)
            so2 = np.random.randint(5, 20)
            no2 = np.random.randint(20, 50)
            co = round(np.random.uniform(0.5, 1.5), 2)
            o3 = np.random.randint(30, 80)
            
            if pm25 <= 35:
                aqi = np.random.randint(0, 50)
                level = '优'
            elif pm25 <= 75:
                aqi = np.random.randint(51, 100)
                level = '良'
            elif pm25 <= 115:
                aqi = np.random.randint(101, 150)
                level = '轻度污染'
            else:
                aqi = np.random.randint(151, 200)
                level = '中度污染'
            
            lon, lat = coords[station]
            data.append({
                '日期': datetime.now().strftime('%Y-%m-%d'),
                '站点': station,
                'PM2.5': pm25,
                'PM10': pm10,
                'SO2': so2,
                'NO2': no2,
                'CO': co,
                'O3': o3,
                'AQI': aqi,
                '质量等级': level,
                '经度': lon,
                '纬度': lat
            })
        
        return pd.DataFrame(data), datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        st.error(f"获取实时数据失败: {str(e)}")
        return None, None

@st.cache_data
def load_historical_data():
    try:
        df = pd.read_csv('../data/pm25_data.csv')
        df['日期'] = pd.to_datetime(df['日期'])
        df['月份'] = df['日期'].dt.month
        df['季度'] = df['日期'].dt.quarter
        return df
    except Exception as e:
        st.warning(f"加载历史数据失败，使用模拟数据: {str(e)}")
        stations = ['鹿城站', '龙湾站', '瓯海站', '瑞安站', '乐清站', '永嘉站', '洞头站', '平阳站', '苍南站', '泰顺站']
        coords = {
            '鹿城站': (120.65, 28.01), '龙湾站': (120.75, 27.95), '瓯海站': (120.60, 27.98),
            '瑞安站': (120.62, 27.80), '乐清站': (120.95, 28.15), '永嘉站': (120.80, 28.25),
            '洞头站': (121.10, 27.85), '平阳站': (120.50, 27.65), '苍南站': (120.35, 27.50),
            '泰顺站': (119.75, 27.68)
        }
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        data = []
        for date in dates:
            for station in stations:
                pm25 = np.random.randint(25, 75)
                pm10 = pm25 + np.random.randint(15, 30)
                so2 = np.random.randint(5, 20)
                no2 = np.random.randint(20, 50)
                co = round(np.random.uniform(0.5, 1.5), 2)
                o3 = np.random.randint(30, 80)
                if pm25 <= 35:
                    aqi = np.random.randint(0, 50)
                    level = '优'
                elif pm25 <= 75:
                    aqi = np.random.randint(51, 100)
                    level = '良'
                elif pm25 <= 115:
                    aqi = np.random.randint(101, 150)
                    level = '轻度污染'
                else:
                    aqi = np.random.randint(151, 200)
                    level = '中度污染'
                lon, lat = coords[station]
                data.append({
                    '日期': date, '站点': station, 'PM2.5': pm25, 'PM10': pm10,
                    'SO2': so2, 'NO2': no2, 'CO': co, 'O3': o3, 'AQI': aqi,
                    '质量等级': level, '经度': lon, '纬度': lat
                })
        df = pd.DataFrame(data)
        df['月份'] = df['日期'].dt.month
        df['季度'] = df['日期'].dt.quarter
        return df

def main():
    st.title('🌍 温州市城市空气质量 PM2.5 时空可视化分析')
    st.markdown('---')

    tab1, tab2 = st.tabs(['📊 实时数据', '📈 历史分析'])

    with tab1:
        st.subheader('🔄 实时空气质量数据')
        
        if st.button('刷新实时数据', use_container_width=True):
            with st.spinner('正在获取最新数据...'):
                realtime_df, update_time = fetch_realtime_data()
                if realtime_df is not None:
                    st.success(f'数据更新成功！更新时间: {update_time}')
                    st.session_state['realtime_data'] = realtime_df
                    st.session_state['update_time'] = update_time
        
        if 'realtime_data' in st.session_state:
            realtime_df = st.session_state['realtime_data']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('当前PM2.5均值', f"{realtime_df['PM2.5'].mean():.1f} μg/m³")
            with col2:
                st.metric('当前AQI均值', f"{realtime_df['AQI'].mean():.1f}")
            with col3:
                st.metric('更新时间', st.session_state['update_time'])
            
            st.subheader('各站点实时数据')
            st.dataframe(realtime_df[['站点', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'AQI', '质量等级']], use_container_width=True)
            
            st.subheader('📍 实时空间分布')
            fig, ax = plt.subplots(figsize=(12, 8))
            scatter = ax.scatter(realtime_df['经度'], realtime_df['纬度'], 
                                s=realtime_df['PM2.5']*25, 
                                c=realtime_df['PM2.5'],
                                cmap='coolwarm', alpha=0.8)
            
            for i, row in realtime_df.iterrows():
                ax.text(row['经度'], row['纬度']+0.02, row['站点'], fontsize=10, ha='center')
            
            ax.set_xlabel('经度 (°E)', fontsize=12)
            ax.set_ylabel('纬度 (°N)', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.5)
            plt.colorbar(scatter, label='PM2.5浓度 (μg/m³)')
            st.pyplot(fig)
            
            st.subheader('🏭 各站点PM2.5实时浓度对比')
            fig, ax = plt.subplots(figsize=(12, 5))
            sorted_data = realtime_df.sort_values('PM2.5')
            colors = []
            for val in sorted_data['PM2.5']:
                if val <= 35:
                    colors.append('#00E400')
                elif val <= 75:
                    colors.append('#FFFF00')
                else:
                    colors.append('#FF7E00')
            ax.bar(sorted_data['站点'], sorted_data['PM2.5'], color=colors)
            ax.set_xticklabels(sorted_data['站点'], rotation=45, ha='right')
            ax.set_ylabel('PM2.5浓度 (μg/m³)')
            st.pyplot(fig)

        else:
            st.info('点击上方按钮获取实时数据')

    with tab2:
        historical_df = load_historical_data()
        if historical_df is None:
            st.error('无法加载历史数据')
            return
        
        st.sidebar.header('🔍 筛选条件')
        selected_stations = st.sidebar.multiselect(
            '选择监测站点',
            historical_df['站点'].unique(),
            default=historical_df['站点'].unique()
        )
        
        selected_months = st.sidebar.slider(
            '选择月份范围',
            1, 12, (1, 12)
        )
        
        filtered_df = historical_df[
            (historical_df['站点'].isin(selected_stations)) &
            (historical_df['月份'] >= selected_months[0]) &
            (historical_df['月份'] <= selected_months[1])
        ]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('PM2.5年均浓度', f"{filtered_df['PM2.5'].mean():.1f} μg/m³")
        with col2:
            st.metric('AQI年均值', f"{filtered_df['AQI'].mean():.1f}")
        with col3:
            st.metric('优良天数比例', f"{(len(filtered_df[filtered_df['质量等级'].isin(['优', '良'])])/len(filtered_df)*100):.1f}%")
        with col4:
            st.metric('监测站点数量', len(selected_stations))
        
        st.markdown('---')
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader('📈 PM2.5月均浓度变化趋势')
            monthly_data = filtered_df.groupby('月份')['PM2.5'].mean()
            months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(1, 13), monthly_data.reindex(range(1, 13)).values, marker='o', color='#E74C3C', linewidth=3)
            ax.set_xlabel('月份', fontsize=12)
            ax.set_ylabel('PM2.5浓度 (μg/m³)', fontsize=12)
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(months, fontsize=10)
            ax.set_ylim(0, 80)
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
        
        with col_b:
            st.subheader('📊 PM2.5季度平均浓度')
            seasonal_data = filtered_df.groupby('季度')['PM2.5'].mean()
            season_labels = ['春季', '夏季', '秋季', '冬季']
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.bar(season_labels, seasonal_data.reindex([1, 2, 3, 4]).values, color=['#667eea', '#764ba2', '#f093fb', '#f5576c'], width=0.6)
            ax.set_xlabel('季度', fontsize=12)
            ax.set_ylabel('PM2.5浓度 (μg/m³)', fontsize=12)
            ax.set_ylim(0, 80)
            ax.tick_params(axis='both', labelsize=11)
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}', ha='center', va='bottom', fontsize=10)
            st.pyplot(fig)
        
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader('🏭 各站点PM2.5平均浓度')
            station_data = filtered_df.groupby('站点')['PM2.5'].mean().sort_values()
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = []
            for val in station_data.values:
                if val < 35:
                    colors.append('#00E400')
                elif val < 50:
                    colors.append('#7ED321')
                elif val < 60:
                    colors.append('#C3C300')
                elif val < 75:
                    colors.append('#FF7E00')
                else:
                    colors.append('#FF0000')
            bars = ax.barh(station_data.index, station_data.values, color=colors, height=0.7)
            ax.set_xlabel('PM2.5平均浓度 (μg/m³)', fontsize=12)
            ax.set_ylabel('监测站点', fontsize=12)
            ax.set_xlim(0, 75)
            ax.tick_params(axis='both', labelsize=11)
            st.pyplot(fig)
        
        with col_d:
            st.subheader('🎯 空气质量等级分布')
            quality_counts = filtered_df['质量等级'].value_counts()
            colors = {'优': '#00E400', '良': '#FFFF00', '轻度污染': '#FF7E00', '中度污染': '#FF0000'}
            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(quality_counts.values, labels=quality_counts.index,
                   colors=[colors[k] for k in quality_counts.index],
                   autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
            ax.axis('equal')
            st.pyplot(fig)
        
        st.subheader('📍 PM2.5空间分布')
        fig, ax = plt.subplots(figsize=(12, 8))
        station_locations = filtered_df.groupby('站点').agg({
            'PM2.5': 'mean',
            '经度': 'first',
            '纬度': 'first'
        }).reset_index()
        
        scatter = ax.scatter(station_locations['经度'], station_locations['纬度'], 
                            s=station_locations['PM2.5']*20, 
                            c=station_locations['PM2.5'],
                            cmap='coolwarm', alpha=0.8)
        
        for i, row in station_locations.iterrows():
            ax.text(row['经度'], row['纬度']+0.02, row['站点'], fontsize=10, ha='center')
        
        ax.set_xlabel('经度 (°E)', fontsize=12)
        ax.set_ylabel('纬度 (°N)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.colorbar(scatter, label='PM2.5浓度 (μg/m³)')
        st.pyplot(fig)
        
        col_e, col_f = st.columns(2)
        with col_e:
            st.subheader('📅 各月份空气质量等级分布')
            monthly_quality = filtered_df.groupby(['月份', '质量等级']).size().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(10, 5))
            monthly_quality.plot(kind='bar', stacked=True, ax=ax, 
                               color={'优': '#00E400', '良': '#FFFF00', '轻度污染': '#FF7E00', '中度污染': '#FF0000'})
            ax.set_xlabel('月份', fontsize=12)
            ax.set_ylabel('天数', fontsize=12)
            ax.legend(title='空气质量等级')
            st.pyplot(fig)
        
        with col_f:
            st.subheader('🔗 污染物相关性矩阵')
            corr_data = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'AQI']]
            corr_matrix = corr_data.corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax,
                        annot_kws={'size': 10})
            st.pyplot(fig)
        
        st.download_button(
            label='📥 下载数据',
            data=filtered_df.to_csv(index=False),
            file_name='温州PM25数据.csv',
            mime='text/csv'
        )
    
    st.markdown('---')
    st.markdown('📊 **数据来源**：温州市生态环境监测中心 | **分析周期**：2024年1月-12月')
    st.markdown('⚠️ **说明**：实时数据为模拟数据，实际应用中可接入官方API获取真实数据')

if __name__ == '__main__':
    main()