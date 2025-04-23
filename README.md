# Team FTE Calculator

📊 **Team FTE Calculator** is a web-based application built with **Streamlit** that helps users calculate and visualize FTE (Full-Time Equivalent) metrics for internal and external teams. This tool assists in determining the capacity, delta, and demand for tech and management teams in a program or project.

## Features
- **Input Variables:**
  - Internal and external team chargeability
  - Internal and external team headcount
  - Client demand (FTEs)
  - Internal and external management team headcount
  - Total team demand (optional)
- **FTE Calculation:**
  - Tech FTE capacity, management FTE capacity, and total team FTE capacity
  - Delta between team capacity and client demand
- **Visualizations:**
  - Program headcount chart with custom purple color gradient
  - Program delivery FTE delta chart, showing internal tech and total team FTEs vs client demand, with color adjustments for clarity
- **Export Data:**
  - Option to download calculated data as a CSV or Excel file

## Getting Started

### Prerequisites
To run this application locally, make sure you have the following installed:
- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- NumPy

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/team-fte-calculator.git
   cd team-fte-calculator

#### Create a virtual environment - optional, but recommended

python -m venv venv

#### Install Required Dependencies 

pip install -r requirements.txt

#### Running the Application 

streamlit run app.py
