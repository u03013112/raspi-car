if [ "$1" = "" ]; then
	echo Input image 1 not selected
	exit
fi

if [ "$2" = "" ]; then
	echo Input image 2 not selected
	exit
fi

echo Stiching files $1 and $2

FILE1=$1
FILE2=$2

RESULT_NAME=${FILE1%.*}_${FILE2%.*}-pano

mkdir -p tmp
pto_gen --projection=2 --fov=360 -o ./tmp/project.pto $1 $2
pto_template --output=./tmp/project.pto --template=stereopi-template.pto ./tmp/project.pto
pto2mk -o ./tmp/project.mk -p $RESULT_NAME ./tmp/project.pto
make -f ./tmp/project.mk all clean
rm -rf ./tmp
