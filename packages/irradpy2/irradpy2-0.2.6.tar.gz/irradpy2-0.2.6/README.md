# irrapy2

**irrapy2** is a lightweight Python toolkit for downloading, parsing, and processing **multi-source ground-based solar radiation and meteorological datasets**, combined with a simple forecasting module (RNN / LSTM / Informer).

The package provides a unified interface to several international radiation networks:

- **BSRN** – Baseline Surface Radiation Network  
- **MIDC (NREL)** – Measurement & Instrumentation Data Center  
- **SAURAN** – Southern African Universities Radiometric Network  
- **SRML** – Solar Radiation Monitoring Laboratory (UOregon)  
- **SURFRAD (NOAA)** – Surface Radiation Budget Network  
- **SOLRAD (NOAA)** – Solar Radiation Network  

It also includes a built-in forecasting tool for solar irradiance time series.

---

## 📦 Installation

```bash
pip install irrapy2
```

---

## 🚀 Quick Start

### Download BSRN data

```python
from irrapy2 import download_bsrn

download_bsrn(
    site="cab",
    start="2023-01-01",
    end="2023-01-31",
    username="your_bsrn_username",
    password="your_bsrn_password",
    save_path="bsrn_out.csv"
)
```

### Download MIDC data

```python
from irrapy2 import download_midc

download_midc(
    site="BMS",
    begin="20230101",
    end="20230131",
    save_path="midc_out.csv"
)
```

### Forecast Solar Radiation

```python
from irrapy2 import run_forecast

metrics = run_forecast(
    csv_path="bsrn_out.csv",
    model="lstm",       # rnn / lstm / informer
    seq_len=72,
    horizon=6,
    epochs=10
)

print(metrics)
```

---

## 📁 Supported Datasets

| Source | Region | Module | Time Handling |
|--------|--------|---------|---------------|
| BSRN | Global | `download_bsrn` | UTC |
| MIDC (NREL) | USA | `download_midc` | Local + DST + UTC |
| SAURAN | Africa | `download_sauran` | Local → UTC |
| SRML | USA | `download_srml` | America/Los_Angeles |
| SURFRAD | USA | `download_surfrad` | UTC |
| SOLRAD | USA | `download_solrad` | UTC + Local |

---

## 🔧 Requirements

```
pandas
numpy
requests
pytz
torch
scikit-learn
```

---

## 📄 License

This project is open-source and licensed under the **Apache License 2.0**.

---

## 🙌 Contributing

Issues and pull requests are welcome.  
Feel free to open a PR if you want to add more stations, enhance parsing logic, or improve the forecasting module.
