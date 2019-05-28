import pulumi
from pulumi_aws import ec2 

vpc_cidr = "172.23.0.0/16"

def subnet(cidr, zone, vpc, isPublic):
    if eval(isPublic):
        helper = "Public"
    else:
        helper = "Private"        
    res = ec2.Subnet("Pulumi Subnet"+helper+" "+zone,
                     availability_zone="us-east-2"+zone,
                     cidr_block=cidr,
                     map_public_ip_on_launch=isPublic,
                     tags={"Name": "Subnet-"+zone,"Type":helper},
                     vpc_id=vpc
    )
    return res
myvpc = ec2.Vpc("Pulumi VPC",
                assign_generated_ipv6_cidr_block='False',
                cidr_block=vpc_cidr,
                enable_dns_hostnames='True',
                enable_dns_support='True',
                tags={"Name": "Pulumi Vpc"}
)
pubsubneta = subnet('172.23.0.0/24', 'a', myvpc, 'True') 
pubsubnetb = subnet('172.23.1.0/24', 'b', myvpc, 'True') 
pubsubnetc = subnet('172.23.2.0/24', 'c', myvpc, 'True') 

privsubneta = subnet('172.23.4.0/24', 'a', myvpc, 'False') 
privsubnetb = subnet('172.23.5.0/24', 'b', myvpc, 'False') 
privsubnetc = subnet('172.23.6.0/24', 'c', myvpc, 'False') 

igw = ec2.InternetGateway("Pulumi IGW",
                          tags={"Name": "Pulumi IGW"},
                          vpc_id=myvpc
)
    

#res = ec2.Subnet("Pulumi Subnet",
#    availability_zone= "us-east-2a",
#    cidr_block= "172.23.0.0/24",
#    map_public_ip_on_launch= 'True',
#    vpc_id= myvpc
#)
