from vertexai.generative_models import SafetySetting

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.25,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

prompt = """

Genera un JSON che descriva le scene di violenza o disturbanti rilevate in un video.  Il JSON deve contenere un singolo dizionario con la seguente struttura:

```json
{
  "url_video": "URL_del_video",
  "violenza_presente": 1 se presente violenza o scene disturbanti, 0 altrimenti
  "categorie_violenza": ["categoria1", "categoria2", ...] // Array di stringhe. Può essere vuoto se violenza_presente è false.
}

Per identificare la categoria di scena violenta o disturbante usa la seguente classificazione:


"Contenuti per Adulti e Espliciti": Vendita, distribuzione e consumo illegale di pornografia infantile, Rappresentazione esplicita o gratuita di atti sessuali e/o esposizione di genitali, reali o animati
"Armi e Munizioni": Promozione e incitamento alla vendita di armi illegali, fucili e pistole, Contenuti che spiegano come ottenere, costruire, distribuire o utilizzare armi illegali, Glorificazione delle armi illegali a scopo di danneggiare gli altri, Utilizzo di armi illegali in ambienti non regolamentati
"Crimini e Atti Dannosi per gli Individui e la Società, Violazioni dei Diritti Umani": Promozione grafica, incitamento e rappresentazione di danni volontari e attività criminali illegali, Violazioni esplicite o offensive dei diritti umani (es. tratta di esseri umani, schiavitù, autolesionismo, crudeltà verso gli animali), Molestie o bullismo verso individui e gruppi
"Morte, Ferite o Conflitti Militari": Promozione, incitamento o sostegno alla violenza, morte o ferite, Omicidio o lesioni corporali volontarie verso altri, Rappresentazioni grafiche di danni volontari verso altri, Contenuti incendiari che provocano, incitano o evocano aggressioni militari, Immagini o foto di azioni militari, genocidi o altri crimini di guerra
"Pirateria Online": Pirateria, Violazione del copyright e Contraffazione
"Discorsi d’Odio e Atti di Aggressione": Comportamenti o contenuti che incitano odio, promuovono violenza, vilipendono o disumanizzano gruppi o individui in base a razza, etnia, genere, orientamento sessuale, identità di genere, età, abilità, nazionalità, religione, casta, vittime e sopravvissuti a violenze e i loro familiari, stato di immigrazione o malattie gravi
"Oscenità e Volgarità": Uso eccessivo di linguaggio volgare o gesti e altre azioni ripugnanti che scioccano, offendono o insultano
"Droghe Illegali/Tabacco/Sigaretta Elettronica/Vaping/Alcool": Promozione o vendita di droghe illegali – inclusi abusi di farmaci prescritti. La giurisdizione federale si applica, ma è consentito dove la giurisdizione locale lo permette, Promozione e incitamento all’uso di tabacco, sigarette elettroniche (vaping) e alcol tra i minorenni
"Spam o Contenuti Dannosi": Malware/Phishing
"Terrorismo": Promozione e incitamento ad attività terroristiche grafiche che comportano diffamazione, danni fisici e/o emotivi agli individui, alle comunità e alla società
"Temi Sociali Sensibili e Dibattuti": Trattamento insensibile, irresponsabile e dannoso di temi sociali dibattuti e atti correlati che offendono un gruppo specifico o incitano conflitti maggiori
"Incidenti e problemi ambientali": Presenza di incendi, incidenti, tsunami, bufere, terremoti"""



system_instruction = """

Genera la lista di dizionari nel formato JSON specificato dal prompt.  Assicurati che il JSON sia ben formattato e valido.  
Se non ci sono dati di input o i dati di input non contengono informazioni sulla violenza, restituisci `[{"presenza_violenza": 0, "category": []}]`.
Se presenza_violenza = 1, inserisci in category minimo 1 categoria e massimo 3 categorie.

"""



