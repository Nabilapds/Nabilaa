import pandas as pd
import streamlit as st

st.title("Dashboard Saya")

# Membaca data dari file CSV terpisah
df = pd.read_csv("data.csv")

# Menampilkan data ke Streamlit
st.dataframe(df)

"""
Dasbor Analitik Keuangan Daerah
Perbandingan Antar Kota + Eksplorasi Data (EDA)

Jalankan lokal :  streamlit run app.py
Data           :  letakkan file CSV/XLSX di folder yang sama (mis. data.csv)
                  atau unggah lewat sidebar.
Kolom wajib    :  'Kota' dan 'Tahun'. Kolom lain bertipe angka dibaca otomatis.
"""

import glob
import io

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# KONFIGURASI HALAMAN & GAYA
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dasbor Analitik Antar Kota",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETTE = px.colors.qualitative.Safe
PLOT_TEMPLATE = "plotly_white"

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {font-weight: 800; letter-spacing: -0.5px;}
    div[data-testid="stMetric"] {
        background: #F6F8FB; border: 1px solid #E3E8EF;
        padding: 14px 16px; border-radius: 12px;
    }
    div[data-testid="stMetricLabel"] {color: #5B6B7F;}
    .small-note {color:#6B7785; font-size: 0.85rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# FUNGSI BANTU
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def baca_data(file_bytes: bytes | None, nama: str | None, path: str | None) -> pd.DataFrame:
    """Membaca CSV/XLSX dari unggahan atau dari path lokal."""
    if file_bytes is not None:
        buf = io.BytesIO(file_bytes)
        if nama.lower().endswith((".xlsx", ".xls")):
            return pd.read_excel(buf)
        return pd.read_csv(buf)
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def cari_file_default() -> str | None:
    for pola in ("*.csv", "*.xlsx", "*.xls"):
        hasil = sorted(glob.glob(pola))
        if hasil:
            return hasil[0]
    return None


def bersihkan(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]
    df["Kota"] = df["Kota"].astype(str).str.strip()
    df["Tahun"] = pd.to_numeric(df["Tahun"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Kota", "Tahun"])
    df["Tahun"] = df["Tahun"].astype(int)
    for c in df.columns.difference(["Kota", "Tahun"]):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.sort_values(["Kota", "Tahun"]).reset_index(drop=True)


def fmt(x: float) -> str:
    if pd.isna(x):
        return "-"
    return f"{x:,.2f}"


def hitung_cagr(awal: float, akhir: float, n: int) -> float:
    if n <= 0 or pd.isna(awal) or pd.isna(akhir) or awal <= 0 or akhir <= 0:
        return np.nan
    return (akhir / awal) ** (1 / n) - 1


def atur_grafik(fig, tinggi=430):
    fig.update_layout(
        template=PLOT_TEMPLATE,
        height=tinggi,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, x=0),
        font=dict(size=13),
    )
    return fig


# ----------------------------------------------------------------------------
# SIDEBAR: DATA & FILTER
# ----------------------------------------------------------------------------
st.sidebar.title("⚙️ Pengaturan")
upload = st.sidebar.file_uploader("Unggah data (CSV / XLSX)", type=["csv", "xlsx", "xls"])

path_default = cari_file_default()
if upload is not None:
    mentah = baca_data(upload.getvalue(), upload.name, None)
    sumber = upload.name
elif path_default:
    mentah = baca_data(None, None, path_default)
    sumber = path_default
else:
    st.title("📊 Dasbor Analitik Antar Kota")
    st.info("Belum ada data. Unggah file CSV/XLSX lewat sidebar atau taruh file data di folder aplikasi.")
    st.stop()

if not {"Kota", "Tahun"}.issubset(mentah.columns):
    st.error("Data harus memiliki kolom **Kota** dan **Tahun**.")
    st.stop()

df = bersihkan(mentah)
kolom_angka = [c for c in df.columns if c not in ("Kota", "Tahun") and pd.api.types.is_numeric_dtype(df[c])]
if not kolom_angka:
    st.error("Tidak ditemukan kolom numerik selain Kota dan Tahun.")
    st.stop()

# tambahkan kolom total
df["TOTAL"] = df[kolom_angka].sum(axis=1, min_count=1)
indikator_semua = kolom_angka + ["TOTAL"]

semua_kota = sorted(df["Kota"].unique())
tahun_min, tahun_max = int(df["Tahun"].min()), int(df["Tahun"].max())

st.sidebar.caption(f"Sumber data: `{sumber}`")
st.sidebar.markdown("---")

kota_pilih = st.sidebar.multiselect("Pilih kota", semua_kota, default=semua_kota[: min(5, len(semua_kota))])
if tahun_min < tahun_max:
    rentang = st.sidebar.slider("Rentang tahun", tahun_min, tahun_max, (tahun_min, tahun_max))
else:
    rentang = (tahun_min, tahun_max)
indikator = st.sidebar.selectbox("Indikator utama", indikator_semua, index=len(indikator_semua) - 1)

if not kota_pilih:
    st.warning("Pilih minimal satu kota di sidebar.")
    st.stop()

dff = df[(df["Kota"].isin(kota_pilih)) & (df["Tahun"].between(*rentang))].copy()
if dff.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

tahun_ref = st.sidebar.selectbox(
    "Tahun pembanding (bar & peringkat)",
    sorted(dff["Tahun"].unique(), reverse=True),
)

# ----------------------------------------------------------------------------
# HEADER & KPI
# ----------------------------------------------------------------------------
st.title("📊 Dasbor Analitik Antar Kota")
st.markdown(
    f"<span class='small-note'>{len(kota_pilih)} kota • {rentang[0]}–{rentang[1]} • "
    f"{len(dff):,} observasi • indikator: <b>{indikator}</b></span>",
    unsafe_allow_html=True,
)

data_ref = dff[dff["Tahun"] == tahun_ref]
total_ref = data_ref[indikator].sum()
rata_ref = data_ref[indikator].mean()
tertinggi = data_ref.loc[data_ref[indikator].idxmax()] if data_ref[indikator].notna().any() else None
terendah = data_ref.loc[data_ref[indikator].idxmin()] if data_ref[indikator].notna().any() else None

# pertumbuhan YoY agregat
agg_tahun = dff.groupby("Tahun")[indikator].sum()
yoy = np.nan
if tahun_ref in agg_tahun.index and (tahun_ref - 1) in agg_tahun.index and agg_tahun[tahun_ref - 1] > 0:
    yoy = agg_tahun[tahun_ref] / agg_tahun[tahun_ref - 1] - 1

k1, k2, k3, k4 = st.columns(4)
k1.metric(f"Total {indikator} ({tahun_ref})", fmt(total_ref), None if pd.isna(yoy) else f"{yoy:+.1%} YoY")
k2.metric("Rata-rata per kota", fmt(rata_ref))
k3.metric("Tertinggi", tertinggi["Kota"] if tertinggi is not None else "-", fmt(tertinggi[indikator]) if tertinggi is not None else None, delta_color="off")
k4.metric("Terendah", terendah["Kota"] if terendah is not None else "-", fmt(terendah[indikator]) if terendah is not None else None, delta_color="off")

st.markdown("")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🏙️ Perbandingan Antar Kota", "📈 Tren & Pertumbuhan", "🔍 Eksplorasi Data (EDA)", "🔗 Korelasi & Regresi", "🗂️ Data"]
)

# ----------------------------------------------------------------------------
# TAB 1: PERBANDINGAN ANTAR KOTA
# ----------------------------------------------------------------------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        urut = data_ref.sort_values(indikator, ascending=True)
        fig = px.bar(
            urut, x=indikator, y="Kota", orientation="h", text=indikator,
            color=indikator, color_continuous_scale="Blues",
            title=f"Peringkat Kota – {indikator} ({tahun_ref})",
        )
        fig.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(atur_grafik(fig), use_container_width=True)

    with c2:
        avg_kota = dff.groupby("Kota")[indikator].mean().reset_index().sort_values(indikator, ascending=False)
        fig = px.bar(
            avg_kota, x="Kota", y=indikator, color="Kota",
            color_discrete_sequence=PALETTE,
            title=f"Rata-rata {indikator} ({rentang[0]}–{rentang[1]})",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(atur_grafik(fig), use_container_width=True)

    # Heatmap kota x tahun
    pivot = dff.pivot_table(index="Kota", columns="Tahun", values=indikator, aggfunc="sum")
    fig = px.imshow(
        pivot, aspect="auto", color_continuous_scale="YlGnBu", text_auto=".0f",
        title=f"Heatmap {indikator}: Kota × Tahun",
    )
    st.plotly_chart(atur_grafik(fig, 80 + 55 * len(pivot)), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        # Komposisi komponen per kota pada tahun pembanding
        komponen = st.multiselect(
            "Komponen untuk komposisi", kolom_angka, default=kolom_angka[: min(6, len(kolom_angka))], key="komp"
        )
        if komponen:
            long = data_ref.melt(id_vars="Kota", value_vars=komponen, var_name="Komponen", value_name="Nilai")
            fig = px.bar(
                long, x="Kota", y="Nilai", color="Komponen", barmode="stack",
                color_discrete_sequence=PALETTE, title=f"Komposisi per Kota ({tahun_ref})",
            )
            st.plotly_chart(atur_grafik(fig), use_container_width=True)

    with c4:
        # Radar: profil relatif (dinormalisasi) tiap kota
        if len(komponen) >= 3:
            rata = dff.groupby("Kota")[komponen].mean()
            norm = (rata - rata.min()) / (rata.max() - rata.min()).replace(0, np.nan)
            norm = norm.fillna(0)
            fig = go.Figure()
            for i, kota in enumerate(norm.index):
                fig.add_trace(
                    go.Scatterpolar(
                        r=norm.loc[kota].tolist() + [norm.loc[kota].iloc[0]],
                        theta=komponen + [komponen[0]],
                        name=kota, fill="toself", opacity=0.45,
                        line=dict(color=PALETTE[i % len(PALETTE)]),
                    )
                )
            fig.update_layout(title="Profil Relatif Antar Kota (0–1)", polar=dict(radialaxis=dict(range=[0, 1])))
            st.plotly_chart(atur_grafik(fig), use_container_width=True)
        else:
            st.caption("Pilih minimal 3 komponen untuk menampilkan radar.")

# ----------------------------------------------------------------------------
# TAB 2: TREN & PERTUMBUHAN
# ----------------------------------------------------------------------------
with tab2:
    fig = px.line(
        dff, x="Tahun", y=indikator, color="Kota", markers=True,
        color_discrete_sequence=PALETTE, title=f"Tren {indikator} per Kota",
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(atur_grafik(fig, 460), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        # CAGR per kota
        baris = []
        for kota, g in dff.groupby("Kota"):
            g = g.dropna(subset=[indikator]).sort_values("Tahun")
            if len(g) >= 2:
                n = g["Tahun"].iloc[-1] - g["Tahun"].iloc[0]
                baris.append(
                    {"Kota": kota, "Awal": g[indikator].iloc[0], "Akhir": g[indikator].iloc[-1],
                     "CAGR": hitung_cagr(g[indikator].iloc[0], g[indikator].iloc[-1], n)}
                )
        cagr = pd.DataFrame(baris)
        if not cagr.empty:
            cagr = cagr.sort_values("CAGR", ascending=False)
            fig = px.bar(
                cagr, x="Kota", y="CAGR", color="CAGR", color_continuous_scale="RdYlGn",
                title="Laju Pertumbuhan Tahunan Majemuk (CAGR)",
            )
            fig.update_yaxes(tickformat=".0%")
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(atur_grafik(fig), use_container_width=True)
            st.dataframe(
                cagr.style.format({"Awal": "{:,.2f}", "Akhir": "{:,.2f}", "CAGR": "{:.2%}"}),
                use_container_width=True, hide_index=True,
            )

    with c2:
        # Pertumbuhan YoY
        yoy_df = dff.sort_values(["Kota", "Tahun"]).copy()
        yoy_df["YoY"] = yoy_df.groupby("Kota")[indikator].pct_change()
        yoy_df = yoy_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["YoY"])
        if not yoy_df.empty:
            fig = px.line(
                yoy_df, x="Tahun", y="YoY", color="Kota", markers=True,
                color_discrete_sequence=PALETTE, title="Pertumbuhan Year-on-Year",
            )
            fig.update_yaxes(tickformat=".0%")
            fig.add_hline(y=0, line_dash="dot", line_color="gray")
            fig.update_xaxes(dtick=1)
            st.plotly_chart(atur_grafik(fig), use_container_width=True)

# ----------------------------------------------------------------------------
# TAB 3: EKSPLORASI DATA (EDA)
# ----------------------------------------------------------------------------
with tab3:
    st.subheader("Ringkasan Dataset")
    a, b, c, d = st.columns(4)
    a.metric("Jumlah baris", f"{len(dff):,}")
    b.metric("Jumlah kolom", f"{dff.shape[1]}")
    c.metric("Missing value", f"{int(dff[kolom_angka].isna().sum().sum()):,}")
    d.metric("Baris duplikat", f"{int(dff.duplicated(['Kota', 'Tahun']).sum()):,}")

    st.markdown("**Statistik deskriptif**")
    desk = dff[indikator_semua].describe().T
    desk["skewness"] = dff[indikator_semua].skew()
    st.dataframe(desk.style.format("{:,.2f}"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        miss = dff[kolom_angka].isna().mean().mul(100).reset_index()
        miss.columns = ["Kolom", "Persen Missing"]
        fig = px.bar(miss, x="Kolom", y="Persen Missing", title="Persentase Data Hilang per Kolom",
                     color_discrete_sequence=["#E4572E"])
        st.plotly_chart(atur_grafik(fig, 350), use_container_width=True)
    with c2:
        tipe = pd.DataFrame({"Kolom": dff.columns, "Tipe": dff.dtypes.astype(str).values,
                             "Unik": [dff[c].nunique() for c in dff.columns]})
        st.markdown("**Tipe data & nilai unik**")
        st.dataframe(tipe, use_container_width=True, hide_index=True, height=300)

    st.subheader("Distribusi Variabel")
    var = st.selectbox("Pilih variabel", indikator_semua, index=indikator_semua.index(indikator), key="eda_var")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(dff, x=var, nbins=20, marginal="rug", color_discrete_sequence=["#2E86AB"],
                           title=f"Histogram {var}")
        st.plotly_chart(atur_grafik(fig, 380), use_container_width=True)
    with c2:
        fig = px.box(dff, x="Kota", y=var, color="Kota", points="all",
                     color_discrete_sequence=PALETTE, title=f"Boxplot {var} per Kota")
        fig.update_layout(showlegend=False)
        st.plotly_chart(atur_grafik(fig, 380), use_container_width=True)

    # Deteksi outlier (IQR)
    st.subheader("Deteksi Outlier (metode IQR)")
    seri = dff[var].dropna()
    q1, q3 = seri.quantile([0.25, 0.75])
    iqr = q3 - q1
    batas_bawah, batas_atas = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outlier = dff[(dff[var] < batas_bawah) | (dff[var] > batas_atas)][["Kota", "Tahun", var]]
    st.caption(f"Batas wajar: {batas_bawah:,.2f} s.d. {batas_atas:,.2f} • ditemukan **{len(outlier)}** outlier")
    if len(outlier):
        st.dataframe(outlier, use_container_width=True, hide_index=True)

    st.subheader("Sebaran Antar Kota & Waktu")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.violin(dff, x="Kota", y=var, color="Kota", box=True,
                        color_discrete_sequence=PALETTE, title=f"Violin {var}")
        fig.update_layout(showlegend=False)
        st.plotly_chart(atur_grafik(fig, 380), use_container_width=True)
    with c2:
        per_tahun = dff.groupby("Tahun")[var].agg(["mean", "median", "std"]).reset_index()
        fig = px.line(per_tahun.melt("Tahun"), x="Tahun", y="value", color="variable", markers=True,
                      title=f"Rata-rata, Median & Std {var} per Tahun")
        fig.update_xaxes(dtick=1)
        st.plotly_chart(atur_grafik(fig, 380), use_container_width=True)

# ----------------------------------------------------------------------------
# TAB 4: KORELASI & REGRESI
# ----------------------------------------------------------------------------
with tab4:
    st.subheader("Matriks Korelasi")
    metode = st.radio("Metode", ["pearson", "spearman"], horizontal=True)
    korel = dff[indikator_semua].corr(method=metode)
    fig = px.imshow(korel, text_auto=".2f", aspect="auto", zmin=-1, zmax=1,
                    color_continuous_scale="RdBu_r", title=f"Korelasi {metode.title()}")
    st.plotly_chart(atur_grafik(fig, 560), use_container_width=True)

    st.subheader("Regresi Linier Sederhana")
    c1, c2 = st.columns(2)
    x_var = c1.selectbox("Variabel X (prediktor)", indikator_semua, index=0)
    y_var = c2.selectbox("Variabel Y (respons)", indikator_semua, index=min(1, len(indikator_semua) - 1))

    sub = dff[[x_var, y_var, "Kota", "Tahun"]].dropna()
    if len(sub) >= 3 and x_var != y_var:
        x, y = sub[x_var].values, sub[y_var].values
        slope, intercept = np.polyfit(x, y, 1)
        pred = slope * x + intercept
        ss_res = np.sum((y - pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
        rmse = np.sqrt(ss_res / len(y))

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Slope (β₁)", f"{slope:,.4f}")
        m2.metric("Intercept (β₀)", f"{intercept:,.4f}")
        m3.metric("R²", f"{r2:.3f}")
        m4.metric("RMSE", f"{rmse:,.3f}")

        fig = px.scatter(sub, x=x_var, y=y_var, color="Kota", hover_data=["Tahun"],
                         color_discrete_sequence=PALETTE, title=f"{y_var} vs {x_var}")
        xs = np.linspace(x.min(), x.max(), 100)
        fig.add_trace(go.Scatter(x=xs, y=slope * xs + intercept, mode="lines",
                                 name="Garis regresi", line=dict(color="black", dash="dash")))
        st.plotly_chart(atur_grafik(fig, 480), use_container_width=True)

        resid = pd.DataFrame({"Prediksi": pred, "Residual": y - pred})
        fig = px.scatter(resid, x="Prediksi", y="Residual", title="Plot Residual",
                         color_discrete_sequence=["#2E86AB"])
        fig.add_hline(y=0, line_dash="dot", line_color="gray")
        st.plotly_chart(atur_grafik(fig, 350), use_container_width=True)
        st.caption(
            f"Persamaan: **{y_var} = {intercept:,.3f} + {slope:,.3f} × {x_var}**. "
            "Periksa plot residual: pola melengkung/menyebar menandakan asumsi linieritas/homoskedastisitas kurang terpenuhi."
        )
    else:
        st.info("Pilih dua variabel berbeda dengan minimal 3 observasi.")

# ----------------------------------------------------------------------------
# TAB 5: DATA
# ----------------------------------------------------------------------------
with tab5:
    st.subheader("Data Terfilter")
    st.dataframe(dff, use_container_width=True, height=480)
    st.download_button(
        "⬇️ Unduh data terfilter (CSV)",
        dff.to_csv(index=False).encode("utf-8"),
        file_name="data_terfilter.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("Dibuat dengan Streamlit • Plotly • Pandas • NumPy")
