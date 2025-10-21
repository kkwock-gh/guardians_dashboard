# TDSS Dashboard

**Techdev Dashboard for Troubleshooting**

A Streamlit-based dashboard application for technical troubleshooting and monitoring.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kkwock-gh/tdss_dashboard.git
   cd tdss_dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

To launch the Streamlit dashboard, run:

```bash
streamlit run app.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

If it doesn't open automatically, you can manually navigate to the URL shown in the terminal.

## 📋 Features

- **Home Page**: Overview with key metrics and system status
- **Dashboard**: Real-time monitoring and visualizations
- **Analytics**: Data analysis and insights
- **Settings**: Customizable dashboard preferences

## 🛠️ Development

### Project Structure

```
tdss_dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

### Customization

You can customize the dashboard by modifying `app.py`:

- Add new pages by creating new functions and updating the navigation
- Add custom visualizations using Streamlit's charting components
- Integrate with your own data sources and APIs

## 📦 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips

- Press `R` in the browser to refresh/rerun the app
- Use `Ctrl+C` in the terminal to stop the server
- Check the Streamlit documentation at https://docs.streamlit.io for more features
