rm -rf code/samples
mkdir -p code/samples

cd code/samples

d0=$HOME/NVIDIA_CUDA-11.4_Samples
d1=$d0/bin/x86_64/linux/release

samples=(
	deviceQuery
	deviceQueryDrv
	vectorAdd
	vectorAddDrv
	matrixMul
	matrixMulDrv
)

for sample in "${samples[@]}"; do
	cp "$d1/$sample" .
done
