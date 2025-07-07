# brand-safety-project

# 🛡️ Brand Safety

Il progetto **Brand Safety** ha l'obiettivo di identificare la presenza di **scene violente o disturbanti** all'interno di video provenienti dalla **medialibrary di Repubblica**.

---

## 🎯 Obiettivo

Data una lista di URL video (medialibrary), il sistema:

- Analizza automaticamente il contenuto dei video.
- Rileva la presenza di elementi **violenti o disturbanti**.
- Classifica le scene problematiche secondo le **categorie GARM** (Global Alliance for Responsible Media), fornite da Manzoni.
- Restituisce un output strutturato in **JSON** e **CSV** contenente:
  - `flag` = 1 se viene rilevato almeno un contenuto sensibile, 0 altrimenti.
  - Le **categorie di disturbo rilevate** (massimo 3 per video).

---

## 📥 Input

- Una lista di **link video** della medialibrary.
- I video sono scaricati o processati automaticamente.

---

## 📤 Output

Per ogni video analizzato, vengono generati:

- `output.json`: file JSON con il dettaglio delle analisi.
- `output/.csv`: tabella con:
  - `video_id`
  - `flag` (0 o 1)
  - `categorie` (max 3, separate da virgola)

---

## 🗂️ Struttura del progetto

    <br>

    <!-- TREEVIEW START -->
    ```bash
    ├── check_url_availability.py --controlla preliminarmente quanti video sono ancora disponibili
    ├── data/
    │   └── [lista di url tvmanager]
    ├── prompt.txt   
    ├── output/
    │   ├── [generated_output.csv]
    │   └── [generated_output.json]
    ├── requirements.txt
    ├── README.md
    └── src/
        ├── conf 
        ├── extraction -- in caso di estrazione link tvmanager da link html
        ├── query -- in caso di estrazione link html da cms
        ├── utils.py
        └── main.py
    ```

    <!-- TREEVIEW END -->


## ⚙️ Per avviare l’analisi:

python src/main.py

