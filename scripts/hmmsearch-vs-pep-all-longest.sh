hmm=$1
SpeciesGroup=$2
ProteomeFolder="./sequences/pep/$SpeciesGroup/*.pep.all.longest.fa"

NOW=$(date +"%Y-%m-%d")
OUTFOLDER=results/$NOW/hmmsearch-vs-pep-all-longest
for i in $ProteomeFolder;
	do
		SPECIES=$(echo $(basename $i) | cut -f1 -d.);
		hmmsearch --domtblout "duf1220-vs-$SPECIES.domtblout" --tblout "duf1220-vs-$SPECIES.tblout" --domE 1e-10 -E 1e-10 --cpu=8 $hmm $i;
	done;
mkdir -p $OUTFOLDER
mv *.tblout $OUTFOLDER
mv *.domtblout $OUTFOLDER
