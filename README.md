# Shell scripts

There are convenince scripts to gather data about the code written until
the first release.

To do this, go to compiler's GitHub page, find the first working release.

Then go to `data/compiler-name/compiler` and run `../../../commitCSV.sh`
with the date of the release. It will populate `../meta/mvp.txt` with
the list of commits.

Now run `git checkout` with the `head -n1 ../meta/mvp.txt` and either
run `../../../findwcl.sh` to count the amount of non-empty lines in the
source files, or run `../../../findls.sh > flist`, and edit `flist` to
have only the files you care about. Afterwards, run
`cat flist | xargs sed '/^\s*$/d' | wc -l`.
