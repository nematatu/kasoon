from bing_image_downloader import downloader
query_string = input("input:")

downloader.download(query_string,output_dir=r'./img',adult_filter_off=True,timeout=120,verbose= True)