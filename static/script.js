document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("runBtn");

    const seisImg = document.getElementById("seisImg");
    const plotStatus = document.getElementById("plotStatus");

    btn.addEventListener("click", async () => {

        const mseedFile = document.getElementById("mseed").files[0];
        const xmlFile = document.getElementById("xml").files[0];
        const dist = document.getElementById("distance").value;
        const magType = document.getElementById("magType").value;

        if (!mseedFile || !xmlFile) {
            alert("Harap pilih file .mseed dan .xml terlebih dahulu.");
            return;
        }

        const formData = new FormData();
        formData.append("mseed", mseedFile);
        formData.append("xml", xmlFile);
        formData.append("distance", dist);
        formData.append("mag_type", magType);

        document.getElementById("results").textContent = "Processing...";
        plotStatus.textContent = "Membuat plot...";
        seisImg.src = "";

        try {
            const response = await fetch("/process", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            // ===============================
            // STATION INFO
            // ===============================
            document.getElementById("lat").innerText = data.station.latitude;
            document.getElementById("lon").innerText = data.station.longitude;
            document.getElementById("elev").innerText = data.station.elevation;
            document.getElementById("code").innerText = data.station.code;

            // ===============================
            // MAGNITUDE RESULT (FIXED)
            // ===============================
            let txt = "Hasil Magnitudo:\n\n";

            for (const tr_id in data.magnitudes) {
                const mag = data.magnitudes[tr_id];

                txt += `${tr_id} :\n`;
                txt += `   ML : ${mag.ML}\n`;
                txt += `   MS : ${mag.MS}\n`;
                txt += `   MB : ${mag.MB}\n\n`;
            }

            document.getElementById("results").innerText = txt;

            // ===============================
            // PLOT
            // ===============================
            if (data.plot && data.plot.length > 0) {
                seisImg.src = "data:image/png;base64," + data.plot;
                plotStatus.innerText = "Plot berhasil dibuat.";
            } else {
                plotStatus.innerText = "Plot tidak tersedia.";
            }

        } catch (err) {
            console.error(err);
            alert("Gagal memproses data: " + err);
        }
    });
});