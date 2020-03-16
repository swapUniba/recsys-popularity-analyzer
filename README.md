# Framework per l'analisi del popularity bias
Il seguente framework permette l'esecuzione di diversi algoritmi di raccomandazione di tipo collaborative-filtering
o content-based. Esso presenta anche script per il calcolo di metriche e generazioni di grafici a partire dall'output 
degli algoritmi di raccomandazione.

Presenta i moduli:

* collaborative-filtering: per l'esecuzione di algoritmi collaborativi offerti dalla libreria Lenskit 
* content-based-lucene: per l'esecuzione di algoritmi content-based con libreria Pylucene
* content-based-classification: per l'esecuzione di algoritmi content-based con classificazione (tecniche di apprendimento supervisionato libreria Scikit-learn)
* content-based-word-embedding: per l'esecuzione di algoritmi content-based con tecniche di word-embedding offerte dalla libreria Gensim
* analysis: per il calcolo delle metriche/grafici 
* utils: per il mapping dei contenuti testuali, splitting degli utenti e altre operazioni di supporto

Potrebbe risultare utile scaricare le seguenti cartelle:
* recs: https://1drv.ms/u/s!AjfPOmmKNJRdnBWg2bRCaCyhe7lo?e=NxMid1 (raccomandazioni generate per i diversi algoritmi sul dataset MovieLens1M)
* datasets: https://1drv.ms/u/s!AjfPOmmKNJRdnBibCprJTSripSzw?e=avGcLD (contenente i dati con cui le precedenti raccomandazioni sono state generate: MovieLens1M, MovieLens20M, descrizioni, generi, tags, lista item popolari, suddivisione degli utenti)

## Installazione
* STEP1: assicurati di disporre di una versione python3.6 o superiore
* STEP2: apri il terminale e scrivi ```pip install numpy scipy pandas sklearn lenskit gensim matplotlib```
* STEP3 (opzionale): per poter eseguire algoritmi con lucene, installa PyLucene (https://lucene.apache.org/pylucene/index.html)


## Come configurare ed eseguire gli algoritmi

### collaborative-filering
Per il lancio degli algoritmi cf e' semplicemente necessario lanciare lo script **run.py** all'interno di questo modulo. A differenza delle altre tecniche di raccomandazione, tale script esegue tutti gli algoritmi e serializza i diversi risultati in un file .parquet 

### content-based-lucene (richiede Pylucene)
Presenta due script:
* build_index: estrae i contenuti per ogni item nel dataset e li serializza in un indice Lucene
* run_queries: permette l'esecuzione vera e proprio dell'algoritmo di raccomandazione. All'interno di tale script vi e' una sezione per la configurazione dei parametri con cui si vuole che l'algoritmo venga lanciato.

NB: E' necessario costruire l'indice prima di eseguire l'algoritmo

### content-based-classification e content-based-word-embedding
Questi due moduli presentano all'intern uno script chiamato **run.py** per l'esecuzione dei rispettivi algoritmi. Anche in questo caso, all'interno di tali script vi e' una sezione per la configurazione dei parametri con cui si vuole che gli algoritmi vengano lanciati.



## Come eseguire il calcolo delle metriche
Il modulo analysis contiene lo script **run.py** per il calcolo di metriche e grafici a partire dai risultati prodotti da un determinato algoritmo content-based. Al suo interno vi e' una sezione per la configurazione, dove va riportato il nome dell'algoritmo, il percorso verso i risultati da esso prodotto, il path del dataset utilizzato. Per gli algoritmi di collaborative filtering e' necessario invece lanciare lo script **run_cf.py** vista la modalita' differente con cui Lenskit memorizza i risultati. 
