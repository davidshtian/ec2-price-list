import boto3
import json
import csv
import sys

regions = ['Asia Pacific (Mumbai)','Asia Pacific (Osaka-Local)','Asia Pacific (Seoul)','Asia Pacific (Singapore)','Asia Pacific (Sydney)','Asia Pacific (Tokyo)','Canada (Central)','EU (Frankfurt)','EU (Ireland)','EU (London)','EU (Paris)','EU (Stockholm)','South America (Sao Paulo)','US East (N. Virginia)','US East (Ohio)','US West (N. California)','US West (Oregon)']
instance_types = ['a1.medium','a1.large','a1.xlarge','a1.2xlarge','a1.4xlarge','c1.medium','c1.xlarge','c3.large','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge','c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge','c5.large','c5.xlarge','c5.2xlarge','c5.4xlarge','c5.9xlarge','c5.12xlarge','c5.18xlarge','c5.24xlarge','c5.metal','c5d.large','c5d.xlarge','c5d.2xlarge','c5d.4xlarge','c5d.9xlarge','c5d.18xlarge','c5n.large','c5n.xlarge','c5n.2xlarge','c5n.4xlarge','c5n.9xlarge','c5n.18xlarge','cc2.8xlarge','cr1.8xlarge','d2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge','f1.2xlarge','f1.4xlarge','f1.16xlarge','g2.2xlarge','g2.8xlarge','g3.4xlarge','g3.8xlarge','g3.16xlarge','g3s.xlarge','h1.2xlarge','h1.4xlarge','h1.8xlarge','h1.16xlarge','hs1.8xlarge','i2.xlarge','i2.2xlarge','i2.4xlarge','i2.8xlarge','i3.large','i3.xlarge','i3.2xlarge','i3.4xlarge','i3.8xlarge','i3.16xlarge','i3en.large','i3en.xlarge','i3en.2xlarge','i3en.3xlarge','i3en.6xlarge','i3en.12xlarge','i3en.24xlarge','m1.small','m1.medium','m1.large','m1.xlarge','m2.xlarge','m2.2xlarge','m2.4xlarge','m3.medium','m3.large','m3.xlarge','m3.2xlarge','m4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge','m4.16xlarge','m5.large','m5.xlarge','m5.2xlarge','m5.4xlarge','m5.8xlarge','m5.12xlarge','m5.16xlarge','m5.24xlarge','m5.metal','m5a.large','m5a.xlarge','m5a.2xlarge','m5a.4xlarge','m5a.8xlarge','m5a.12xlarge','m5a.16xlarge','m5a.24xlarge','m5ad.large','m5ad.xlarge','m5ad.2xlarge','m5ad.4xlarge','m5ad.12xlarge','m5ad.24xlarge','m5d.large','m5d.xlarge','m5d.2xlarge','m5d.4xlarge','m5d.8xlarge','m5d.12xlarge','m5d.16xlarge','m5d.24xlarge','m5d.metal','p2.xlarge','p2.8xlarge','p2.16xlarge','p3.2xlarge','p3.8xlarge','p3.16xlarge','p3dn.24xlarge','r3.large','r3.xlarge','r3.2xlarge','r3.4xlarge','r3.8xlarge','r4.large','r4.xlarge','r4.2xlarge','r4.4xlarge','r4.8xlarge','r4.16xlarge','r5.large','r5.xlarge','r5.2xlarge','r5.4xlarge','r5.8xlarge','r5.12xlarge','r5.16xlarge','r5.24xlarge','r5a.large','r5a.xlarge','r5a.2xlarge','r5a.4xlarge','r5a.8xlarge','r5a.12xlarge','r5a.16xlarge','r5a.24xlarge','r5ad.large','r5ad.xlarge','r5ad.2xlarge','r5ad.4xlarge','r5ad.12xlarge','r5ad.24xlarge','r5d.large','r5d.xlarge','r5d.2xlarge','r5d.4xlarge','r5d.8xlarge','r5d.12xlarge','r5d.16xlarge','r5d.24xlarge','t1.micro','t2.nano','t2.micro','t2.small','t2.medium','t2.large','t2.xlarge','t2.2xlarge','t3.nano','t3.micro','t3.small','t3.medium','t3.large','t3.xlarge','t3.2xlarge','t3a.nano','t3a.micro','t3a.small','t3a.medium','t3a.large','t3a.xlarge','t3a.2xlarge','x1.16xlarge','x1.32xlarge','x1e.xlarge','x1e.2xlarge','x1e.4xlarge','x1e.8xlarge','x1e.16xlarge','x1e.32xlarge','z1d.large','z1d.xlarge','z1d.2xlarge','z1d.3xlarge','z1d.6xlarge','z1d.12xlarge']

pricing = boto3.client('pricing')

def pricing_query(location, instanceType):
    instancePrice = []

    # location = 'US West (Oregon)'
    tenancy = "Shared"
    # instanceType = "m5.xlarge"
    operatingSystem = "Linux"
    preInstalledSw = "NA"
    licenseModel = "No License required"    

    instanceData = pricing.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'location',        'Value': location},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy',         'Value': tenancy},
            {'Type': 'TERM_MATCH', 'Field': 'instanceType',    'Value': instanceType},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': operatingSystem},
            {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw',  'Value': preInstalledSw}    

        ],
        MaxResults=100
    )    

    # pprint(instanceData)    

    for instanceVal in instanceData["PriceList"]:
        instanceValJson = json.loads(instanceVal)
        if("OnDemand" in instanceValJson["terms"] and len(instanceValJson["terms"]["OnDemand"]) > 0):
            for onDemandValues in instanceValJson["terms"]["OnDemand"].keys():
                for priceDimensionValues in instanceValJson["terms"]["OnDemand"][onDemandValues]["priceDimensions"]:
                    if("Used" in instanceValJson["product"]["attributes"]["capacitystatus"]):
                        instancePrice = (instanceValJson["terms"]["OnDemand"][onDemandValues]
                                         ["priceDimensions"][priceDimensionValues]["pricePerUnit"])    
    if 'USD' in instancePrice:
        instanceString = str(instancePrice['USD'])
    else:
        instanceString = 'NA'
    return instanceString

def double(l):
    tmp = l.copy()
    for i in range(len(l)):
        tmp.insert(2*i+1,l[i])
    return tmp

def list2csv(slist, ocsv, instance_type):
	csvfile = open(ocsv, 'a', newline='') 
	writer = csv.writer(csvfile)

	writer.writerow(slist)

	print('Write {} completed.'.format(instance_type))
	csvfile.close()

def price_csv_file(price_file):
    with open(price_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile) 
        double_regions = double(regions)
        double_regions.insert(0, "instance type")
        writer.writerow(double_regions)        

    for instance_type in instance_types:
        price_list = [instance_type,]
        for region in regions:
            ec2_price = pricing_query(region, instance_type)
            if ec2_price == "NA":
                ec2_price_month = "NA"
            else:
                ec2_price_month = float(ec2_price) * 6.7 * 24 * 30
            price_list.append(ec2_price)
            price_list.append(ec2_price_month)
        list2csv(price_list, price_file, instance_type)

price_csv_file(sys.argv[1])
