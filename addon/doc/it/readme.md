# Rapid Settings #

* Autore: Alberto buffolino.

Questo add-on fornisce un accesso veloce a tutte le impostazioni di NVDA, raggruppando tutte le categorie delle impostazioni in una struttura ad albero, e permettendoti di ricercare fra di esse quando si dimentica dov'&egrave; una specifica opzione.

Inoltre, il titolo della finestra ti d&agrave; informazioni sull'attuale profilo di configurazione attivo (configurazione normale, o altro, se lo hai creato).

## Utilizzo ##

Premi semplicemente NVDA+O e naviga nell'albero, espandendo la sezione delle impostazioni desiderata. Quando vuoi cambiare un valore di un'impostazione, premi tab e modifica il valore nella combobox, editbox, e cos&igrave; via.

Puoi anche cercare in tutte le impostazioni, usando l'apposito campo prima dell'albero; per ripristinare l'albero originale dopo una ricerca, premi semplicemente invio nel campo di ricerca.

## Comandi da tastiera ##

* NVDA+O (tutti i layout): apre la finestra principale.
* Invio (nel campo di ricerca): ripristina l'albero originale delle impostazioni.

## Cambiamenti per 1.0 ##

* Primo rilascio.

### Bug ancora presenti ###

* Il contenuto del campo di ricerca non viene aggiornato in Braille quando questo viene pulito automaticamente.
* Se premi esc su una combobox, una editbox, un radio button o uno slider, l'evento non viene processato dalla finestra di dialogo principale, generando errori.
* Quando selezioni un display Braille che richiede la selezione di una porta, la combobox per la porta non sar&agrave; mostrata immediatamente.
* Se ottieni un errore nella selezione di un display Braille (display non trovato), dopo aver premuto ok appare la finestra di dialogo originale.
