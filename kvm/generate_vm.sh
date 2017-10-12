#!/bin/bash
set -e
# 将原有raw image作为backing file利用qcow2的特性快速创建Vm

# 将作为raw image的raw格式的disk(作为base的disk，通常是装完系统)
raw_disk="Centos7_base_raw.img"
# raw image中vm的名称
raw_vm_name="Cen7_base_raw"
# 存放vm disk的目录
disk_dir="\/vm_image\/disk\/"
# 产出新vm的名称前缀
clone_disk_base_name="Cen7_lab"
# 产出多少个vm
number=4

######################开始#####################
echo "Start at $(date)\n"
for i in `seq $number`
do
    echo "Creating $i vm.....\n"
    New_file="${HOME}/${clone_disk_base_name}$i"
    MAC_address=$(echo $RANDOM | md5sum | sed 's/\(..\)/&:/g' | cut -c1-17)
    qemu-img create -f qcow2 -o size=20G,backing_file=${disk_dir}${raw_disk} \
    ${clone_disk_base_name}$i
    virsh dumpxml ${raw_vm_name}>$New_file
    sed -i "s/<name>.*<\/name>/<name>${clone_disk_base_name}$i<\/name>/g" $New_file
    sed -i "s/<uuid>.*<\/uuid>/<uuid>$(uuidgen)<\/uuid>/g" $New_file
    sed -i "s/${disk_dir}${raw_disk}/${disk_dir}${clone_disk_base_name}$i/g" $New_file
    sed -i "s/<mac address='*'\/>/${MAC_address}/g" $New_file
    virsh define ${New_file}
done
echo "End at $(date)\n"
