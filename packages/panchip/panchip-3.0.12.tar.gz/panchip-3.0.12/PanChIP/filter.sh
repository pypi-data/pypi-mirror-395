Analysis="915"
Filter="7619"
sedinput=$(sed 's/\//\\\//g' <<< "$input")
sedoutput=$(sed 's/\//\\\//g' <<< "$output")
sedlib=$(sed 's/\//\\\//g' <<< "$lib")
rep="tmp"

printf "Running PanChIP filter...\n"

lib2sum() {
sort -u -k1,1 -k2,2n -k3,3n -k4,4n $input/$1.bed | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $input/$1.sum
}
rep2sum() {
sort -u -k1,1 -k2,2n -k3,3n -k4,4n $lib/$1.bed | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $lib/$rep/$1.sum
}
lib2wc() {
wc -l $input/$1.bed | awk '{print $1}' > $input/$1.wc
}

mkdir -p $lib/$rep
for i in $inputfiles
do
lib2sum "$i"
lib2wc "$i"
done
echo $inputfiles | sed -e 's/ /.sum '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.sum/' | xargs cat > $input/SUM.count
echo $inputfiles | sed -e 's/ /.sum '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.sum/' | xargs rm
echo $inputfiles | sed -e 's/ /.wc '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.wc/' | xargs cat > $input/WC.count
echo $inputfiles | sed -e 's/ /.wc '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.wc/' | xargs rm
paste $input/SUM.count $input/WC.count | awk '{print $1/$2}' > $input/SUMdivbyWC.count
for cnt in $(seq 1 1 $Filter)
do
  if [ $(jobs -r | wc -l) -ge $threads ]; then
    wait $(jobs -r -p | head -1)
  fi
  (rep2sum "$cnt") &
done
printf ""
wait
seq $Filter | sed 's:.*:'$sedlib'\/'$rep'\/&.sum:' | xargs cat > $lib/SUM.count
seq $Filter | sed 's:.*:'$sedlib'\/'$rep'\/&.sum:' | xargs rm

subtask1() {
bedtools intersect -a $input/$1.bed -b $lib/$2.bed | sort -u -k1,1 -k2,2n -k3,3n -k4,4n | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $output/$3/$1/intersect.$2.count
bedtools intersect -a $lib/$2.bed -b $input/$1.bed | sort -u -k1,1 -k2,2n -k3,3n -k4,4n | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $output/$3/$1/intersect2.$2.count
}
catfunc() {
seq $Filter | sed 's:.*:'$2'.&.count:' | xargs cat > $1.dist
}
subtask2() {
catfunc "$output/$2/$1/intersect" "$sedoutput\/$2\/$1\/intersect"
catfunc "$output/$2/$1/intersect2" "$sedoutput\/$2\/$1\/intersect2"
rm $output/$2/$1/intersect.*.count
rm $output/$2/$1/intersect2.*.count
sort -u -k1,1 -k2,2n -k3,3n -k4,4n $input/$1.bed | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $output/$2/$1/$1.dist
awk '{for(i=1;i<='$Filter';i++) {print}}' $output/$2/$1/$1.dist > $output/$2/$1/$1.tmp
paste $output/$2/$1/intersect.dist $output/$2/$1/intersect2.dist $lib/SUM.count $output/$2/$1/$1.tmp | awk '{if($3==0||$4==0) {print 0} else {print sqrt($1*$2/$3/$4)}}' > $output/$2/$1/intersect.normalized.dist
rm $output/$2/$1/$1.tmp $output/$2/$1/intersect.dist $output/$2/$1/intersect2.dist
}
task1() {
mkdir -p $output/$2/$1
for factor in $(seq 1 1 $Filter)
do
subtask1 "$1" "$factor" "$2"
done
subtask2 "$1" "$2"
}
task2() {
cp $output/$rep/$1/intersect.normalized.dist $output/$1.txt
}

mkdir -p $output
mkdir -p $output/$rep
for file in $inputfiles
do
  if [ $(jobs -r | wc -l) -ge $threads ]; then
    wait $(jobs -r -p | head -1)
  fi
  (echo Begin processing $file; task1 "$file" "$rep") &
done
wait
printf "Processing output files...\n"
for file in $inputfiles
do
  if [ $(jobs -r | wc -l) -ge $threads ]; then
    wait $(jobs -r -p | head -1)
  fi
  (task2 "$file") &
done
wait
echo $inputfiles | sed -e 's/ /.txt '$sedoutput'\//g' -e 's/^/'$sedlib'\/Filter.txt '$sedoutput'\//' -e 's/$/.txt/' | xargs paste | awk 'BEGIN{print "'$(sed -e 's/ /\\t/g' -e 's/^/TF\\tExperiment\\t/' <<< $inputfiles)'"} {print}' > $output/primary.output.tsv
awk '{if(NR>1) {print $3}}' $output/primary.output.tsv > $output/primary.output.tmp

for i in $(seq 1 1 $Analysis)
do
touch $output/$rep/$i.tf
touch $output/$rep/mean.dist
touch $output/$rep/std.dist
connectivity=$(awk '{if(NR=='$i') {print}}' $lib/Connectivity.txt)
connectivityn=$(awk '{if(NR=='$i') {print}}' $lib/Connectivity.txt | awk '{if(length($0)==0) {print 0} else {print gsub(/ /, "")+1}}')
for file in $(awk '{if(NR=='$i') {print}}' $lib/Connectivity.txt | sed 's/ /\n/g')
do
awk '{if(NR=='$file') {print}}' $output/primary.output.tmp >> $output/$rep/$i.tf
done
awk 'BEGIN{sum=0;} {sum=sum+$1} END{if('$connectivityn'==0) {print 0} else {print sum/'$connectivityn'}}' $output/$rep/$i.tf >> $output/$rep/mean.dist 
connectivitymean=$(awk 'BEGIN{sum=0;} {sum=sum+$1} END{if('$connectivityn'==0) {print 0} else {print sum/'$connectivityn'}}' $output/$rep/$i.tf)
awk 'BEGIN{sum=0;} {sum=sum+($1-'$connectivitymean')*($1-'$connectivitymean')} END{if('$connectivityn'==0) {printf "NA\n"} else {printf "%s\n", sqrt(sum/'$connectivityn')}}' $output/$rep/$i.tf >> $output/$rep/std.dist
rm $output/$rep/$i.tf
done
paste $lib/../Analysis/Analysis.txt $output/$rep/mean.dist $output/$rep/std.dist | awk 'BEGIN{printf "TF\tMean\tStandard Deviation\tSignal-to-noise Ratio\tFilter\n"} {if($3=="NA"||$3==0) {printf "%s\t%s\t%s\tNA\tFAIL\n",$1,$2,$3} else {if($2/$3>2) {printf "%s\t%s\t%s\t%s\tPASS\n",$1,$2,$3,$2/$3} else {printf "%s\t%s\t%s\t%s\tFAIL\n",$1,$2,$3,$2/$3}}}' > $output/statistics.tsv
rm $output/primary.output.tmp
for file in $inputfiles
do
rm $output/$file.txt
done
rm -r $lib/$rep
rm -r $output/$rep
mkdir -p $output/input.stat
for file in SUM SUMdivbyWC WC
do
mv $input/$file.count $output/input.stat/$file.count
done
printf "Completed PanChIP filter!\n"
