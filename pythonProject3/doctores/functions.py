def handle_uploaded_file(f):
    with open('doctor/static/'+f.name) as destination:
        for chunk in f.chunks():
            destination.write(chunk)
