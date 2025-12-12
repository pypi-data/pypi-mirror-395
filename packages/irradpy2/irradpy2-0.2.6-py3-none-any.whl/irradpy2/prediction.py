import os, json, math
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
# =====================================================
# Global settings (default values, can be overridden)
# =====================================================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CHECKPOINT_DIR = "checkpoints"
RESULT_DIR = "results"
CONFIG_DIR = "configs"
for d in [CHECKPOINT_DIR, RESULT_DIR, CONFIG_DIR]:
    os.makedirs(d, exist_ok=True)


# =====================================================
# Auto-mapping for multi-site meteorological datasets
# (Supports SURFRAD, BSRN, MIDC, SRML, SOLRAD, NOAA, etc.)
# =====================================================
COLUMN_KEYWORDS = {
    # ---- Global irradiance (GHI) ----
    "Global": [
        "global", "ghi", "avg_global", "global_irradiance",
        "total_irradiance", "dw_psp", "dwpsp",
        "dw_solar", "dwsolar", "ghi_", "ghi2"
    ],

    # ---- Direct irradiance (DNI) ----
    "Direct": [
        "direct", "dni", "avg_direct",
        "beam_irradiance", "dnic", "dnic"
    ],

    # ---- Diffuse irradiance (DHI) ----
    "Diffuse": [
        "diffuse", "dhi", "diffuse_irradiance"
    ],

    # ---- Air temperature ----
    "AirTemp": [
        "airtemp", "temp", "temperature", "tair",
        "drybulb", "airtc", "towerdrybulb"
    ],

    # ---- Relative humidity ----
    "RH": [
        "rh", "humidity", "relative_humidity"
    ],

    # ---- Pressure ----
    "Pressure": [
        "pressure", "press", "mbar", "bp_mbar"
    ]
}


# =====================================================
#  Column matching helper
# =====================================================
def match_column(columns, keywords):
    """Return the first column whose name contains ANY keyword."""
    for col in columns:
        cname = col.lower().replace(" ", "").replace("_", "")
        for kw in keywords:
            if kw in cname:
                return col
    return None


# =====================================================
#  Standardize CSV (auto-detect time + meteorological fields)
# =====================================================
def standardize_csv(file_path):
    print(f"\n📥 Reading file: {file_path}")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # -------- Time column detection (UTC → Local → fallback) --------
    utc_kw = ["utc_time", "utc", "timestamp_utc", "time_utc"]
    local_kw = ["local_time", "local", "lst", "lt"]
    basic_kw = ["time", "date", "timestamp"]

    utc_col = match_column(df.columns, utc_kw)
    local_col = match_column(df.columns, local_kw)
    basic_col = match_column(df.columns, basic_kw)

    if utc_col:
        time_col = utc_col
        print(f"⏱ Using UTC time: {time_col}")
    elif local_col:
        time_col = local_col
        print(f"⏱ Using Local time: {time_col}")
    else:
        time_col = basic_col
        print(f"⏱ Using fallback time: {time_col}")

    if time_col is None:
        raise ValueError("❌ No timestamp column detected!")

    df["Timestamp"] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp")

    # -------- Meteorological feature detection --------
    features = {}
    for key, kw_list in COLUMN_KEYWORDS.items():
        col = match_column(df.columns, kw_list)
        if col:
            features[key] = df[col].astype(float)
        else:
            print(f"⚠ Missing {key}, filling zeros.")
            features[key] = pd.Series(0, index=df.index)

    df_std = pd.DataFrame({"Timestamp": df["Timestamp"], **features})

    # Replace error codes and fill gaps
    df_std = df_std.replace([-9999, -99, -999], np.nan)
    df_std = df_std.ffill().bfill()
    return df_std


# =====================================================
# Dataset builder
# =====================================================
class SeqDataset(Dataset):
    """Sequence-to-one supervised dataset."""
    def __init__(self, X, y, seq_len, horizon):
        self.X = X
        self.y = y
        self.seq_len = seq_len
        self.horizon = horizon

    def __len__(self):
        return max(0, len(self.X) - self.seq_len - self.horizon)

    def __getitem__(self, i):
        x = self.X[i:i+self.seq_len]
        y = self.y[i+self.seq_len+self.horizon-1]
        return (
            torch.tensor(x, dtype=torch.float32),
            torch.tensor(y, dtype=torch.float32)
        )


# =====================================================
# Models
# =====================================================
class RNNModel(nn.Module):
    def __init__(self, in_dim, hidden=128):
        super().__init__()
        self.rnn = nn.RNN(in_dim, hidden, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, x):
        out, _ = self.rnn(x)
        return self.fc(out[:, -1]).squeeze()


class LSTMModel(nn.Module):
    def __init__(self, in_dim, hidden=128):
        super().__init__()
        self.lstm = nn.LSTM(in_dim, hidden, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1]).squeeze()


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(0, max_len).unsqueeze(1)
        div = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000) / d_model))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)].to(x.device)


class InformerLite(nn.Module):
    def __init__(self, in_dim, d_model=128, nhead=4, num_layers=2):
        super().__init__()
        self.in_proj = nn.Linear(in_dim, d_model)
        self.pos = PositionalEncoding(d_model)
        layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead,
            dim_feedforward=256, dropout=0.1,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers)
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        x = self.pos(self.in_proj(x))
        out = self.encoder(x)
        return self.fc(out[:, -1]).squeeze()


# =====================================================
# Training utilities
# =====================================================
def evaluate(model, loader):
    model.eval()
    loss_fn = nn.MSELoss()
    total = 0
    with torch.no_grad():
        for xb, yb in loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            total += loss_fn(model(xb), yb).item() * len(xb)
    return total / len(loader.dataset)


def calc_metrics(y_true, y_pred):
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred)**2)))
    mape = float(
        np.mean(np.abs((y_true - y_pred) / np.clip(y_true, 1e-3, None))) * 100
    )
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}


def train_model(model, train_loader, val_loader, epochs=50, lr=1e-3):
    model = model.to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    best_val = float("inf")
    history = {"train_loss": [], "val_loss": []}

    for ep in range(epochs):
        model.train()
        total = 0
        for xb, yb in train_loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            total += loss.item() * len(xb)

        train_loss = total / len(train_loader.dataset)
        val_loss = evaluate(model, val_loader)
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        print(f"Epoch {ep+1}/{epochs} | Train={train_loss:.4f} | Val={val_loss:.4f}")

        if val_loss < best_val:
            best_val = val_loss
            torch.save(model.state_dict(), f"{CHECKPOINT_DIR}/best_model.pt")

    return model, history


# =====================================================
# Main pipeline (NOW SUPPORTS CUSTOM PARAMETERS)
# =====================================================
def run_forecast(
        csv_path,
        model="lstm",
        seq_len=72,
        horizon=6,
        epochs=50,
        batch_size=64):
    """
    Unified forecasting API:
        - Auto-detects meteorological fields
        - Supports RNN / LSTM / Informer
        - Allows custom seq_len, horizon, epochs, batch_size
    """
    print(f"\n🚀 Running forecast ({model.upper()})")

    df_std = standardize_csv(csv_path)
    features = ["Global", "Direct", "Diffuse", "AirTemp", "RH", "Pressure"]

    X = df_std[features].values
    y = df_std["Global"].values

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    y_max = np.max(y)
    y_scaled = y / y_max

    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y_scaled, test_size=0.3, shuffle=False
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, shuffle=False
    )

    ds_train = SeqDataset(X_train, y_train, seq_len, horizon)
    ds_val = SeqDataset(X_val, y_val, seq_len, horizon)
    ds_test = SeqDataset(X_test, y_test, seq_len, horizon)

    dl_train = DataLoader(ds_train, batch_size=batch_size, shuffle=True)
    dl_val = DataLoader(ds_val, batch_size=batch_size)
    dl_test = DataLoader(ds_test, batch_size=batch_size)

    in_dim = X_train.shape[1]

    if model == "rnn":
        net = RNNModel(in_dim)
    elif model == "lstm":
        net = LSTMModel(in_dim)
    elif model == "informer":
        net = InformerLite(in_dim)
    else:
        raise ValueError("❌ model must be rnn / lstm / informer")

    net, history = train_model(net, dl_train, dl_val, epochs)

    net.load_state_dict(torch.load(f"{CHECKPOINT_DIR}/best_model.pt"))
    net.eval()

    y_true, y_pred = [], []
    with torch.no_grad():
        for xb, yb in dl_test:
            pred = net(xb.to(DEVICE)).cpu().numpy()
            y_pred.extend(pred)
            y_true.extend(yb.numpy())

    y_true = np.array(y_true) * y_max
    y_pred = np.clip(np.array(y_pred), 0, None) * y_max

    pd.DataFrame({"y_true": y_true, "y_pred": y_pred}).to_csv(
        f"{RESULT_DIR}/{model}_pred.csv", index=False
    )

    metrics = calc_metrics(y_true, y_pred)
    print(f"✅ Done! MAE={metrics['MAE']:.4f} RMSE={metrics['RMSE']:.4f} MAPE={metrics['MAPE']:.2f}%")

    return metrics


# =====================================================
# Script entry
# =====================================================
if __name__ == "__main__":
    run_forecast(
        csv_path="sauran_NMU_201901.csv",
        model="lstm",
        seq_len=72,
        horizon=6,
        epochs=10,
        batch_size=64
    )
