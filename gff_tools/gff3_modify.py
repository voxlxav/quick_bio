import csv

#wczytanie pliku
input_file = "/Users/aleksandra.strojwas/Desktop/the_last_dance/mitos_results/Trochulus_striolatus_A.17.30.01.fasta/striolatus.gff"
output_file = "STRIOLATUS.gff"

#lista nagłówków, które nalezy dodac
columns = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame"]

with open(input_file, "r") as infile, open(output_file, "w", newline='') as outfile:
    writer = csv.writer(outfile, delimiter="\t")
    
    #dodawanie nagłówków 
    writer.writerow(columns)
    
    for line in infile:
        #pomijanie komentarzy i pierwszego "ogólnego" wiersza
        if line.startswith("#") or "region" in line:
            continue
        
        #rozdzielenie kolumn
        row = line.strip().split("\t")
        
        #usuwanie sekwencji niekodujących 
        if row[2] == "ncRNA_gene":
            continue

        if row[2] == "origin_of_replication":
            row[2] = "other"
        
        if row[2] == "gene":
            row[2] = "CDS"
        
        #ekstrakcja nazw genów
        attributes = row[8]
        name_value = None
        for attr in attributes.split(";"):
            if attr.startswith("Name="):
                name_value = attr.split("=")[1]
                break
        
        #nadpisanie pierwszej kolumny - wprowadzenie nazw 
        if name_value:
            row[0] = name_value
        
        #pomijanie eksonów 
        if row[2] == "exon":
            continue
        
        #usunięcie ostatniej kolumny 
        row = row[:-1]
        
        #zapisanie przetworzonego wiersza 
        writer.writerow(row)

print(f"Przetworzony plik zapisano jako {output_file}")
