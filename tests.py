import requests


#upload a file test
url = 'http://127.0.0.1:5000/upload'
filename = 'img.png' #include your filename here. i.e. image.png
r = requests.post(url, files={'file': open(filename, 'rb')})
print r.text, r.status_code


#download a file test
file = 'img.png'
url = 'http://127.0.0.1:5000/{file}'.format(file=file)

r = requests.get(url, stream=True)

if r.status_code == 200:
    with open('uploads/output.png', 'wb') as handle:
        for block in r.iter_content(1024):
            if not block:
                break
            handle.write(block)

if r.status_code == 404:
    print 'File not found.'

