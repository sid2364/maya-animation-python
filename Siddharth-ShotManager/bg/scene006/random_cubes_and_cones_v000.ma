//Maya ASCII 2013 scene
//Name: random_cubes_and_cones.ma
//Last modified: Mon, May 25, 2015 08:48:00 AM
//Codeset: 1252
requires maya "2013";
requires "Mayatomr" "2013.0 - 3.10.1.4 ";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2013";
fileInfo "version" "2013 x64";
fileInfo "cutIdentifier" "201202220241-825136";
fileInfo "osv" "Microsoft Windows XP Professional x64 Edition Service Pack 2 (Build 3790)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 45.939358491341295 3.8130616399555617 -14.045071377317662 ;
	setAttr ".r" -type "double3" -4.5383527295992145 466.99999999998511 0 ;
	setAttr ".rp" -type "double3" 0 3.5527136788005009e-015 3.5527136788005009e-015 ;
	setAttr ".rpt" -type "double3" -1.1455548018549981e-014 1.579658079259904e-015 3.5598967982681165e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 48.189502255781001;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pCylinder1";
createNode mesh -n "pCylinderShape1" -p "pCylinder1";
	setAttr -k off ".v";
	setAttr -s 101 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".db" yes;
	setAttr ".bw" 4;
createNode transform -n "null1";
createNode transform -n "pCylinder2" -p "null1";
	setAttr ".t" -type "double3" -7.3823139774723812 6.1473017328941415 7.9225537395016623 ;
	setAttr ".r" -type "double3" 265.08329305326731 26.283052106146279 239.74636261737226 ;
createNode transform -n "pCylinder3" -p "null1";
	setAttr ".t" -type "double3" -6.6583120736610013 3.3958916365467728 -9.1098858949390902 ;
	setAttr ".r" -type "double3" 154.55811831603043 297.2565930876782 233.06729119514088 ;
createNode transform -n "pCylinder4" -p "null1";
	setAttr ".t" -type "double3" -6.3792591232980982 3.3369182754306803 -1.4720346875858148 ;
	setAttr ".r" -type "double3" 51.099209900926709 35.198315574945987 201.1618916698059 ;
createNode transform -n "pCylinder5" -p "null1";
	setAttr ".t" -type "double3" -1.1925841072270966 1.0993317745777187 -5.7752715879139966 ;
	setAttr ".r" -type "double3" 58.255898405824688 267.26853001171179 262.20911155359346 ;
createNode transform -n "pCylinder6" -p "null1";
	setAttr ".t" -type "double3" -2.9710514830005046 17.133358778718669 -9.9443679798595586 ;
	setAttr ".r" -type "double3" 191.43846484341674 304.68982013953223 19.402091553835 ;
createNode transform -n "pCylinder7" -p "null1";
	setAttr ".t" -type "double3" 8.6970547273319028 4.0268599334762234 -1.8739525306302625 ;
	setAttr ".r" -type "double3" 351.29557113785683 350.49376832198999 184.13806236355651 ;
createNode transform -n "pCylinder8" -p "null1";
	setAttr ".t" -type "double3" -2.3613158710603894 17.309425607214894 -4.1681367210619591 ;
	setAttr ".r" -type "double3" 15.496212157692893 163.74174153378993 284.89085527726002 ;
createNode transform -n "pCylinder9" -p "null1";
	setAttr ".t" -type "double3" 8.8011479666416506 13.164144516597435 9.7236568012003737 ;
	setAttr ".r" -type "double3" 31.45842676969044 269.57452546706605 329.77606615093697 ;
createNode transform -n "pCylinder10" -p "null1";
	setAttr ".t" -type "double3" 6.3987045836228731 14.558696402433895 -3.9465075110878445 ;
	setAttr ".r" -type "double3" 330.0740140439998 240.63533108675696 78.895039661426338 ;
createNode transform -n "pCylinder11" -p "null1";
	setAttr ".t" -type "double3" -3.9754739042647547 19.940141842154503 -4.0589900758770403 ;
	setAttr ".r" -type "double3" 302.28297351080801 104.34484549983975 24.266663372677129 ;
createNode transform -n "pCylinder12" -p "null1";
	setAttr ".t" -type "double3" 8.3887691744259669 8.6206744790303311 3.4686760778500556 ;
	setAttr ".r" -type "double3" 47.254942498901819 203.12948365944101 349.13018582091337 ;
createNode transform -n "pCylinder13" -p "null1";
	setAttr ".t" -type "double3" 9.0184089060705794 15.342283876452454 8.2421936945965051 ;
	setAttr ".r" -type "double3" 312.71407454691439 335.24086785933349 333.98605603025487 ;
createNode transform -n "pCylinder14" -p "null1";
	setAttr ".t" -type "double3" 9.7857099021585405 2.584575755380869 -8.0423892572623288 ;
	setAttr ".r" -type "double3" 2.4264196970959828 299.36536284215583 68.909286760446548 ;
createNode transform -n "pCylinder15" -p "null1";
	setAttr ".t" -type "double3" -5.1965102013690023 0.38704096758470197 3.1821561355800299 ;
	setAttr ".r" -type "double3" 23.402814106463996 163.92399155960095 16.959501661696933 ;
createNode transform -n "pCylinder16" -p "null1";
	setAttr ".t" -type "double3" 3.1860206641702185 1.6652988397027979 -5.677315373609721 ;
	setAttr ".r" -type "double3" 283.74562350018903 12.440960556731838 208.7639795773274 ;
createNode transform -n "pCylinder17" -p "null1";
	setAttr ".t" -type "double3" 4.8577046580584415 12.132176824061816 -8.9224691842097243 ;
	setAttr ".r" -type "double3" 119.4630276239298 344.92169863543438 73.333276928697103 ;
createNode transform -n "pCylinder18" -p "null1";
	setAttr ".t" -type "double3" 4.2985693821899584 16.088099721388915 -2.1843036785005543 ;
	setAttr ".r" -type "double3" 279.5323504970529 348.31420683411164 6.292062019250908 ;
createNode transform -n "pCylinder19" -p "null1";
	setAttr ".t" -type "double3" -3.3760355278265308 17.186323393146932 2.6225345552766441 ;
	setAttr ".r" -type "double3" 152.27162526386789 66.652231230195596 350.8216980861821 ;
createNode transform -n "pCylinder20" -p "null1";
	setAttr ".t" -type "double3" -9.6318406954306504 7.9329182302871111 -7.0786019904176234 ;
	setAttr ".r" -type "double3" 92.895926902150975 15.777589686035604 198.98785113525295 ;
createNode transform -n "pCylinder21" -p "null1";
	setAttr ".t" -type "double3" 4.0594589905751768 5.1046219702657254 3.5482571664720624 ;
	setAttr ".r" -type "double3" 131.07835181073654 276.48945963883619 159.33748373929549 ;
createNode transform -n "pCylinder22" -p "null1";
	setAttr ".t" -type "double3" -5.5666638528905938 7.3415030843080658 5.7865431856702365 ;
	setAttr ".r" -type "double3" 338.38046977163901 56.375494210753708 357.56190366460226 ;
createNode transform -n "pCylinder23" -p "null1";
	setAttr ".t" -type "double3" -3.1572672683989929 18.894770344461573 1.7212757238636183 ;
	setAttr ".r" -type "double3" 307.8764796032911 127.7684792807205 76.444393562020053 ;
createNode transform -n "pCylinder24" -p "null1";
	setAttr ".t" -type "double3" 0.95826591988793908 16.44542220231893 -0.88081258406096374 ;
	setAttr ".r" -type "double3" 137.79789558235981 313.7600097978563 225.97466082190954 ;
createNode transform -n "pCylinder25" -p "null1";
	setAttr ".t" -type "double3" -5.0564948133974248 6.6987423254700218 5.1378824833050487 ;
	setAttr ".r" -type "double3" 90.650399293107284 70.522673532190112 351.59200555003173 ;
createNode transform -n "pCylinder26" -p "null1";
	setAttr ".t" -type "double3" -9.134518408204082 10.392651177468528 6.9987774204804118 ;
	setAttr ".r" -type "double3" 109.32230640627721 286.57385963996495 299.00722589478016 ;
createNode transform -n "pCylinder27" -p "null1";
	setAttr ".t" -type "double3" -8.5233754428067776 1.3038189090468522 0.83750628066248822 ;
	setAttr ".r" -type "double3" 58.806643802961815 265.58142119707276 6.9243150988994095 ;
createNode transform -n "pCylinder28" -p "null1";
	setAttr ".t" -type "double3" -3.8668919816599772 12.033516048693279 4.7561174982001564 ;
	setAttr ".r" -type "double3" 127.8576239832893 146.61541389791816 71.962145794770947 ;
createNode transform -n "pCylinder29" -p "null1";
	setAttr ".t" -type "double3" 1.4968108150028119 2.2944834622683041 -1.3400172338398608 ;
	setAttr ".r" -type "double3" 335.92799683701475 273.22863991390187 357.26814260135325 ;
createNode transform -n "pCylinder30" -p "null1";
	setAttr ".t" -type "double3" -2.1123229516935815 6.6189912119596332 9.129906731632957 ;
	setAttr ".r" -type "double3" 27.141566387865119 73.616217969074853 35.634935570044554 ;
createNode transform -n "pCylinder31" -p "null1";
	setAttr ".t" -type "double3" 4.6192016823469206 1.2226227834215253 4.0419729149205992 ;
	setAttr ".r" -type "double3" 134.33687043660376 275.79102386805368 146.15725962437949 ;
createNode transform -n "pCylinder32" -p "null1";
	setAttr ".t" -type "double3" 7.1888584714920931 7.7045007407973642 -1.584987855981602 ;
	setAttr ".r" -type "double3" 174.08549750638906 102.11846582476362 84.670051085201649 ;
createNode transform -n "pCylinder33" -p "null1";
	setAttr ".t" -type "double3" -1.2718524254873014 19.60968335537618 -7.2887931462164506 ;
	setAttr ".r" -type "double3" 38.370111698948904 99.143419901513866 252.81081045818311 ;
createNode transform -n "pCylinder34" -p "null1";
	setAttr ".t" -type "double3" -7.24507471106977 11.413562915159241 9.3502179905182317 ;
	setAttr ".r" -type "double3" 253.74779853387594 180.13623987049044 13.655870922134937 ;
createNode transform -n "pCylinder35" -p "null1";
	setAttr ".t" -type "double3" 2.9254417983050338 9.2511168402081161 4.4608533360153295 ;
	setAttr ".r" -type "double3" 141.74656621554351 197.75550990724582 78.613284100976443 ;
createNode transform -n "pCylinder36" -p "null1";
	setAttr ".t" -type "double3" 1.8080338656007164 4.2739144650697503 -0.63903065790817237 ;
	setAttr ".r" -type "double3" 39.323231747763636 348.7196479512267 121.11793028707758 ;
createNode transform -n "pCylinder37" -p "null1";
	setAttr ".t" -type "double3" 3.409189023414477 3.777537410284606 -9.1151290142058237 ;
	setAttr ".r" -type "double3" 41.661710613168935 319.35513914891703 223.69580178349207 ;
createNode transform -n "pCylinder38" -p "null1";
	setAttr ".t" -type "double3" 6.4853392015394178 13.626491360930871 -9.1988702894288146 ;
	setAttr ".r" -type "double3" 304.63678682228476 336.77313609607177 191.4717906998448 ;
createNode transform -n "pCylinder39" -p "null1";
	setAttr ".t" -type "double3" -8.412169982428324 6.8213763755627577 -5.5840158479937019 ;
	setAttr ".r" -type "double3" 89.546106429805874 131.09413811966417 109.08880904542676 ;
createNode transform -n "pCylinder40" -p "null1";
	setAttr ".t" -type "double3" 1.6774862291455435 2.5181849708176407 4.7824884801376832 ;
	setAttr ".r" -type "double3" 261.01906577468355 77.533597789161036 50.967572271900949 ;
createNode transform -n "pCylinder41" -p "null1";
	setAttr ".t" -type "double3" -6.4156173636135989 2.0611782153356906 -8.7052141607587643 ;
	setAttr ".r" -type "double3" 68.48079354682595 165.81021897311402 317.22508441796532 ;
createNode transform -n "pCylinder42" -p "null1";
	setAttr ".t" -type "double3" 3.0908091031815523 6.7289403455746637 -2.165070613099342 ;
	setAttr ".r" -type "double3" 7.8288058137801873 281.28301621099519 60.79461752687282 ;
createNode transform -n "pCylinder43" -p "null1";
	setAttr ".t" -type "double3" -3.4754867018785092 14.953772158941565 5.6259141108904931 ;
	setAttr ".r" -type "double3" 331.9508612657591 356.45301377483014 131.49301446377487 ;
createNode transform -n "pCylinder44" -p "null1";
	setAttr ".t" -type "double3" 8.8793413151003229 2.302234121044815 9.1657079097401564 ;
	setAttr ".r" -type "double3" 164.66574272695576 347.60871281040079 72.748889681537847 ;
createNode transform -n "pCylinder45" -p "null1";
	setAttr ".t" -type "double3" -2.9699533557056519 16.252944395354202 -8.8370005555585109 ;
	setAttr ".r" -type "double3" 281.93101178398882 99.092669479114193 21.214232019428 ;
createNode transform -n "pCylinder46" -p "null1";
	setAttr ".t" -type "double3" -1.8630812218288391 12.801407386090268 2.4750999424977245 ;
	setAttr ".r" -type "double3" 61.905056386434119 31.28476498798835 278.60900238440814 ;
createNode transform -n "pCylinder47" -p "null1";
	setAttr ".t" -type "double3" -1.1655188548322233 0.55816106820871347 -5.0614578064487903 ;
	setAttr ".r" -type "double3" 127.80234450745729 352.7444420520016 312.50257700166088 ;
createNode transform -n "pCylinder48" -p "null1";
	setAttr ".t" -type "double3" 5.6076012012996586 10.58040458633435 -8.6853253657335916 ;
	setAttr ".r" -type "double3" 120.24946641105726 202.85733728124976 47.854300898080446 ;
createNode transform -n "pCylinder49" -p "null1";
	setAttr ".t" -type "double3" 5.9000486016408775 6.6099225369357084 3.5483857069065614 ;
	setAttr ".r" -type "double3" 107.3512480104601 55.838966982204127 58.070596007426424 ;
createNode transform -n "pCylinder50" -p "null1";
	setAttr ".t" -type "double3" -5.1110089723773422 2.1437710353333217 -4.2562246494758149 ;
	setAttr ".r" -type "double3" 274.89050978481384 240.61471207746584 70.944342122011818 ;
createNode transform -n "pCylinder51" -p "null1";
	setAttr ".t" -type "double3" 2.5442443135157067 3.872647568288925 6.4396751581918394 ;
	setAttr ".r" -type "double3" 190.13155124206841 70.745018637668366 60.183148067292649 ;
createNode transform -n "null2";
createNode transform -n "pCylinder52" -p "null2";
	setAttr ".t" -type "double3" 3.8135706287335847 10.509611651331102 3.837822688506332 ;
	setAttr ".r" -type "double3" 330.59252276820706 317.55948050839771 207.2584665748013 ;
createNode transform -n "pCylinder53" -p "null2";
	setAttr ".t" -type "double3" 0.78408782737432503 14.695778803201927 2.5437645755122578 ;
	setAttr ".r" -type "double3" 79.300990009674322 227.41557453115624 155.62022796694049 ;
createNode transform -n "pCylinder54" -p "null2";
	setAttr ".t" -type "double3" -6.9518735307069761 6.5709814040538239 -1.5215580291694408 ;
	setAttr ".r" -type "double3" 143.52446118335416 30.302884652597491 345.0163271146908 ;
createNode transform -n "pCylinder55" -p "null2";
	setAttr ".t" -type "double3" -8.5975310697765988 1.9307119818636376 -1.0623804148798897 ;
	setAttr ".r" -type "double3" 73.428016083945479 246.74711002320419 21.092205198050241 ;
createNode transform -n "pCylinder56" -p "null2";
	setAttr ".t" -type "double3" -8.2325134689261716 2.5751191697662157 -8.6173348401251264 ;
	setAttr ".r" -type "double3" 338.17438078622382 32.087743134729052 260.61352476868001 ;
createNode transform -n "pCylinder57" -p "null2";
	setAttr ".t" -type "double3" -2.5172689907685459 5.4771365240476255 -8.4735993409988986 ;
	setAttr ".r" -type "double3" 202.13111153220086 173.45823337273657 52.789506228544035 ;
createNode transform -n "pCylinder58" -p "null2";
	setAttr ".t" -type "double3" -8.619424459097063 10.7293163399801 1.4875535647702165 ;
	setAttr ".r" -type "double3" 4.0527773109348253 342.00880321033497 256.21922103424492 ;
createNode transform -n "pCylinder59" -p "null2";
	setAttr ".t" -type "double3" -5.1497164827627451 11.10734399861693 -7.4496843580016048 ;
	setAttr ".r" -type "double3" 159.38043441289196 103.94925054583686 213.14714253441619 ;
createNode transform -n "pCylinder60" -p "null2";
	setAttr ".t" -type "double3" -2.4762866272575623 13.220147620610053 -5.0628371979990678 ;
	setAttr ".r" -type "double3" 265.26272511780996 100.9785408954174 216.53664062344109 ;
createNode transform -n "pCylinder61" -p "null2";
	setAttr ".t" -type "double3" -6.161312237374279 4.1194813048715133 5.036747695771659 ;
	setAttr ".r" -type "double3" 177.23012084171651 19.953305476479095 228.73902364792124 ;
createNode transform -n "pCylinder62" -p "null2";
	setAttr ".t" -type "double3" 6.8344666083706542 17.166145094547179 4.9362381236583843 ;
	setAttr ".r" -type "double3" 50.309973360670682 120.21882004494827 330.45636935661145 ;
createNode transform -n "pCylinder63" -p "null2";
	setAttr ".t" -type "double3" 0.56603436400540552 5.1080683233058544 4.5385420554247986 ;
	setAttr ".r" -type "double3" 252.38869986055437 128.94109283688329 102.36173660653652 ;
createNode transform -n "pCylinder64" -p "null2";
	setAttr ".t" -type "double3" -9.0421730192627017 10.728594606647949 5.8493691992947205 ;
	setAttr ".r" -type "double3" 166.77582868801662 113.7327750967965 294.21952368602928 ;
createNode transform -n "pCylinder65" -p "null2";
	setAttr ".t" -type "double3" 1.5746250499157028 13.273122153905003 3.2151535532970339 ;
	setAttr ".r" -type "double3" 159.21550841385894 65.433798672014774 250.34733489144335 ;
createNode transform -n "pCylinder66" -p "null2";
	setAttr ".t" -type "double3" 1.6588419676986206 1.9845313452012014 -1.2184616871883041 ;
	setAttr ".r" -type "double3" 210.60898868261569 189.80608165071408 259.8641897136294 ;
createNode transform -n "pCylinder67" -p "null2";
	setAttr ".t" -type "double3" 9.3175063707891788 0.29068546143967033 2.8318287381817022 ;
	setAttr ".r" -type "double3" 19.614080923496861 269.8117053053677 11.717744677986177 ;
createNode transform -n "pCylinder68" -p "null2";
	setAttr ".t" -type "double3" 3.3988949230929215 9.0194234686406656 1.0535629694292599 ;
	setAttr ".r" -type "double3" 80.567370244584424 44.817796586699203 246.66436002142302 ;
createNode transform -n "pCylinder69" -p "null2";
	setAttr ".t" -type "double3" 8.6012852312239367 12.942420903625864 9.8673058752840248 ;
	setAttr ".r" -type "double3" 233.41190869773644 240.61566499045006 36.218532566056716 ;
createNode transform -n "pCylinder70" -p "null2";
	setAttr ".t" -type "double3" 9.5433709016314019 4.3268023137155414 -7.4857663865214974 ;
	setAttr ".r" -type "double3" 153.30460973527883 98.49050605722411 22.082368784413905 ;
createNode transform -n "pCylinder71" -p "null2";
	setAttr ".t" -type "double3" 1.5858137969277912 8.8548507964433831 8.0980638587589411 ;
	setAttr ".r" -type "double3" 138.617951831803 321.90385120462287 50.411254080246636 ;
createNode transform -n "pCylinder72" -p "null2";
	setAttr ".t" -type "double3" 2.1603875774029255 5.6103952341332741 -1.1997842745351335 ;
	setAttr ".r" -type "double3" 153.35400873844139 83.651313795246594 307.82884358118395 ;
createNode transform -n "pCylinder73" -p "null2";
	setAttr ".t" -type "double3" 1.9022409110448706 17.153336581385435 4.3430133706393388 ;
	setAttr ".r" -type "double3" 194.35092906395781 182.51486590015585 40.012581797696157 ;
createNode transform -n "pCylinder74" -p "null2";
	setAttr ".t" -type "double3" -4.8932415475698559 18.397644962700156 3.2831370770095276 ;
	setAttr ".r" -type "double3" 304.85310901115423 224.46982884207023 212.18459946409078 ;
createNode transform -n "pCylinder75" -p "null2";
	setAttr ".t" -type "double3" 0.7600128024937689 17.246596051643216 5.0544216253090468 ;
	setAttr ".r" -type "double3" 123.19228446136682 13.155104815526947 348.0722967496784 ;
createNode transform -n "pCylinder76" -p "null2";
	setAttr ".t" -type "double3" 0.28473293333850336 16.838967650178134 0.21912319692054183 ;
	setAttr ".r" -type "double3" 182.52829104935702 345.08946980801261 272.93707208019367 ;
createNode transform -n "pCylinder77" -p "null2";
	setAttr ".t" -type "double3" 1.2931804577907808 3.3887941671279243 1.146148225955324 ;
	setAttr ".r" -type "double3" 240.94435718256784 234.3648969014726 244.40128491327897 ;
createNode transform -n "pCylinder78" -p "null2";
	setAttr ".t" -type "double3" 1.4150255823465852 10.231401129774163 8.9769572635254704 ;
	setAttr ".r" -type "double3" 7.7696484430559885 230.29910284640178 316.79373638297614 ;
createNode transform -n "pCylinder79" -p "null2";
	setAttr ".t" -type "double3" 4.603854477340894 12.918153726842721 2.4269071861935174 ;
	setAttr ".r" -type "double3" 272.41733090112604 232.49630846062055 112.67361000277819 ;
createNode transform -n "pCylinder80" -p "null2";
	setAttr ".t" -type "double3" 5.8634678047332542 6.6963426558039751 4.3645828809517511 ;
	setAttr ".r" -type "double3" 288.602238288526 133.88713221246692 347.53506997914275 ;
createNode transform -n "pCylinder81" -p "null2";
	setAttr ".t" -type "double3" -5.379852939406728 6.6762760154845102 9.7838452041528328 ;
	setAttr ".r" -type "double3" 151.24919545044224 16.630616942658794 358.98975125382924 ;
createNode transform -n "pCylinder82" -p "null2";
	setAttr ".t" -type "double3" -8.1021093547091425 2.4049565950830565 -0.064487385878599923 ;
	setAttr ".r" -type "double3" 333.56261134857283 334.37747726073212 32.641880705541261 ;
createNode transform -n "pCylinder83" -p "null2";
	setAttr ".t" -type "double3" 3.9465457706819134 19.549921065280827 6.6713915070023582 ;
	setAttr ".r" -type "double3" 324.22847670367906 255.97281943899193 16.47957122956921 ;
createNode transform -n "pCylinder84" -p "null2";
	setAttr ".t" -type "double3" 2.4232756728564393 2.3860500620073677 7.5761508095891941 ;
	setAttr ".r" -type "double3" 228.91984630230576 211.35655346536984 303.49141797722092 ;
createNode transform -n "pCylinder85" -p "null2";
	setAttr ".t" -type "double3" 2.0948275715626519 19.675994379811492 -0.65578740964325632 ;
	setAttr ".r" -type "double3" 164.10674388806478 205.52539959973865 302.58006896624897 ;
createNode transform -n "pCylinder86" -p "null2";
	setAttr ".t" -type "double3" -3.3153036034182897 17.375261494999069 5.478229726694801 ;
	setAttr ".r" -type "double3" 21.951971763739479 208.22079526274203 24.290678347969251 ;
createNode transform -n "pCylinder87" -p "null2";
	setAttr ".t" -type "double3" -6.1641388395558145 7.0718133984040605 -5.9821532191759434 ;
	setAttr ".r" -type "double3" 273.02608174125453 201.85640202972721 120.88591638623781 ;
createNode transform -n "pCylinder88" -p "null2";
	setAttr ".t" -type "double3" 9.6685338322749317 8.6713034045843642 9.7000339943466827 ;
	setAttr ".r" -type "double3" 122.0155871469259 144.59390764393302 252.09786191529341 ;
createNode transform -n "pCylinder89" -p "null2";
	setAttr ".t" -type "double3" 2.018006474577712 16.861997860472076 -8.4962689270606653 ;
	setAttr ".r" -type "double3" 241.54919149471519 171.69980815799119 128.43972922123447 ;
createNode transform -n "pCylinder90" -p "null2";
	setAttr ".t" -type "double3" 2.9027155331597339 17.008476460743545 6.8806773133193957 ;
	setAttr ".r" -type "double3" 272.58468131689932 235.80602275667093 27.811505863141278 ;
createNode transform -n "pCylinder91" -p "null2";
	setAttr ".t" -type "double3" 5.2369150599609782 2.1182293036443123 -2.8245034050331537 ;
	setAttr ".r" -type "double3" 51.909274038012938 281.85982247919532 10.066724393834834 ;
createNode transform -n "pCylinder92" -p "null2";
	setAttr ".t" -type "double3" -7.8658519510034486 13.24507398154071 -2.5873749427140798 ;
	setAttr ".r" -type "double3" 215.40623566740476 30.941250713043029 149.70216265056493 ;
createNode transform -n "pCylinder93" -p "null2";
	setAttr ".t" -type "double3" 4.3595295158414782 10.060626369208778 -1.8268311707820075 ;
	setAttr ".r" -type "double3" 351.71764905247704 75.902743686733331 174.25412793330273 ;
createNode transform -n "pCylinder94" -p "null2";
	setAttr ".t" -type "double3" -2.5806510718386821 15.077808986134425 9.3054616702982038 ;
	setAttr ".r" -type "double3" 182.19747898843531 88.624531657744683 358.46052129324988 ;
createNode transform -n "pCylinder95" -p "null2";
	setAttr ".t" -type "double3" -6.6027033681377016 15.126274610983359 7.1638050902369059 ;
	setAttr ".r" -type "double3" 309.69774109094664 114.96586855631858 275.75590033110183 ;
createNode transform -n "pCylinder96" -p "null2";
	setAttr ".t" -type "double3" -0.56597754820469603 1.1482871974401831 6.4826098246761497 ;
	setAttr ".r" -type "double3" 345.40519185112316 35.930243461336104 288.52430426365459 ;
createNode transform -n "pCylinder97" -p "null2";
	setAttr ".t" -type "double3" -2.4581789340456712 18.30486884510567 -5.5389826679176117 ;
	setAttr ".r" -type "double3" 324.65929692272215 68.745429723488229 68.006117941691045 ;
createNode transform -n "pCylinder98" -p "null2";
	setAttr ".t" -type "double3" 6.8999317104065057 3.5272019075181227 -3.8923612236675798 ;
	setAttr ".r" -type "double3" 252.5848804828664 319.32140036852763 345.69701064141469 ;
createNode transform -n "pCylinder99" -p "null2";
	setAttr ".t" -type "double3" 7.1700563445550394 14.780600071110829 6.256389066103015 ;
	setAttr ".r" -type "double3" 119.38298101805299 109.34803961638239 2.2890467363643463 ;
createNode transform -n "pCylinder100" -p "null2";
	setAttr ".t" -type "double3" 9.6143581400667912 9.5777086702059968 3.0744132715302257 ;
	setAttr ".r" -type "double3" 32.298637203331623 203.16242911840121 173.81813274255865 ;
createNode transform -n "pCylinder101" -p "null2";
	setAttr ".t" -type "double3" 2.9641334463606981 16.724428792497296 -8.580128686001359 ;
	setAttr ".r" -type "double3" 255.71404580324946 74.781005877831475 107.005210000508 ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder2" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder3" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder4" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder5" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder6" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder7" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder8" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder9" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder10" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder11" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder12" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder13" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder14" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder15" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder16" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder17" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder18" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder19" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder20" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder21" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder22" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder23" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder24" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder25" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder26" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder27" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder28" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder29" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder30" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder31" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder32" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder33" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder34" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder35" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder36" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder37" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder38" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder39" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder40" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder41" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder42" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder43" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder44" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder45" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder46" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder47" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder48" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder49" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder50" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder51" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder52" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder53" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder54" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder55" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder56" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder57" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder58" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder59" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder60" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder61" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder62" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder63" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder64" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder65" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder66" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder67" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder68" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder69" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder70" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder71" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder72" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder73" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder74" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder75" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder76" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder77" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder78" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder79" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder80" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder81" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder82" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder83" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder84" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder85" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder86" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder87" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder88" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder89" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder90" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder91" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder92" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder93" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder94" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder95" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder96" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder97" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder98" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder99" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder100" ;
parent -s -nc -r -add "|pCylinder1|pCylinderShape1" "pCylinder101" ;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 4096\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n"
		+ "                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n"
		+ "            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 4096\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n"
		+ "            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n"
		+ "            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n"
		+ "                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 4096\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n"
		+ "                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n"
		+ "                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n"
		+ "            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 4096\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n"
		+ "                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 4096\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n"
		+ "                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n"
		+ "                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n"
		+ "            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 4096\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n"
		+ "            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n"
		+ "            -motionTrails 1\n            -clipGhosts 1\n            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n"
		+ "                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 4096\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n"
		+ "                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 0\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 0\n                -hairSystems 0\n                -follicles 0\n                -nCloths 0\n                -nParticles 0\n                -nRigids 0\n                -dynamicConstraints 0\n"
		+ "                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 0\n                -clipGhosts 0\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n"
		+ "            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 4096\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 0\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 0\n            -hairSystems 0\n            -follicles 0\n            -nCloths 0\n            -nParticles 0\n            -nRigids 0\n            -dynamicConstraints 0\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 0\n            -clipGhosts 0\n            -shadows 0\n            $editorName;\n"
		+ "modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 1\n                -showReferenceMembers 1\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n"
		+ "                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n"
		+ "            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n"
		+ "            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n"
		+ "                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n"
		+ "                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n"
		+ "                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n"
		+ "                -showPinIcons 1\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n"
		+ "                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n"
		+ "                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n"
		+ "                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n"
		+ "                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n"
		+ "                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n"
		+ "                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n"
		+ "                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n"
		+ "                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -ignoreAssets 1\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -island 0\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -ignoreAssets 1\n                -additiveGraphingMode 0\n"
		+ "                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -island 0\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -syncedSelection 1\n                -extendToShapes 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n"
		+ "\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Texture Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n"
		+ "                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 4096\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n"
		+ "                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n"
		+ "                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                $editorName;\nstereoCameraView -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n"
		+ "                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 4096\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n"
		+ "                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                $editorName;\nstereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n"
		+ "\t\t\t\t-defaultImage \"\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 37 100 -ps 2 63 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Script Editor\")) \n\t\t\t\t\t\"scriptedPanel\"\n\t\t\t\t\t\"$panelName = `scriptedPanel -unParent  -type \\\"scriptEditorPanel\\\" -l (localizedPanelLabel(\\\"Script Editor\\\")) -mbv $menusOkayInPanels `\"\n\t\t\t\t\t\"scriptedPanel -edit -l (localizedPanelLabel(\\\"Script Editor\\\")) -mbv $menusOkayInPanels  $panelName\"\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 4096\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 0\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -fluids 0\\n    -hairSystems 0\\n    -follicles 0\\n    -nCloths 0\\n    -nParticles 0\\n    -nRigids 0\\n    -dynamicConstraints 0\\n    -locators 1\\n    -manipulators 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 0\\n    -clipGhosts 0\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 4096\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 0\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -fluids 0\\n    -hairSystems 0\\n    -follicles 0\\n    -nCloths 0\\n    -nParticles 0\\n    -nRigids 0\\n    -dynamicConstraints 0\\n    -locators 1\\n    -manipulators 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 0\\n    -clipGhosts 0\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 24 -ast 1 -aet 48 ";
	setAttr ".st" 6;
createNode polyCylinder -n "polyCylinder1";
	setAttr ".sc" 1;
	setAttr ".cuv" 3;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 1;
	setAttr -av ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -k on ".an";
	setAttr -k on ".pt";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 101 ".dsm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -k on ".mico";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -k on ".micr";
	setAttr -k on ".micg";
	setAttr -k on ".micb";
	setAttr -cb on ".mica";
	setAttr -av -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :defaultObjectSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr -av ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -av -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -av -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr ".fn" -type "string" "im";
	setAttr -k on ".if";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -av -k on ".fir";
	setAttr -k on ".aap";
	setAttr -av -k on ".gh";
	setAttr -cb on ".sd";
connectAttr "polyCylinder1.out" "|pCylinder1|pCylinderShape1.i";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "|pCylinder1|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "|null1|pCylinder2|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder3|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder4|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder5|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder6|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder7|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder8|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder9|pCylinderShape1.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "|null1|pCylinder10|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder11|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder12|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder13|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder14|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder15|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder16|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder17|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder18|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder19|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder20|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder21|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder22|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder23|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder24|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder25|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder26|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder27|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder28|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder29|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder30|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder31|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder32|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder33|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder34|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder35|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder36|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder37|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder38|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder39|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder40|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder41|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder42|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder43|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder44|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder45|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder46|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder47|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder48|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder49|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder50|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null1|pCylinder51|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder52|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder53|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder54|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder55|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder56|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder57|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder58|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder59|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder60|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder61|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder62|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder63|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder64|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder65|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder66|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder67|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder68|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder69|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder70|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder71|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder72|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder73|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder74|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder75|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder76|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder77|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder78|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder79|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder80|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder81|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder82|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder83|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder84|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder85|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder86|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder87|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder88|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder89|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder90|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder91|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder92|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder93|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder94|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder95|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder96|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder97|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder98|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder99|pCylinderShape1.iog" ":initialShadingGroup.dsm" 
		-na;
connectAttr "|null2|pCylinder100|pCylinderShape1.iog" ":initialShadingGroup.dsm"
		 -na;
connectAttr "|null2|pCylinder101|pCylinderShape1.iog" ":initialShadingGroup.dsm"
		 -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of random_cubes_and_cones.ma
