rm algo.submission.demo.tar.bz2 city.* files.md5 README region.* user.profile.tags.*
mkdir train/
mkdir test/
mv training2nd/clk* training2nd/conv* training2nd/imp* train/
mv training3rd/clk* training3rd/conv* training3rd/imp* train/
rm -rf training*
mv testing2nd/* testing3rd/* test/
rm -rf testing*

cd train/
bzip2 -d *
cat imp.* > imp_all.txt
cat clk.* > clk_all.txt
cat conv.* > conv_all.txt
rm imp.* clk.* conv.*

cd ../test/
bzip2 -d *
cat * > test_imp.txt
rm l*

cd ../

