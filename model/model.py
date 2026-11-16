from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        risultato = []
        for distributore in self._distributori:
            prezzi_distributori = distributore.get_prezzi()
            prezzi_mese=[]
            for p in prezzi_distributori:
                if p.data.month == mese:
                    prezzi_mese.append(p.prezzo_litro)

            prezzo_medio=sum(prezzi_mese)/len(prezzi_mese)

            risultato.append((distributore.nome, prezzo_medio))
        return risultato

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno == 7:
            return costo_corrente, list(sequenza_parziale)
        else:
            costo_minimo = None
            sequenza_ottima = []

            for distributore in self._distributori:
                prezzo_settimanale_singolo_distributore = prezzi_settimana[distributore.id]
                prezzo_giornaliero_singolo_distributore = prezzo_settimanale_singolo_distributore[giorno] * 100

                if ultimo_distributore is not None and ultimo_distributore != distributore.id:
                    nuovo_costo = costo_corrente + prezzo_giornaliero_singolo_distributore + 5
                else:
                    nuovo_costo = costo_corrente + prezzo_giornaliero_singolo_distributore

                sequenza_parziale.append(distributore.id)
                costo_trovato, sequenza_trovata = self.__ricorsione(sequenza_parziale, giorno + 1, distributore.id,
                                                                    nuovo_costo, prezzi_settimana)
                sequenza_parziale.pop()

                if costo_minimo is None or costo_trovato < costo_minimo:
                    costo_minimo = costo_trovato
                    sequenza_ottima = sequenza_trovata

            return costo_minimo, sequenza_ottima
    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        risultato= {}
        for distributore in self._distributori:
            prezzi_distributori = distributore.get_prezzi()

            prezzi_settimana=[]
            for p in prezzi_distributori:
                if p.data.month == mese and p.data.day<=7:
                    prezzi_settimana.append(p.prezzo_litro)

            risultato[distributore.id]=prezzi_settimana
        return risultato