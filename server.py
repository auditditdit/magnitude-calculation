from flask import Flask, request, jsonify, render_template
from obspy import read, read_inventory
import base64
import io
import matplotlib.pyplot as plt
import numpy as np

# =====================================================
# --------------- OOP CLASS DEFINITIONS ---------------
# =====================================================

class StationXMLReader:
    """ membaca informasi stasiun dari StationXML """

    def __init__(self, xml_file):
        self.inv = read_inventory(xml_file)
        self.net = self.inv.networks[0]
        self.sta = self.net.stations[0]

    def get_station_info(self):
        return {
            "latitude": self.sta.latitude,
            "longitude": self.sta.longitude,
            "elevation": self.sta.elevation,
            "code": self.sta.code,
        }


class MagnitudeCalculator:
    """ menghitung ML, MS, MB """

    @staticmethod
    def compute_max_amplitude(stream):
        amplitudes = {}
        for tr in stream:
            amplitudes[tr.id] = np.max(np.abs(tr.data))
        return amplitudes

    # -------------------------
    # Rumusan 3 jenis magnitudo
    # -------------------------
    @staticmethod
    def ML(A, R):
        return np.log10(A) + 1.11 * np.log10(R / 100) + 0.00189 * R

    @staticmethod
    def MS(A, R):
        return np.log10(A) + 1.66 * np.log10(R / 100) + 0.0008 * R

    @staticmethod
    def MB(A, R):
        return np.log10(A) + 0.75 * np.log10(R) + 0.002 * R


class SeismogramPlotter:
    """ plotting 3 komponen seismogram BHZ-BHN-BHE """

    @staticmethod
    def extract_components(stream):
        comps = {"BHZ": None, "BHN": None, "BHE": None}
        for tr in stream:
            ch = tr.stats.channel.upper()
            if ch.endswith("Z"):
                comps["BHZ"] = tr
            elif ch.endswith("N"):
                comps["BHN"] = tr
            elif ch.endswith("E"):
                comps["BHE"] = tr
        return comps

    @staticmethod
    def generate_plot(stream):
        comps = SeismogramPlotter.extract_components(stream)
        fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        order = ["BHZ", "BHN", "BHE"]

        for i, comp in enumerate(order):
            ax = axes[i]
            tr = comps.get(comp)

            ax.set_title(f"Seismogram {comp}", fontsize=11)

            if tr is not None:
                t = tr.times()
                ax.plot(t, tr.data, linewidth=0.9)
                ax.grid(alpha=0.3)
            else:
                ax.text(0.5, 0.5, f"{comp} Not Found",
                        ha="center", va="center", fontsize=11)

            ax.set_ylabel("Amplitude", fontsize=9)

        axes[-1].set_xlabel("Time (s)", fontsize=10)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()

        return img_base64


# =====================================================
# ----------------- FLASK APPLICATION -----------------
# =====================================================

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/main")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    try:
        # Ambil input
        mseed_file = request.files["mseed"]
        xml_file = request.files["xml"]
        distance = float(request.form["distance"])

        # Baca file
        stream = read(mseed_file)
        station_reader = StationXMLReader(xml_file)
        station = station_reader.get_station_info()

        # Hitung magnitudo
        mag_calc = MagnitudeCalculator()
        amplitudes = mag_calc.compute_max_amplitude(stream)

        # hitung ML, MS, MB utk setiap trace
        magnitudes = {}
        for tr_id, A in amplitudes.items():
            ML = mag_calc.ML(A, distance)
            MS = mag_calc.MS(A, distance)
            MB = mag_calc.MB(A, distance)

            magnitudes[tr_id] = {
                "ML": round(ML, 3),
                "MS": round(MS, 3),
                "MB": round(MB, 3),
            }

        # buat plot
        plot_base64 = SeismogramPlotter.generate_plot(stream)

        # kirim JSON
        return jsonify({
            "station": station,
            "magnitudes": magnitudes,
            "plot": plot_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)