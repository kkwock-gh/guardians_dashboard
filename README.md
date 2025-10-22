# Guardians Dashboard

Guardians Dashboard is a Streamlit-based application designed for technical troubleshooting, real-time monitoring, and analytics. This dashboard provides a user-friendly interface to visualize key system metrics, analyze incidents, and customize your monitoring experience.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Navigation](#navigation)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 📊 **Real-time Monitoring Dashboard:** Instantly view the status of multiple systems and monitor key metrics.
- 📈 **Analytics and Insights:** Analyze performance data, incidents, and trends.
- ⚙️ **Customizable Settings:** Adjust refresh rates, themes, and notification preferences.
- 🔍 **Advanced Troubleshooting Tools:** Use built-in tools to assist with technical troubleshooting tasks.

---

## Getting Started

These instructions will help you set up and run the Guardians Dashboard locally for development or troubleshooting purposes.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

---

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kkwock-gh/guardians_dashboard.git
    cd guardians_dashboard
    ```

2. **Install dependencies:**

    The required Python packages are listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    Required packages include:
    - streamlit >= 1.28.0
    - pandas >= 2.0.0
    - numpy >= 1.24.0

---

## Usage

To start the dashboard locally, run:

```bash
streamlit run app.py
```

The application will open in your default web browser. You can also access it at `http://localhost:8501`.

## Running via Docker
```
docker build --no-cache -t guardians_dashboard:latest .

docker run -it --rm \
  -p 8502:8502 \
  -v /screening/scratch/kkwock/haystack_db:/app/haystack_db \
  guardians_dashboard:latest
```
---

## Navigation

The dashboard contains the following sections, accessible via the sidebar:

- **Home:** Overview, key metrics (Active Systems, Alerts, Response Time, Uptime), and feature summary.
- **Dashboard:** Main area for monitoring visualizations, including charts and live data.
- **Analytics:** Displays data analysis on components, performance scores, and incidents.
- **Settings:** Customize refresh rates, theme, and notification options.

### Example Metrics (Home Page)

- **Active Systems**
- **Alerts**
- **Response Time**
- **Uptime**

### Example Visualizations

- Line charts for system data (Dashboard)
- Tabular analytics of component health and incidents (Analytics)

---

## Customization

You can tailor your dashboard experience in the **Settings** section:

- **Refresh Rate:** Adjust how often the dashboard updates data.
- **Theme:** Switch between Light, Dark, or Auto themes.
- **Notifications:** Enable or disable notification popups.

Click **Save Settings** after making adjustments.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

## Support

If you have any issues or suggestions, please open an issue in the [GitHub repository](https://github.com/kkwock-gh/guardians_dashboard/issues).

---

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
