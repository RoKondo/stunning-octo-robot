import pulumi
from pulumi_aws import ec2 

vpc_cidr = "172.20.0.0/16"
vpc_network = "172.20"

def dbsubnet(cidr, zone, vpc,):
    resp = ec2.Subnet("Pulumi DB-Subnet "+zone,
                     availability_zone="us-east-2"+zone,
                     cidr_block=cidr,
                     map_public_ip_on_launch='False',
                     tags={"Name": "DBSubnet-"+zone,"Type":"private"},
                     vpc_id=vpc
    )
    return resp

def subnet(cidr, zone, vpc, isPublic):
    if eval(isPublic):
        helper = "Public"
    else:
        helper = "Private"        
    resp = ec2.Subnet("Pulumi Subnet "+helper+" "+zone,
                     availability_zone="us-east-2"+zone,
                     cidr_block=cidr,
                     map_public_ip_on_launch=isPublic,
                     tags={"Name": helper+"Subnet-"+zone,"Type":helper},
                     vpc_id=vpc
    )
    return resp

def routeTablePub(vpc, gateway):
    resp = ec2.RouteTable("Pulumi Public Route Table",
                          vpc_id=vpc
    )

    route1 = ec2.Route("Default Out",
                       destination_cidr_block="0.0.0.0/0",
                       gateway_id=gateway,
                       route_table_id=resp,
    )
    return resp
def publicAcl(vpc):
    resp = ec2.NetworkAcl("Public ACL",
                          vpc_id=vpc    
    )

    http = ec2.NetworkAclRule("Port 80 Access",
                              cidr_block="0.0.0.0/0",
                              egress="False",
                              from_port="80",
                              network_acl_id=resp,
                              protocol="6",
                              rule_action="Allow",
                              rule_number="100",
                              to_port="80"
    )

    https = ec2.NetworkAclRule("Port 443 Access",
                              cidr_block="0.0.0.0/0",
                              from_port="443",
                              egress="False",
                              network_acl_id=resp,
                              protocol="6",
                              rule_action="Allow",
                              rule_number="110",
                              to_port="443"
    )

    ssh = ec2.NetworkAclRule("Port 22 Access",
                              cidr_block="0.0.0.0/0",
                              from_port="22",
                              egress="False",
                              network_acl_id=resp,
                              protocol="6",
                              rule_action="Allow",
                              rule_number="120",
                              to_port="22"
    )
    allout = ec2.NetworkAclRule("Allow /0 to outbounds rule",
                                cidr_block="0.0.0.0/0",
                                egress="True",
                                network_acl_id=resp,
                                protocol="-1",
                                rule_action="Allow",
                                rule_number="100",
    )
    return resp
def routeTablePriv():
    reps = ec2.RouteTable(""
    )

def privateAcl(vpc, cidr):
    resp = ec2.NetworkAcl("Public ACL",
        vpc_id=vpc    
    )
    ssh = ec2.NetworkAclRule("Port 22 Access",
                              cidr_block=cidr,
                              from_port="22",
                              network_acl_id=resp,
                              protocol="6",
                              rule_action="Allow",
                              rule_number="120",
                              to_port="22"
    )
    http = ec2.NetworkAclRule("Port 80 Access",
                              cidr_block=cidr,
                              from_port="80",
                              network_acl_id=resp,
                              protocol="6",
                              rule_action="Allow",
                              rule_number="120",
                              to_port="22"
    )

def main():
    myvpc = ec2.Vpc("Pulumi VPC",
                    assign_generated_ipv6_cidr_block='False',
                    cidr_block=vpc_cidr,
                    enable_dns_hostnames='True',
                    enable_dns_support='True',
                    tags={"Name": "Pulumi Vpc"}
    )
    pubsubneta = subnet(vpc_network+'.0.0/24', 'a', myvpc, 'True') 
    pubsubnetb = subnet(vpc_network+'.1.0/24', 'b', myvpc, 'True') 
    pubsubnetc = subnet(vpc_network+'.2.0/24', 'c', myvpc, 'True') 

    privsubneta = subnet(vpc_network+'.4.0/24', 'a', myvpc, 'False') 
    privsubnetb = subnet(vpc_network+'.5.0/24', 'b', myvpc, 'False') 
    privsubnetc = subnet(vpc_network+'.6.0/24', 'c', myvpc, 'False') 

    dbsubneta = dbsubnet(vpc_network+'.8.0/24', 'a', myvpc) 
    dbsubnetb = dbsubnet(vpc_network+'.9.0/24', 'b', myvpc) 
    dbsubnetc = dbsubnet(vpc_network+'.10.0/24', 'c', myvpc) 

    igw = ec2.InternetGateway("Pulumi IGW",
                              tags={"Name": "Pulumi IGW"},
                              vpc_id=myvpc
    )
     
    publicAcl(myvpc)
    rtpublic = routeTablePub(myvpc, igw)

if __name__ == '__main__':
    main()
