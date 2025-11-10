# Forage Data Science Projects

Welcome to my **Forage Data Science Projects**! This repository documents my journey through 100 days of learning project-driven data science.

---

## Projects

### 1. **Project 1: [ACCENTURE DATA ANALYTICS AND VISUALIZATION]**

- **Description**:  
  We conducted a comprehensive data analysis project for **Social Buzz**, a rapidly growing social media platform. Our goal was to audit their big data practices, provide IPO recommendations, and analyze content category popularity to inform their scaling strategy.

 
- **Tools**:
  - `pandas`, `seaborn`, `matplotlib`

- **Outcome**:  
 
  - Identified the top 5 content categories by popularity
  - Provided insights on content popularity trends throughout the day
  - Developed recommendations for targeted content scheduling
  - Highlighted opportunities for cross-category content development
  - Identified underperforming categories for potential improvement
  - Delivered a comprehensive report on big data best practices
  - Prepared actionable recommendations for a successful IPO

---

### 2. **Project 2: [British Airways]**

- **Description**:  
  The goal of this project was to scrape customer reviews from the Skytrax website, specifically focusing on feedback related to **British Airways (BA)**. After collecting the reviews, I performed data cleaning, sentiment analysis, and topic modeling to identify key insights about customer satisfaction and dissatisfaction. The project aimed to uncover trends in customer sentiment, common themes in the feedback, and actionable insights to help BA improve its service quality and customer experience.

- **Tools**:  
  - **Web Scraping**: `BeautifulSoup`, `Selenium`
  - **Programming Language**: `Python`
  - **Data Cleaning and Analysis**: `Pandas`, `NumPy`, `NLTK (Natural Language Toolkit)`
  - **Sentiment Analysis**: `Vader`, `TextBlob`
  - **Topic Modeling**: `Latent Dirichlet Allocation (LDA)`
  - **Data Visualization**: `Matplotlib`, `Seaborn`, `WordCloud`
  - **Presentation**: `Microsoft PowerPoint`

- **Outcome**:  
  The data scraping process collected a comprehensive dataset of BA reviews. Through sentiment analysis, I found that:
  - The majority of the reviews were positive, particularly regarding staff service and in-flight comfort.
  - Negative reviews focused on delays, luggage handling, and pricing issues.  

  Topic modeling revealed key themes such as:
  - **“on-time performance”**
  - **“staff friendliness”**
  - **“baggage issues”**

  The insights were summarized in a **PowerPoint slide** with visualizations, providing actionable recommendations for British Airways to address customer pain points and enhance overall service quality.

---


### 3. **Project 3: BCG x PowerCo Churn Analysis**

**Description:**
This project focuses on analyzing customer churn for PowerCo. The aim was to investigate whether price sensitivity is the most influential factor in customer churn and, if not, to what extent it influences churn. The analysis included examining customer data, visualizing distributions, and performing exploratory data analysis (EDA) to derive actionable insights.

**Tools:**

- Data Analysis: Pandas
- Data Visualization: Matplotlib, Seaborn
- Exploratory Data Analysis: Jupyter Notebook

**Outcome:**

- Analyzed the impact of various factors on customer churn, including price sensitivity.
- Reported data types and descriptive statistics of the datasets.
- Visualized distributions of relevant columns to identify trends and patterns.
- Provided insights on customer behavior to inform retention strategies.

...

---

## Streamlit Dashboards

Each project now has an accompanying Streamlit dashboard that lives alongside the source notebooks under the `projects/` directory. Launch any dashboard with the commands below (run from the repository root):

- **Social Buzz Content Performance** (`projects/accenture_social_buzz/app.py`)

  ```bash
  streamlit run projects/accenture_social_buzz/app.py
  ```

- **British Airways Customer Feedback** (`projects/british_airways_reviews/app.py`)

  ```bash
  streamlit run projects/british_airways_reviews/app.py
  ```

- **PowerCo Customer Churn Explorer** (`projects/powerco_churn/app.py`)

  ```bash
  streamlit run projects/powerco_churn/app.py
  ```

- **Lloyds Customer Segmentation** (`projects/lloyds_customer_segments/app.py`)

  ```bash
  streamlit run projects/lloyds_customer_segments/app.py
  ```

### Repository Layout

```text
projects/
├── accenture_social_buzz/
│   ├── notebooks/
│   └── app.py
├── british_airways_reviews/
│   ├── notebooks/
│   └── app.py
├── powerco_churn/
│   ├── notebooks/
│   └── app.py
└── lloyds_customer_segments/
    ├── notebooks/
    └── app.py
```

The dashboards consume the cleaned datasets in the top-level `data/` folder, so there is no need to duplicate data files inside each project.

## About

This repository is part of my commitment to learning data science through hands-on projects. Each project is designed to tackle real-world problems and enhance my skills in data analysis, machine learning, and data visualization.

## Contact

Feel free to reach out if you have any questions or suggestions!

- Email: [21407alfredmunga@gmail.com]
\

Happy Learning!
