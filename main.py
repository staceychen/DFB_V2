from flask import Flask, request, url_for, render_template, send_file, redirect
from flask_uploads import UploadSet, configure_uploads, DATA
import DirectFlightBuilder

year = 1989
app = Flask(__name__)
inputquery = UploadSet('inputquery', DATA)

app.config['UPLOADS_DEFAULT_DEST'] = 'inputs'
configure_uploads(app, inputquery)

@app.route('/')
def preprocess():
    DirectFlightBuilder.new_file()
    global year
    year = 1989
    return render_template("preprocess.html")

@app.route('/processing', methods = ['GET', 'POST'])
def processing():
    global year
    year += 1
    if request.method == 'GET' and year < 2019:
        # do stuff when the link is submitted
        DirectFlightBuilder.pre_processing(year)
        
        
        # redirect to end the POST handling
        return render_template("preprocess.html", year = year)
        
    
    # show the form, it wasn't submitted
    return redirect(url_for('call_builder'))

@app.route('/home', methods =['GET', 'POST'])
def call_builder():
    if "add" in request.form:
        a = request.form['a']
        b = request.form['b']
        a_radius = int(request.form['a_radius'])
        b_radius = int(request.form['b_radius'])
        a_lat = float(request.form['a_lat'])
        a_lng = float(request.form['a_lng'])
        b_lat = float(request.form['b_lat'])
        b_lng = float(request.form['b_lng'])
    
        DirectFlightBuilder.direct_flight_builder(a, (a_lat, a_lng), a_radius, b, (b_lat, b_lng), b_radius)
            
        return render_template("index.html")
        
    elif "download" in request.form:
        return redirect("/download")
    
    elif "clear" in request.form:
        DirectFlightBuilder.new_file()
        
        return render_template("index.html")
    
    
    elif "upload" in request.form:
        if 'inputquery' in request.files:
            filename = inputquery.save(request.files['inputquery'])
            
            #try:
            DirectFlightBuilder.process_input_file(filename)
            print("upload successful")
            return render_template("index.html", status = '<h3>SUCCESSFUL UPLOAD - Click Download Button</h3>')
            #except:
                #return render_template("index.html", status = '<h3>ERROR UPLOADING FILE - Try Again</h3>')
            
        
        return render_template('index.html')
        
    else:
        return render_template("index.html")
        
@app.route('/download')
def downloadFile ():
    path = "outputs/flights.csv"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug = True)

