"""This module had script for create crawler in s3 path of csv file,incase of any exception it displays them"""
import boto3
import argparse
import csv
from botocore.exceptions import ClientError

# '''Instantiate the glue client'''
glue_client = boto3.client('glue',region_name = 'ap-south-1'
                            )
class crawler():
    """This is the Crawler class in the module"""
    def __init__(self,crawler_name,database_name,role,s3_path):
        """This is the init method of class ModifyFile"""
        self.crawler_name=crawler_name
        self.database_name=database_name
        self.s3_path=s3_path
        self.role=role
        
    def check_crawler_name(self):
        """This method checks if the crwaler name need to update in s3 path of csv file is present or not"""
        with open('crawler_details.csv','r')as check_file:
            csvreader = csv.DictReader(check_file)
            check=[]
            for row in csvreader:
                check.append(row['crawler_name'])
            
            if self.crawler_name in check:
                print("The crawler is already present")
                '''if the crawler is present it will update the details present '''
                self.update()
            else:
                self.create_crawler()
    def create_crawler(self):
        """This method that creates a new crawler in s3 path of csv file"""
        datas_new=[self.crawler_name,self.database_name,self.s3_path,self.role]
        with open('crawler_details.csv','a') as append_file:
             write_data= csv.writer(append_file)
             write_data.writerow(datas_new)
             print("The new crawler details are added to the csv file")
        # try:
        #     glue_client.create_crawler(
        #     Name = self.crawler_name,
        #     Role = self.role,
        #     DatabaseName = self.database_name,
            # Targets = 
            # {
            #     'S3Targets': 
            #     [
            #         {
        #                 'Path':self.s3_path
        #             }
        #         ]
        #     }
        # )
        # except Eception as CE:
        #     print("The invalid input error ", CE)
            

    def update(self):
        '''Update the details of crawler in a new csv file'''
        with open('crawler_details.csv', 'r') as file :
            csv_reader = csv.DictReader(file)
            with open('crawler_details_updated.csv', 'a') as new_file:
                csv_writer = csv.DictWriter(new_file,fieldnames=csv_reader.fieldnames)
                # csv_writer.writeheader()
                for row in csv_reader:
                    if row['crawler_name']==self.crawler_name:
                        row['database_name'] = self.database_name
                        row['s3_path'] = self.s3_path
                        row['role'] = self.role
                        csv_writer.writerow(row)
        
def main():
    parser = argparse.ArgumentParser(description='This argparser used for getiing input')
    parser.add_argument('--crawler_name',type=str, help='Enter the crawler name you need to check')
    parser.add_argument('--database_name', type=str, help='Enter the database name you need to check')
    parser.add_argument('--s3_path', type=str, help='Enter the s3_path you need to check')
    parser.add_argument('--role', type=str, help='Enter the role you need to check')
    
    args = parser.parse_args()
    crawl = crawler(args.crawler_name,args.database_name,args.s3_path,args.role)
    crawl.check_crawler_name()

if __name__ == '__main__' :
    main()    