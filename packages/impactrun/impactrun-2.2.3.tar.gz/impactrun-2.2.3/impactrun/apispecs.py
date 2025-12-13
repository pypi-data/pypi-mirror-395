import os

apispeclist = [spec[:-5].lower() for spec in os.listdir(os.path.join(os.getcwd(), "specs"))]
