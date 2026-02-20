"""
BIST Swing Trade Tarama ve Puanlama Sistemi
==========================================
Yazar: Kıdemli Python / Algo Trading Uzmanı
Amaç: BIST hisselerini 1 aylık swing trade perspektifinden taramak,
      temel + teknik analiz puanlamasıyla en iyi fırsatları bulmak.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time
import warnings
import plotly.graph_objects as go
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# BIST HİSSE LİSTESİ
# Kaynak: BIST 500 bileşenleri (manuel liste – yfinance endeks listesi desteklemiyor)
# .IS uzantısı yfinance için zorunlu
# ─────────────────────────────────────────────────────────────────────────────
BIST_TICKERS = [
    "THYAO.IS","EREGL.IS","GARAN.IS","AKBNK.IS","YKBNK.IS","ISCTR.IS","KCHOL.IS",
    "SASA.IS","BIMAS.IS","FROTO.IS","TUPRS.IS","ASELS.IS","TOASO.IS","PGSUS.IS",
    "HALKB.IS","VAKBN.IS","TKFEN.IS","ENKAI.IS","KOZAL.IS","KRDMD.IS","PETKM.IS",
    "TTKOM.IS","TAVHL.IS","OTKAR.IS","SAHOL.IS","ARCLK.IS","VESTL.IS","MGROS.IS",
    "EKGYO.IS","ULKER.IS","TCELL.IS","SISE.IS","DOHOL.IS","AEFES.IS","LOGO.IS",
    "MAVI.IS","NETAS.IS","KOZA1.IS","BRISA.IS","CCOLA.IS","IHLGM.IS","ALARK.IS",
    "ZOREN.IS","AKSEN.IS","AYGAZ.IS","GOLTS.IS","TSKB.IS","KLNMA.IS","ISGYO.IS",
    "SODA.IS","CIMSA.IS","OYAKC.IS","ADANA.IS","HEKTS.IS","DOAS.IS","TTRAK.IS",
    "KARSN.IS","BSOKE.IS","ADEL.IS","NUHCM.IS","GUBRF.IS","LINK.IS","MERIT.IS",
    "SELEC.IS","SNPAM.IS","BOSCH.IS","TURSG.IS","ISDMR.IS","FENER.IS","GSRAY.IS",
    "BJKAS.IS","TKNSA.IS","ASUZU.IS","KERVT.IS","ORGE.IS","IZFAS.IS","TRKCM.IS",
    "AKGRT.IS","ANSGR.IS","RAYSG.IS","AGESA.IS","ALKIM.IS","GEREL.IS","SARKY.IS",
    "KUTPO.IS","ERBOS.IS","PRKME.IS","KRDMA.IS","KRDMB.IS","DMSAS.IS","KAPLM.IS",
    "BIOEN.IS","TUREX.IS","CANTE.IS","BNTAS.IS","PARSN.IS","CLEBI.IS","SODSN.IS",
    "YATAS.IS","IPEKE.IS","MPARK.IS","DENGE.IS","GLBMD.IS","ODAS.IS","BERA.IS",
    "TPIC.IS","ATAGY.IS","MAGEN.IS","INDES.IS","INTEM.IS","OBASE.IS","DENGE.IS",
    "KFEIN.IS","ARAT.IS","GRSEL.IS","FADE.IS","VKGYO.IS","ISGYO.IS","RYGYO.IS",
    "DZGYO.IS","TRGYO.IS","OZGYO.IS","SNGYO.IS","HLGYO.IS","ALGYO.IS","VBTS.IS",
    "HTTPIS.IS","ASUZU.IS","FMIZP.IS","HURGZ.IS","PKART.IS","PLTUR.IS","RYCO.IS",
    "SANEL.IS","KATMR.IS","DAGHL.IS","MHRGY.IS","DESPC.IS","DGNMO.IS","ODINE.IS",
    "ETYAT.IS","FONET.IS","INFMK.IS","KAREL.IS","MIATK.IS","NETAŞ.IS","SILVR.IS",
    "SMART.IS","SOKM.IS","TBORG.IS","GWIND.IS","ENERY.IS","ESEN.IS","EUPWR.IS",
    "KLSER.IS","KGYO.IS","ATAGY.IS","YEOTK.IS","BOSSA.IS","CELHA.IS","CEMTS.IS",
    "CMBTN.IS","DYOBY.IS","EGEEN.IS","EKIZ.IS","FLAP.IS","GEDIZ.IS","GEDZA.IS",
    "GOODY.IS","HATEK.IS","IHGZT.IS","IHLAS.IS","IHEVA.IS","ISATR.IS","ISBTR.IS",
    "JANTS.IS","KIPA.IS","KORDS.IS","KRSAN.IS","LIDER.IS","LKMNH.IS","MEMSA.IS",
    "MEGES.IS","MOBTL.IS","MRSHL.IS","NBIOTK.IS","NETAS.IS","NTGAZ.IS","NUGYO.IS",
    "OSMEN.IS","OZBAL.IS","OZRDN.IS","PENGD.IS","PETUN.IS","PINSU.IS","PKENT.IS",
    "PRZMA.IS","PSDTC.IS","QNBFB.IS","QNBFL.IS","RHEAG.IS","RTALB.IS","RUBNS.IS",
    "SAMAT.IS","SANFM.IS","SANKO.IS","SEGYO.IS","SEKFK.IS","SEKUR.IS","SELGD.IS",
    "SERVE.IS","SEZGI.IS","SILVR.IS","SKBNK.IS","SKYLP.IS","SMRTG.IS","TATGD.IS",
    "TCELL.IS","TEBNK.IS","TEKTU.IS","Tesla.IS","TMSN.IS","TMPOL.IS","TNZTP.IS",
    "TOASO.IS","TREYD.IS","TSPOR.IS","TUCLK.IS","TUKAS.IS","TUMTK.IS","TUREX.IS",
    "TURGZ.IS","TURSG.IS","ULUUN.IS","ULUSE.IS","UNLU.IS","UZERB.IS","VERUS.IS",
    "VKING.IS","YAPRK.IS","YESIL.IS","YGGYO.IS","YKSGR.IS","YKSLN.IS","YUNSA.IS",
    "ZEDUR.IS","AAIGM.IS","ABANA.IS","ACSEL.IS","AFYON.IS","AGYO.IS","AHSGY.IS",
    "AKBLK.IS","AKFGY.IS","AKFYE.IS","AKMGY.IS","AKPAZ.IS","AKSGY.IS","AKSEL.IS",
    "ALBRK.IS","ALFAS.IS","ALTINS.IS","ALTNY.IS","ALVES.IS","ANELE.IS","ANGEN.IS",
    "ARDYZ.IS","ARENA.IS","ARSAN.IS","ATATP.IS","ATCGY.IS","AVGYO.IS","AVOD.IS",
    "AZTEK.IS","BABSK.IS","BAKAB.IS","BALAT.IS","BANVT.IS","BARMA.IS","BAYRK.IS",
    "BEGYO.IS","BEYAZ.IS","BFREN.IS","BIENY.IS","BIGCH.IS","BIMAS.IS","BLCYT.IS",
    "BMSTL.IS","BOSSA.IS","BRKSN.IS","BRKVY.IS","BRSAN.IS","BURCE.IS","BURVA.IS",
    "BVSAN.IS","CEMAS.IS","CEMTS.IS","CEOEM.IS","CIMSA.IS","COMDO.IS","COSMO.IS",
    "CRDFA.IS","CRFSA.IS","CUSAN.IS","CVKMD.IS","CWENE.IS","DAPGM.IS","DATA.IS",
    "DENGE.IS","DERHL.IS","DERIM.IS","DESA.IS","DESPC.IS","DEVA.IS","DGNMO.IS",
    "DITAS.IS","DMRGD.IS","DNISI.IS","DOBUR.IS","DOCO.IS","DURDO.IS","DYOBY.IS",
    "ECILC.IS","ECZYT.IS","EDIP.IS","EGEPO.IS","EGSER.IS","ELITE.IS","EMKEL.IS",
    "EMNIS.IS","ENPLA.IS","EPLAS.IS","ERSU.IS","ESCOM.IS","ESEN.IS","ETILR.IS",
    "ETYAT.IS","EUHOL.IS","EURO.IS","EUROB.IS","EUYO.IS","FBASE.IS","FENER.IS",
    "FMIZP.IS","FONET.IS","FORMT.IS","FORTE.IS","FRIGO.IS","FZLGY.IS","GARAN.IS",
    "GARFA.IS","GEDIK.IS","GESAN.IS","GLBMD.IS","GLRYH.IS","GOLDS.IS","GOODY.IS",
    "GRNYO.IS","GRSEL.IS","GSDDE.IS","GSDHO.IS","GSRAY.IS","GUBRF.IS","GULFA.IS",
    "GVENS.IS","GWIND.IS","HALKB.IS","HATEK.IS","HDFGS.IS","HEDEF.IS","HEKTS.IS",
    "HLGYO.IS","HTTBT.IS","HUNER.IS","HURGZ.IS","ICBCT.IS","IDGYO.IS","IHLGM.IS",
    "IHLAS.IS","IHTIY.IS","IMASM.IS","INDES.IS","INTEM.IS","IPEKE.IS","ISATR.IS",
    "ISBTR.IS","ISCTR.IS","ISFIN.IS","ISGSY.IS","ISGYO.IS","ISKPL.IS","ISKUR.IS",
    "ISYAT.IS","ITTFH.IS","IZTAR.IS","JANTS.IS","KAPLM.IS","KARSN.IS","KERVT.IS",
    "KFEIN.IS","KGYO.IS","KHOLS.IS","KNFRT.IS","KONTR.IS","KONYA.IS","KORDS.IS",
    "KOZAA.IS","KOZAL.IS","KRDMA.IS","KRDMB.IS","KRDMD.IS","KRPLA.IS","KRSAN.IS",
    "KRVGD.IS","KSTUR.IS","KTLEV.IS","KTSKR.IS","KUTPO.IS","KWPWR.IS","LIDER.IS",
]

# Tekrar edenleri ve geçersizleri temizle
BIST_TICKERS = list(dict.fromkeys(BIST_TICKERS))  # unique

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────────────────────────────────────────

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """RSI hesapla (pandas_ta olmadan saf numpy/pandas ile)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def calculate_macd(series: pd.Series, fast=12, slow=26, signal=9):
    """MACD, Sinyal ve Histogram hesapla."""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """ATR (Average True Range) hesapla."""
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()


# ─────────────────────────────────────────────────────────────────────────────
# ANA PUANLAMA FONKSİYONU
# ─────────────────────────────────────────────────────────────────────────────

def score_ticker(ticker: str, sector_stats: dict) -> dict | None:
    """
    Bir hisse için temel + teknik analiz puanı hesapla.
    Dönüş: dict (skor ve detaylar) ya da None (hata/yetersiz veri).
    """
    try:
        # ── Veri İndir ──────────────────────────────────────────────────────
        # 1 yıllık günlük veri (MA200 için yeterli)
        raw = yf.download(ticker, period="1y", interval="1d",
                          auto_adjust=True, progress=False)
        if raw is None or len(raw) < 60:
            return None

        # MultiIndex sütunları düzleştir
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)

        raw = raw.dropna(subset=["Close", "High", "Low", "Volume"])
        if len(raw) < 60:
            return None

        close = raw["Close"].squeeze()
        high  = raw["High"].squeeze()
        low   = raw["Low"].squeeze()
        vol   = raw["Volume"].squeeze()

        # ── Hareketli Ortalamalar ────────────────────────────────────────────
        ma50  = close.rolling(50).mean()
        ma200 = close.rolling(200).mean()
        current_price = float(close.iloc[-1])
        ma50_val  = float(ma50.iloc[-1])
        ma200_val = float(ma200.iloc[-1]) if not np.isnan(ma200.iloc[-1]) else None

        # ZORUNLU TREND FİLTRESİ: Fiyat MA50 VE MA200 üzerinde olmalı
        # MA200 mevcut değilse (< 200 gün veri) sadece MA50 kontrolü yap
        above_ma50  = current_price > ma50_val
        above_ma200 = (ma200_val is None) or (current_price > ma200_val)

        trend_ok = above_ma50 and above_ma200
        if not trend_ok:
            # Elendi – düşük skor döndür ama kaydı tut
            return {
                "Ticker": ticker, "Fiyat": round(current_price, 2),
                "Toplam Skor": 0, "Temel Skor": 0, "Teknik Skor": 0,
                "RSI": None, "MACD Sinyal": "-", "Hacim OK": False,
                "MA50 Üzeri": above_ma50, "MA200 Üzeri": above_ma200,
                "Elendi": "Trend Altı"
            }

        # ── RSI ─────────────────────────────────────────────────────────────
        rsi_series = calculate_rsi(close, 14)
        rsi_val = float(rsi_series.iloc[-1]) if not rsi_series.empty else 50.0

        # ── MACD ─────────────────────────────────────────────────────────────
        macd_line, signal_line, histogram = calculate_macd(close)
        macd_val   = float(macd_line.iloc[-1])
        signal_val = float(signal_line.iloc[-1])
        hist_val   = float(histogram.iloc[-1])
        hist_prev  = float(histogram.iloc[-2]) if len(histogram) > 1 else 0.0

        # MACD crossover: önceki bar'da MACD < Signal, şimdi MACD > Signal
        macd_cross = (float(macd_line.iloc[-2]) < float(signal_line.iloc[-2])) and (macd_val > signal_val)
        # Histogram pozitif ve büyüyor
        hist_growing = hist_val > 0 and hist_val > hist_prev

        # ── Hacim ───────────────────────────────────────────────────────────
        vol_5d  = float(vol.iloc[-5:].mean())
        vol_20d = float(vol.iloc[-20:].mean())
        volume_ok = vol_5d > vol_20d

        # ── ATR (Volatilite) ─────────────────────────────────────────────────
        atr_series = calculate_atr(high, low, close, 14)
        atr_val = float(atr_series.iloc[-1])
        atr_pct = (atr_val / current_price) * 100  # Fiyata göre % ATR

        # ── Temel Analiz Verisi ──────────────────────────────────────────────
        info = {}
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info or {}
        except Exception:
            pass

        pb_ratio = info.get("priceToBook", None)
        pe_ratio = info.get("trailingPE", None) or info.get("forwardPE", None)
        earnings_growth = info.get("earningsQuarterlyGrowth", None)  # Çeyreklik kar büyümesi
        revenue_growth  = info.get("revenueGrowth", None)
        sector = info.get("sector", "Unknown")

        # ─────────────────────────────────────────────────────────────────────
        # PUANLAMA
        # ─────────────────────────────────────────────────────────────────────
        temel_skor    = 0
        teknik_skor   = 0
        skor_detay    = {}

        # ── 1. TEMEL ANALİZ (Maks 40) ────────────────────────────────────────

        # 1a. PD/DD – Maks 15 Puan
        # Sektör ortalaması yoksa sabit eşikler kullan
        pb_skor = 0
        if pb_ratio is not None and pb_ratio > 0:
            sektör_pb_ort = sector_stats.get(sector, {}).get("pb_mean", 3.0)
            if pb_ratio < sektör_pb_ort * 0.5:
                pb_skor = 15     # Sektörün yarısından ucuz
            elif pb_ratio < sektör_pb_ort * 0.75:
                pb_skor = 12
            elif pb_ratio < sektör_pb_ort:
                pb_skor = 8
            elif pb_ratio < sektör_pb_ort * 1.25:
                pb_skor = 4
            else:
                pb_skor = 0
        else:
            pb_skor = 5  # Veri yok → nötr puan
        skor_detay["PD/DD Skor"] = pb_skor
        temel_skor += pb_skor

        # 1b. F/K – Maks 15 Puan
        pe_skor = 0
        if pe_ratio is not None and pe_ratio > 0:
            sektör_pe_ort = sector_stats.get(sector, {}).get("pe_mean", 15.0)
            if pe_ratio < sektör_pe_ort * 0.5:
                pe_skor = 15
            elif pe_ratio < sektör_pe_ort * 0.75:
                pe_skor = 12
            elif pe_ratio < sektör_pe_ort:
                pe_skor = 8
            elif pe_ratio < sektör_pe_ort * 1.5:
                pe_skor = 4
            elif pe_ratio > 0:
                pe_skor = 1
        else:
            pe_skor = 5  # Veri yok → nötr
        skor_detay["F/K Skor"] = pe_skor
        temel_skor += pe_skor

        # 1c. Net Kar Büyümesi – Maks 10 Puan
        eg_skor = 0
        if earnings_growth is not None:
            if earnings_growth > 0.50:
                eg_skor = 10   # %50+ büyüme
            elif earnings_growth > 0.25:
                eg_skor = 8
            elif earnings_growth > 0.10:
                eg_skor = 6
            elif earnings_growth > 0:
                eg_skor = 4
            else:
                eg_skor = 0   # Kar düşüşü → puan yok
        else:
            # Gelir büyümesini yedek olarak kullan
            if revenue_growth is not None and revenue_growth > 0.15:
                eg_skor = 4
            else:
                eg_skor = 3   # Veri yok → düşük nötr
        skor_detay["Kar Büyüme Skor"] = eg_skor
        temel_skor += eg_skor

        # ── 2. TEKNİK ANALİZ (Maks 60) ───────────────────────────────────────

        # 2a. RSI – Maks 20 Puan
        rsi_skor = 0
        if rsi_val < 30:
            rsi_skor = 2    # Aşırı satım ama trend kötü olabilir
        elif rsi_val < 40:
            rsi_skor = 8
        elif rsi_val < 50:
            rsi_skor = 12
        elif rsi_val <= 60:
            rsi_skor = 20   # Altın bölge: momentum var, henüz aşırı alım yok
        elif rsi_val <= 70:
            rsi_skor = 15   # Güçlü ama biraz fazla ısınmış
        elif rsi_val <= 80:
            rsi_skor = 7    # Aşırı alım bölgesi
        else:
            rsi_skor = 2    # Ekstrem aşırı alım
        skor_detay["RSI Skor"] = rsi_skor
        teknik_skor += rsi_skor

        # 2b. MACD – Maks 20 Puan
        macd_skor = 0
        if macd_cross:
            macd_skor = 20   # Tam crossover – en güçlü sinyal
        elif hist_growing and macd_val > 0:
            macd_skor = 16   # MACD pozitif ve histogram büyüyor
        elif hist_growing and macd_val < 0:
            macd_skor = 10   # Histogram büyüyor ama MACD hala negatif
        elif hist_val > 0:
            macd_skor = 8    # Histogram pozitif ama büyümüyor
        elif macd_val > signal_val:
            macd_skor = 5    # MACD sinyalin üzerinde ama histogram küçülüyor
        else:
            macd_skor = 0
        skor_detay["MACD Skor"] = macd_skor
        teknik_skor += macd_skor

        # 2c. Hacim – Maks 10 Puan
        hacim_skor = 0
        if vol_5d > 0 and vol_20d > 0:
            vol_ratio = vol_5d / vol_20d
            if vol_ratio > 2.0:
                hacim_skor = 10   # Hacim patlaması
            elif vol_ratio > 1.5:
                hacim_skor = 8
            elif vol_ratio > 1.2:
                hacim_skor = 6
            elif vol_ratio > 1.0:
                hacim_skor = 4
            else:
                hacim_skor = 0    # Hacim düşük → ilgi yok
        skor_detay["Hacim Skor"] = hacim_skor
        teknik_skor += hacim_skor

        # 2d. ATR Volatilite – Maks 10 Puan
        # Swing trade için ideal ATR: %1.5 – %4.5 arası
        atr_skor = 0
        if atr_pct < 0.8:
            atr_skor = 1    # Çok hareketsiz, swing için fırsat yok
        elif atr_pct < 1.5:
            atr_skor = 4
        elif atr_pct <= 3.0:
            atr_skor = 10   # İdeal swing volatilitesi
        elif atr_pct <= 4.5:
            atr_skor = 7
        elif atr_pct <= 6.0:
            atr_skor = 4    # Biraz riskli ama kabul edilebilir
        else:
            atr_skor = 1    # Aşırı volatil = risk yüksek
        skor_detay["ATR Skor"] = atr_skor
        teknik_skor += atr_skor

        # ── EKSTRA FAKTÖRLER (Bonus/Ceza) ────────────────────────────────────
        # 2e. MA Üçlü Düzeni: MA50 > MA200 (Altın Çapraz yapısı) +5 Bonus
        if ma200_val and ma50_val > ma200_val:
            bonus = 5
            skor_detay["MA Golden Cross Bonus"] = bonus
            teknik_skor += bonus
        else:
            skor_detay["MA Golden Cross Bonus"] = 0

        # 2f. Fiyatın MA50'ye Yakınlığı: MA50'nin %2-8 üzerinde ideal pozisyon
        ma50_dist_pct = ((current_price - ma50_val) / ma50_val) * 100
        if 2 <= ma50_dist_pct <= 8:
            prox_bonus = 5
        elif 8 < ma50_dist_pct <= 15:
            prox_bonus = 2   # Biraz uzaklaşmış ama tamam
        elif ma50_dist_pct > 15:
            prox_bonus = 0   # Çok uzaklaşmış, geri çekilme riski
        else:
            prox_bonus = 3   # MA50'ye çok yakın ama üzerinde
        skor_detay["MA50 Mesafe Bonus"] = prox_bonus
        teknik_skor += prox_bonus

        # ── SINIR KONTROLÜ ───────────────────────────────────────────────────
        temel_skor  = min(temel_skor, 40)
        teknik_skor = min(teknik_skor, 60)
        toplam_skor = temel_skor + teknik_skor

        # MACD sinyal etiketi
        if macd_cross:
            macd_label = "🔥 Crossover"
        elif hist_growing:
            macd_label = "📈 Hist. Büyüyor"
        elif hist_val > 0:
            macd_label = "✅ Pozitif"
        else:
            macd_label = "❌ Negatif"

        return {
            "Ticker":        ticker,
            "Fiyat":         round(current_price, 2),
            "Sektör":        sector,
            "Toplam Skor":   round(toplam_skor, 1),
            "Temel Skor":    round(temel_skor, 1),
            "Teknik Skor":   round(teknik_skor, 1),
            "RSI":           round(rsi_val, 1),
            "MACD Sinyal":   macd_label,
            "Hacim OK":      volume_ok,
            "MA50 Üzeri":    above_ma50,
            "MA200 Üzeri":   above_ma200,
            "ATR%":          round(atr_pct, 2),
            "PD/DD":         round(pb_ratio, 2) if pb_ratio else "N/A",
            "F/K":           round(pe_ratio, 2) if pe_ratio else "N/A",
            "Kar Büyümesi":  f"{earnings_growth*100:.1f}%" if earnings_growth else "N/A",
            "Elendi":        None,
            **skor_detay
        }

    except Exception as e:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# SEKTÖR İSTATİSTİKLERİ TOPLAMA
# (İlk 80 hisseden hızlı sektör ortalamaları çek)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def build_sector_stats(sample_tickers: list) -> dict:
    """
    Sektör bazlı F/K ve PD/DD ortalamalarını örneklem hisselerden hesapla.
    Cache'lenir (1 saat geçerli).
    """
    records = []
    for tkr in sample_tickers[:80]:
        try:
            info = yf.Ticker(tkr).info or {}
            records.append({
                "sector": info.get("sector", "Unknown"),
                "pb": info.get("priceToBook"),
                "pe": info.get("trailingPE") or info.get("forwardPE"),
            })
            time.sleep(0.05)
        except Exception:
            continue

    df = pd.DataFrame(records).dropna(subset=["sector"])
    stats = {}
    for sector, grp in df.groupby("sector"):
        stats[sector] = {
            "pb_mean": grp["pb"].dropna().mean() or 3.0,
            "pe_mean": grp["pe"].dropna().mean() or 15.0,
        }
    return stats


# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT ARAYÜZÜ
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="BIST Swing Trade Tarayıcı",
    page_icon="📈",
    layout="wide"
)

# Başlık
st.title("📈 BIST Swing Trade Tarama & Puanlama Sistemi")
st.markdown("""
**Sistem Mantığı:** Her hisse 100 puan üzerinden değerlendirilir.  
- 🔵 **%40** → Temel Analiz (PD/DD, F/K, Kar Büyümesi)  
- 🟠 **%60** → Teknik Analiz (Trend, RSI, MACD, Hacim, ATR)  
- ✅ **70+ puan** → AL Listesi | ⛔ Fiyat MA50/MA200 altında → Otomatik Eleme
""")

st.divider()

# Sidebar – Ayarlar
with st.sidebar:
    st.header("⚙️ Tarama Ayarları")
    min_score = st.slider("Minimum AL Skoru", 50, 90, 70, 5)
    max_tickers = st.slider("Taranacak Hisse Sayısı", 50, len(BIST_TICKERS), 300, 50)
    delay = st.slider("İstekler Arası Gecikme (sn)", 0.1, 1.0, 0.3, 0.1,
                      help="Çok hızlı gidince yfinance kısıtlayabilir")
    show_eliminated = st.checkbox("Elenen Hisseleri de Göster", False)

    st.divider()
    st.subheader("📋 Manuel Hisse Ekle")
    extra_raw = st.text_area("Ekstra hisseler (virgülle ayır)", "THYAO.IS, EREGL.IS")
    extra_tickers = [t.strip().upper() for t in extra_raw.split(",") if t.strip()]

    start_button = st.button("🚀 Taramayı Başlat", type="primary", use_container_width=True)

# Taranacak liste
scan_list = list(dict.fromkeys(extra_tickers + BIST_TICKERS[:max_tickers]))

# ─────────────────────────────────────────────────────────────────────────────
# TARAMA
# ─────────────────────────────────────────────────────────────────────────────

if start_button:
    st.info(f"🔍 {len(scan_list)} hisse taranıyor... Bu işlem birkaç dakika sürebilir.")

    # Önce sektör istatistiklerini oluştur
    with st.spinner("Sektör ortalamaları hesaplanıyor..."):
        sector_stats = build_sector_stats(scan_list)

    results = []
    progress_bar = st.progress(0, text="Tarama başlıyor...")
    status_text  = st.empty()
    error_count  = 0

    for i, ticker in enumerate(scan_list):
        status_text.text(f"⏳ Taranan: {ticker}  ({i+1}/{len(scan_list)})")
        result = score_ticker(ticker, sector_stats)
        if result:
            results.append(result)
        else:
            error_count += 1
        progress_bar.progress((i + 1) / len(scan_list),
                               text=f"{i+1}/{len(scan_list)} tamamlandı")
        time.sleep(delay)

    progress_bar.empty()
    status_text.empty()

    if not results:
        st.error("Hiç sonuç alınamadı. İnternet bağlantınızı veya ticker listesini kontrol edin.")
        st.stop()

    # DataFrame oluştur
    df_all = pd.DataFrame(results)
    df_all = df_all.sort_values("Toplam Skor", ascending=False).reset_index(drop=True)

    # AL listesi (elenmemiş + min_score üzeri)
    df_al = df_all[(df_all["Elendi"].isna()) & (df_all["Toplam Skor"] >= min_score)].copy()

    # ── Özet Metrikleri ──────────────────────────────────────────────────────
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔍 Taranan", len(scan_list))
    col2.metric("✅ Veri Alınan", len(df_all))
    col3.metric("🚀 AL Listesi", len(df_al))
    col4.metric("⚠️ Hata / Veri Yok", error_count)

    # ── AL LİSTESİ TABLOSU ───────────────────────────────────────────────────
    st.subheader(f"🚀 AL Listesi ({min_score}+ Puan, Toplam: {len(df_al)} Hisse)")

    if df_al.empty:
        st.warning("Hiç hisse eşiği geçemedi. Skoru düşürmeyi deneyin.")
    else:
        display_cols = [
            "Ticker", "Fiyat", "Sektör", "Toplam Skor",
            "Temel Skor", "Teknik Skor", "RSI", "MACD Sinyal",
            "ATR%", "PD/DD", "F/K", "Kar Büyümesi",
            "Hacim OK", "MA50 Üzeri", "MA200 Üzeri"
        ]
        display_cols = [c for c in display_cols if c in df_al.columns]

        def color_score(val):
            if isinstance(val, (int, float)):
                if val >= 80: return "background-color: #1a6b3c; color: white"
                if val >= 70: return "background-color: #2d9e5f; color: white"
                if val >= 60: return "background-color: #f4a83a"
            return ""

        styled = df_al[display_cols].style.applymap(
            color_score, subset=["Toplam Skor"]
        ).format({"Fiyat": "{:.2f}", "Toplam Skor": "{:.1f}",
                  "Temel Skor": "{:.1f}", "Teknik Skor": "{:.1f}",
                  "RSI": "{:.1f}", "ATR%": "{:.2f}%"})

        st.dataframe(styled, use_container_width=True, height=500)

        # CSV İndir
        csv_data = df_al[display_cols].to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            "📥 AL Listesini CSV İndir",
            data=csv_data,
            file_name=f"bist_al_listesi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

    # ── TÜM SONUÇLAR TABLOSU ─────────────────────────────────────────────────
    st.subheader("📊 Tüm Tarama Sonuçları")
    if show_eliminated:
        df_show = df_all
    else:
        df_show = df_all[df_all["Elendi"].isna()]

    display_cols2 = [
        "Ticker", "Fiyat", "Toplam Skor", "Temel Skor", "Teknik Skor",
        "RSI", "MACD Sinyal", "ATR%", "Hacim OK", "MA50 Üzeri", "MA200 Üzeri", "Elendi"
    ]
    display_cols2 = [c for c in display_cols2 if c in df_show.columns]
    st.dataframe(df_show[display_cols2], use_container_width=True, height=400)

    # ── SKOR DAĞILIM GRAFİĞİ ─────────────────────────────────────────────────
    st.subheader("📉 Skor Dağılımı")
    df_chart = df_all[df_all["Elendi"].isna()].head(40)
    if not df_chart.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_chart["Ticker"],
            y=df_chart["Temel Skor"],
            name="Temel Analiz",
            marker_color="#4A90D9"
        ))
        fig.add_trace(go.Bar(
            x=df_chart["Ticker"],
            y=df_chart["Teknik Skor"],
            name="Teknik Analiz",
            marker_color="#F4A83A"
        ))
        fig.add_hline(y=min_score, line_dash="dash", line_color="red",
                      annotation_text=f"AL Eşiği ({min_score})")
        fig.update_layout(
            barmode="stack",
            title="Hisse Başına Temel + Teknik Skor (İlk 40)",
            xaxis_tickangle=-45,
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="white",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── EN İYİ 5 HİSSE DETAY KARTI ───────────────────────────────────────────
    if not df_al.empty:
        st.subheader("🏆 En İyi 5 Hisse – Detay Kartları")
        top5 = df_al.head(5)
        cols = st.columns(min(5, len(top5)))
        for idx, (_, row) in enumerate(top5.iterrows()):
            with cols[idx]:
                score_emoji = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "⭐"
                st.markdown(f"""
<div style="background:#1e2d3d;padding:16px;border-radius:10px;border-left:4px solid #4A90D9;">
<h4>{score_emoji} {row['Ticker']}</h4>
<b>Fiyat:</b> {row['Fiyat']} ₺<br>
<b>Toplam Skor:</b> {row['Toplam Skor']}/100<br>
<b>Temel:</b> {row['Temel Skor']}/40<br>
<b>Teknik:</b> {row['Teknik Skor']}/60<br>
<b>RSI:</b> {row.get('RSI','N/A')}<br>
<b>MACD:</b> {row.get('MACD Sinyal','N/A')}<br>
<b>ATR%:</b> {row.get('ATR%','N/A')}<br>
<b>Sektör:</b> {row.get('Sektör','N/A')}
</div>
""", unsafe_allow_html=True)

    st.success("✅ Tarama tamamlandı!")
    st.caption(f"Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

else:
    # Henüz tarama yapılmadı – bilgi ekranı
    st.info("⬅️ Sol panelden ayarları yapıp **Taramayı Başlat** butonuna basın.")

    with st.expander("📖 Puanlama Sistemi Detayları"):
        st.markdown("""
### Temel Analiz (40 Puan)
| Kriter | Maks Puan | Mantık |
|--------|-----------|--------|
| PD/DD  | 15 | Sektör ortalamasına göre ucuz olana daha yüksek puan |
| F/K    | 15 | Makul F/K'ya yüksek puan, çok pahalıya 0 puan |
| Kar Büyümesi | 10 | %50+ büyüme = tam puan, düşüş = 0 puan |

### Teknik Analiz (60 Puan)
| Kriter | Maks Puan | Mantık |
|--------|-----------|--------|
| Trend Filtresi | Zorunlu | MA50 ve MA200 altı → Otomatik eleme |
| RSI | 20 | 50–60 arası ideal (20 puan), aşırı alım/satım cezalandırılır |
| MACD | 20 | Crossover = 20 puan, histogram büyüme = 16 puan |
| Hacim | 10 | 5 günlük hacim > 20 günlük hacim = tam puan |
| ATR Volatilite | 10 | %1.5–%3 arası ideal swing volatilitesi |
| MA Golden Cross | 5 bonus | MA50 > MA200 yapısı |
| MA50 Mesafe | 5 bonus | Fiyat MA50'nin %2–8 üzerindeyse ideal |

### AL Sinyali
Toplam skor **70 ve üzeri** olan hisseler otomatik AL listesine alınır.
        """)
